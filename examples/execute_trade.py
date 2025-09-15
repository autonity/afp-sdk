import os
from datetime import datetime, timedelta
from decimal import Decimal
from pprint import pprint
from time import sleep

import afp


AUTONITY_RPC_URL = "https://bakerloo.autonity-apis.com"
TRADER1_PRIVATE_KEY = os.environ["TRADER1_PRIVATE_KEY"]
TRADER2_PRIVATE_KEY = os.environ["TRADER2_PRIVATE_KEY"]

PRODUCT_ID = "0xf82118deb932a8649d519d8d34e7f7b278a44bdb3f2663f6049aaea6ee33b211"
COLLATERAL_ASSET = "0x15d7B75e16162C36d86c971508c0d6eF2D7F131D"


def main():
    app = afp.AFP(rpc_url=AUTONITY_RPC_URL)

    # Trader #1 adds collateral to their margin account
    margin_account = app.MarginAccount(afp.PrivateKeyAuthenticator(TRADER1_PRIVATE_KEY))
    margin_account.deposit(COLLATERAL_ASSET, Decimal("100"))

    # Trader #1 submits bid
    trading = app.Trading(afp.PrivateKeyAuthenticator(TRADER1_PRIVATE_KEY))

    product = trading.product(PRODUCT_ID)
    pprint(product.model_dump())

    bid_intent = trading.create_intent(
        product=product,
        side="bid",
        limit_price=Decimal("1.23"),
        quantity=2,
        max_trading_fee_rate=Decimal("0.1"),
        good_until_time=datetime.now() + timedelta(hours=1),
    )
    pprint(bid_intent.model_dump())

    bid_order = trading.submit_limit_order(bid_intent)
    pprint(bid_order.model_dump())

    # Trader #2 submits ask
    trading = app.Trading(afp.PrivateKeyAuthenticator(TRADER2_PRIVATE_KEY))

    ask_intent = trading.create_intent(
        product=product,
        side="ask",
        limit_price=Decimal("1.23"),
        quantity=2,
        max_trading_fee_rate=Decimal("0.1"),
        good_until_time=datetime.now() + timedelta(hours=1),
    )
    pprint(ask_intent.model_dump())

    ask_order = trading.submit_limit_order(ask_intent)
    pprint(ask_order.model_dump())

    # Check order fills
    sleep(0.5)
    fills = trading.order_fills(product_id=product.id)
    pprint([fill.model_dump() for fill in fills])


if __name__ == "__main__":
    main()
