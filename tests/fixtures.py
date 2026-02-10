"""Shared test fixtures and helpers for integration tests."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from unittest.mock import Mock

import ipld_car  # type: ignore (untyped library)
from requests import Response

from afp.dtos import (
    ComponentLink,
    ExchangeParameters,
    ExchangeProductListingSubmission,
    ExchangeProductUpdateSubmission,
    ExtendedMetadata,
    ExtendedMetadataDAG,
    LoginSubmission,
    OrderSubmission,
)
from afp.enums import ListingState, OrderSide, OrderState, OrderType, TradeState
from afp.schemas import (
    ExchangeProduct,
    IntentData,
    MarketDepthData,
    MarketDepthItem,
    OHLCVItem,
    OracleFallback,
    Order,
    OrderFill,
    OutcomePointTimeSeries,
    OutcomeSpaceTimeSeries,
    Trade,
)


# Sample data factories for DTOs


def make_exchange_product(**overrides: Any) -> ExchangeProduct:
    """Create a sample ExchangeProduct with optional field overrides."""
    defaults = {
        "id": "0x1234567890123456789012345678901234567890123456789012345678901234",
        "symbol": "BTCUSD",
        "tick_size": 1,
        "collateral_asset": "0x0000000000000000000000000000000000000001",
        "listing_state": ListingState.PUBLIC,
        "min_price": Decimal("0"),
        "max_price": Decimal("100000"),
    }
    return ExchangeProduct(**{**defaults, **overrides})


def make_intent_data(**overrides: Any) -> IntentData:
    """Create a sample IntentData with optional field overrides."""
    defaults = {
        "trading_protocol_id": "0xabcd",
        "product_id": "0x1234567890123456789012345678901234567890123456789012345678901234",
        "limit_price": Decimal("50000"),
        "quantity": 100,
        "max_trading_fee_rate": Decimal("0.001"),
        "side": OrderSide.BID,
        "good_until_time": 1700000000,
        "nonce": 1,
        "referral": "0x0000000000000000000000000000000000000000",
    }
    return IntentData(**{**defaults, **overrides})


def make_order(**overrides: Any) -> Order:
    """Create a sample Order with optional field overrides."""
    intent_data = make_intent_data()
    defaults = {
        "id": "order-123",
        "type": OrderType.LIMIT_ORDER,
        "timestamp": 1700000000,
        "state": OrderState.OPEN,
        "fill_quantity": 0,
        "intent": {
            "hash": "0x9876543210987654321098765432109876543210987654321098765432109876",
            "margin_account_id": "0x1111111111111111111111111111111111111111",
            "intent_account_id": "0x2222222222222222222222222222222222222222",
            "signature": "0xabcdef",
            "data": intent_data.model_dump(),
        },
    }
    return Order(**{**defaults, **overrides})


def make_trade(**overrides: Any) -> Trade:
    """Create a sample Trade with optional field overrides."""
    defaults = {
        "id": "123",
        "product_id": "0x1234567890123456789012345678901234567890123456789012345678901234",
        "price": Decimal("50000"),
        "timestamp": 1700000000,
        "state": TradeState.CLEARED,
        "transaction_id": "0xabc123",
        "rejection_reason": None,
    }
    return Trade(**{**defaults, **overrides})


def make_order_fill(**overrides: Any) -> OrderFill:
    """Create a sample OrderFill with optional field overrides."""
    defaults = {
        "order": make_order().model_dump(),
        "trade": make_trade().model_dump(),
        "quantity": 50,
        "price": Decimal("50000"),
        "trading_fee_rate": Decimal("0.001"),
    }
    return OrderFill(**{**defaults, **overrides})


def make_market_depth_item(**overrides: Any) -> MarketDepthItem:
    """Create a sample MarketDepthItem with optional field overrides."""
    defaults = {
        "price": Decimal("50000"),
        "quantity": 100,
    }
    return MarketDepthItem(**{**defaults, **overrides})


def make_market_depth_data(**overrides: Any) -> MarketDepthData:
    """Create a sample MarketDepthData with optional field overrides."""
    defaults = {
        "product_id": "0x1234567890123456789012345678901234567890123456789012345678901234",
        "bids": [
            make_market_depth_item(price=Decimal("49900"), quantity=50).model_dump(),
            make_market_depth_item(price=Decimal("49800"), quantity=100).model_dump(),
        ],
        "asks": [
            make_market_depth_item(price=Decimal("50100"), quantity=50).model_dump(),
            make_market_depth_item(price=Decimal("50200"), quantity=100).model_dump(),
        ],
    }
    return MarketDepthData(**{**defaults, **overrides})


def make_ohlcv_item(**overrides: Any) -> OHLCVItem:
    """Create a sample OHLCVItem with optional field overrides."""
    defaults = {
        "timestamp": 1700000000,
        "open": Decimal("50000"),
        "high": Decimal("51000"),
        "low": Decimal("49000"),
        "close": Decimal("50500"),
        "volume": 1000,
    }
    return OHLCVItem(**{**defaults, **overrides})


def make_login_submission(**overrides: Any) -> LoginSubmission:
    """Create a sample LoginSubmission with optional field overrides."""
    defaults = {
        "message": "Login message",
        "signature": "0xabcdef1234567890",
    }
    return LoginSubmission(**{**defaults, **overrides})


def make_exchange_parameters(**overrides: Any) -> ExchangeParameters:
    """Create a sample ExchangeParameters with optional field overrides."""
    defaults = {
        "trading_protocol_id": "0xabcd",
        "maker_trading_fee_rate": Decimal("0.001"),
        "taker_trading_fee_rate": Decimal("0.002"),
    }
    return ExchangeParameters(**{**defaults, **overrides})


def make_order_submission(**overrides: Any) -> OrderSubmission:
    """Create a sample OrderSubmission with optional field overrides."""
    intent_data = make_intent_data()
    defaults = {
        "type": OrderType.LIMIT_ORDER,
        "intent": {
            "hash": "0x9876543210987654321098765432109876543210987654321098765432109876",
            "margin_account_id": "0x1111111111111111111111111111111111111111",
            "intent_account_id": "0x2222222222222222222222222222222222222222",
            "signature": "0xabcdef",
            "data": intent_data.model_dump(),
        },
        "cancellation_data": None,
    }
    return OrderSubmission(**{**defaults, **overrides})


def make_product_listing_submission(
    **overrides: Any,
) -> ExchangeProductListingSubmission:
    """Create a sample ExchangeProductListingSubmission."""
    defaults = {
        "id": "0x1234567890123456789012345678901234567890123456789012345678901234",
    }
    return ExchangeProductListingSubmission(**{**defaults, **overrides})


def make_product_update_submission(**overrides: Any) -> ExchangeProductUpdateSubmission:
    """Create a sample ExchangeProductUpdateSubmission."""
    defaults = {
        "listing_state": ListingState.PUBLIC,
    }
    return ExchangeProductUpdateSubmission(**{**defaults, **overrides})


# IPFS-specific fixtures


def make_outcome_space_time_series(**overrides: Any) -> OutcomeSpaceTimeSeries:
    """Create a sample OutcomeSpaceTimeSeries with optional field overrides."""
    defaults = {
        "fsp_type": "scalar",
        "description": "Test outcome space",
        "base_case": {
            "condition": "value is valid",
            "fsp_resolution": "value",
        },
        "edge_cases": [],
        "units": "USD",
        "source_name": "Test Source",
        "source_uri": "https://example.com/data",
        "frequency": "daily",
        "history_api_spec": None,
    }
    return OutcomeSpaceTimeSeries(**{**defaults, **overrides})


def make_outcome_point_time_series(**overrides: Any) -> OutcomePointTimeSeries:
    """Create a sample OutcomePointTimeSeries with optional field overrides."""
    defaults = {
        "fsp_type": "scalar",
        "observation": {
            "reference_date": "2024-01-01",
            "release_date": "2024-01-02",
        },
    }
    return OutcomePointTimeSeries(**{**defaults, **overrides})


def make_oracle_fallback(**overrides: Any) -> OracleFallback:
    """Create a sample OracleFallback with optional field overrides."""
    defaults = {
        "fallback_time": datetime(2025, 1, 15, tzinfo=timezone.utc),
        "fallback_fsp": Decimal("100"),
    }
    return OracleFallback(**{**defaults, **overrides})


def make_extended_metadata(**overrides: Any) -> ExtendedMetadata:
    """Create a sample ExtendedMetadata with optional field overrides."""
    from afp.schemas import OracleConfig

    defaults = {
        "outcome_space": make_outcome_space_time_series(),
        "outcome_point": make_outcome_point_time_series(),
        "oracle_config": OracleConfig(
            description="Test oracle",
            project_url="https://example.com",
        ),
        "oracle_fallback": make_oracle_fallback(),
    }
    return ExtendedMetadata(**{**defaults, **overrides})


def make_extended_metadata_dag(**overrides: Any) -> ExtendedMetadataDAG:
    """Create a sample ExtendedMetadataDAG with optional field overrides."""
    # Use real valid CIDs (minimum valid base32 CIDs)
    defaults = {
        "outcome_space": ComponentLink(
            data="bafyreiaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            schema_="bafyreibbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        ).model_dump(),
        "outcome_point": ComponentLink(
            data="bafyreiccccccccccccccccccccccccccccccccccccccccccccccccccccc",
            schema_="bafyreiddddddddddddddddddddddddddddddddddddddddddddddddddddd",
        ).model_dump(),
        "oracle_config": ComponentLink(
            data="bafyreieeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            schema_="bafyreifffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        ).model_dump(),
        "oracle_fallback": ComponentLink(
            data="bafyreiggggggggggggggggggggggggggggggggggggggggggggggggggggg",
            schema_="bafyreihhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh",
        ).model_dump(),
    }
    return ExtendedMetadataDAG(**{**defaults, **overrides})


# Response generators


def make_ndjson_response(items: list[Any]) -> Response:
    """Create a mock Response with iter_lines() returning NDJSON."""
    mock_response = Response()
    mock_response.status_code = 200
    mock_response._content = b""  # type: ignore
    mock_response.iter_lines = Mock(  # type: ignore
        return_value=iter([item.model_dump_json().encode() for item in items])
    )
    return mock_response


def make_error_response(status_code: int, detail: str | list[Any]) -> Response:
    """Generate standardized error responses for various HTTP codes."""
    import requests

    mock_response = Response()
    mock_response.status_code = status_code
    mock_response._content = b""  # type: ignore

    if isinstance(detail, str):
        mock_response.json = Mock(return_value={"detail": detail})  # type: ignore
    else:
        mock_response.json = Mock(return_value={"detail": detail})  # type: ignore

    # Simulate raise_for_status behavior
    http_error = requests.exceptions.HTTPError(response=mock_response)
    mock_response.raise_for_status = Mock(side_effect=http_error)  # type: ignore

    return mock_response


def make_success_response(data: dict[str, Any]) -> Response:
    """Create a mock successful Response."""
    mock_response = Response()
    mock_response.status_code = 200
    mock_response._content = b""  # type: ignore
    mock_response.json = Mock(return_value=data)  # type: ignore
    mock_response.history = []  # type: ignore
    return mock_response


# IPFS-specific helpers


def make_ipfs_car_response(root_cid: str) -> Response:
    """Create a mock IPFS CAR upload response."""
    mock_response = Response()
    mock_response.status_code = 200
    mock_response._content = b""  # type: ignore
    mock_response.json = Mock(  # type: ignore
        return_value={
            "Root": {
                "Cid": {"/": root_cid},
            },
        }
    )
    return mock_response


def make_ipfs_block_response(content: bytes) -> Response:
    """Create a mock IPFS block download response."""
    mock_response = Response()
    mock_response.status_code = 200
    mock_response._content = content  # type: ignore
    return mock_response


def make_car_bytes(blocks: list[ipld_car.Block]) -> bytes:
    """Generate CAR file bytes from blocks."""
    root_cid = blocks[0][0]
    return ipld_car.encode([root_cid], blocks).tobytes()
