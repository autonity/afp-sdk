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

schema_cids = SimpleNamespace(
    # afp-product-schemas v0.2
    ORACLE_CONFIG_V02="QmfXNPrsPvhKmMPKxsxr6Z3TzH35eHykzpQrruSjPFqeYa",
    ORACLE_CONFIG_PROTOTYPE1_V02="QmfXNPrsPvhKmMPKxsxr6Z3TzH35eHykzpQrruSjPFqeYb",
    ORACLE_FALLBACK_V02="QmfXNPrsPvhKmMPKxsxr6Z3TzH35eHykzpQrruSjPFqeYc",
    OUTCOME_POINT_V02="QmfXNPrsPvhKmMPKxsxr6Z3TzH35eHykzpQrruSjPFqeYd",
    OUTCOME_POINT_EVENT_V02="QmfXNPrsPvhKmMPKxsxr6Z3TzH35eHykzpQrruSjPFqeYe",
    OUTCOME_POINT_SCALAR_V02="QmfXNPrsPvhKmMPKxsxr6Z3TzH35eHykzpQrruSjPFqeYf",
    OUTCOME_POINT_TIME_SERIES_V02="QmfXNPrsPvhKmMPKxsxr6Z3TzH35eHykzpQrruSjPFqeYg",
    OUTCOME_SPACE_V02="QmfXNPrsPvhKmMPKxsxr6Z3TzH35eHykzpQrruSjPFqeYh",
    OUTCOME_SPACE_SCALAR_V02="QmfXNPrsPvhKmMPKxsxr6Z3TzH35eHykzpQrruSjPFqeYi",
    OUTCOME_SPACE_TIME_SERIES_V02="QmfXNPrsPvhKmMPKxsxr6Z3TzH35eHykzpQrruSjPFqeYj",
)

defaults = SimpleNamespace(
    # Authentication parameters
    KEYFILE=os.getenv("AFP_KEYFILE", None),
    KEYFILE_PASSWORD=os.getenv("AFP_KEYFILE_PASSWORD", ""),
    PRIVATE_KEY=os.getenv("AFP_PRIVATE_KEY", None),
    # Venue parameters
    EXCHANGE_URL=os.getenv(
        "AFP_EXCHANGE_URL", "https://afp-exchange-stable.up.railway.app/"
    ),
    # IPFS client parameters
    IPFS_API_URL=os.getenv("AFP_IPFS_API_URL", "http://127.0.0.1:5001/api/v0"),
    IPFS_API_KEY=os.getenv("AFP_IPFS_API_KEY", None),
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
        "AFP_CLEARING_DIAMOND_ADDRESS", "0x08e725d38BCABCf62806E84bE044dF67E8b476Ae"
    ),
    MARGIN_ACCOUNT_REGISTRY_ADDRESS=os.getenv(
        "AFP_MARGIN_ACCOUNT_REGISTRY_ADDRESS",
        "0x1FAa342Ea34332ee1186FE48f03894F70F7fFc4f",
    ),
    ORACLE_PROVIDER_ADDRESS=os.getenv(
        "AFP_ORACLE_PROVIDER_ADDRESS", "0x06CaDDDf6CC08048596aE051c8ce644725219C73"
    ),
    PRODUCT_REGISTRY_ADDRESS=os.getenv(
        "AFP_PRODUCT_REGISTRY_ADDRESS", "0xB605fc6B76eA4592CaA3AEd26EFd3edbAc5A3A24"
    ),
    SYSTEM_VIEWER_ADDRESS=os.getenv(
        "AFP_SYSTEM_VIEWER_ADDRESS", "0xBeC22149650CcaC2a1233c7b489aFF3ea24df36d"
    ),
)
