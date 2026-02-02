import re
from datetime import date, datetime, timedelta
from decimal import Decimal
from functools import reduce
from operator import getitem
from typing import Any

import requests
from binascii import Error
from eth_typing.evm import ChecksumAddress
from hexbytes import HexBytes
from pydantic import AnyUrl
from web3 import Web3

from .constants import MINIMUM_ORACLE_FALLBACK_INTERVAL, MONTH_CODES
from .exceptions import ValidationError


# Generic type validators


def validate_timedelta(value: timedelta) -> timedelta:
    if value.total_seconds() < 0:
        raise ValueError(f"{value} should be positive")
    return value


def validate_non_negative_timestamp(value: datetime) -> datetime:
    if value.timestamp() < 0:
        raise ValueError(f"{value} should be greater than {datetime.fromtimestamp(0)}")
    return value


def validate_hexstr(value: str, length: int | None = None) -> str:
    value = str(value)
    if not value.startswith("0x"):
        raise ValueError(f"{value} should start with '0x'")
    try:
        byte_value = HexBytes(value)
    except Error:
        raise ValueError(f"{value} includes non-hexadecimal characters")
    if length is not None and len(byte_value) != length:
        raise ValueError(f"{value} should be 32 bytes long")
    return value


def validate_hexstr32(value: str) -> str:
    return validate_hexstr(value, length=32)


def validate_address(value: str) -> ChecksumAddress:
    try:
        return Web3.to_checksum_address(value)
    except ValueError:
        raise ValueError(f"{value} is not a valid blockchain address")


def validate_url(value: str) -> str:
    AnyUrl(value)
    return value


def validate_all_caps(value: str) -> str:
    if value != value.upper():
        raise ValueError(f"{value} should use capital letters only")
    return value


# Live data verifiers


def verify_collateral_asset(w3: Web3, address: str) -> ChecksumAddress:
    address = validate_address(address)
    if len(w3.eth.get_code(address)) == 0:
        raise ValidationError(
            f"No contract found at collateral asset address {address}"
        )
    return address


def verify_oracle(w3: Web3, address: str) -> ChecksumAddress:
    address = validate_address(address)
    if len(w3.eth.get_code(address)) == 0:
        raise ValidationError(f"No contract found at oracle address {address}")
    return address


def verify_url(value: str) -> str:
    try:
        requests.head(value)
    except requests.RequestException as ex:
        raise ValidationError(f"Not possible to connect to URL {value}") from ex
    return value


# Schema-specific model validators


def validate_limit_price(
    value: Decimal,
    min_price: Decimal,
    max_price: Decimal,
    tick_size: int,
    rounding: str | None = None,
) -> Decimal:
    if value < min_price:
        raise ValueError(
            f"IntentData: limit_price: {value} should be greater than "
            f"the product's minimum price {min_price}"
        )
    if value > max_price:
        raise ValueError(
            f"IntentData: limit_price: {value} should be less than the product's "
            f"maximum price {max_price}"
        )
    if rounding is None:
        num_fractional_digits = abs(int(value.normalize().as_tuple().exponent))
        if num_fractional_digits > tick_size:
            raise ValueError(
                f"IntentData: limit_price: {value} should have at most "
                f"{tick_size} fractional digits"
            )
    return value.quantize(Decimal("10") ** -tick_size, rounding=rounding)


def validate_price_limits(min_price: Decimal, max_price: Decimal) -> None:
    if min_price >= max_price:
        raise ValueError(
            f"PredictionProductV1.min_price {min_price} "
            f"should be less than PredictionProductV1.max_price {max_price}"
        )


def validate_time_limits(
    start_time: datetime, earliest_fsp_submission_time: datetime
) -> None:
    if start_time >= earliest_fsp_submission_time:
        raise ValueError(
            f"BaseProduct.start_time {start_time} should be less than "
            "ExpirySpecification.earliest_fsp_submission_time "
            f"{earliest_fsp_submission_time}"
        )


def validate_matching_fsp_types(
    outcome_space_fsp_type: str, outcome_point_fsp_type: str
) -> None:
    if outcome_space_fsp_type != outcome_point_fsp_type:
        raise ValueError(
            f"OutcomeSpace.fsp_type '{outcome_space_fsp_type}' should match "
            f"OutcomePoint.fsp_type '{outcome_point_fsp_type}'"
        )


def validate_oracle_fallback_time(
    fallback_time: datetime, earliest_fsp_submission_time: datetime
) -> None:
    earliest_fallback_time = (
        earliest_fsp_submission_time + MINIMUM_ORACLE_FALLBACK_INTERVAL
    )
    if fallback_time < earliest_fallback_time:
        raise ValueError(
            f"OracleFallback: fallback_time {fallback_time} "
            f"should be at least {MINIMUM_ORACLE_FALLBACK_INTERVAL} after "
            "ExpirySpecification.earliest_fsp_submission_time "
            f"{earliest_fsp_submission_time}"
        )


def validate_oracle_fallback_fsp(
    fallback_fsp: Decimal, min_price: Decimal, max_price: Decimal
) -> None:
    if not (min_price <= fallback_fsp <= max_price):
        raise ValueError(
            f"OracleFallback: fallback_fsp {fallback_fsp} should be between "
            f"PredictionProductV1.min_price {min_price} and "
            f"PredictionProductV1.max_price {max_price}"
        )


def validate_outcome_space_conditions(
    base_case_condition: str,
    edge_case_conditions: list[str],
    outcome_point_dict: dict[Any, Any],
) -> None:
    conditions = [base_case_condition] + edge_case_conditions
    schemas = ["BaseCaseResolution"] + [
        f"EdgeCase[{i}]" for i in range(len(edge_case_conditions))
    ]
    for condition, schema in zip(conditions, schemas):
        for variable in re.findall(r"{(.*?)}", condition):
            parts = variable.split(".")
            try:
                referred_value = reduce(getitem, parts, outcome_point_dict)
            except (TypeError, KeyError):
                raise ValueError(
                    f"{schema}: condition: Invalid template variable '{variable}'"
                )
            if isinstance(referred_value, dict) or isinstance(referred_value, list):  # type: ignore
                raise ValueError(
                    f"{schema}: Template variable '{variable}' "
                    "should not refer to a nested object or list"
                )


def validate_symbol(symbol: str, frequency: str, release_date: date) -> None:
    match frequency:
        case "daily":
            pattern = (
                r"[A-Z]{1,8}(?P<day>(0[1-9]|[1-2][0-9]|3[01]))"
                r"(?P<month>[FGHJKMNQUVXZ])(?P<year>[0-9]{2})"
            )
        case "weekly" | "fortnightly":
            pattern = (
                r"[A-Z]{1,8}(?P<weekno>(0[1-9]|[1-4][0-9]|5[0-3]))"
                r"W(?P<year>[0-9]{2})"
            )
        case "semimonthly":
            pattern = (
                r"[A-Z]{1,8}(?P<occurrence>[12])"
                r"(?P<month>[FGHJKMNQUVXZ])(?P<year>[0-9]{2})"
            )
        case "monthly" | "quarterly":
            pattern = r"[A-Z]{1,8}(?P<month>[FGHJKMNQUVXZ])(?P<year>[0-9]{2})"
        case "yearly":
            pattern = r"[A-Z]{1,8}(?P<year>[0-9]{4})"
        case _:
            raise ValueError(
                f"OutcomeSpaceTimeSeries: frequency: Unexpected value '{frequency}'"
            )
    if match := re.fullmatch(pattern, symbol):
        groups = match.groupdict()

        if "day" in groups and int(groups["day"]) != release_date.day:
            raise ValueError(
                f"ProductMetadata: symbol: Day component of symbol '{symbol}' "
                f"should match TemporalObservation.release_date {release_date}"
            )
        if "month" in groups and MONTH_CODES[groups["month"]] != release_date.month:
            raise ValueError(
                f"ProductMetadata: symbol: Month component of symbol '{symbol}' "
                f"should match TemporalObservation.release_date {release_date}"
            )
        if "year" in groups and int(groups["year"]) % 2000 != release_date.year % 2000:
            raise ValueError(
                f"ProductMetadata: symbol: Year component of symbol '{symbol}' "
                f"should match TemporalObservation.release_date {release_date}"
            )
        if (
            "weekno" in groups
            and int(groups["weekno"]) != release_date.isocalendar().week
        ):
            raise ValueError(
                f"ProductMetadata: symbol: Week number component of symbol '{symbol}' "
                f"should match TemporalObservation.release_date {release_date}"
            )
        if "occurrence" in groups and int(
            groups["occurrence"]
        ) != _semimonthly_occurrence(release_date.day):
            raise ValueError(
                f"ProductMetadata: symbol: Occurrence component of symbol '{symbol}' "
                f"should match TemporalObservation.release_date {release_date}"
            )
    else:
        raise ValueError(
            f"ProductMetadata: symbol: Symbol '{symbol}' should match regexp pattern "
            f"'{pattern}' for OutcomeSpaceTimeSeries.frequency '{frequency}'"
        )


def _semimonthly_occurrence(day_of_month: int) -> int:
    return 1 if day_of_month <= 15 else 2
