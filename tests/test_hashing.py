from datetime import datetime
from decimal import Decimal
from typing import cast

import eth_account
from eth_typing.evm import ChecksumAddress
from hexbytes import HexBytes

from afp import signing
from afp.enums import OrderSide
from afp.schemas import IntentData


def test_generate_intent_hash():
    intent_data = IntentData(
        trading_protocol_id="0x783b16190c71278E78f69Af32815CcA818A9822f",
        product_id="0xa74b5c2da3083e4189f56b2582c4455d21bbbd199d7699fc6ebddd82e8fd02b5",
        limit_price=Decimal("1.0"),
        quantity=1,
        max_trading_fee_rate=Decimal("0.1"),
        side=OrderSide.ASK,
        good_until_time=datetime.fromisoformat("2030-01-01T12:00:00Z"),
        nonce=42,
    )
    margin_account_id = cast(
        ChecksumAddress, "0x51541B823f9C28e8E43E18c0F0d50B405FCB8aD4"
    )
    intent_account_id = cast(
        ChecksumAddress, "0x44163AaD36b0f6986fd09D0d6AD990F0341F16E7"
    )

    expected_hash = HexBytes(
        "0x54aeb60873e54eebcc582af5bef7caf005425a2083d6b98c5d7c27f3952f2e57"
    )
    actual_hash = signing.generate_intent_hash(
        intent_data=intent_data,
        margin_account_id=margin_account_id,
        intent_account_id=intent_account_id,
        tick_size=18,
    )
    assert expected_hash == actual_hash


def test_generate_order_cancellation_hash():
    intent_hash = "0x9540b615aa488fb276c71231926d81b2d5f1d43711d306c630df1cf86c81ed88"
    nonce = 42

    expected_hash = HexBytes(
        "0x95672a703e451a4617ecd229400b675e59d21c0d866325cdc87a86d84a898fe8"
    )
    actual_hash = signing.generate_order_cancellation_hash(nonce, intent_hash)
    assert expected_hash == actual_hash


def test_generate_product_id():
    builder = eth_account.Account.from_key(
        "0x0cc549714a138639cbd51f79ff38f279e490afd2b2b98cc910af6e3d699d6049"
    )
    symbol = "PROD-X-1"

    expected_hash = HexBytes(
        "0x89ed228125682fca3832f5fb52236ebabc3d29e64fa0867556a0621a310c49d7"
    )
    actual_hash = signing.generate_product_id(builder, symbol)
    assert expected_hash == actual_hash
