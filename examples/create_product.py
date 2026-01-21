import os
from datetime import datetime, timedelta
from decimal import Decimal
from pprint import pprint

import afp
from afp import schemas


AUTONITY_RPC_URL = "https://bakerloo.autonity-apis.com"
PRIVATE_KEY = os.environ["PRIVATE_KEY"]


def main():
    authenticator = afp.PrivateKeyAuthenticator(PRIVATE_KEY)
    app = afp.AFP(rpc_url=AUTONITY_RPC_URL, authenticator=authenticator)
    product = app.Product()

    specification = schemas.PredictionProductV1(
        base=schemas.BaseProduct(
            metadata=schemas.ProductMetadata(
                builder=authenticator.address,
                symbol="USCPIG26",
                description="US CPI February 2026 MoM change (annualized)",
            ),
            oracle_spec=schemas.OracleSpecification(
                oracle_address="0x72EeD9f7286292f119089F56e3068a3A931FCD49",
                fsv_decimals=2,
                fsp_alpha=Decimal("1.0"),
                fsp_beta=Decimal("0.0"),
                fsv_calldata="0x",
            ),
            collateral_asset="0xDEfAaC81a079533Bf2fb004c613cc2870cF0A5b5",
            start_time=datetime.now() + timedelta(minutes=1),
            point_value=Decimal("1"),
            price_decimals=2,
            extended_metadata="QmPK1s3pNYLi9ERiq3BDxKa4XosgWwFRQUydHUtz4YgpqB",
        ),
        expiry_spec=schemas.ExpirySpecification(
            earliest_fsp_submission_time=datetime.now() + timedelta(days=7),
            tradeout_interval=86400,
        ),
        min_price=Decimal("1.75"),
        max_price=Decimal("3.75"),
    )
    pprint(specification.model_dump())

    product.register(specification)
    print(product.state(product.id(specification)))


if __name__ == "__main__":
    main()
