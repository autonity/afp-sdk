import os
from datetime import datetime, timedelta
from decimal import Decimal
from pprint import pprint

import afp


AUTONITY_RPC_URL = "https://bakerloo.autonity-apis.com"
PRIVATE_KEY = os.environ["PRIVATE_KEY"]


def main():
    app = afp.AFP(
        rpc_url=AUTONITY_RPC_URL, authenticator=afp.PrivateKeyAuthenticator(PRIVATE_KEY)
    )
    product = app.Product()

    specification = product.create(
        symbol="USCPIG26",
        description="US CPI February 2026 MoM change (annualized)",
        fsv_decimals=2,
        fsp_alpha=Decimal("1.0"),
        fsp_beta=Decimal("0.0"),
        fsv_calldata="0x",
        collateral_asset="0xDEfAaC81a079533Bf2fb004c613cc2870cF0A5b5",
        start_time=datetime.now() + timedelta(minutes=1),
        point_value=Decimal("1"),
        price_decimals=2,
        earliest_fsp_submission_time=datetime.now() + timedelta(days=7),
        tradeout_interval=86400,
        min_price=Decimal("1.75"),
        max_price=Decimal("3.75"),
        extended_metadata="QmPK1s3pNYLi9ERiq3BDxKa4XosgWwFRQUydHUtz4YgpqB",
    )
    pprint(specification.model_dump())

    product.register(specification)
    print(product.state(specification.id))


if __name__ == "__main__":
    main()
