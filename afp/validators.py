from datetime import datetime, timedelta

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
