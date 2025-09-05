import os

from web3 import Web3


# Constants from clearing/contracts/lib/constants.sol
RATE_MULTIPLIER = 10**4
FEE_RATE_MULTIPLIER = 10**6
FULL_PRECISION_MULTIPLIER = 10**18

USER_AGENT = "afp-sdk"
DEFAULT_EXCHANGE_API_VERSION = 1
EXCHANGE_URL = os.getenv(
    "AFP_EXCHANGE_URL", "https://afp-exchange-stable.up.railway.app"
)

CHAIN_ID = int(os.getenv("AFP_CHAIN_ID", 65000000))

CLEARING_DIAMOND_ADDRESS = Web3.to_checksum_address(
    os.getenv(
        "AFP_CLEARING_DIAMOND_ADDRESS", "0x5B5411F1548254d25360d71FE40cFc1cC983B2A2"
    )
)
MARGIN_ACCOUNT_REGISTRY_ADDRESS = Web3.to_checksum_address(
    os.getenv(
        "AFP_MARGIN_ACCOUNT_REGISTRY_ADDRESS",
        "0x99f4FA9Cdce7AD227eB84907936a8FeF2095D846",
    )
)
ORACLE_PROVIDER_ADDRESS = Web3.to_checksum_address(
    os.getenv(
        "AFP_ORACLE_PROVIDER_ADDRESS", "0xF2A2A27da33D30B4BF38D7e186E7B0b1e964e55c"
    )
)
PRODUCT_REGISTRY_ADDRESS = Web3.to_checksum_address(
    os.getenv(
        "AFP_PRODUCT_REGISTRY_ADDRESS", "0x86B3829471929B115367DA0958f56A6AB844b08e"
    )
)
SYSTEM_VIEWER_ADDRESS = Web3.to_checksum_address(
    os.getenv("AFP_SYSTEM_VIEWER_ADDRESS", "0xfF2DFcC44a95cce96E03EfC33C65c8Be671Bae5B")
)
