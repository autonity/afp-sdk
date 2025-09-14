import pytest
from requests import Response
from unittest.mock import Mock
from web3.exceptions import ContractCustomError, ContractLogicError, Web3RPCError
from web3.types import RPCResponse

import afp
from afp.api.base import ExchangeAPI
from afp.decorators import convert_web3_error, refresh_token_on_expiry
from afp.exceptions import AuthenticationError
from afp.exchange import ExchangeClient
from afp.exceptions import ClearingSystemError
from afp.bindings.clearing_facet import ABI as CLEARING_ABI


PRIVATE_KEY = "0x32df57bd2cbdca044227974f6937d5722da13344218daa4286071e7850d28694"


class FakeExchangeAPI(ExchangeAPI):
    @refresh_token_on_expiry
    def get_data(self):
        return self._exchange._send_request("GET", "/foo")


def test_refresh_token_on_expiry__token_expired(monkeypatch):
    login_mock = Mock()
    send_request_mock = Mock(
        side_effect=[AuthenticationError, None], return_value=Response()
    )

    monkeypatch.setattr(FakeExchangeAPI, "_login", login_mock)
    monkeypatch.setattr(ExchangeClient, "_send_request", send_request_mock)

    app = afp.AFP(authenticator=afp.PrivateKeyAuthenticator(PRIVATE_KEY))
    exchange_api = FakeExchangeAPI(app.config)
    assert login_mock.call_count == 1

    exchange_api.get_data()
    assert login_mock.call_count == 2
    assert send_request_mock.call_count == 2


def test_refresh_token_on_expiry__token_did_not_expire(monkeypatch):
    login_mock = Mock()
    send_request_mock = Mock(return_value=Response())

    monkeypatch.setattr(FakeExchangeAPI, "_login", login_mock)
    monkeypatch.setattr(ExchangeClient, "_send_request", send_request_mock)

    app = afp.AFP(authenticator=afp.PrivateKeyAuthenticator(PRIVATE_KEY))
    exchange_api = FakeExchangeAPI(app.config)
    assert login_mock.call_count == 1

    exchange_api.get_data()
    assert login_mock.call_count == 1
    assert send_request_mock.call_count == 1


def test_convert_web3_error__contract_custom_error():
    error_selector = "0x72e58de7"
    error_message = "Invalid intent"

    @convert_web3_error(CLEARING_ABI)
    def raise_custom_error():
        raise ContractCustomError(error_selector, data=error_selector)

    with pytest.raises(ClearingSystemError, match=error_message):
        raise_custom_error()


def test_convert_web3_error__contract_logic_error():
    error_message = "Something went wrong"

    @convert_web3_error()
    def raise_logic_error():
        raise ContractLogicError(error_message, data=error_message)

    with pytest.raises(ClearingSystemError, match=error_message):
        raise_logic_error()


def test_convert_web3_error__rpc_error():
    error_message = "Insufficient funds"
    rpc_response: RPCResponse = {
        "jsonrpc": "2.0",
        "id": 10,
        "error": {
            "code": -32000,
            "message": error_message,
        },
    }

    @convert_web3_error()
    def raise_rpc_error():
        raise Web3RPCError(str(rpc_response["error"]), rpc_response=rpc_response)

    with pytest.raises(ClearingSystemError, match=error_message):
        raise_rpc_error()
