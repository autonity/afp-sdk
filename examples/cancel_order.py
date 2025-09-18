import os
from datetime import datetime, timedelta
from decimal import Decimal
from pprint import pprint
from time import sleep

import afp


PRIVATE_KEY = os.environ["TRADER_PRIVATE_KEY"]
PRODUCT_ID = "0xf82118deb932a8649d519d8d34e7f7b278a44bdb3f2663f6049aaea6ee33b211"


def main():
    app = afp.AFP(authenticator=afp.PrivateKeyAuthenticator(PRIVATE_KEY))
    trading = app.Trading()

    # Trader submits bid
    intent = trading.create_intent(
        product=trading.product(PRODUCT_ID),
        side="bid",
        limit_price=Decimal("2.34"),
        quantity=1,
        max_trading_fee_rate=Decimal("0.1"),
        good_until_time=datetime.now() + timedelta(hours=1),
    )
    limit_order = trading.submit_limit_order(intent)
    pprint(limit_order.model_dump())

    # Trader cancels the bid
    cancel_order = trading.submit_cancel_order(intent.hash)
    pprint(cancel_order.model_dump())

    # Check that the order is cancelled
    sleep(0.5)
    pprint(trading.order(limit_order.id).model_dump())


if __name__ == "__main__":
    main()
