import re

import eth_account

from afp.api.base import ExchangeAPI


def test_generate_eip4361_message():
    account = eth_account.Account.from_key(
        "0x0cc549714a138639cbd51f79ff38f279e490afd2b2b98cc910af6e3d699d6049"
    )
    nonce = "12345678"

    expected_message_regex = re.compile(
        r"\S+ wants you to sign in with your Ethereum account:\n"
        rf"{account.address}\n\n\n"
        r"URI: \S+\n"
        r"Version: 1\n"
        r"Chain ID: \S+\n"
        rf"Nonce: {nonce}\n"
        r"Issued At: \S+"
    )

    actual_message = ExchangeAPI._generate_eip4361_message(account, nonce)

    assert expected_message_regex.match(actual_message)
