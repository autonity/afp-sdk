import warnings
from datetime import datetime
from decimal import Decimal
from typing import Any, cast

from eth_typing.evm import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3

from .. import constants, hashing, validators
from ..bindings import (
    ClearingDiamond,
    OracleSpecification,
    Product as OnChainProduct,
    ProductMetadata,
    ProductRegistry,
)
from ..bindings.erc20 import ERC20
from ..bindings.facade import CLEARING_DIAMOND_ABI
from ..bindings.product_registry import ABI as PRODUCT_REGISTRY_ABI
from ..decorators import convert_web3_error
from ..exceptions import NotFoundError
from ..schemas import ProductSpecification, Transaction
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
        start_time: datetime,
        earliest_fsp_submission_time: datetime,
        collateral_asset: str,
        tick_size: int,
        unit_value: Decimal,
        initial_margin_requirement: Decimal,
        maintenance_margin_requirement: Decimal,
        auction_bounty: Decimal,
        tradeout_interval: int,
        extended_metadata: str,
        oracle_address: str | None = None,
    ) -> ProductSpecification:
        """Creates a product specification with the given product data.

        The builder account's address is derived from the private key; the price
        quotation symbol is retrieved from the collateral asset.

        Parameters
        ----------
        symbol : str
        description : str
        fsv_decimals: int
        fsp_alpha: Decimal
        fsp_beta: int
        fsv_calldata: str
        start_time : datetime
        earliest_fsp_submission_time : datetime
        collateral_asset : str
        tick_size : int
        unit_value : Decimal
        initial_margin_requirement : Decimal
        maintenance_margin_requirement : Decimal
        auction_bounty : Decimal
        tradeout_interval : int
        extended_metadata : str
        oracle_address: str, optional

        Returns
        -------
        afp.schemas.ProductSpecification
        """
        if oracle_address is None:
            oracle_address = self._config.oracle_provider_address

        if len(self._w3.eth.get_code(Web3.to_checksum_address(collateral_asset))) == 0:
            raise NotFoundError(f"No ERC20 token found at address {collateral_asset}")
        if len(self._w3.eth.get_code(Web3.to_checksum_address(oracle_address))) == 0:
            raise NotFoundError(f"No contract found at oracle address {oracle_address}")

        erc20_contract = ERC20(self._w3, Web3.to_checksum_address(collateral_asset))
        price_quotation = erc20_contract.symbol()

        product_id = Web3.to_hex(
            hashing.generate_product_id(self._authenticator.address, symbol)
        )

        return ProductSpecification(
            id=product_id,
            builder_id=self._authenticator.address,
            symbol=symbol,
            description=description,
            oracle_address=oracle_address,
            fsv_decimals=fsv_decimals,
            fsp_alpha=fsp_alpha,
            fsp_beta=fsp_beta,
            fsv_calldata=fsv_calldata,
            price_quotation=price_quotation,
            collateral_asset=collateral_asset,
            start_time=start_time,
            earliest_fsp_submission_time=earliest_fsp_submission_time,
            tick_size=tick_size,
            unit_value=unit_value,
            initial_margin_requirement=initial_margin_requirement,
            maintenance_margin_requirement=maintenance_margin_requirement,
            auction_bounty=auction_bounty,
            tradeout_interval=tradeout_interval,
            extended_metadata=extended_metadata,
        )

    def create_product(self, **kwargs: Any) -> ProductSpecification:
        """Deprecated alias of `Product.create`."""
        warnings.warn(
            "Product.create_product() is deprecated. Use Product.create() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.create(**kwargs)

    ### Transactions ###

    @convert_web3_error(PRODUCT_REGISTRY_ABI)
    def register(self, product_specification: ProductSpecification) -> Transaction:
        """Submits a product specification to the clearing system.

        Parameters
        ----------
        product_specification : afp.schemas.ProductSpecification

        Returns
        -------
        afp.schemas.Transaction
            Transaction parameters.
        """
        erc20_contract = ERC20(
            self._w3, cast(ChecksumAddress, product_specification.collateral_asset)
        )
        decimals = erc20_contract.decimals()

        product_registry_contract = ProductRegistry(
            self._w3, self._config.product_registry_address
        )
        return self._transact(
            product_registry_contract.register(
                self._convert_product_specification(product_specification, decimals)
            )
        )

    def register_product(self, product: ProductSpecification) -> Transaction:
        """Deprecated alias of `Product.register`."""
        warnings.warn(
            "Product.register_product() is deprecated. Use Product.register() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.register(product)

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

    def product_state(self, product_id: str) -> str:
        """Deprecated alias of `Product.state`."""
        warnings.warn(
            "Product.product_state() is deprecated. Use Product.state() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.state(product_id)

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
        product: ProductSpecification, decimals: int
    ) -> OnChainProduct:
        return OnChainProduct(
            metadata=ProductMetadata(
                builder=cast(ChecksumAddress, product.builder_id),
                symbol=product.symbol,
                description=product.description,
            ),
            oracle_spec=OracleSpecification(
                oracle_address=cast(ChecksumAddress, product.oracle_address),
                fsv_decimals=product.fsv_decimals,
                fsp_alpha=int(product.fsp_alpha * constants.FULL_PRECISION_MULTIPLIER),
                fsp_beta=int(product.fsp_beta * 10**product.fsv_decimals),
                fsv_calldata=HexBytes(product.fsv_calldata),
            ),
            price_quotation=product.price_quotation,
            collateral_asset=cast(ChecksumAddress, product.collateral_asset),
            start_time=int(product.start_time.timestamp()),
            earliest_fsp_submission_time=int(
                product.earliest_fsp_submission_time.timestamp()
            ),
            tick_size=product.tick_size,
            unit_value=int(product.unit_value * 10**decimals),
            initial_margin_requirement=int(
                product.initial_margin_requirement * constants.RATE_MULTIPLIER
            ),
            maintenance_margin_requirement=int(
                product.maintenance_margin_requirement * constants.RATE_MULTIPLIER
            ),
            auction_bounty=int(product.auction_bounty * constants.RATE_MULTIPLIER),
            tradeout_interval=product.tradeout_interval,
            extended_metadata=product.extended_metadata,
        )
