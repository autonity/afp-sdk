"""AFP data structures."""

from decimal import Decimal
from typing import Annotated, Any, Literal, Self

from pydantic import AfterValidator, AnyUrl, BeforeValidator, Field, model_validator

from . import constants, validators
from .enums import ListingState, OrderSide, OrderState, OrderType, TradeState
from .types import AliasedModel, CID, ISODate, ISODateTime, Model, Timestamp


# Trading API


class ExchangeProduct(AliasedModel):
    id: str
    symbol: str
    tick_size: int
    collateral_asset: str
    listing_state: ListingState
    min_price: Decimal
    max_price: Decimal

    def __str__(self) -> str:
        return self.id


class IntentData(AliasedModel):
    trading_protocol_id: str
    product_id: str
    limit_price: Decimal
    quantity: Annotated[int, Field(gt=0)]
    max_trading_fee_rate: Annotated[
        Decimal,
        Field(le=Decimal((2**32 - 1) / constants.FEE_RATE_MULTIPLIER)),  # uint32
    ]
    side: OrderSide
    good_until_time: Timestamp
    nonce: int
    referral: Annotated[str, AfterValidator(validators.validate_address)]


class Intent(AliasedModel):
    hash: str
    margin_account_id: str
    intent_account_id: str
    signature: str
    data: IntentData


class Order(AliasedModel):
    id: str
    type: OrderType
    timestamp: Timestamp
    state: OrderState
    fill_quantity: int
    intent: Intent


class OrderCancellationData(AliasedModel):
    intent_hash: Annotated[str, AfterValidator(validators.validate_hexstr32)]
    nonce: int
    intent_account_id: str
    signature: str


class Trade(AliasedModel):
    # Convert ID from int to str for backward compatibility
    id: Annotated[str, BeforeValidator(str)]
    product_id: str
    price: Decimal
    timestamp: Timestamp
    state: TradeState
    transaction_id: str | None
    rejection_reason: str | None


class OrderFill(AliasedModel):
    order: Order
    trade: Trade
    quantity: int
    price: Decimal
    trading_fee_rate: Decimal


class MarketDepthItem(AliasedModel):
    price: Decimal
    quantity: int


class MarketDepthData(AliasedModel):
    product_id: str
    bids: list[MarketDepthItem]
    asks: list[MarketDepthItem]


class OHLCVItem(AliasedModel):
    timestamp: Timestamp
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


# Margin Account API


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


class ExpirySpecification(AliasedModel):
    earliest_fsp_submission_time: ISODateTime
    tradeout_interval: Annotated[int, Field(ge=0)]


class OracleSpecification(AliasedModel):
    oracle_address: Annotated[str, AfterValidator(validators.validate_address)]
    fsv_decimals: Annotated[int, Field(ge=0, le=255)]  # uint8
    fsp_alpha: Decimal
    fsp_beta: Decimal
    fsv_calldata: Annotated[str, AfterValidator(validators.validate_hexstr)]


class ProductMetadata(AliasedModel):
    builder: Annotated[str, AfterValidator(validators.validate_address)]
    symbol: Annotated[
        str,
        Field(pattern=r"^[A-Z0-9]{1,16}$", min_length=1, max_length=16),
    ]
    description: str


class BaseProduct(AliasedModel):
    metadata: ProductMetadata
    oracle_spec: OracleSpecification
    collateral_asset: Annotated[str, AfterValidator(validators.validate_address)]
    start_time: ISODateTime
    point_value: Decimal
    price_decimals: Annotated[int, Field(ge=0, le=255)]  # uint8
    extended_metadata: CID


class PredictionProductV1(AliasedModel):
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
    spec_variant: Literal["underlying-history", "product-fsv"] | None = None


class ApiSpecJSONPath(ApiSpec):
    standard: Literal["JSONPath"] = "JSONPath"  # type: ignore
    url: Annotated[
        AnyUrl,
        Field(min_length=1, max_length=2083),
        AfterValidator(validators.verify_url),
    ]
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
    timezone: Annotated[
        str,
        Field(pattern=r"^[A-Za-z][A-Za-z0-9_+-]*(/[A-Za-z][A-Za-z0-9_+-]*)*$"),
    ] = "UTC"


class BaseCaseResolution(Model):
    condition: Annotated[str, Field(min_length=1)]
    fsp_resolution: Annotated[str, Field(min_length=1)]


class EdgeCase(Model):
    condition: Annotated[str, Field(min_length=1)]
    fsp_resolution: Annotated[str, Field(min_length=1)]


class OutcomeSpace(Model):
    fsp_type: Literal["scalar", "binary", "ternary"]
    description: Annotated[str, Field(min_length=1)]
    base_case: BaseCaseResolution
    edge_cases: Annotated[list[EdgeCase], Field(default_factory=list)]


class OutcomeSpaceScalar(OutcomeSpace):
    fsp_type: Literal["scalar"] = "scalar"  # type: ignore
    units: Annotated[str, Field(min_length=1)]
    source_name: Annotated[str, Field(min_length=1)]
    source_uri: Annotated[
        AnyUrl,
        Field(min_length=1, max_length=2083),
        AfterValidator(validators.verify_url),
    ]


class OutcomeSpaceTimeSeries(OutcomeSpaceScalar):
    frequency: Literal[
        "daily",
        "weekly",
        "fortnightly",
        "semimonthly",
        "monthly",
        "quarterly",
        "yearly",
    ]
    history_api_spec: ApiSpecJSONPath | ApiSpec | None = None


class OutcomePoint(Model):
    fsp_type: Literal["scalar", "binary", "ternary"]


class TemporalObservation(Model):
    reference_date: ISODate
    release_date: ISODate


class OutcomePointScalar(OutcomePoint):
    pass


class OutcomePointEvent(OutcomePoint):
    fsp_type: Literal["binary", "ternary"]  # type: ignore
    outcome: Annotated[str, Field(min_length=1)]


class OutcomePointTimeSeries(OutcomePointScalar):
    fsp_type: Literal["scalar"] = "scalar"  # type: ignore
    observation: TemporalObservation


class OracleConfig(Model):
    description: Annotated[str, Field(min_length=1)]
    project_url: Annotated[
        AnyUrl | None,
        Field(min_length=1, max_length=2083),
        AfterValidator(validators.verify_url),
    ] = None


class OracleConfigPrototype1(OracleConfig):
    evaluation_api_spec: ApiSpecJSONPath | ApiSpec


class OracleFallback(Model):
    fallback_time: ISODateTime
    fallback_fsp: Decimal


class PredictionProduct(Model):
    product: PredictionProductV1
    outcome_space: OutcomeSpace
    outcome_point: OutcomePoint
    oracle_config: OracleConfig
    oracle_fallback: OracleFallback
