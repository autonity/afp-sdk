from decimal import Decimal
from functools import cache
from typing import Iterable

from eth_typing.evm import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from web3.exceptions import ContractCustomError

from .. import validators
from ..bindings import (
    BidData,
    ClearingDiamond,
    MarginAccount as MarginContract,
    MarginAccountRegistry,
    ProductRegistry,
    Side as OnChainOrderSide,
)
from ..bindings.erc20 import ERC20
from ..bindings.facade import CLEARING_DIAMOND_ABI
from ..bindings.margin_account import ABI as MARGIN_CONTRACT_ABI
from ..bindings.margin_account_registry import ABI as MARGIN_ACCOUNT_REGISTRY_ABI
from ..bindings.product_registry import ABI as PRODUCT_REGISTRY_ABI
from ..decorators import convert_web3_error
from ..exceptions import NotFoundError
from ..schemas import AuctionData, Bid, OrderSide, Position, Transaction
from .base import ClearingSystemAPI


class MarginAccount(ClearingSystemAPI):
    """API for managing margin accounts."""

    ### Factories ###

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

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def authorize(self, collateral_asset: str, intent_account_id: str) -> Transaction:
        """Authorizes a blockchain account to submit intents to the clearing system
        using the margin account associated with the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.
        intent_account_id : str
            The address of the intent account.

        Returns
        -------
        afp.schemas.Transaction
            Transaction parameters.
        """
        collateral_asset = validators.validate_address(collateral_asset)
        intent_account_id = validators.validate_address(intent_account_id)
        return self._transact(
            self._margin_contract(collateral_asset).authorize(intent_account_id)
        )

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def deposit(
        self, collateral_asset: str, amount: Decimal
    ) -> tuple[Transaction, Transaction]:
        """Deposits the specified amount of collateral tokens into the margin account
        associated with the collateral asset.

        First approves the token transfer with the collateral token, then executes the
        transfer.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.
        amount : Decimal
            The amount of collateral tokens to deposit.

        Returns
        -------
        afp.schemas.Transaction
            Parameters of the approval transaction.
        afp.schemas.Transaction
            Parameters of the deposit transaction.
        """
        collateral_asset = validators.validate_address(collateral_asset)
        token_amount = int(amount * 10 ** self._decimals(collateral_asset))
        token_contract = ERC20(self._w3, collateral_asset)

        tx1 = self._transact(
            token_contract.approve(
                self._margin_contract(collateral_asset)._contract.address,  # type: ignore
                token_amount,
            )
        )
        tx2 = self._transact(
            self._margin_contract(collateral_asset).deposit(token_amount)
        )
        return (tx1, tx2)

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def withdraw(self, collateral_asset: str, amount: Decimal) -> Transaction:
        """Withdraws the specified amount of collateral tokens from the margin account
        associated with the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.
        amount : Decimal
            The amount of collateral tokens to withdraw.

        Returns
        -------
        afp.schemas.Transaction
            Transaction parameters.
        """
        collateral_asset = validators.validate_address(collateral_asset)
        token_amount = int(amount * 10 ** self._decimals(collateral_asset))
        return self._transact(
            self._margin_contract(collateral_asset).withdraw(token_amount)
        )

    @convert_web3_error(CLEARING_DIAMOND_ABI)
    def request_liquidation(
        self, margin_account_id: str, collateral_asset: str
    ) -> Transaction:
        """Request a liquidation auction to be started.

        Parameters
        ----------
        margin_account_id : str
            The ID of the margin account to be liquidated.
        collateral_asset : str
            The address of the collateral token that the margin account is trading with.

        Returns
        -------
        afp.schemas.Transaction
            Transaction parameters.
        """
        margin_account_id = validators.validate_address(margin_account_id)
        collateral_asset = validators.validate_address(collateral_asset)

        clearing_contract = ClearingDiamond(
            self._w3, self._config.clearing_diamond_address
        )
        return self._transact(
            clearing_contract.request_liquidation(margin_account_id, collateral_asset)
        )

    @convert_web3_error(CLEARING_DIAMOND_ABI, PRODUCT_REGISTRY_ABI)
    def submit_bids(
        self, margin_account_id: str, collateral_asset: str, bids: Iterable[Bid]
    ) -> Transaction:
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
        afp.schemas.Transaction
            Transaction parameters.
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

        clearing_contract = ClearingDiamond(
            self._w3, self._config.clearing_diamond_address
        )
        return self._transact(
            clearing_contract.bid_auction(
                margin_account_id, collateral_asset, converted_bids
            )
        )

    ### Views ###

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def capital(self, collateral_asset: str) -> Decimal:
        """Returns the amount of collateral tokens in the margin account associated
        with the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        Decimal
        """
        collateral_asset = validators.validate_address(collateral_asset)
        amount = self._margin_contract(collateral_asset).capital(
            self._authenticator.address
        )
        return Decimal(amount) / 10 ** self._decimals(collateral_asset)

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def position(self, collateral_asset: str, position_id: str) -> Position:
        """Returns the parameters of a position in the margin account associated with
        the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.
        position_id: str
            The ID of the position.

        Returns
        -------
        afp.schemas.Position
        """
        validators.validate_hexstr32(position_id)
        data = self._margin_contract(collateral_asset).position_data(
            self._authenticator.address, HexBytes(position_id)
        )
        decimals = self._decimals(collateral_asset)
        return Position(
            id=Web3.to_hex(data.position_id),
            quantity=data.quantity,
            cost_basis=Decimal(data.cost_basis) / 10**decimals,
            maintenance_margin=Decimal(data.maintenance_margin) / 10**decimals,
            pnl=Decimal(data.pnl) / 10**decimals,
        )

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def positions(self, collateral_asset: str) -> list[Position]:
        """Returns all positions in the margin account associated with the collateral
        asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        list of afp.schemas.Position
        """
        collateral_asset = validators.validate_address(collateral_asset)
        position_ids = self._margin_contract(collateral_asset).positions(
            self._authenticator.address
        )
        return [self.position(collateral_asset, Web3.to_hex(id)) for id in position_ids]

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def equity(self, collateral_asset: str) -> Decimal:
        """Returns the margin account equity in the margin account associated with the
        collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        Decimal
        """
        collateral_asset = validators.validate_address(collateral_asset)
        amount = self._margin_contract(collateral_asset).mae(
            self._authenticator.address
        )
        return Decimal(amount) / 10 ** self._decimals(collateral_asset)

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def maintenance_margin_available(self, collateral_asset: str) -> Decimal:
        """Returns the maintenance margin available in the margin account associated
        with the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        Decimal
        """
        collateral_asset = validators.validate_address(collateral_asset)
        amount = self._margin_contract(collateral_asset).mma(
            self._authenticator.address
        )
        return Decimal(amount) / 10 ** self._decimals(collateral_asset)

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def maintenance_margin_used(self, collateral_asset: str) -> Decimal:
        """Returns the maintenance margin used in the margin account associated with
        the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        Decimal
        """
        collateral_asset = validators.validate_address(collateral_asset)
        amount = self._margin_contract(collateral_asset).mmu(
            self._authenticator.address
        )
        return Decimal(amount) / 10 ** self._decimals(collateral_asset)

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def profit_and_loss(self, collateral_asset: str) -> Decimal:
        """Returns the profit and loss in the margin account associated with the
        collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        Decimal
        """
        collateral_asset = validators.validate_address(collateral_asset)
        amount = self._margin_contract(collateral_asset).pnl(
            self._authenticator.address
        )
        return Decimal(amount) / 10 ** self._decimals(collateral_asset)

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def withdrawable_amount(self, collateral_asset: str) -> Decimal:
        """Returns the amount of collateral tokens withdrawable from the margin account
        associated with the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        Decimal
        """
        collateral_asset = validators.validate_address(collateral_asset)
        amount = self._margin_contract(collateral_asset).withdrawable(
            self._authenticator.address
        )
        return Decimal(amount) / 10 ** self._decimals(collateral_asset)

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

        clearing_contract = ClearingDiamond(
            self._w3, self._config.clearing_diamond_address
        )
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
    @convert_web3_error(MARGIN_ACCOUNT_REGISTRY_ABI)
    def _margin_contract(self, collateral_asset: ChecksumAddress) -> MarginContract:
        margin_account_registry_contract = MarginAccountRegistry(
            self._w3, self._config.margin_account_registry_address
        )
        try:
            margin_contract_address = (
                margin_account_registry_contract.get_margin_account(
                    Web3.to_checksum_address(collateral_asset)
                )
            )
        except ContractCustomError:
            raise NotFoundError("No margin account found for collateral asset")
        return MarginContract(self._w3, margin_contract_address)

    @cache
    def _tick_size(self, product_id: str) -> int:
        product_registry_contract = ProductRegistry(
            self._w3, self._config.product_registry_address
        )
        return product_registry_contract.tick_size(HexBytes(product_id))
