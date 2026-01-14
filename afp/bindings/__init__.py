"""Typed bindings around the smart contracts of the Autonomous Futures Protocol."""

from .facade import (
    ClearingDiamond,
    MarginAccountRegistry,
    OracleProvider,
    ProductRegistry,
    SystemViewer,
)
from .margin_account import MarginAccount
from .types import (
    BaseProduct,
    ClearingConfig,
    Config,
    ExpirySpecification,
    FinalSettlementConfig,
    FuturesProductV1,
    Intent,
    IntentData,
    MarginData,
    MarginSpecification,
    MarkPriceConfig,
    OracleSpecification,
    PositionData,
    PredictionProductV1,
    ProductMetadata,
    ProductState,
    Settlement,
    Side,
    Trade,
)

__all__ = (
    # Contract bindings
    "ClearingDiamond",
    "MarginAccount",
    "MarginAccountRegistry",
    "OracleProvider",
    "ProductRegistry",
    "SystemViewer",
    # Structures
    "BaseProduct",
    "ClearingConfig",
    "Config",
    "ExpirySpecification",
    "FinalSettlementConfig",
    "FuturesProductV1",
    "Intent",
    "IntentData",
    "MarginData",
    "MarginSpecification",
    "MarkPriceConfig",
    "OracleSpecification",
    "PositionData",
    "PredictionProductV1",
    "ProductMetadata",
    "ProductState",
    "Settlement",
    "Side",
    "Trade",
    # Enumerations
    "ProductState",
    "Side",
)
