from datetime import datetime
from decimal import Decimal
from functools import partial
from typing import Annotated, Any, Literal, Self

import inflection
from pydantic import (
    AfterValidator,
    AliasGenerator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
    computed_field,
    model_validator,
)

from . import validators
from .enums import ListingState, OrderSide, OrderState, OrderType, TradeState


# Use datetime internally but UNIX timestamp in client-server communication
Timestamp = Annotated[
    datetime,
    BeforeValidator(validators.ensure_datetime),
    PlainSerializer(validators.ensure_timestamp, return_type=int, when_used="json"),
]


class Model(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            alias=partial(inflection.camelize, uppercase_first_letter=False),
        ),
        frozen=True,
        populate_by_name=True,
    )

    # Change the default value of by_alias to True
    def model_dump_json(self, by_alias: bool = True, **kwargs: Any) -> str:
        return super().model_dump_json(by_alias=by_alias, **kwargs)


class PaginationFilter(Model):
    batch: Annotated[None | int, Field(gt=0, exclude=True)]
    batch_size: Annotated[None | int, Field(gt=0, exclude=True)]
    newest_first: Annotated[None | bool, Field(exclude=True)]

    @computed_field
    @property
    def page(self) -> None | int:
        return self.batch

    @computed_field
    @property
    def page_size(self) -> None | int:
        return self.batch_size

    @computed_field
    @property
    def sort(self) -> None | Literal["ASC", "DESC"]:
        match self.newest_first:
            case None:
                return None
            case True:
                return "DESC"
            case False:
                return "ASC"


# Authentication


class LoginSubmission(Model):
    message: str
    signature: str


class ExchangeParameters(Model):
    trading_protocol_id: str
    maker_trading_fee_rate: Decimal
    taker_trading_fee_rate: Decimal


# Admin API


class ExchangeProductListingSubmission(Model):
    id: Annotated[str, AfterValidator(validators.validate_hexstr32)]


class ExchangeProductUpdateSubmission(Model):
    listing_state: ListingState


# Trading API


class ExchangeProduct(Model):
    id: str
    symbol: str
    tick_size: int
    collateral_asset: str
    listing_state: ListingState
    min_price: Decimal
    max_price: Decimal

    def __str__(self) -> str:
        return self.id


class ExchangeProductFilter(PaginationFilter):
    pass


class IntentData(Model):
    trading_protocol_id: str
    product_id: str
    limit_price: Decimal
    quantity: Annotated[int, Field(gt=0)]
    max_trading_fee_rate: Decimal
    side: OrderSide
    good_until_time: Timestamp
    nonce: int
    referral: Annotated[str | None, AfterValidator(validators.validate_address)] = None


class Intent(Model):
    hash: str
    margin_account_id: str
    intent_account_id: str
    signature: str
    data: IntentData


class Order(Model):
    id: str
    type: OrderType
    timestamp: Timestamp
    state: OrderState
    fill_quantity: int
    intent: Intent


class OrderFilter(PaginationFilter):
    intent_account_id: str
    product_id: None | Annotated[str, AfterValidator(validators.validate_hexstr32)]
    type: None | OrderType
    states: Annotated[list[OrderState], Field(exclude=True)]
    side: None | OrderSide
    start: None | Timestamp
    end: None | Timestamp

    @computed_field
    @property
    def state(self) -> str | None:
        return ",".join(self.states) if self.states else None


class OrderCancellationData(Model):
    intent_hash: Annotated[str, AfterValidator(validators.validate_hexstr32)]
    nonce: int
    intent_account_id: str
    signature: str


class OrderSubmission(Model):
    type: OrderType
    intent: Intent | None = None
    cancellation_data: OrderCancellationData | None = None


class Trade(Model):
    # Convert ID from int to str for backward compatibility
    id: Annotated[str, BeforeValidator(str)]
    product_id: str
    price: Decimal
    timestamp: Timestamp
    state: TradeState
    transaction_id: str | None
    rejection_reason: str | None


class OrderFill(Model):
    order: Order
    trade: Trade
    quantity: int
    price: Decimal
    trading_fee_rate: Decimal


class OrderFillFilter(PaginationFilter):
    intent_account_id: str
    product_id: None | Annotated[str, AfterValidator(validators.validate_hexstr32)]
    intent_hash: None | Annotated[str, AfterValidator(validators.validate_hexstr32)]
    start: None | Timestamp
    end: None | Timestamp
    trade_states: Annotated[list[TradeState], Field(exclude=True)]

    @computed_field
    @property
    def trade_state(self) -> str | None:
        return ",".join(self.trade_states) if self.trade_states else None


class MarketDepthItem(Model):
    price: Decimal
    quantity: int


class MarketDepthData(Model):
    product_id: str
    bids: list[MarketDepthItem]
    asks: list[MarketDepthItem]


class OHLCVItem(Model):
    timestamp: Timestamp
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


# Clearing API


class Transaction(Model):
    hash: str
    data: dict[str, Any]
    receipt: dict[str, Any]


class Position(Model):
    id: str
    quantity: int
    cost_basis: Decimal
    maintenance_margin: Decimal
    pnl: Decimal


# Product API


class ExpirySpecification(Model):
    earliest_fsp_submission_time: Timestamp
    tradeout_interval: Annotated[int, Field(ge=0)]


class OracleSpecification(Model):
    oracle_address: Annotated[str, AfterValidator(validators.validate_address)]
    fsv_decimals: Annotated[int, Field(ge=0, lt=256)]  # uint8
    fsp_alpha: Decimal
    fsp_beta: Decimal
    fsv_calldata: Annotated[str, AfterValidator(validators.validate_hexstr)]


class ProductMetadata(Model):
    builder_id: Annotated[str, AfterValidator(validators.validate_address)]
    symbol: str
    description: str


class BaseProduct(Model):
    id: str
    metadata: ProductMetadata
    oracle_spec: OracleSpecification
    collateral_asset: Annotated[str, AfterValidator(validators.validate_address)]
    start_time: Timestamp
    point_value: Annotated[Decimal, Field(gt=0)]
    price_decimals: Annotated[int, Field(ge=0)]
    extended_metadata: str = ""

    def __str__(self) -> str:
        return self.id


class PredictionProductV1(BaseProduct):
    expiry_spec: ExpirySpecification
    min_price: Decimal
    max_price: Decimal

    @model_validator(mode="after")
    def validate_price_limits(self) -> Self:
        validators.validate_price_limits(self.min_price, self.max_price)
        return self


# Liquidation API


class Bid(Model):
    product_id: Annotated[str, AfterValidator(validators.validate_hexstr32)]
    price: Annotated[Decimal, Field(gt=0)]
    quantity: Annotated[int, Field(gt=0)]
    side: OrderSide


class AuctionData(Model):
    start_block: int
    margin_account_equity_at_initiation: Decimal
    maintenance_margin_used_at_initiation: Decimal
    margin_account_equity_now: Decimal
    maintenance_margin_used_now: Decimal
