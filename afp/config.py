from dataclasses import dataclass

from eth_typing.evm import ChecksumAddress

from .auth import Authenticator


@dataclass(frozen=True)
class Config:
    rpc_url: str | None
    authenticator: Authenticator | None

    exchange_url: str
    chain_id: int
    clearing_diamond_address: ChecksumAddress
    margin_account_registry_address: ChecksumAddress
    oracle_provider_address: ChecksumAddress
    product_registry_address: ChecksumAddress
    system_viewer_address: ChecksumAddress
