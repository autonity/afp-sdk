import re
from unittest.mock import Mock

import eth_account

import afp
from afp.api.base import ExchangeAPI


def test_generate_eip4361_message(monkeypatch):
    nonce = "12345678"
    account = eth_account.Account.from_key(
        "0x32df57bd2cbdca044227974f6937d5722da13344218daa4286071e7850d28694"
    )

    monkeypatch.setattr(ExchangeAPI, "_login", Mock())

    expected_message_regex = re.compile(
        r"\S+ wants you to sign in with your Ethereum account:\n"
        rf"{account.address}\n\n\n"
        r"URI: \S+\n"
        r"Version: 1\n"
        r"Chain ID: \S+\n"
        rf"Nonce: {nonce}\n"
        r"Issued At: \S+"
    )

    app = afp.AFP(authenticator=afp.PrivateKeyAuthenticator(account.key))
    actual_message = ExchangeAPI(app.config)._generate_eip4361_message(nonce)

    assert expected_message_regex.match(actual_message)
