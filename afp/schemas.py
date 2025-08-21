from datetime import datetime
from decimal import Decimal
from functools import partial
from typing import Annotated, Any

import inflection
from pydantic import (
    AfterValidator,
    AliasGenerator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
)

from . import validators
from .enums import OrderSide, OrderState, OrderType, TradeState


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


# Authentication


class LoginSubmission(Model):
    message: str
    signature: str


class ExchangeParameters(Model):
    trading_protocol_id: str
    trading_fee_rate: Decimal


# Trading API


class ExchangeProductSubmission(Model):
    id: Annotated[str, AfterValidator(validators.validate_hexstr32)]


class ExchangeProduct(Model):
    id: str
    symbol: str
    tick_size: int
    collateral_asset: str


class IntentData(Model):
    trading_protocol_id: str
    product_id: str
    limit_price: Annotated[Decimal, Field(gt=0)]
    quantity: Annotated[int, Field(gt=0)]
    max_trading_fee_rate: Annotated[Decimal, Field(ge=0)]
    side: OrderSide
    good_until_time: Timestamp
    nonce: int


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
    id: int
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


class OrderFillFilter(Model):
    intent_account_id: str
    product_id: None | Annotated[str, AfterValidator(validators.validate_hexstr32)]
    margin_account_id: (
        None | Annotated[str, AfterValidator(validators.validate_address)]
    )
    intent_hash: None | Annotated[str, AfterValidator(validators.validate_hexstr32)]
    start: None | Timestamp
    end: None | Timestamp
    trade_state: None | TradeState


class MarketDepthItem(Model):
    price: Decimal
    quantity: int


class MarketDepthData(Model):
    product_id: str
    bids: list[MarketDepthItem]
    asks: list[MarketDepthItem]


# Clearing API


class Position(Model):
    id: str
    quantity: int
    cost_basis: Decimal
    maintenance_margin: Decimal
    pnl: Decimal


# Builder API


class ProductSpecification(Model):
    id: str
    # Product Metadata
    builder_id: str
    symbol: str
    description: str
    # Orace Specification
    oracle_address: Annotated[str, AfterValidator(validators.validate_address)]
    fsv_decimals: Annotated[int, Field(ge=0, lt=256)]  # uint8
    fsp_alpha: Decimal
    fsp_beta: int
    fsv_calldata: Annotated[str, AfterValidator(validators.validate_hexstr)]
    # Product
    start_time: Timestamp
    earliest_fsp_submission_time: Timestamp
    collateral_asset: Annotated[str, AfterValidator(validators.validate_address)]
    price_quotation: str
    tick_size: Annotated[int, Field(ge=0)]
    unit_value: Annotated[Decimal, Field(gt=0)]
    initial_margin_requirement: Annotated[Decimal, Field(gt=0)]
    maintenance_margin_requirement: Annotated[Decimal, Field(gt=0)]
    offer_price_buffer: Annotated[Decimal, Field(ge=0, lt=1)]
    auction_bounty: Annotated[Decimal, Field(ge=0, le=1)]
    tradeout_interval: Annotated[int, Field(ge=0)]
    extended_metadata: str


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
