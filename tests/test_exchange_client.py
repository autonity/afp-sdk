from datetime import datetime
from unittest.mock import Mock

import pytest
import requests
from requests import Response
from requests.adapters import HTTPAdapter

from afp.dtos import (
    ExchangeProductFilter,
    OrderFillFilter,
    OrderFilter,
)
from afp.enums import OrderSide, OrderState, TradeState
from afp.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ExchangeError,
    NotFoundError,
    RateLimitExceeded,
    ValidationError,
)
from afp.exchange import ExchangeClient

from .fixtures import (
    make_error_response,
    make_exchange_parameters,
    make_exchange_product,
    make_login_submission,
    make_market_depth_data,
    make_ndjson_response,
    make_ohlcv_item,
    make_order,
    make_order_fill,
    make_order_submission,
    make_product_listing_submission,
    make_product_update_submission,
    make_success_response,
)


def test_generate_login_nonce__success__returns_message(monkeypatch):
    """Test successful nonce generation."""
    fake_response = make_success_response({"message": "test-nonce-12345"})
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    nonce = client.generate_login_nonce()

    assert nonce == "test-nonce-12345"
    request = mock_send.call_args[0][0]
    assert request.method == "GET"
    assert "v1/nonce" in request.url


def test_login__success__returns_exchange_parameters(monkeypatch):
    """Test successful login with signature."""
    params = make_exchange_parameters(
        trading_protocol_id="0xabcd",
        maker_trading_fee_rate="0.001",
        taker_trading_fee_rate="0.002",
    )
    fake_response = make_success_response(params.model_dump())
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    login_submission = make_login_submission(
        message="test-nonce",
        signature="0xsignature",
    )
    result = client.login(login_submission)

    assert result.trading_protocol_id == "0xabcd"
    assert str(result.maker_trading_fee_rate) == "0.001"

    request = mock_send.call_args[0][0]
    assert request.method == "POST"
    assert "v1/login" in request.url
    assert "test-nonce" in request.body


def test_login__sends_correct_headers(monkeypatch):
    """Test that login request includes correct headers."""
    params = make_exchange_parameters()
    fake_response = make_success_response(params.model_dump())
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    client.login(make_login_submission())

    request = mock_send.call_args[0][0]
    assert request.headers["Content-Type"] == "application/json"
    assert request.headers["Accept"] == "application/json"
    assert "afp-sdk/" in request.headers["User-Agent"]


def test_get_approved_products__success__returns_list(monkeypatch):
    """Test successful retrieval of approved products."""
    product1 = make_exchange_product(id="prod1", symbol="BTCUSD")
    product2 = make_exchange_product(id="prod2", symbol="ETHUSD")
    fake_response = make_success_response(
        {"products": [product1.model_dump(), product2.model_dump()]}
    )
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    filter_obj = ExchangeProductFilter(
        batch=None,
        batch_size=None,
        newest_first=None,
    )
    products = client.get_approved_products(filter_obj)

    assert len(products) == 2
    assert products[0].id == "prod1"
    assert products[0].symbol == "BTCUSD"
    assert products[1].id == "prod2"

    request = mock_send.call_args[0][0]
    assert request.method == "GET"
    assert "v1/products" in request.url


def test_get_approved_products__with_pagination__includes_params(monkeypatch):
    """Test that pagination parameters are included in request."""
    fake_response = make_success_response({"products": []})
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    filter_obj = ExchangeProductFilter(
        batch=2,
        batch_size=50,
        newest_first=True,
    )
    client.get_approved_products(filter_obj)

    request = mock_send.call_args[0][0]
    assert "page=2" in request.url
    assert "page_size=50" in request.url
    assert "sort=DESC" in request.url


def test_get_product_by_id__success__returns_product(monkeypatch):
    """Test successful retrieval of single product by ID."""
    product = make_exchange_product(id="prod123", symbol="BTCUSD")
    fake_response = make_success_response(product.model_dump())
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    result = client.get_product_by_id("prod123")

    assert result.id == "prod123"
    assert result.symbol == "BTCUSD"

    request = mock_send.call_args[0][0]
    assert request.method == "GET"
    assert "v1/products/prod123" in request.url


def test_list_product__success__returns_none(monkeypatch):
    """Test successful product listing submission."""
    fake_response = Response()
    fake_response.status_code = 200
    fake_response._content = b""  # type: ignore
    fake_response.history = []  # type: ignore
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    listing = make_product_listing_submission()
    result = client.list_product(listing)

    assert result is None

    request = mock_send.call_args[0][0]
    assert request.method == "POST"
    assert "v1/products" in request.url
    assert listing.id in request.body


def test_update_product_listing__success__returns_none(monkeypatch):
    """Test successful product listing update."""
    fake_response = Response()
    fake_response.status_code = 200
    fake_response._content = b""  # type: ignore
    fake_response.history = []  # type: ignore
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    update = make_product_update_submission()
    result = client.update_product_listing("prod123", update)

    assert result is None

    request = mock_send.call_args[0][0]
    assert request.method == "PATCH"
    assert "v1/products/prod123" in request.url


def test_submit_order__success__returns_order(monkeypatch):
    """Test successful order submission."""
    order = make_order(id="order123", state=OrderState.OPEN)
    fake_response = make_success_response(order.model_dump())
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    submission = make_order_submission()
    result = client.submit_order(submission)

    assert result.id == "order123"
    assert result.state == OrderState.OPEN

    request = mock_send.call_args[0][0]
    assert request.method == "POST"
    assert "v1/orders" in request.url


def test_get_orders__success__returns_list(monkeypatch):
    """Test successful retrieval of orders."""
    order1 = make_order(id="order1")
    order2 = make_order(id="order2")
    fake_response = make_success_response(
        {"orders": [order1.model_dump(), order2.model_dump()]}
    )
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    filter_obj = OrderFilter(
        intent_account_id="0x1111111111111111111111111111111111111111",
        product_id=None,
        type=None,
        states=[OrderState.OPEN],
        side=OrderSide.BID,
        start=None,
        end=None,
        batch=None,
        batch_size=None,
        newest_first=None,
    )
    orders = client.get_orders(filter_obj)

    assert len(orders) == 2
    assert orders[0].id == "order1"

    request = mock_send.call_args[0][0]
    assert request.method == "GET"
    assert "v1/orders" in request.url
    assert "side=BID" in request.url


def test_get_orders__with_state_filter__includes_comma_separated_states(monkeypatch):
    """Test that multiple states are comma-separated in query params."""
    fake_response = make_success_response({"orders": []})
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    filter_obj = OrderFilter(
        intent_account_id="0x1111111111111111111111111111111111111111",
        product_id=None,
        type=None,
        states=[OrderState.OPEN, OrderState.COMPLETED],
        side=None,
        start=None,
        end=None,
        batch=None,
        batch_size=None,
        newest_first=None,
    )
    client.get_orders(filter_obj)

    request = mock_send.call_args[0][0]
    assert (
        "state=OPEN%2CCOMPLETED" in request.url or "state=OPEN,COMPLETED" in request.url
    )


def test_get_order_by_id__success__returns_order(monkeypatch):
    """Test successful retrieval of single order by ID."""
    order = make_order(id="order123")
    fake_response = make_success_response(order.model_dump())
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    result = client.get_order_by_id("order123")

    assert result.id == "order123"

    request = mock_send.call_args[0][0]
    assert request.method == "GET"
    assert "v1/orders/order123" in request.url


def test_get_order_fills__success__returns_list(monkeypatch):
    """Test successful retrieval of order fills."""
    fill1 = make_order_fill(quantity=10)
    fill2 = make_order_fill(quantity=20)
    fake_response = make_success_response(
        {"orderFills": [fill1.model_dump(), fill2.model_dump()]}
    )
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    filter_obj = OrderFillFilter(
        intent_account_id="0x1111111111111111111111111111111111111111",
        product_id=None,
        intent_hash=None,
        start=None,
        end=None,
        trade_states=[TradeState.CLEARED],
        batch=None,
        batch_size=None,
        newest_first=None,
    )
    fills = client.get_order_fills(filter_obj)

    assert len(fills) == 2
    assert fills[0].quantity == 10
    assert fills[1].quantity == 20

    request = mock_send.call_args[0][0]
    assert request.method == "GET"
    assert "v1/order-fills" in request.url


def test_iter_order_fills__success__yields_items(monkeypatch):
    """Test NDJSON streaming for order fills."""
    fill1 = make_order_fill(quantity=10)
    fill2 = make_order_fill(quantity=20)
    fake_response = make_ndjson_response([fill1, fill2])
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    filter_obj = OrderFillFilter(
        intent_account_id="0x1111111111111111111111111111111111111111",
        product_id=None,
        intent_hash=None,
        start=None,
        end=None,
        trade_states=[],
        batch=None,
        batch_size=None,
        newest_first=None,
    )
    fills = list(client.iter_order_fills(filter_obj))

    assert len(fills) == 2
    assert fills[0].quantity == 10
    assert fills[1].quantity == 20

    request = mock_send.call_args[0][0]
    assert request.method == "GET"
    assert "v1/stream/order-fills" in request.url
    assert request.headers["Accept"] == "application/x-ndjson"


def test_get_market_depth_data__success__returns_depth(monkeypatch):
    """Test successful retrieval of market depth data."""
    depth_data = make_market_depth_data(product_id="prod123")
    fake_response = make_success_response(depth_data.model_dump())
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    result = client.get_market_depth_data("prod123")

    assert result.product_id == "prod123"
    assert len(result.bids) == 2
    assert len(result.asks) == 2

    request = mock_send.call_args[0][0]
    assert request.method == "GET"
    assert "v1/market-depth/prod123" in request.url


def test_iter_market_depth_data__success__yields_snapshots(monkeypatch):
    """Test NDJSON streaming for market depth data."""
    depth1 = make_market_depth_data(product_id="prod123")
    depth2 = make_market_depth_data(product_id="prod123")
    fake_response = make_ndjson_response([depth1, depth2])
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    snapshots = list(client.iter_market_depth_data("prod123"))

    assert len(snapshots) == 2
    assert all(s.product_id == "prod123" for s in snapshots)

    request = mock_send.call_args[0][0]
    assert request.method == "GET"
    assert "v1/stream/market-depth/prod123" in request.url


def test_get_time_series_data__success__returns_ohlcv_list(monkeypatch):
    """Test successful retrieval of time series data."""
    item1 = make_ohlcv_item(timestamp=1700000000)
    item2 = make_ohlcv_item(timestamp=1700000060)
    fake_response = make_success_response(
        {"data": [item1.model_dump(), item2.model_dump()]}
    )
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    result = client.get_time_series_data("prod123", start=1700000000, interval=60)

    assert len(result) == 2
    # Timestamps are converted to datetime objects
    assert isinstance(result[0].timestamp, datetime)
    assert isinstance(result[1].timestamp, datetime)

    request = mock_send.call_args[0][0]
    assert request.method == "GET"
    assert "v1/time-series/prod123" in request.url
    assert "start=1700000000" in request.url
    assert "interval=60" in request.url


def test_iter_time_series_data__success__yields_items(monkeypatch):
    """Test NDJSON streaming for time series data."""
    item1 = make_ohlcv_item(timestamp=1700000000)
    item2 = make_ohlcv_item(timestamp=1700000060)
    fake_response = make_ndjson_response([item1, item2])
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    items = list(client.iter_time_series_data("prod123", start=1700000000, interval=60))

    assert len(items) == 2
    # Timestamps are converted to datetime objects
    assert isinstance(items[0].timestamp, datetime)

    request = mock_send.call_args[0][0]
    assert request.method == "GET"
    assert "v1/stream/time-series/prod123" in request.url


def test_send_request__401__raises_authentication_error(monkeypatch):
    """Test that 401 status code raises AuthenticationError."""
    fake_response = make_error_response(401, "Invalid credentials")
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    with pytest.raises(AuthenticationError):
        client.generate_login_nonce()


def test_send_request__403__raises_authorization_error(monkeypatch):
    """Test that 403 status code raises AuthorizationError."""
    fake_response = make_error_response(403, "Forbidden")
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    with pytest.raises(AuthorizationError):
        client.generate_login_nonce()


def test_send_request__404__raises_not_found_error(monkeypatch):
    """Test that 404 status code raises NotFoundError."""
    fake_response = make_error_response(404, "Resource not found")
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    with pytest.raises(NotFoundError):
        client.get_product_by_id("nonexistent")


def test_send_request__429__raises_rate_limit_exceeded(monkeypatch):
    """Test that 429 status code raises RateLimitExceeded."""
    fake_response = make_error_response(429, "Too many requests")
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    with pytest.raises(RateLimitExceeded):
        client.generate_login_nonce()


def test_send_request__400_with_detail__raises_validation_error(monkeypatch):
    """Test that 400 with detail raises ValidationError."""
    fake_response = make_error_response(400, "Invalid quantity")
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    with pytest.raises(ValidationError, match="Invalid quantity"):
        client.submit_order(make_order_submission())


def test_send_request__422_with_detail_list__raises_validation_error(monkeypatch):
    """Test that 422 with detail list raises ValidationError."""
    detail = [
        {"msg": "Field is required", "loc": ["body", "quantity"]},
        {"msg": "Invalid type", "loc": ["body", "price"]},
    ]
    fake_response = make_error_response(422, detail)
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    with pytest.raises(ValidationError, match="Field is required"):
        client.submit_order(make_order_submission())


def test_send_request__500__raises_exchange_error(monkeypatch):
    """Test that 500 status code raises ExchangeError."""
    fake_response = make_error_response(500, "Internal server error")
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    with pytest.raises(ExchangeError):
        client.generate_login_nonce()


def test_send_request__network_timeout__raises_exchange_error(monkeypatch):
    """Test that network timeout raises ExchangeError."""
    mock_send = Mock(side_effect=requests.exceptions.Timeout("Connection timeout"))
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    with pytest.raises(ExchangeError, match="Failed to send request"):
        client.generate_login_nonce()


def test_send_request__connection_error__raises_exchange_error(monkeypatch):
    """Test that connection error raises ExchangeError."""
    mock_send = Mock(
        side_effect=requests.exceptions.ConnectionError("Connection refused")
    )
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    with pytest.raises(ExchangeError, match="Failed to send request"):
        client.generate_login_nonce()


def test_send_request__constructs_correct_url(monkeypatch):
    """Test that URLs are constructed correctly."""
    fake_response = make_success_response({"message": "test"})
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com/")
    client._send_request("GET", "/nonce", api_version=1)

    request = mock_send.call_args[0][0]
    assert request.url == "http://test.com/v1/nonce"


def test_send_request__with_custom_api_version__uses_correct_version(monkeypatch):
    """Test that custom API version is used in URL."""
    fake_response = make_success_response({"message": "test"})
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    client._send_request("GET", "/nonce", api_version=2)

    request = mock_send.call_args[0][0]
    assert "v2/nonce" in request.url


def test_send_request__streaming_sets_ndjson_accept_header(monkeypatch):
    """Test that streaming requests set NDJSON accept header."""
    fake_response = make_ndjson_response([])
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    filter_obj = OrderFillFilter(
        intent_account_id="0x1111111111111111111111111111111111111111",
        product_id=None,
        intent_hash=None,
        start=None,
        end=None,
        trade_states=[],
        batch=None,
        batch_size=None,
        newest_first=None,
    )
    list(client.iter_order_fills(filter_obj))

    request = mock_send.call_args[0][0]
    assert request.headers["Accept"] == "application/x-ndjson"


def test_send_request__non_streaming_sets_json_accept_header(monkeypatch):
    """Test that non-streaming requests set JSON accept header."""
    fake_response = make_success_response({"message": "test"})
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    client.generate_login_nonce()

    request = mock_send.call_args[0][0]
    assert request.headers["Accept"] == "application/json"


def test_send_request__always_sets_content_type_header(monkeypatch):
    """Test that all requests set Content-Type header."""
    fake_response = make_success_response({"message": "test"})
    mock_send = Mock(return_value=fake_response)
    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://test.com")
    client.generate_login_nonce()

    request = mock_send.call_args[0][0]
    assert request.headers["Content-Type"] == "application/json"
