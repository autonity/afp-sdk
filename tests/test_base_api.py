import re
from decimal import Decimal
from unittest.mock import Mock

import pytest
import eth_account
from hexbytes import HexBytes
from web3 import Web3, HTTPProvider
from web3.contract.contract import ContractFunction
from web3.eth import Eth

import afp
from afp.api.base import BaseAPI, ClearingSystemAPI, ExchangeAPI
from afp.bindings import MarginAccount
from afp.constants import defaults
from afp.exceptions import ConfigurationError
from afp.exchange import ExchangeClient
from afp.schemas import ExchangeParameters

from . import NULL_ADDRESS, AuthenticatorStub


def test_BaseAPI__raises_error_for_missing_authenticator():
    app = afp.AFP()
    with pytest.raises(ConfigurationError):
        BaseAPI(app.config)


def test_ClearingSystemAPI__raises_error_for_missing_rpc_url():
    app = afp.AFP(authenticator=AuthenticatorStub())
    with pytest.raises(ConfigurationError):
        ClearingSystemAPI(app.config)


def test_ClearingSystemAPI__applies_transaction_parameters(monkeypatch):
    mock_build_transaction = Mock(return_value={})
    mock_wait_for_transaction_receipt = Mock(return_value={})
    mock_get_transaction_count = Mock(return_value=5)
    mock_send_raw_transaction = Mock(return_value=HexBytes("0x"))

    monkeypatch.setattr(ContractFunction, "build_transaction", mock_build_transaction)
    monkeypatch.setattr(Eth, "get_transaction_count", mock_get_transaction_count)
    monkeypatch.setattr(Eth, "send_raw_transaction", mock_send_raw_transaction)
    monkeypatch.setattr(
        Eth, "wait_for_transaction_receipt", mock_wait_for_transaction_receipt
    )

    w3 = Web3()
    margin_contract = MarginAccount(w3, NULL_ADDRESS)
    authorize = margin_contract.authorize(NULL_ADDRESS)

    assert defaults.TIMEOUT_SECONDS != 4

    app = afp.AFP(
        authenticator=AuthenticatorStub(),
        rpc_url="http://foobar",
        gas_limit=1,
        max_fee_per_gas=2,
        max_priority_fee_per_gas=3,
        timeout_seconds=4,
    )
    api = ClearingSystemAPI(app.config)

    assert isinstance(api._w3.provider, HTTPProvider)
    assert api._w3.provider.endpoint_uri == "http://foobar"

    api._transact(authorize)

    mock_build_transaction.assert_called_once()
    tx_params = mock_build_transaction.call_args_list[0].args[0]
    assert tx_params["from"] == NULL_ADDRESS
    assert tx_params["nonce"] == 5
    assert tx_params["gasLimit"] == 1
    assert tx_params["maxFeePerGas"] == 2
    assert tx_params["maxPriorityFeePerGas"] == 3

    mock_wait_for_transaction_receipt.assert_called_once()
    timeout = mock_wait_for_transaction_receipt.call_args_list[0].kwargs["timeout"]
    assert timeout == 4


def test_ExchangeAPI__applies_exchange_parameters(monkeypatch):
    fake_exchange_params = ExchangeParameters(
        trading_protocol_id="baz",
        maker_trading_fee_rate=Decimal("0"),
        taker_trading_fee_rate=Decimal("0"),
    )
    mock_login = Mock(return_value=fake_exchange_params)
    mock_generate_login_nonce = Mock(return_value="12345678")

    monkeypatch.setattr(ExchangeClient, "login", mock_login)
    monkeypatch.setattr(
        ExchangeClient, "generate_login_nonce", mock_generate_login_nonce
    )

    app = afp.AFP(
        authenticator=AuthenticatorStub(), exchange_url="http://foobar", chain_id=12345
    )
    api = ExchangeAPI(app.config)

    assert api._exchange._base_url == "http://foobar"
    mock_login.assert_called_once()
    login_submission = mock_login.call_args_list[0].args[0]
    assert "Chain ID: 12345" in login_submission.message


def test_ExchangeAPI__generates_eip4361_message(monkeypatch):
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
