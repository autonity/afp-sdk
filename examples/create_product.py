import os
from datetime import datetime, timedelta
from decimal import Decimal
from pprint import pprint

import afp


AUTONITY_RPC_URL = "https://bakerloo.autonity-apis.com"
PRIVATE_KEY = os.environ["BUILDER_PRIVATE_KEY"]


def main():
    app = afp.AFP(
        rpc_url=AUTONITY_RPC_URL, authenticator=afp.PrivateKeyAuthenticator(PRIVATE_KEY)
    )
    product = app.Product()

    specification = product.create(
        symbol="SDK-TEST-1",
        description="Test Product 1",
        oracle_address="0xd8A8C5A492Fc2448cFcF980218c0F7D2De4d6FB3",
        fsv_decimals=1,
        fsp_alpha=Decimal("10000"),
        fsp_beta=Decimal("0"),
        fsv_calldata="0x",
        start_time=datetime.now() + timedelta(minutes=1),
        earliest_fsp_submission_time=datetime.now() + timedelta(days=7),
        collateral_asset="0xB855D5e83363A4494e09f0Bb3152A70d3f161940",
        tick_size=6,
        unit_value=Decimal("1"),
        initial_margin_requirement=Decimal("0.2"),
        maintenance_margin_requirement=Decimal("0.1"),
        auction_bounty=Decimal("0.1"),
        tradeout_interval=3600,
        extended_metadata="QmPK1s3pNYLi9ERiq3BDxKa4XosgWwFRQUydHUtz4YgpqB",
    )
    pprint(specification.model_dump())

    product.register(specification)
    print(product.state(specification.id))


if __name__ == "__main__":
    main()
