import secrets
from datetime import datetime
from decimal import Decimal
from typing import Generator

from web3 import Web3

from .. import signing, validators
from ..decorators import refresh_token_on_expiry
from ..enums import OrderType
from ..schemas import (
    ExchangeProduct,
    Intent,
    IntentData,
    MarketDepthData,
    Order,
    OrderCancellationData,
    OrderFill,
    OrderFillFilter,
    OrderSide,
    OrderSubmission,
    TradeState,
)
from .base import ExchangeAPI


class Trading(ExchangeAPI):
    """API for trading in the AutEx exchange.

    Authenticates with the exchange on creation.

    Parameters
    ----------
    private_key : str
        The private key of the account that submits intents to the exchange.

    Raises
    ------
    afp.exceptions.AuthenticationError
        If the exchange rejects the login attempt.
    """

    @staticmethod
    def _generate_nonce() -> int:
        return secrets.randbelow(2**31)  # Postgres integer range

    def create_intent(
        self,
        *,
        product: ExchangeProduct,
        side: str,
        limit_price: Decimal,
        quantity: int,
        max_trading_fee_rate: Decimal,
        good_until_time: datetime,
        margin_account_id: str | None = None,
    ) -> Intent:
        """Creates an intent with the given intent data, generates its hash and signs it
        with the configured account's private key.

        The intent account's address is derived from the private key. The intent account
        is assumed to be the same as the margin account if the margin account ID is not
        specified.

        Parameters
        ----------
        product : afp.schemas.ExchangeProduct
        side : str
        limit_price : decimal.Decimal
        quantity : decimal.Decimal
        max_trading_fee_rate : decimal.Decimal
        good_until_time : datetime.datetime
        margin_account_id : str, optional

        Returns
        -------
        afp.schemas.Intent
        """
        margin_account_id = (
            validators.validate_address(margin_account_id)
            if margin_account_id is not None
            else self._account.address
        )

        intent_data = IntentData(
            trading_protocol_id=self._trading_protocol_id,
            product_id=product.id,
            limit_price=limit_price,
            quantity=quantity,
            max_trading_fee_rate=max_trading_fee_rate,
            side=getattr(OrderSide, side.upper()),
            good_until_time=good_until_time,
            nonce=self._generate_nonce(),
        )
        intent_hash = signing.generate_intent_hash(
            intent_data=intent_data,
            margin_account_id=margin_account_id,
            intent_account_id=self._account.address,
            tick_size=product.tick_size,
        )
        signature = signing.sign_message(self._account, intent_hash)
        return Intent(
            hash=Web3.to_hex(intent_hash),
            margin_account_id=margin_account_id,
            intent_account_id=self._account.address,
            signature=Web3.to_hex(signature),
            data=intent_data,
        )

    @refresh_token_on_expiry
    def submit_limit_order(self, intent: Intent) -> Order:
        """Sends an intent expressing a limit order to the exchange.

        Parameters
        ----------
        intent : afp.schemas.Intent

        Returns
        -------
        afp.schemas.Order

        Raises
        ------
        afp.exceptions.ValidationError
            If the exchange rejects the intent.
        """
        submission = OrderSubmission(
            type=OrderType.LIMIT_ORDER,
            intent=intent,
        )
        return self._exchange.submit_order(submission)

    @refresh_token_on_expiry
    def submit_cancel_order(self, intent_hash: str) -> Order:
        """Sends a cancellation order to the exchange.

        Parameters
        ----------
        intent_hash : str

        Returns
        -------
        afp.schemas.Order

        Raises
        ------
        afp.exceptions.ValidationError
            If the exchange rejects the cancellation.
        """
        nonce = self._generate_nonce()
        cancellation_hash = signing.generate_order_cancellation_hash(nonce, intent_hash)
        signature = signing.sign_message(self._account, cancellation_hash)
        cancellation_data = OrderCancellationData(
            intent_hash=intent_hash,
            nonce=nonce,
            intent_account_id=self._account.address,
            signature=Web3.to_hex(signature),
        )
        submission = OrderSubmission(
            type=OrderType.CANCEL_ORDER,
            cancellation_data=cancellation_data,
        )
        return self._exchange.submit_order(submission)

    @refresh_token_on_expiry
    def products(self) -> list[ExchangeProduct]:
        """Retrieves the products approved for trading on the exchange.

        Returns
        -------
        list of afp.schemas.ExchangeProduct
        """
        return self._exchange.get_approved_products()

    @refresh_token_on_expiry
    def product(self, product_id: str) -> ExchangeProduct:
        """Retrieves a product for trading by its ID.

        Parameters
        ----------
        product_id : str

        Returns
        -------
        afp.schemas.ExchangeProduct

        Raises
        ------
        afp.exceptions.NotFoundError
            If no such product exists.
        """
        value = validators.validate_hexstr32(product_id)
        return self._exchange.get_product_by_id(value)

    @refresh_token_on_expiry
    def order(self, order_id: str) -> Order:
        """Retrieves an order by its ID from the orders that have been submitted by the
        authenticated account.

        Parameters
        ----------
        order_id : str

        Returns
        -------
        afp.schemas.Order

        Raises
        ------
        afp.exceptions.NotFoundError
            If no such order exists.
        """
        value = validators.validate_hexstr32(order_id)
        return self._exchange.get_order_by_id(value)

    @refresh_token_on_expiry
    def open_orders(self) -> list[Order]:
        """Retrieves all open and partially filled limit orders that have been submitted
        by the authenticated account.

        Returns
        -------
        list of afp.schemas.Order
        """
        return self._exchange.get_open_orders()

    @refresh_token_on_expiry
    def order_fills(
        self,
        *,
        product_id: str | None = None,
        margin_account_id: str | None = None,
        intent_hash: str | None = None,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[OrderFill]:
        """Retrieves the authenticated account's order fills that match the given
        parameters.

        Parameters
        ----------
        product_id : str, optional
        margin_account_id : str, optional
        intent_hash : str, optional
        start : datetime.datetime, optional
        end : datetime.datetime, optional

        Returns
        -------
        list of afp.schemas.OrderFill
        """
        filter = OrderFillFilter(
            intent_account_id=self._account.address,
            product_id=product_id,
            margin_account_id=margin_account_id,
            intent_hash=intent_hash,
            start=start,
            end=end,
            trade_state=None,
        )
        return self._exchange.get_order_fills(filter)

    @refresh_token_on_expiry
    def iter_order_fills(
        self,
        *,
        product_id: str | None = None,
        margin_account_id: str | None = None,
        intent_hash: str | None = None,
    ) -> Generator[OrderFill, None, None]:
        """Subscribes to the authenticated account's new order fills that match the
        given parameters.

        Returns a generator that yields new order fills as they are published by the
        exchange. A new order fill gets publised as soon as there is a match in the
        order book, before the trade is submitted to clearing.

        Parameters
        ----------
        product_id : str, optional
        margin_account_id : str, optional
        intent_hash : str, optional

        Yields
        -------
        afp.schemas.OrderFill
        """
        filter = OrderFillFilter(
            intent_account_id=self._account.address,
            product_id=product_id,
            margin_account_id=margin_account_id,
            intent_hash=intent_hash,
            start=None,
            end=None,
            trade_state=TradeState.PENDING,
        )
        yield from self._exchange.iter_order_fills(filter)

    @refresh_token_on_expiry
    def market_depth(self, product_id: str) -> MarketDepthData:
        """Retrieves the depth of market for the given product.

        Parameters
        ----------
        product_id : str

        Returns
        -------
        afp.schemas.MarketDepthData

        Raises
        ------
        afp.exceptions.NotFoundError
            If no such product exists.
        """
        value = validators.validate_hexstr32(product_id)
        return self._exchange.get_market_depth_data(value)

    @refresh_token_on_expiry
    def iter_market_depth(
        self, product_id: str
    ) -> Generator[MarketDepthData, None, None]:
        """Subscribes to updates of the depth of market for the given product.

        Returns a generator that yields the updated market depth data as it is published
        by the exhange.

        Parameters
        ----------
        product_id : str

        Yields
        -------
        afp.schemas.MarketDepthData

        Raises
        ------
        afp.exceptions.NotFoundError
            If no such product exists.
        """
        value = validators.validate_hexstr32(product_id)
        yield from self._exchange.iter_market_depth_data(value)
