"""AFP data structures."""

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
    model_validator,
)

from . import validators
from .enums import ListingState, OrderSide, OrderState, OrderType, TradeState


# Use datetime internally but UNIX timestamp in client-server communication
Timestamp = Annotated[
    datetime,
    BeforeValidator(validators.ensure_datetime),
    AfterValidator(validators.validate_non_negative_timestamp),
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


class IntentData(Model):
    trading_protocol_id: str
    product_id: str
    limit_price: Decimal
    quantity: Annotated[int, Field(gt=0)]
    max_trading_fee_rate: Decimal
    side: OrderSide
    good_until_time: Timestamp
    nonce: int
    referral: Annotated[str, AfterValidator(validators.validate_address)]


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
    fsv_decimals: Annotated[int, Field(ge=0, le=255)]  # uint8
    fsp_alpha: Decimal
    fsp_beta: Decimal
    fsv_calldata: Annotated[str, AfterValidator(validators.validate_hexstr)]


class ProductMetadata(Model):
    builder: Annotated[str, AfterValidator(validators.validate_address)]
    symbol: str
    description: str


class BaseProduct(Model):
    metadata: ProductMetadata
    oracle_spec: OracleSpecification
    collateral_asset: Annotated[str, AfterValidator(validators.validate_address)]
    start_time: Timestamp
    point_value: Decimal
    price_decimals: Annotated[int, Field(ge=0, le=255)]
    extended_metadata: str = ""


class PredictionProductV1(Model):
    base: BaseProduct
    expiry_spec: ExpirySpecification
    min_price: Decimal
    max_price: Decimal

    @model_validator(mode="after")
    def validate_price_limits(self) -> Self:
        validators.validate_price_limits(self.min_price, self.max_price)
        return self


class ApiSpec(Model):
    standard: Literal["JSONPath", "GraphQL"]
    spec_variant: Literal["underlying-history", "product-fsv"]


class ApiSpecJSONPath(ApiSpec):
    url: Annotated[str, Field(min_length=1, max_length=2083)]
    date_path: str
    value_path: str
    auth_param_location: Literal["query", "header", "none"] = "none"
    auth_param_name: str | None = None
    auth_param_prefix: str | None = None
    continuation_token_param: str | None = None
    continuation_token_path: str | None = None
    date_format_custom: str | None = None
    date_format_type: Literal["iso_8601", "unix_timestamp", "custom"] = "iso_8601"
    headers: dict[str, str] | None = None
    max_pages: Annotated[int | None, Field(ge=1)] = 10
    timestamp_scale: Annotated[int | float, Field(ge=1)] = 1
    timezone: str = "UTC"


class BaseCaseResolution(Model):
    fsp_resolution: Annotated[str, Field(min_length=1)]


class EdgeCase(Model):
    condition: Annotated[str, Field(min_length=1)]
    fsp_resolution: Annotated[str, Field(min_length=1)]


class OutcomeSpaceEvent(Model):
    description: Annotated[str, Field(min_length=1)]
    outcome_statement: Annotated[str, Field(min_length=1)]
    base_case: BaseCaseResolution
    category: str | None = None
    expected_resolution_date: str | None = None
    tags: list[str]
    edge_cases: list[EdgeCase]


class OutcomeSpaceTimeSeries(Model):
    description: Annotated[str, Field(min_length=1)]
    outcome_statement: Annotated[str, Field(min_length=1)]
    base_case: BaseCaseResolution
    frequency: Literal["daily", "weekly", "monthly", "quarterly", "yearly"]
    units: Annotated[str, Field(min_length=1)]
    source_name: Annotated[str, Field(min_length=1)]
    source_uri: Annotated[str, Field(min_length=1, max_length=2083)]
    edge_cases: list[EdgeCase]
    history_api_spec: ApiSpecJSONPath | ApiSpec | None = None


class OutcomePointEvent(Model):
    outcome: Annotated[str, Field(min_length=1)]


class OutcomePointTimeSeries(Model):
    reference_date: str
    release_date: str | None = None


class OracleConfig(Model):
    description: Annotated[str, Field(min_length=1)]
    project_url: Annotated[str | None, Field(min_length=1, max_length=2083)] = None


class OracleConfigPrototype1(OracleConfig):
    evaluation_api_spec: ApiSpecJSONPath | ApiSpec


class PredictionProduct(Model):
    product: PredictionProductV1
    outcome_space: OutcomeSpaceTimeSeries | OutcomeSpaceEvent
    outcome_point: OutcomePointTimeSeries | OutcomePointEvent
    oracle_config: OracleConfigPrototype1 | OracleConfig | None = None
