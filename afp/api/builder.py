from datetime import datetime
from decimal import Decimal
from typing import cast

from eth_typing.evm import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3

from .. import config, signing, validators
from ..bindings import (
    OracleSpecification,
    Product,
    ProductMetadata,
    ProductRegistry,
)
from ..bindings.erc20 import ERC20
from ..bindings.product_registry import ABI as PRODUCT_REGISTRY_ABI
from ..decorators import convert_web3_error
from ..exceptions import NotFoundError
from ..schemas import ProductSpecification
from .base import ClearingSystemAPI


class Builder(ClearingSystemAPI):
    """API for building and submitting new products.

    Parameters
    ----------
    private_key : str
        The private key of the blockchain account that submits the product.
    autonity_rpc_url : str
        The URL of a JSON-RPC provider for Autonity. (HTTPS only.)
    """

    @convert_web3_error()
    def create_product(
        self,
        *,
        symbol: str,
        description: str,
        oracle_address: str,
        fsv_decimals: int,
        fsp_alpha: Decimal,
        fsp_beta: int,
        fsv_calldata: str,
        start_time: datetime,
        earliest_fsp_submission_time: datetime,
        collateral_asset: str,
        tick_size: int,
        unit_value: Decimal,
        initial_margin_requirement: Decimal,
        maintenance_margin_requirement: Decimal,
        offer_price_buffer: Decimal,
        auction_bounty: Decimal,
        tradeout_interval: int,
        extended_metadata: str,
    ) -> ProductSpecification:
        """Creates a product specification with the given product data.

        The builder account's address is derived from the private key; the price
        quotation symbol is retrieved from the collateral asset.

        Parameters
        ----------
        symbol : str
        description : str
        oracle_address: str
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
        offer_price_buffer : Decimal
        auction_bounty : Decimal
        tradeout_interval : int
        extended_metadata : str

        Returns
        -------
        afp.schemas.ProductSpecification
        """
        product_id = Web3.to_hex(signing.generate_product_id(self._account, symbol))

        erc20_contract = ERC20(self._w3, Web3.to_checksum_address(collateral_asset))
        price_quotation = erc20_contract.symbol()

        if not price_quotation:
            raise NotFoundError(f"No ERC20 token found at address {collateral_asset}")

        if len(self._w3.eth.get_code(Web3.to_checksum_address(oracle_address))) == 0:
            raise NotFoundError(f"No contract found at oracle address {oracle_address}")

        return ProductSpecification(
            id=product_id,
            builder_id=self._account.address,
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
            offer_price_buffer=offer_price_buffer,
            auction_bounty=auction_bounty,
            tradeout_interval=tradeout_interval,
            extended_metadata=extended_metadata,
        )

    @convert_web3_error(PRODUCT_REGISTRY_ABI)
    def register_product(self, product: ProductSpecification) -> str:
        """Submits a product specification to the clearing system.

        Parameters
        ----------
        product : afp.schemas.ProductSpecification

        Returns
        -------
        str
            The hash of the transaction.
        """
        erc20_contract = ERC20(
            self._w3, cast(ChecksumAddress, product.collateral_asset)
        )
        decimals = erc20_contract.decimals()

        product_registry_contract = ProductRegistry(self._w3)
        tx_hash = product_registry_contract.register(
            self._convert_product_specification(product, decimals)
        ).transact()
        self._w3.eth.wait_for_transaction_receipt(tx_hash)
        return Web3.to_hex(tx_hash)

    @convert_web3_error(PRODUCT_REGISTRY_ABI)
    def product_state(self, product_id: str) -> str:
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
        product_registry_contract = ProductRegistry(self._w3)
        state = product_registry_contract.state(HexBytes(product_id))
        return state.name

    @staticmethod
    def _convert_product_specification(
        product: ProductSpecification, decimals: int
    ) -> Product:
        return Product(
            metadata=ProductMetadata(
                builder=cast(ChecksumAddress, product.builder_id),
                symbol=product.symbol,
                description=product.description,
            ),
            oracle_spec=OracleSpecification(
                oracle_address=cast(ChecksumAddress, product.oracle_address),
                fsv_decimals=product.fsv_decimals,
                fsp_alpha=int(product.fsp_alpha * config.FULL_PRECISION_MULTIPLIER),
                fsp_beta=product.fsp_beta,
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
                product.initial_margin_requirement * config.RATE_MULTIPLIER
            ),
            maintenance_margin_requirement=int(
                product.maintenance_margin_requirement * config.RATE_MULTIPLIER
            ),
            offer_price_buffer=int(product.offer_price_buffer * config.RATE_MULTIPLIER),
            auction_bounty=int(product.auction_bounty * config.RATE_MULTIPLIER),
            tradeout_interval=product.tradeout_interval,
            extended_metadata=product.extended_metadata,
        )
