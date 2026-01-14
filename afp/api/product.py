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
    PredictionProductV1,
    ProductMetadata,
    Transaction,
)
from .base import ClearingSystemAPI


class Product(ClearingSystemAPI):
    """API for managing products."""

    ### Factories ###

    @convert_web3_error()
    def create(
        self,
        *,
        symbol: str,
        description: str,
        fsv_decimals: int,
        fsp_alpha: Decimal,
        fsp_beta: Decimal,
        fsv_calldata: str,
        collateral_asset: str,
        start_time: datetime,
        point_value: Decimal,
        price_decimals: int,
        earliest_fsp_submission_time: datetime,
        tradeout_interval: int,
        min_price: Decimal,
        max_price: Decimal,
        extended_metadata: str = "",
        oracle_address: str | None = None,
    ) -> PredictionProductV1:
        """Creates a product specification with the given product data.

        The builder account's address is derived from the private key; the price
        quotation symbol is retrieved from the collateral asset.

        Parameters
        ----------
        symbol : str
        description : str
        fsv_decimals: int
        fsp_alpha: Decimal
        fsp_beta: Decimal
        fsv_calldata: str
        collateral_asset : str
        start_time : datetime
        point_value : Decimal
        price_decimals : int
        earliest_fsp_submission_time : datetime
        tradeout_interval : int
        min_price : Decimal
        max_price : Decimal
        extended_metadata : str, optional
        oracle_address: str, optional

        Returns
        -------
        afp.schemas.PredictionProductV1
        """
        if oracle_address is None:
            oracle_address = self._config.oracle_provider_address

        # Verify contracts
        collateral_asset = validators.verify_collateral_asset(
            self._w3, collateral_asset
        )
        oracle_address = validators.verify_oracle(self._w3, oracle_address)

        product_id = Web3.to_hex(
            hashing.generate_product_id(self._authenticator.address, symbol)
        )

        return PredictionProductV1(
            id=product_id,
            base=BaseProduct(
                metadata=ProductMetadata(
                    builder_id=self._authenticator.address,
                    symbol=symbol,
                    description=description,
                ),
                oracle_spec=OracleSpecification(
                    oracle_address=oracle_address,
                    fsv_decimals=fsv_decimals,
                    fsp_alpha=fsp_alpha,
                    fsp_beta=fsp_beta,
                    fsv_calldata=fsv_calldata,
                ),
                collateral_asset=collateral_asset,
                start_time=start_time,
                point_value=point_value,
                price_decimals=price_decimals,
                extended_metadata=extended_metadata,
            ),
            expiry_spec=ExpirySpecification(
                earliest_fsp_submission_time=earliest_fsp_submission_time,
                tradeout_interval=tradeout_interval,
            ),
            min_price=min_price,
            max_price=max_price,
        )

    @convert_web3_error()
    def parse(self, spec: dict[str, Any]) -> PredictionProductV1:
        """Creates a product specification from a dictionary.

        The dictionary must follow the schema of the afp.schemas.ProductSpec model.

        Parameters
        ----------
        spec : dict
            A dictionary that follows the PredictionProductV1 v0.2 JSON schema.

        Returns
        -------
        afp.schemas.PredictionProductV1
        """
        # Set default values
        if spec["base"]["oracleSpec"].get("oracleAddress") is None:
            spec["base"]["oracleSpec"]["oracleAddress"] = (
                self._config.oracle_provider_address
            )
        if spec["base"]["metadata"].get("builderId") is None:
            spec["base"]["metadata"]["builderId"] = self._authenticator.address

        # Verify contracts
        spec["base"]["collateralAsset"] = validators.verify_collateral_asset(
            self._w3, spec["base"]["collateralAsset"]
        )
        spec["base"]["oracleSpec"]["oracleAddress"] = validators.verify_oracle(
            self._w3, spec["base"]["oracleSpec"]["oracleAddress"]
        )

        # Generate ID
        spec["id"] = Web3.to_hex(
            hashing.generate_product_id(
                spec["base"]["metadata"]["builderId"],
                spec["base"]["metadata"]["symbol"],
            )
        )

        return PredictionProductV1.model_validate(spec)

    ### Transactions ###

    @convert_web3_error(PRODUCT_REGISTRY_ABI)
    def register(self, product_spec: PredictionProductV1) -> Transaction:
        """Submits a product specification to the clearing system.

        Parameters
        ----------
        product_spec : afp.schemas.ProductSpec

        Returns
        -------
        afp.schemas.Transaction
            Transaction parameters.
        """
        erc20_contract = ERC20(
            self._w3, cast(ChecksumAddress, product_spec.base.collateral_asset)
        )
        decimals = erc20_contract.decimals()

        product_registry_contract = ProductRegistry(
            self._w3, self._config.product_registry_address
        )
        return self._transact(
            product_registry_contract.register_prediction_product(
                self._convert_product_specification(product_spec, decimals)
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

    @convert_web3_error(PRODUCT_REGISTRY_ABI)
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

    @convert_web3_error(PRODUCT_REGISTRY_ABI)
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
                    builder=cast(ChecksumAddress, product.base.metadata.builder_id),
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
