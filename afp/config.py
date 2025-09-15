from dataclasses import dataclass

from eth_typing.evm import ChecksumAddress

from .auth import Authenticator


@dataclass(frozen=True)
class Config:
    authenticator: Authenticator | None

    # Venue parameters
    exchange_url: str

    # Blockchain parameters
    rpc_url: str | None
    chain_id: int
    gas_limit: int | None
    max_fee_per_gas: int | None
    max_priority_fee_per_gas: int | None
    timeout_seconds: int

    # Clearing System parameters
    clearing_diamond_address: ChecksumAddress
    margin_account_registry_address: ChecksumAddress
    oracle_provider_address: ChecksumAddress
    product_registry_address: ChecksumAddress
    system_viewer_address: ChecksumAddress
