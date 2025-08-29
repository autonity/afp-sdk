from datetime import datetime, timedelta
from decimal import Decimal

from binascii import Error
from eth_typing.evm import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3


def ensure_timestamp(value: int | datetime) -> int:
    return int(value.timestamp()) if isinstance(value, datetime) else value


def ensure_datetime(value: datetime | int) -> datetime:
    return value if isinstance(value, datetime) else datetime.fromtimestamp(value)


def validate_timedelta(value: timedelta) -> timedelta:
    if value.total_seconds() < 0:
        raise ValueError(f"{value} should be positive")
    return value


def validate_hexstr(value: str, length: int | None = None) -> str:
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
    value: Decimal, tick_size: int, rounding: str | None = None
) -> Decimal:
    if rounding is None:
        num_fractional_digits = abs(int(value.normalize().as_tuple().exponent))
        if num_fractional_digits > tick_size:
            raise ValueError(
                f"Limit price {value} can have at most {tick_size} fractional digits"
            )
    return value.quantize(Decimal("10") ** -tick_size, rounding=rounding)
