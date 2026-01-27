import os
from datetime import timedelta
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

# IPFS client constants
IPFS_CID_ENCODING = "base32"
IPFS_REQUEST_TIMEOUT = 30
JSON_SCHEMAS_DIRECTORY = os.path.join(os.path.dirname(__file__), "json-schemas")

# Product schema constants
MINIMUM_ORACLE_FALLBACK_INTERVAL = timedelta(days=7)
MONTH_CODES = {
    "F": 1,
    "G": 2,
    "H": 3,
    "J": 4,
    "K": 5,
    "M": 6,
    "N": 7,
    "Q": 8,
    "U": 9,
    "V": 10,
    "X": 11,
    "Z": 12,
}

schema_cids = SimpleNamespace(
    # afp-product-schemas v0.2.0
    ORACLE_CONFIG_V020="bafyreifcec2km7hxwq6oqzjlspni2mgipetjb7pqtaewh2efislzoctboi",
    ORACLE_CONFIG_PROTOTYPE1_V020="bafyreiaw34o6l3rmatabzbds2i2myazdw2yolevcpsoyd2i2g3ms7wa2eq",
    ORACLE_FALLBACK_V020="bafyreicgr6dfo5yduixjkcifghiulskfegwojvuwodtouvivl362zndhxe",
    OUTCOME_POINT_V020="bafyreibnfg6nq74dvpkre5rakkccij7iadp5rxpim7omsatjnrpmj3y7v4",
    OUTCOME_POINT_EVENT_V020="bafyreihur3dzwhja6uxsbcw6eeoj3xmmc4e3zkmyzpot5v5dleevxe5zam",
    OUTCOME_POINT_TIME_SERIES_V020=(
        "bafyreidzs7okcpqiss6ztftltyptqwnw5e5opsy5yntospekjha4kpykaa"
    ),
    OUTCOME_SPACE_V020="bafyreicheoypx6synljushh7mq2572iyhlolf4nake2p5dwobgnj3r5eua",
    OUTCOME_SPACE_SCALAR_V020="bafyreihn3oiaxffe4e2w7pwtreadpw3obfd7gqlogbcxm56jc2hzfvco74",
    OUTCOME_SPACE_TIME_SERIES_V020=(
        "bafyreid35a67db4sqh4fs6boddyt2xvscbqy6nqvsp5jjur56qhkw4ixre"
    ),
)

defaults = SimpleNamespace(
    # Authentication parameters
    KEYFILE=os.getenv("AFP_KEYFILE", None),
    KEYFILE_PASSWORD=os.getenv("AFP_KEYFILE_PASSWORD", ""),
    PRIVATE_KEY=os.getenv("AFP_PRIVATE_KEY", None),
    # Venue parameters
    EXCHANGE_URL=os.getenv(
        "AFP_EXCHANGE_URL", "https://exchange-server-next.up.railway.app/"
    ),
    # IPFS client parameters
    IPFS_API_URL=os.getenv("AFP_IPFS_API_URL", "http://localhost:5001"),
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
