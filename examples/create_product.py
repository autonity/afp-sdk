from datetime import datetime, timedelta
from decimal import Decimal
from pprint import pprint

import afp


BUILDER_ACCOUNT_PRIVATE_KEY = (
    "0x926b0e772d87247fb08832e7fd55e528ae5997680713367a4786c92e7d909154"
)

AUTONITY_RPC_URL = "https://bakerloo.autonity-apis.com"


def main():
    builder = afp.Builder(BUILDER_ACCOUNT_PRIVATE_KEY, AUTONITY_RPC_URL)

    product = builder.create_product(
        symbol="SDK-TEST-1",
        description="Test Product 1",
        oracle_address="0xd8A8C5A492Fc2448cFcF980218c0F7D2De4d6FB3",
        fsv_decimals=1,
        fsp_alpha=Decimal("10000"),
        fsp_beta=0,
        fsv_calldata="0x",
        start_time=datetime.now() + timedelta(minutes=1),
        earliest_fsp_submission_time=datetime.now() + timedelta(days=7),
        collateral_asset="0xB855D5e83363A4494e09f0Bb3152A70d3f161940",
        tick_size=6,
        unit_value=Decimal("1"),
        initial_margin_requirement=Decimal("0.2"),
        maintenance_margin_requirement=Decimal("0.1"),
        offer_price_buffer=Decimal("0.1"),
        auction_bounty=Decimal("0.1"),
        tradeout_interval=3600,
        extended_metadata="QmPK1s3pNYLi9ERiq3BDxKa4XosgWwFRQUydHUtz4YgpqB",
    )
    pprint(product.model_dump())

    builder.register_product(product)
    print(builder.product_state(product.id))


if __name__ == "__main__":
    main()
