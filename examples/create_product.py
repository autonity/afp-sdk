"""Example for creating a product from JSON specification."""

import os
from decimal import Decimal
from os import path
from pprint import pprint

import afp


AUTONITY_RPC_URL = "https://bakerloo.autonity-apis.com"
IPFS_API_URL = "https://rpc.filebase.io"

PRIVATE_KEY = os.environ["PRIVATE_KEY"]
IPFS_API_KEY = os.environ["IPFS_API_KEY"]


def main():
    # 0. Configure the SDK
    authenticator = afp.PrivateKeyAuthenticator(PRIVATE_KEY)
    app = afp.AFP(
        authenticator=authenticator,
        rpc_url=AUTONITY_RPC_URL,
        ipfs_api_url=IPFS_API_URL,
        ipfs_api_key=IPFS_API_KEY,
    )
    product = app.Product()

    # 1. Validate the JSON specification
    with open(
        path.join(path.dirname(__file__), "prediction-product-example.json")
    ) as f:
        specification = product.validate_json(f.read())

    # 2. Upload the extended metadata to IPFS
    pinned_specification = product.pin(specification)
    pprint(product.dump(pinned_specification))

    # 3. Send registration transaction
    tx = product.register(pinned_specification, initial_builder_stake=Decimal("0"))
    print(tx.receipt)

    # 4. Check product state
    id = product.id(pinned_specification)
    print(product.state(id))

    # 5. Download the product specification from blockchain & IPFS and re-validate it
    downloaded_specification = product.get(id)

    # 6. Write the downloaded product specification into a JSON file
    with open("downloaded-product-example.json", "w") as f:
        f.write(product.dump_json(downloaded_specification))


if __name__ == "__main__":
    main()
