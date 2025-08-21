from decimal import Decimal
from functools import cache
from typing import Iterable

from hexbytes import HexBytes
from web3 import Web3

from .. import validators
from ..bindings import (
    BidData,
    ClearingDiamond,
    ProductRegistry,
    Side as OnChainOrderSide,
)
from ..bindings.facade import CLEARING_DIAMOND_ABI
from ..bindings.product_registry import ABI as PRODUCT_REGISTRY_ABI
from ..decorators import convert_web3_error
from ..enums import OrderSide
from ..schemas import AuctionData, Bid
from .base import ClearingSystemAPI


class Liquidation(ClearingSystemAPI):
    """API for participating in liquidation auctions.

    Parameters
    ----------
    private_key : str
        The private key of the blockchain account that participates in a liquidation
        auction.
    autonity_rpc_url : str
        The URL of a JSON-RPC provider for Autonity. (HTTPS only.)
    """

    @staticmethod
    def create_bid(product_id: str, price: Decimal, quantity: int, side: str) -> Bid:
        """Create a bid to be submitted to a liquidation auction.

        Parameters
        ----------
        product_id : str
        price: Decimal
        quantity: int
        side: str

        Returns
        -------
        afp.schemas.Bid
        """
        return Bid(
            product_id=product_id,
            price=price,
            quantity=quantity,
            side=getattr(OrderSide, side.upper()),
        )

    ### Transactions ###

    @convert_web3_error(CLEARING_DIAMOND_ABI)
    def request_liquidation(self, margin_account_id: str, collateral_asset: str) -> str:
        """Request a liquidation auction to be started.

        Parameters
        ----------
        margin_account_id : str
            The ID of the margin account to be liquidated.
        collateral_asset : str
            The address of the collateral token that the margin account is trading with.

        Returns
        -------
        str
            The hash of the transaction.
        """
        margin_account_id = validators.validate_address(margin_account_id)
        collateral_asset = validators.validate_address(collateral_asset)

        clearing_contract = ClearingDiamond(self._w3)
        tx_hash = clearing_contract.request_liquidation(
            margin_account_id, collateral_asset
        ).transact()
        self._w3.eth.wait_for_transaction_receipt(tx_hash)
        return Web3.to_hex(tx_hash)

    @convert_web3_error(CLEARING_DIAMOND_ABI, PRODUCT_REGISTRY_ABI)
    def submit_bids(
        self, margin_account_id: str, collateral_asset: str, bids: Iterable[Bid]
    ) -> str:
        """Submit bids to a liquidation auction.

        Parameters
        ----------
        margin_account_id : str
            The ID of the margin account that is being liquidated.
        collateral_asset : str
            The address of the collateral token that the margin account is trading with.
        bids: list of afp.schemas.Bid

        Returns
        -------
        str
            The hash of the transaction.
        """
        margin_account_id = validators.validate_address(margin_account_id)
        collateral_asset = validators.validate_address(collateral_asset)

        converted_bids = [
            BidData(
                product_id=HexBytes(bid.product_id),
                price=int(bid.price * 10 ** self._tick_size(bid.product_id)),
                quantity=bid.quantity,
                side=getattr(OnChainOrderSide, bid.side.name),
            )
            for bid in bids
        ]

        clearing_contract = ClearingDiamond(self._w3)
        tx_hash = clearing_contract.bid_auction(
            margin_account_id, collateral_asset, converted_bids
        ).transact()
        self._w3.eth.wait_for_transaction_receipt(tx_hash)
        return Web3.to_hex(tx_hash)

    ### Views ###

    @convert_web3_error(CLEARING_DIAMOND_ABI)
    def auction_data(
        self, margin_account_id: str, collateral_asset: str
    ) -> AuctionData:
        """Returns information on a liquidation auction.

        Parameters
        ----------
        margin_account_id : str
            The ID of the margin account to be liquidated.
        collateral_asset : str
            The address of the collateral token that the margin account is trading with.

        Returns
        -------
        str
            The hash of the transaction.
        """
        margin_account_id = validators.validate_address(margin_account_id)
        collateral_asset = validators.validate_address(collateral_asset)

        clearing_contract = ClearingDiamond(self._w3)
        data = clearing_contract.auction_data(margin_account_id, collateral_asset)
        divisor = 10 ** self._decimals(collateral_asset)
        return AuctionData(
            start_block=data.start_block,
            margin_account_equity_at_initiation=(
                Decimal(data.mae_at_initiation) / divisor
            ),
            maintenance_margin_used_at_initiation=(
                Decimal(data.mmu_at_initiation) / divisor
            ),
            margin_account_equity_now=(Decimal(data.mae_now) / divisor),
            maintenance_margin_used_now=(Decimal(data.mmu_now) / divisor),
        )

    ### Internal getters ###

    @cache
    def _tick_size(self, product_id: str) -> int:
        product_registry_contract = ProductRegistry(self._w3)
        return product_registry_contract.tick_size(HexBytes(product_id))
