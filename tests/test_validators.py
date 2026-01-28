import decimal
from datetime import date, datetime, UTC
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
    validators.validate_hexstr32(
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
    assert (
        str(
            validators.validate_limit_price(
                Decimal("1.25"), Decimal("1"), Decimal("2"), 2
            )
        )
        == "1.25"
    )
    assert (
        str(
            validators.validate_limit_price(
                Decimal("1.25"), Decimal("1"), Decimal("2"), 4
            )
        )
        == "1.2500"
    )


def test_validate_limit_price__rounding():
    assert (
        str(
            validators.validate_limit_price(
                Decimal("1.25"), Decimal("1"), Decimal("2"), 1, decimal.ROUND_DOWN
            )
        )
        == "1.2"
    )


def test_validate_limit_price__not_enough_digits():
    with pytest.raises(ValueError):
        validators.validate_limit_price(Decimal("1.25"), Decimal("1"), Decimal("2"), 1)


def test_validate_limit_price__invalid_rounding_mode():
    with pytest.raises(TypeError):
        validators.validate_limit_price(
            Decimal("1.25"), Decimal("1"), Decimal("2"), 1, "foobar"
        )


def test_validate_limit_price__min_price_breach():
    with pytest.raises(ValueError):
        validators.validate_limit_price(
            Decimal("1.25"), Decimal("1.26"), Decimal("2"), 2
        )


def test_validate_limit_price__max_price_breach():
    with pytest.raises(ValueError):
        validators.validate_limit_price(
            Decimal("1.25"), Decimal("1"), Decimal("1.24"), 2
        )


def test_validate_price_limits__pass():
    validators.validate_price_limits(Decimal("0.11"), Decimal("0.12"))


def test_validate_price_limits__error():
    with pytest.raises(ValueError):
        validators.validate_price_limits(Decimal("0.11"), Decimal("0.10"))


def test_validate_outcome_space_conditions__pass():
    dct = {
        "a": {
            "b": {
                "c": "hello",
                "d": "world",
            },
        },
    }
    base_case_condition = "Reference to {a.b.c}"
    edge_case_conditions = ["And to {a.b.d} as well"]

    validators.validate_outcome_space_conditions(
        base_case_condition, edge_case_conditions, dct
    )


def test_validate_outcome_space_conditions__error():
    dct = {
        "a": {
            "b": {
                "c": "hello",
                "d": "world",
            },
        },
    }
    base_case_condition = "Reference to {a.b.e}"
    edge_case_conditions = []

    with pytest.raises(ValueError):
        validators.validate_outcome_space_conditions(
            base_case_condition, edge_case_conditions, dct
        )


@pytest.mark.parametrize(
    "symbol,frequency,release_date",
    [
        ("BTCUSD15M24", "daily", "2024-06-15"),
        ("CLAIMS03W25", "weekly", "2025-01-13"),
        ("PAYROLL02W25", "fortnightly", "2025-01-06"),
        ("RETAIL1H26", "semimonthly", "2026-03-15"),
        ("RETAIL2H26", "semimonthly", "2026-03-30"),
        ("CPIH26", "monthly", "2026-03-15"),
        ("GDPH26", "quarterly", "2026-03-30"),
        ("GDPF26", "quarterly", "2026-01-15"),
        ("WORLDGDP2027", "yearly", "2027-03-15"),
    ],
    ids=str,
)
def test_validate_symbol__pass(symbol, frequency, release_date):
    validators.validate_symbol(symbol, frequency, date.fromisoformat(release_date))


@pytest.mark.parametrize(
    "symbol,frequency,release_date",
    [
        ("BTCUSDM2024", "monthly", "2024-06-16"),
        ("BTCUSDA24", "monthly", "2024-01-23"),
        ("CLAIMS54W25", "weekly", "2025-12-31"),
        ("BTCUSD32M24", "daily", "2024-06-31"),
        ("BTCUSDM", "yearly", "2024-06-01"),
        ("WORLDGDP27", "yearly", "2027-12-31"),
        ("BTCUSD15M24", "daily", "2024-06-16"),
        ("CLAIMS02W25", "weekly", "2025-01-23"),
        ("CPIH26", "monthly", "2026-05-15"),
        ("GDPH26", "monthly", "2026-04-15"),
    ],
    ids=str,
)
def test_validate_symbol__error(symbol, frequency, release_date):
    with pytest.raises(ValueError):
        validators.validate_symbol(symbol, frequency, date.fromisoformat(release_date))
