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
        "AFP_EXCHANGE_URL", "https://afp-exchange-stable.up.railway.app"
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
        "AFP_CLEARING_DIAMOND_ADDRESS", "0x5B5411F1548254d25360d71FE40cFc1cC983B2A2"
    ),
    MARGIN_ACCOUNT_REGISTRY_ADDRESS=os.getenv(
        "AFP_MARGIN_ACCOUNT_REGISTRY_ADDRESS",
        "0x99f4FA9Cdce7AD227eB84907936a8FeF2095D846",
    ),
    ORACLE_PROVIDER_ADDRESS=os.getenv(
        "AFP_ORACLE_PROVIDER_ADDRESS", "0xF2A2A27da33D30B4BF38D7e186E7B0b1e964e55c"
    ),
    PRODUCT_REGISTRY_ADDRESS=os.getenv(
        "AFP_PRODUCT_REGISTRY_ADDRESS", "0x86B3829471929B115367DA0958f56A6AB844b08e"
    ),
    SYSTEM_VIEWER_ADDRESS=os.getenv(
        "AFP_SYSTEM_VIEWER_ADDRESS", "0xfF2DFcC44a95cce96E03EfC33C65c8Be671Bae5B"
    ),
)
