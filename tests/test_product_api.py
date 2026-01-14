from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock

import pytest
from web3 import Web3

import afp
from afp.api.product import Product
from afp.schemas import PredictionProductV1

from . import AuthenticatorStub


@pytest.fixture
def product_api():
    """Create a Product API instance for testing."""
    app = afp.AFP(
        authenticator=AuthenticatorStub(),
        rpc_url="http://localhost:8545",
        oracle_provider_address="0x1234567890123456789012345678901234567890",
    )
    return Product(app.config)


def test_product_parse_creates_valid_product_spec(product_api, monkeypatch):
    mock_get_code = Mock(return_value=b"\x01\x02\x03")  # Non-empty bytecode
    monkeypatch.setattr(product_api._w3.eth, "get_code", mock_get_code)

    spec = {
        "metadata": {
            "builder_id": "0xFfbf2643CF22760AfD3b878BA8aE849c48944Aa5",
            "symbol": "BTC-USD-PERP",
            "description": "Bitcoin perpetual futures",
        },
        "oracle_spec": {
            "oracle_address": "0x1234567890123456789012345678901234567890",
            "fsv_decimals": 18,
            "fsp_alpha": "1.0",
            "fsp_beta": "0.5",
            "fsv_calldata": "0x1234",
        },
        "collateral_asset": "0xAbCdEf1234567890AbCdEf1234567890AbCdEf12",
        "start_time": "2024-01-01T00:00Z",
        "point_value": "1.0",
        "price_decimals": 2,
        "extended_metadata": "",
        "expiry_spec": {
            "earliest_fsp_submission_time": "2024-01-01T12:00Z",
            "tradeout_interval": 3600,
        },
        "min_price": "0.01",
        "max_price": "99.99",
    }

    result = product_api.parse(spec)

    assert isinstance(result, PredictionProductV1)

    assert result.metadata.builder_id == "0xFfbf2643CF22760AfD3b878BA8aE849c48944Aa5"
    assert result.metadata.symbol == "BTC-USD-PERP"
    assert result.metadata.description == "Bitcoin perpetual futures"

    assert (
        result.oracle_spec.oracle_address
        == "0x1234567890123456789012345678901234567890"
    )
    assert result.oracle_spec.fsv_decimals == 18
    assert result.oracle_spec.fsp_alpha == Decimal("1.0")
    assert result.oracle_spec.fsp_beta == Decimal("0.5")
    assert result.oracle_spec.fsv_calldata == "0x1234"

    assert result.expiry_spec.earliest_fsp_submission_time == datetime(
        2024, 1, 1, 12, 0, tzinfo=timezone.utc
    )
    assert result.expiry_spec.tradeout_interval == 3600

    assert result.collateral_asset == Web3.to_checksum_address(
        "0xAbCdEf1234567890AbCdEf1234567890AbCdEf12"
    )
    assert result.start_time == datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert result.point_value == Decimal("1.0")
    assert result.price_decimals == 2
    assert result.extended_metadata == ""
    assert result.min_price == Decimal("0.01")
    assert result.max_price == Decimal("99.99")

    assert result.id is not None
    assert result.id.startswith("0x")
