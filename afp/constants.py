import os
from importlib import metadata
from types import SimpleNamespace


def _int_or_none(value: str | None) -> int | None:
    return int(value) if value is not None else None


# Venue API constants
USER_AGENT = "afp-sdk/{}".format(metadata.version("afp-sdk"))
DEFAULT_BATCH_SIZE = 50
DEFAULT_EXCHANGE_API_VERSION = 1

# Clearing System constants
RATE_MULTIPLIER = 10**4
FEE_RATE_MULTIPLIER = 10**6
FULL_PRECISION_MULTIPLIER = 10**18

defaults = SimpleNamespace(
    # Authentication parameters
    KEYFILE=os.getenv("AFP_KEYFILE", None),
    KEYFILE_PASSWORD=os.getenv("AFP_KEYFILE_PASSWORD", ""),
    PRIVATE_KEY=os.getenv("AFP_PRIVATE_KEY", None),
    # Venue parameters
    EXCHANGE_URL=os.getenv(
        "AFP_EXCHANGE_URL", "https://exchange-server-next.up.railway.app/"
    ),
    # Blockchain parameters
    RPC_URL=os.getenv("AFP_RPC_URL", None),
    CHAIN_ID=int(os.getenv("AFP_CHAIN_ID", 65000000)),
    GAS_LIMIT=_int_or_none(os.getenv("AFP_GAS_LIMIT", None)),
    MAX_FEE_PER_GAS=_int_or_none(os.getenv("AFP_MAX_FEE_PER_GAS", None)),
    MAX_PRIORITY_FEE_PER_GAS=_int_or_none(
        os.getenv("AFP_MAX_PRIORITY_FEE_PER_GAS", None)
    ),
    TIMEOUT_SECONDS=int(os.getenv("AFP_TIMEOUT_SECONDS", 10)),
    # Clearing System parameters
    CLEARING_DIAMOND_ADDRESS=os.getenv(
        "AFP_CLEARING_DIAMOND_ADDRESS", "0x6Dc8cd65B03e0462C4D5E954b924ec86D3408FE7"
    ),
    MARGIN_ACCOUNT_REGISTRY_ADDRESS=os.getenv(
        "AFP_MARGIN_ACCOUNT_REGISTRY_ADDRESS",
        "0x801cCa84bcb57418044c882Dfb4B03cc35bE848f",
    ),
    ORACLE_PROVIDER_ADDRESS=os.getenv(
        "AFP_ORACLE_PROVIDER_ADDRESS", "0x72EeD9f7286292f119089F56e3068a3A931FCD49"
    ),
    PRODUCT_REGISTRY_ADDRESS=os.getenv(
        "AFP_PRODUCT_REGISTRY_ADDRESS", "0xab792A6e84c5A22C7A27FEd904AB83ca2fbA4c5e"
    ),
    SYSTEM_VIEWER_ADDRESS=os.getenv(
        "AFP_SYSTEM_VIEWER_ADDRESS", "0xF2F903B8956Ca6868E165989A9ebEEE72F4D3e3F"
    ),
)
