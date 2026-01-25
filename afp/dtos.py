"""Internal schemas for SDK - Exchange communication."""

from decimal import Decimal
from typing import Annotated, Literal

from pydantic import AfterValidator, Field, computed_field

from . import validators
from .enums import ListingState, OrderSide, OrderState, OrderType, TradeState
from .schemas import Intent, OrderCancellationData, Timestamp
from .types import AliasedModel, Model


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


class LoginSubmission(AliasedModel):
    message: str
    signature: str


class ExchangeParameters(AliasedModel):
    trading_protocol_id: str
    maker_trading_fee_rate: Decimal
    taker_trading_fee_rate: Decimal


# Admin API


class ExchangeProductListingSubmission(AliasedModel):
    id: Annotated[str, AfterValidator(validators.validate_hexstr32)]


class ExchangeProductUpdateSubmission(AliasedModel):
    listing_state: ListingState


# Trading API


class ExchangeProductFilter(PaginationFilter):
    pass


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


class OrderSubmission(AliasedModel):
    type: OrderType
    intent: Intent | None = None
    cancellation_data: OrderCancellationData | None = None


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
