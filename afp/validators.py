from datetime import datetime, timedelta
from decimal import Decimal

from binascii import Error
from eth_typing.evm import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3

from .exceptions import NotFoundError


def ensure_timestamp(value: int | float | datetime) -> int:
    return int(value.timestamp()) if isinstance(value, datetime) else int(value)


def ensure_datetime(value: int | float | str) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, int) or isinstance(value, float):
        return datetime.fromtimestamp(value)
    return datetime.fromisoformat(value)


def validate_timedelta(value: timedelta) -> timedelta:
    if value.total_seconds() < 0:
        raise ValueError(f"{value} should be positive")
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
    value: Decimal, tick_size: int, rounding: str | None = None
) -> Decimal:
    if rounding is None:
        num_fractional_digits = abs(int(value.normalize().as_tuple().exponent))
        if num_fractional_digits > tick_size:
            raise ValueError(
                f"Limit price {value} can have at most {tick_size} fractional digits"
            )
    return value.quantize(Decimal("10") ** -tick_size, rounding=rounding)


def verify_collateral_asset(w3: Web3, address: str) -> ChecksumAddress:
    address = validate_address(address)
    if len(w3.eth.get_code(address)) == 0:
        raise NotFoundError(f"No ERC20 token found at address {address}")
    return address


def verify_oracle(w3: Web3, address: str) -> ChecksumAddress:
    address = validate_address(address)
    if len(w3.eth.get_code(address)) == 0:
        raise ValueError(f"No contract found at oracle address {address}")
    return address
