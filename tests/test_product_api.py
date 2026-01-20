from datetime import datetime, timezone
from decimal import Decimal

from web3 import Web3

from afp.schemas import PredictionProductV1


def test_product_parsing_from_dictionary():
    spec = {
        "base": {
            "metadata": {
                "builder": "0xFfbf2643CF22760AfD3b878BA8aE849c48944Aa5",
                "symbol": "BTC-USD-PERP",
                "description": "Bitcoin perpetual futures",
            },
            "oracleSpec": {
                "oracleAddress": "0x1234567890123456789012345678901234567890",
                "fsvDecimals": 18,
                "fspAlpha": "1.0",
                "fspBeta": "0.5",
                "fsvCalldata": "0x1234",
            },
            "collateralAsset": "0xAbCdEf1234567890AbCdEf1234567890AbCdEf12",
            "startTime": "2024-01-01T00:00Z",
            "pointValue": "1.0",
            "priceDecimals": 2,
            "extendedMetadata": "",
        },
        "expirySpec": {
            "earliestFspSubmissionTime": "2024-01-01T12:00Z",
            "tradeoutInterval": 3600,
        },
        "minPrice": "0.01",
        "maxPrice": "99.99",
    }

    result = PredictionProductV1.model_validate(spec)

    assert isinstance(result, PredictionProductV1)

    assert result.base.metadata.builder == "0xFfbf2643CF22760AfD3b878BA8aE849c48944Aa5"
    assert result.base.metadata.symbol == "BTC-USD-PERP"
    assert result.base.metadata.description == "Bitcoin perpetual futures"

    assert (
        result.base.oracle_spec.oracle_address
        == "0x1234567890123456789012345678901234567890"
    )
    assert result.base.oracle_spec.fsv_decimals == 18
    assert result.base.oracle_spec.fsp_alpha == Decimal("1.0")
    assert result.base.oracle_spec.fsp_beta == Decimal("0.5")
    assert result.base.oracle_spec.fsv_calldata == "0x1234"

    assert result.base.collateral_asset == Web3.to_checksum_address(
        "0xAbCdEf1234567890AbCdEf1234567890AbCdEf12"
    )
    assert result.base.start_time == datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert result.base.point_value == Decimal("1.0")
    assert result.base.price_decimals == 2
    assert result.base.extended_metadata == ""

    assert result.expiry_spec.earliest_fsp_submission_time == datetime(
        2024, 1, 1, 12, 0, tzinfo=timezone.utc
    )
    assert result.expiry_spec.tradeout_interval == 3600

    assert result.min_price == Decimal("0.01")
    assert result.max_price == Decimal("99.99")

    assert result.id is not None
    assert result.id.startswith("0x")
