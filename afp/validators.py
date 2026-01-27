from datetime import datetime, timedelta
from decimal import Decimal

import requests
from binascii import Error
from eth_typing.evm import ChecksumAddress
from hexbytes import HexBytes
from pydantic import AnyUrl
from web3 import Web3

from .exceptions import NotFoundError, ValidationError

CID_PATTERN = (
    r"^(Qm[1-9A-HJ-NP-Za-km-z]{44}|b[a-z2-7]{58,}|z[1-9A-HJ-NP-Za-km-z]{48,})$"
)


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


def validate_limit_price(
    value: Decimal,
    min_price: Decimal,
    max_price: Decimal,
    tick_size: int,
    rounding: str | None = None,
) -> Decimal:
    if value < min_price:
        raise ValueError(
            f"Limit price {value} is less than the product's minimum price {min_price}"
        )
    if value > max_price:
        raise ValueError(
            f"Limit price {value} is greater than the product's maximum price {max_price}"
        )
    if rounding is None:
        num_fractional_digits = abs(int(value.normalize().as_tuple().exponent))
        if num_fractional_digits > tick_size:
            raise ValueError(
                f"Limit price {value} can have at most {tick_size} fractional digits"
            )
    return value.quantize(Decimal("10") ** -tick_size, rounding=rounding)


def validate_price_limits(
    min_price: Decimal, max_price: Decimal
) -> tuple[Decimal, Decimal]:
    if min_price >= max_price:
        raise ValueError(
            "The minimum product price should be less than the maximum product price"
        )
    return (min_price, max_price)


def validate_url(value: str) -> str:
    AnyUrl(value)
    return value


def verify_collateral_asset(w3: Web3, address: str) -> ChecksumAddress:
    address = validate_address(address)
    if len(w3.eth.get_code(address)) == 0:
        raise NotFoundError(f"No contract found at collateral asset address {address}")
    return address


def verify_oracle(w3: Web3, address: str) -> ChecksumAddress:
    address = validate_address(address)
    if len(w3.eth.get_code(address)) == 0:
        raise NotFoundError(f"No contract found at oracle address {address}")
    return address


def verify_url(value: str) -> str:
    try:
        requests.head(value)
    except requests.RequestException as ex:
        raise ValidationError(f"Not possible to connect to URL {value}") from ex
    return value
