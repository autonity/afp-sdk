from enum import StrEnum


class OrderType(StrEnum):
    LIMIT_ORDER = "LIMIT_ORDER"
    CANCEL_ORDER = "CANCEL_ORDER"


class OrderState(StrEnum):
    RECEIVED = "RECEIVED"
    PENDING = "PENDING"
    OPEN = "OPEN"
    PARTIAL = "PARTIAL"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class OrderSide(StrEnum):
    BID = "BID"
    ASK = "ASK"


class TradeState(StrEnum):
    PENDING = "PENDING"
    CLEARED = "CLEARED"
    REJECTED = "REJECTED"
