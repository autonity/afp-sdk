import decimal
from datetime import datetime, UTC
from decimal import Decimal

import pytest

from afp import validators
from afp.schemas import Model, Timestamp


class DummyModel(Model):
    timestamp: Timestamp


def test_timestamp_conversion():
    dt_time = datetime.fromisoformat("2030-01-01T12:00:00Z")
    ts_time = 1893499200

    # timestamp -> datetime
    instance = DummyModel(timestamp=ts_time)  # type: ignore
    assert instance.timestamp is not None
    assert instance.timestamp.astimezone(UTC) == dt_time

    # datetime -> timestamp
    assert '"timestamp":%d' % ts_time in instance.model_dump_json()


def test_validate_hexstr32__pass():
    assert validators.validate_hexstr32(
        "0xe50c0a9639bdec3c05484a4e912650e63039fd5032f4050b1d1cdd0dd0efb61b"
    )


@pytest.mark.parametrize(
    "value",
    [
        "e50c0a9639bdec3c05484a4e912650e63039fd5032f4050b1d1cdd0dd0efb61b",
        "0xg50c0a9639bdec3c05484a4e912650e63039fd5032f4050b1d1cdd0dd0efb61b",
        "0xe50c0a9639bdec3c05484a4e912650e63039fd5032f4050b1d1cdd0dd0efb6",
    ],
    ids=str,
)
def test_validate_hexstr32__error(value):
    with pytest.raises(ValueError):
        validators.validate_hexstr32(value)


def test_validate_limit_price__pass():
    assert str(validators.validate_limit_price(Decimal("1.25"), 2)) == "1.25"
    assert str(validators.validate_limit_price(Decimal("1.25"), 4)) == "1.2500"


def test_validate_limit_price__rounding():
    assert (
        str(validators.validate_limit_price(Decimal("1.25"), 1, decimal.ROUND_DOWN))
        == "1.2"
    )


def test_validate_limit_price__error():
    with pytest.raises(ValueError):
        validators.validate_limit_price(Decimal("1.25"), 1)


def test_validate_limit_price__invalid_rounding_mode():
    with pytest.raises(TypeError):
        validators.validate_limit_price(Decimal("1.25"), 1, "foobar")
