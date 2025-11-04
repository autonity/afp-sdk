import secrets
import warnings
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Generator, Iterable

from web3 import Web3

from .. import hashing, validators
from ..constants import DEFAULT_BATCH_SIZE
from ..decorators import refresh_token_on_expiry
from ..enums import OrderSide, OrderState, OrderType, TradeState
from ..schemas import (
    ExchangeProduct,
    ExchangeProductFilter,
    Intent,
    IntentData,
    MarketDepthData,
    OHLCVItem,
    Order,
    OrderFilter,
    OrderCancellationData,
    OrderFill,
    OrderFillFilter,
    OrderSubmission,
)
from .base import ExchangeAPI


class Trading(ExchangeAPI):
    """API for trading in the AutEx exchange."""

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
        rounding: str | None = None,
    ) -> Intent:
        """Creates an intent with the given intent data, generates its hash and signs it
        with the configured account's private key.

        The intent account's address is derived from the private key. The intent account
        is assumed to be the same as the margin account if the margin account ID is not
        specified.

        The limit price must have at most as many fractional digits as the product's
        tick size, or if `rounding` is specified then the limit price is rounded to the
        appropriate number of fractional digits. `rounding` may be one of
        `ROUND_CEILING`, `ROUND_FLOOR`, `ROUND_UP`, `ROUND_DOWN`, `ROUND_HALF_UP`,
        `ROUND_HALF_DOWN`, `ROUND_HALF_EVEN` and `ROUND_05UP`; see the rounding modes of
        the `decimal` module of the Python Standard Library.

        Parameters
        ----------
        product : afp.schemas.ExchangeProduct
        side : str
            One of `BID` and `ASK`.
        limit_price : decimal.Decimal
        quantity : decimal.Decimal
        max_trading_fee_rate : decimal.Decimal
        good_until_time : datetime.datetime
        margin_account_id : str, optional
        rounding : str, optional
            A rounding mode of the `decimal` module or `None` for no rounding.

        Returns
        -------
        afp.schemas.Intent
        """
        margin_account_id = (
            validators.validate_address(margin_account_id)
            if margin_account_id is not None
            else self._authenticator.address
        )

        intent_data = IntentData(
            trading_protocol_id=self._trading_protocol_id,
            product_id=product.id,
            limit_price=validators.validate_limit_price(
                Decimal(limit_price), product.tick_size, rounding
            ),
            quantity=quantity,
            max_trading_fee_rate=max_trading_fee_rate,
            side=OrderSide(side.upper()),
            good_until_time=good_until_time,
            nonce=self._generate_nonce(),
        )
        intent_hash = hashing.generate_intent_hash(
            intent_data=intent_data,
            margin_account_id=margin_account_id,
            intent_account_id=self._authenticator.address,
            tick_size=product.tick_size,
        )
        signature = self._authenticator.sign_message(intent_hash)
        return Intent(
            hash=Web3.to_hex(intent_hash),
            margin_account_id=margin_account_id,
            intent_account_id=self._authenticator.address,
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
        afp.exceptions.RateLimitExceeded
            If the exchange rejects the order because of too many requests from the
            authenticated account.
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
        afp.exceptions.NotFoundError
            If the exchange rejects the cancellation because the intent does not exist.
        afp.exceptions.RateLimitExceeded
            If the exchange rejects the cancellation because of too many requests from
            the authenticated account.
        afp.exceptions.ValidationError
            If the exchange rejects the cancellation because it is invalid.
        """
        nonce = self._generate_nonce()
        cancellation_hash = hashing.generate_order_cancellation_hash(nonce, intent_hash)
        signature = self._authenticator.sign_message(cancellation_hash)
        cancellation_data = OrderCancellationData(
            intent_hash=intent_hash,
            nonce=nonce,
            intent_account_id=self._authenticator.address,
            signature=Web3.to_hex(signature),
        )
        submission = OrderSubmission(
            type=OrderType.CANCEL_ORDER,
            cancellation_data=cancellation_data,
        )
        return self._exchange.submit_order(submission)

    def products(
        self,
        batch: int = 1,
        batch_size: int = DEFAULT_BATCH_SIZE,
        newest_first: bool = True,
    ) -> list[ExchangeProduct]:
        """Retrieves the products approved for trading on the exchange.

        If there are more than `batch_size` number of products then they can be queried
        in batches.

        Parameters
        ----------
        batch : int, optional
            1-based index of the batch of products.
        batch_size : int, optional
            The maximum number of products in one batch.
        newest_first : bool, optional
            Whether to sort products in descending or ascending order by creation time.

        Returns
        -------
        list of afp.schemas.ExchangeProduct
        """
        filter = ExchangeProductFilter(
            batch=batch, batch_size=batch_size, newest_first=newest_first
        )
        return self._exchange.get_approved_products(filter)

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
    def orders(
        self,
        *,
        product_id: str | None = None,
        intent_account_id: str | None = None,
        type_: str | None = None,
        states: Iterable[str] = (),
        side: str | None = None,
        start: datetime | None = None,
        end: datetime | None = None,
        batch: int = 1,
        batch_size: int = DEFAULT_BATCH_SIZE,
        newest_first: bool = True,
    ) -> list[Order]:
        """Retrieves the authenticated account's orders that match the given parameters.

        If there are more than `batch_size` number of orders then they can be queried
        in batches.

        Parameters
        ----------
        product_id : str, optional
        intent_account_id : str, optional
            Defaults to the address of the authenticated account.
        type_ : str, optional
            One of `LIMIT_ORDER` and `CANCEL_ORDER`.
        states : iterable of str
            Any of `RECEIVED`, `PENDING`, `OPEN`, `COMPLETED` and `REJECTED`.
        side : str, optional
            One of `BID` and `ASK`.
        start : datetime.datetime, optional
        end : datetime.datetime, optional
        batch : int, optional
            1-based index of the batch of orders.
        batch_size : int, optional
            The maximum number of orders in one batch.
        newest_first : bool, optional
            Whether to sort orders in descending or ascending order by creation time.

        Returns
        -------
        list of afp.schemas.OrderFill
        """
        if intent_account_id is None:
            intent_account_id = self._authenticator.address

        filter = OrderFilter(
            intent_account_id=intent_account_id,
            product_id=product_id,
            type=None if type_ is None else OrderType(type_.upper()),
            states=[OrderState(state.upper()) for state in states],
            side=None if side is None else OrderSide(side.upper()),
            start=start,
            end=end,
            batch=batch,
            batch_size=batch_size,
            newest_first=newest_first,
        )
        return self._exchange.get_orders(filter)

    @refresh_token_on_expiry
    def open_orders(self, product_id: str | None = None) -> list[Order]:
        """Deprecated alias of Trading.orders(type_="LIMIT_ORDER", states=("OPEN", "PARTIAL"))."""
        warnings.warn(
            "Trading.open_orders() is deprecated. Use "
            'Trading.orders(type_="LIMIT_ORDER", states=("OPEN", "PARTIAL")) instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        return self.orders(
            type_="limit_order", states=("open", "partial"), product_id=product_id
        )

    @refresh_token_on_expiry
    def order_fills(
        self,
        *,
        product_id: str | None = None,
        intent_account_id: str | None = None,
        intent_hash: str | None = None,
        start: datetime | None = None,
        end: datetime | None = None,
        trade_states: Iterable[str] = (),
        batch: int = 1,
        batch_size: int = DEFAULT_BATCH_SIZE,
        newest_first: bool = True,
    ) -> list[OrderFill]:
        """Retrieves the authenticated account's order fills that match the given
        parameters.

        If there are more than `batch_size` number of order fills then they can be
        queried in batches.

        Parameters
        ----------
        product_id : str, optional
        intent_account_id : str, optional
            Defaults to the address of the authenticated account.
        intent_hash : str, optional
        start : datetime.datetime, optional
        end : datetime.datetime, optional
        trade_states : iterable of str
            Any of `PENDING`, `CLEARED` and `REJECTED`.
        batch : int, optional
            1-based index of the batch of order fills.
        batch_size : int, optional
            The maximum number of order fills in one batch.
        newest_first : bool, optional
            Whether to sort order fills in descending or ascending order by creation time.

        Returns
        -------
        list of afp.schemas.OrderFill
        """
        if intent_account_id is None:
            intent_account_id = self._authenticator.address

        filter = OrderFillFilter(
            intent_account_id=intent_account_id,
            product_id=product_id,
            intent_hash=intent_hash,
            start=start,
            end=end,
            trade_states=[TradeState(state.upper()) for state in trade_states],
            batch=batch,
            batch_size=batch_size,
            newest_first=newest_first,
        )
        return self._exchange.get_order_fills(filter)

    @refresh_token_on_expiry
    def iter_order_fills(
        self,
        *,
        product_id: str | None = None,
        intent_account_id: str | None = None,
        intent_hash: str | None = None,
        trade_states: Iterable[str] = ("PENDING",),
    ) -> Generator[OrderFill, None, None]:
        """Subscribes to the authenticated account's new order fills that match the
        given parameters.

        Returns a generator that yields order fills as they are published by the
        exchange.

        If `trade_states` includes `PENDING` (the default value) then a new order fill
        is yielded as soon as there is a match in the order book, before the trade is
        submitted to clearing.

        If `trade_states` is empty or more than one trade state is specified then
        updates to order fills are yielded at every state transition.

        Parameters
        ----------
        product_id : str, optional
        intent_account_id : str, optional
            Defaults to the address of the authenticated account.
        intent_hash : str, optional
        trade_states: iterable of str
            Any of `PENDING`, `CLEARED` and `REJECTED`.

        Yields
        -------
        afp.schemas.OrderFill
        """
        if intent_account_id is None:
            intent_account_id = self._authenticator.address

        filter = OrderFillFilter(
            intent_account_id=intent_account_id,
            product_id=product_id,
            intent_hash=intent_hash,
            start=None,
            end=None,
            trade_states=[TradeState(state.upper()) for state in trade_states],
            batch=None,
            batch_size=None,
            newest_first=None,
        )
        yield from self._exchange.iter_order_fills(filter)

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

    def ohlcv(
        self,
        product_id: str,
        start: datetime | None = None,
        interval: timedelta = timedelta(minutes=5),
    ) -> list[OHLCVItem]:
        """Retrieves Open-High-Low-Close-Volume time series data for the given product.

        Parameters
        ----------
        product_id : str
        start : datetime
            Defaults to 1 day ago.
        interval : timedelta
            The distance between 2 data points. Gets rounded to a multiple of 5 seconds.
            Defaults to 5 minutes.

        Returns
        -------
        list of afp.schemas.OHLCVItem

        Raises
        ------
        afp.exceptions.NotFoundError
            If no such product exists.
        """
        if start is None:
            start = datetime.now() - timedelta(days=1)

        product_id = validators.validate_hexstr32(product_id)
        start_timestamp = int(start.timestamp())
        interval_secs = int(validators.validate_timedelta(interval).total_seconds())
        return self._exchange.get_time_series_data(
            product_id, start_timestamp, interval_secs
        )

    def iter_ohlcv(
        self, product_id: str, interval: timedelta = timedelta(seconds=5)
    ) -> Generator[OHLCVItem, None, None]:
        """Subscribes to Open-High-Low-Close-Volume time series data updates for the
        given product.

        Returns a generator that yields OHLCV data points as they are published
        by the exhange.

        Parameters
        ----------
        product_id : str
        interval : timedelta
            The distance between 2 data points. Gets rounded to a multiple of 5 seconds.
            Defaults to 5 seconds.

        Yields
        -------
        afp.schemas.OHLCVItem

        Raises
        ------
        afp.exceptions.NotFoundError
            If no such product exists.
        """
        product_id = validators.validate_hexstr32(product_id)
        start_timestamp = int(datetime.now().timestamp())
        interval_secs = int(validators.validate_timedelta(interval).total_seconds())
        yield from self._exchange.iter_time_series_data(
            product_id, start_timestamp, interval_secs
        )
