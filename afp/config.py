import os

from web3 import Web3


# Constants from clearing/contracts/lib/constants.sol
RATE_MULTIPLIER = 10**4
FEE_RATE_MULTIPLIER = 10**6
FULL_PRECISION_MULTIPLIER = 10**18

USER_AGENT = "afp-sdk"
EXCHANGE_URL = os.getenv(
    "AFP_EXCHANGE_URL", "https://afp-exchange-staging.up.railway.app"
)

CHAIN_ID = int(os.getenv("AFP_CHAIN_ID", 65010004))

CLEARING_DIAMOND_ADDRESS = Web3.to_checksum_address(
    os.getenv(
        "AFP_CLEARING_DIAMOND_ADDRESS", "0xB894bFf368Bf1EA89c18612670B7E072866a5264"
    )
)
MARGIN_ACCOUNT_REGISTRY_ADDRESS = Web3.to_checksum_address(
    os.getenv(
        "AFP_MARGIN_ACCOUNT_REGISTRY_ADDRESS",
        "0xDA71FdE0E7cfFf445e848EAdB3B2255B68Ed6ef6",
    )
)
ORACLE_PROVIDER_ADDRESS = Web3.to_checksum_address(
    os.getenv(
        "AFP_ORACLE_PROVIDER_ADDRESS", "0x626da921088a5A00C75C208Decbb60E816488481"
    )
)
PRODUCT_REGISTRY_ADDRESS = Web3.to_checksum_address(
    os.getenv(
        "AFP_PRODUCT_REGISTRY_ADDRESS", "0x9b92EAC112c996a513e515Cf8c3BDd83619F730D"
    )
)
