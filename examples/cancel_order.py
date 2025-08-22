from datetime import datetime, timedelta
from decimal import Decimal
from pprint import pprint
from time import sleep

import afp


MARGIN_ACCOUNT_ID = "0x79EFD85867d4Ae3a96a65d66707266647d771023"
INTENT_ACCOUNT_PRIVATE_KEY = (
    "0xdbacc0d8d0b5dc20a7a68f9ceb2daa3d5dc7ab43b06d2eda4b9a41a08be60024"
)

PRODUCT_ID = "0xf82118deb932a8649d519d8d34e7f7b278a44bdb3f2663f6049aaea6ee33b211"


def main():
    # Trader submits bid
    trading = afp.Trading(INTENT_ACCOUNT_PRIVATE_KEY)

    intent = trading.create_intent(
        margin_account_id=MARGIN_ACCOUNT_ID,
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
