from datetime import datetime
from decimal import Decimal
from typing import Any, cast

from eth_typing.evm import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3

from .. import constants, hashing, validators
from ..bindings import (
    BaseProduct as OnChainBaseProduct,
    ClearingDiamond,
    ExpirySpecification as OnChainExpirySpecification,
    OracleSpecification as OnChainOracleSpecification,
    PredictionProductV1 as OnChainPredictionProductV1,
    ProductMetadata as OnChainProductMetadata,
    ProductRegistry,
)
from ..bindings.erc20 import ERC20
from ..bindings.facade import CLEARING_DIAMOND_ABI
from ..bindings.product_registry import ABI as PRODUCT_REGISTRY_ABI
from ..decorators import convert_web3_error
from ..exceptions import NotFoundError
from ..schemas import (
    BaseProduct,
    ExpirySpecification,
    OracleSpecification,
    PredictionProduct,
    PredictionProductV1,
    ProductMetadata,
    Transaction,
)
from .base import ClearingSystemAPI


class Product(ClearingSystemAPI):
    """API for managing products."""

    ### Product Specification ###

    def validate(self, product_dict: dict[str, Any]) -> PredictionProduct:
        """Creates a product specification from a dictionary.

        The dictionary must follow the schema of the afp.schemas.ProductSpec model.

        Parameters
        ----------
        product_dict : dict
            A dictionary that follows the PredictionProduct schema.

        Returns
        -------
        afp.schemas.PredictionProduct
        """
        return self._verify_product_spec(
            PredictionProduct.model_validate(product_dict, by_alias=True)
        )

    def validate_json(self, product_json: str) -> PredictionProduct:
        """Creates a product specification from a dictionary.

        The dictionary must follow the schema of the afp.schemas.ProductSpec model.

        Parameters
        ----------
        product_json : str
            A JSON string that follows the PredictionProduct schema.

        Returns
        -------
        afp.schemas.PredictionProduct
        """
        return self._verify_product_spec(
            PredictionProduct.model_validate_json(product_json, by_alias=True)
        )

    def dump(self, product_spec: PredictionProduct) -> dict[str, Any]:
        """Creates a dictionary from a product specification.

        Parameters
        ----------
        product_spec : afp.schemas.PredictionProduct
            The product specification.

        Returns
        -------
        dict
        """
        return product_spec.model_dump(by_alias=True)

    def dump_json(self, product_spec: PredictionProduct) -> str:
        """Creates a JSON string from a product specification.

        Parameters
        ----------
        product_spec : afp.schemas.PredictionProduct
            The product specification.

        Returns
        -------
        str
        """
        return product_spec.model_dump_json(by_alias=True)

    def id(self, product_spec: PredictionProduct) -> str:
        """Generates the product ID for a product specification.

        This is the ID that the product will get after successful registration.

        Parameters
        ----------
        product_spec : afp.schemas.PredictionProduct
            The product specification.

        Returns
        -------
        str
        """
        return Web3.to_hex(
            hashing.generate_product_id(
                cast(ChecksumAddress, product_spec.product.base.metadata.builder),
                product_spec.product.base.metadata.symbol,
            )
        )

    ### Transactions ###

    @convert_web3_error(PRODUCT_REGISTRY_ABI, CLEARING_DIAMOND_ABI)
    def register(
        self, product_spec: PredictionProduct, initial_builder_stake: Decimal
    ) -> Transaction:
        """Submits a product specification to the clearing system.

        The extended metadata should already be pinned to IPFS and the CID should be
        specified in the afp.schemas.BaseProduct object in the product specification.

        Parameters
        ----------
        product_spec : afp.schemas.PredictionProduct or afp.schemas.PredictionProductV1
            The product specification.
        initial_builder_stake : Decimal
            Registration stake (product maintenance fee) in units of the collateral
            asset.

        Returns
        -------
        afp.schemas.Transaction
            Transaction parameters.
        """
        erc20_contract = ERC20(
            self._w3, cast(ChecksumAddress, product_spec.product.base.collateral_asset)
        )
        decimals = erc20_contract.decimals()

        product_registry_contract = ProductRegistry(
            self._w3, self._config.product_registry_address
        )
        return self._transact(
            product_registry_contract.register_prediction_product(
                self._convert_prediction_product_specification(
                    product_spec.product, decimals
                ),
                int(initial_builder_stake * 10**decimals),
            )
        )

    @convert_web3_error(CLEARING_DIAMOND_ABI)
    def initiate_final_settlement(
        self, product_id: str, accounts: list[str]
    ) -> Transaction:
        """Initiate final settlement (closeout) process for the specified accounts.

        The product must be in Final Settlement state. The accounts must hold non-zero
        positions in the product that offset each other (i.e. the sum of their position
        sizes is 0.)

        Parameters
        ----------
        product_id : str
            The ID of the product.
        accounts : list of str
            List of margin account IDs to initiate settlement for.

        Returns
        -------
        afp.schemas.Transaction
            Transaction parameters.
        """
        product_id = validators.validate_hexstr32(product_id)
        addresses = [validators.validate_address(account) for account in accounts]

        clearing_contract = ClearingDiamond(
            self._w3, self._config.clearing_diamond_address
        )
        return self._transact(
            clearing_contract.initiate_final_settlement(HexBytes(product_id), addresses)
        )

    ### Views ###

    @convert_web3_error(PRODUCT_REGISTRY_ABI, CLEARING_DIAMOND_ABI)
    def get(self, product_id: str) -> PredictionProduct:
        """Retrieves a product registered on chain.

        Parameters
        ----------
        product_id : str
            The ID of the product.

        Returns
        -------
        afp.schemas.PredictionProduct
        """
        product_id = validators.validate_hexstr32(product_id)

        product_registry_contract = ProductRegistry(
            self._w3, self._config.product_registry_address
        )
        # Note: when FuturesProductV1 support is added, call type_of(product_id) first
        # to figure out which view function should be used
        product = product_registry_contract.prediction_product_v1(HexBytes(product_id))

        erc20_contract = ERC20(self._w3, product.base.collateral_asset)
        decimals = erc20_contract.decimals()

        product = self._convert_on_chain_prediction_product(product, decimals)
        return product  # TODO

    @convert_web3_error(PRODUCT_REGISTRY_ABI, CLEARING_DIAMOND_ABI)
    def state(self, product_id: str) -> str:
        """Returns the current state of a product.

        Parameters
        ----------
        product_id : str
            The ID of the product.

        Returns
        -------
        str
        """
        product_id = validators.validate_hexstr32(product_id)
        product_registry_contract = ProductRegistry(
            self._w3, self._config.product_registry_address
        )
        state = product_registry_contract.state(HexBytes(product_id))
        return state.name

    @convert_web3_error(PRODUCT_REGISTRY_ABI, CLEARING_DIAMOND_ABI)
    def collateral_asset(self, product_id: str) -> str:
        """Returns the collateral asset of a product.

        Parameters
        ----------
        product_id : str
            The ID of the product.

        Returns
        -------
        str
        """
        product_id = validators.validate_hexstr32(product_id)
        product_registry_contract = ProductRegistry(
            self._w3, self._config.product_registry_address
        )
        collateral_asset = product_registry_contract.collateral_asset(
            HexBytes(product_id)
        )
        if Web3.to_int(hexstr=collateral_asset) == 0:
            raise NotFoundError("Product not found in the product registry")
        return collateral_asset

    ### Internal helpers ###

    def _verify_product_spec(
        self, product_spec: PredictionProduct
    ) -> PredictionProduct:
        validators.verify_collateral_asset(
            self._w3, product_spec.product.base.collateral_asset
        )
        validators.verify_oracle(
            self._w3, product_spec.product.base.oracle_spec.oracle_address
        )
        return product_spec

    @staticmethod
    def _convert_prediction_product_specification(
        product: PredictionProductV1, collateral_asset_decimals: int
    ) -> OnChainPredictionProductV1:
        return OnChainPredictionProductV1(
            base=OnChainBaseProduct(
                metadata=OnChainProductMetadata(
                    builder=cast(ChecksumAddress, product.base.metadata.builder),
                    symbol=product.base.metadata.symbol,
                    description=product.base.metadata.description,
                ),
                oracle_spec=OnChainOracleSpecification(
                    oracle_address=cast(
                        ChecksumAddress, product.base.oracle_spec.oracle_address
                    ),
                    fsv_decimals=product.base.oracle_spec.fsv_decimals,
                    fsp_alpha=int(
                        product.base.oracle_spec.fsp_alpha
                        * constants.FULL_PRECISION_MULTIPLIER
                    ),
                    fsp_beta=int(
                        product.base.oracle_spec.fsp_beta
                        * 10**product.base.oracle_spec.fsv_decimals
                    ),
                    fsv_calldata=HexBytes(product.base.oracle_spec.fsv_calldata),
                ),
                collateral_asset=cast(ChecksumAddress, product.base.collateral_asset),
                start_time=int(product.base.start_time.timestamp()),
                point_value=int(
                    product.base.point_value * 10**collateral_asset_decimals
                ),
                price_decimals=product.base.price_decimals,
                extended_metadata=product.base.extended_metadata,
            ),
            expiry_spec=OnChainExpirySpecification(
                earliest_fsp_submission_time=int(
                    product.expiry_spec.earliest_fsp_submission_time.timestamp()
                ),
                tradeout_interval=product.expiry_spec.tradeout_interval,
            ),
            max_price=int(product.max_price * 10**product.base.price_decimals),
            min_price=int(product.min_price * 10**product.base.price_decimals),
        )

    @staticmethod
    def _convert_on_chain_prediction_product(
        product: OnChainPredictionProductV1, collateral_asset_decimals: int
    ) -> PredictionProductV1:
        return PredictionProductV1(
            base=BaseProduct(
                metadata=ProductMetadata(
                    builder=product.base.metadata.builder,
                    symbol=product.base.metadata.symbol,
                    description=product.base.metadata.description,
                ),
                oracle_spec=OracleSpecification(
                    oracle_address=product.base.oracle_spec.oracle_address,
                    fsv_decimals=product.base.oracle_spec.fsv_decimals,
                    fsp_alpha=(
                        Decimal(product.base.oracle_spec.fsp_alpha)
                        / constants.FULL_PRECISION_MULTIPLIER
                    ),
                    fsp_beta=(
                        Decimal(product.base.oracle_spec.fsp_beta)
                        / 10**product.base.oracle_spec.fsv_decimals
                    ),
                    fsv_calldata=product.base.oracle_spec.fsv_calldata.to_0x_hex(),
                ),
                collateral_asset=product.base.collateral_asset,
                start_time=datetime.fromtimestamp(product.base.start_time),
                point_value=(
                    Decimal(product.base.point_value) / 10**collateral_asset_decimals
                ),
                price_decimals=product.base.price_decimals,
                extended_metadata=product.base.extended_metadata,
            ),
            expiry_spec=ExpirySpecification(
                earliest_fsp_submission_time=datetime.fromtimestamp(
                    product.expiry_spec.earliest_fsp_submission_time
                ),
                tradeout_interval=product.expiry_spec.tradeout_interval,
            ),
            max_price=Decimal(product.max_price) / 10**product.base.price_decimals,
            min_price=Decimal(product.min_price) / 10**product.base.price_decimals,
        )
