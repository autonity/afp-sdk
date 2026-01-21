from decimal import Decimal
from typing import Any, Type, cast

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
    PredictionProduct,
    PredictionProductV1,
    Transaction,
)
from .base import ClearingSystemAPI


class Product(ClearingSystemAPI):
    """API for managing products."""

    ### Product Specification ###

    def parse[T: Type[PredictionProduct | PredictionProductV1]](
        self, dct: dict[str, Any], schema: T = PredictionProduct
    ) -> T:
        """Creates a product specification from a dictionary.

        The dictionary must follow the schema of the afp.schemas.ProductSpec model.

        Parameters
        ----------
        spec : dict
            A dictionary that follows the PredictionProduct schema.
        schema : type
            afp.schemas.PredictionProduct or afp.schemas.PredictionProductV1

        Returns
        -------
        afp.schemas.PredictionProduct or afp.schemas.PredictionProductV1
        """
        return schema.model_validate(dct)

    def dump(
        self, product_spec: PredictionProduct | PredictionProductV1
    ) -> dict[str, Any]:
        """Creates a dictionary from a product specification.

        Parameters
        ----------
        product_spec : afp.schemas.PredictionProduct or afp.schemas.PredictionProductV1

        Returns
        -------
        dict
        """
        return product_spec.model_dump(by_alias=True)

    def id(self, product_spec: PredictionProduct | PredictionProductV1) -> str:
        """Generates the product ID for a product specification.

        This is the ID that the product will get after successful registration.

        Parameters
        ----------
        product_spec : afp.schemas.PredictionProduct or afp.schemas.PredictionProductV1
            The product specification.

        Returns
        -------
        str
        """
        product = (
            product_spec
            if isinstance(product_spec, PredictionProductV1)
            else product_spec.product
        )

        return Web3.to_hex(
            hashing.generate_product_id(
                cast(ChecksumAddress, product.base.metadata.builder),
                product.base.metadata.symbol,
            )
        )

    ### Transactions ###

    @convert_web3_error(PRODUCT_REGISTRY_ABI, CLEARING_DIAMOND_ABI)
    def register(
        self,
        product_spec: PredictionProduct | PredictionProductV1,
        initial_builder_stake: Decimal,
    ) -> Transaction:
        """Submits a product specification to the clearing system.

        The extended metadata should already be pinned to IPFS and the CID should be
        specified in the afp.schemas.BaseProduct object in the product specification.

        Parameters
        ----------
        product_spec : afp.schemas.PredictionProduct or afp.schemas.PredictionProductV1
            The product specification with or without extended metadata.
        initial_builder_stake : Decimal
            Registration stake (product maintenance fee) in units of the collateral
            asset.

        Returns
        -------
        afp.schemas.Transaction
            Transaction parameters.
        """
        product = (
            product_spec
            if isinstance(product_spec, PredictionProductV1)
            else product_spec.product
        )

        # Verify contracts exist
        validators.verify_collateral_asset(self._w3, product.base.collateral_asset)
        validators.verify_oracle(self._w3, product.base.oracle_spec.oracle_address)

        erc20_contract = ERC20(
            self._w3, cast(ChecksumAddress, product.base.collateral_asset)
        )
        decimals = erc20_contract.decimals()

        product_registry_contract = ProductRegistry(
            self._w3, self._config.product_registry_address
        )
        return self._transact(
            product_registry_contract.register_prediction_product(
                self._convert_product_specification(product, decimals),
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

    @staticmethod
    def _convert_product_specification(
        product: PredictionProductV1, decimals: int
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
                point_value=int(product.base.point_value * 10**decimals),
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
