from abc import ABC
from datetime import datetime
from functools import cache
from typing import cast
from urllib.parse import urlparse

from eth_account.account import Account
from eth_account.signers.local import LocalAccount
from eth_typing.evm import ChecksumAddress
from siwe import ISO8601Datetime, SiweMessage, siwe  # type: ignore (untyped library)
from web3 import Web3, HTTPProvider
from web3.middleware import Middleware, SignAndSendRawMiddlewareBuilder

from .. import config, signing
from ..bindings.erc20 import ERC20
from ..exchange import ExchangeClient
from ..schemas import LoginSubmission


EXCHANGE_DOMAIN = urlparse(config.EXCHANGE_URL).netloc


class ClearingSystemAPI(ABC):
    _account: LocalAccount
    _w3: Web3

    def __init__(self, private_key: str, autonity_rpc_url: str):
        self._account = Account.from_key(private_key)
        self._w3 = Web3(HTTPProvider(autonity_rpc_url))

        # Configure the default sender account
        self._w3.eth.default_account = self._account.address
        signing_middleware = SignAndSendRawMiddlewareBuilder.build(self._account)
        self._w3.middleware_onion.add(cast(Middleware, signing_middleware))

    @cache
    def _decimals(self, collateral_asset: ChecksumAddress) -> int:
        token_contract = ERC20(self._w3, collateral_asset)
        return token_contract.decimals()


class ExchangeAPI(ABC):
    _account: LocalAccount
    _exchange: ExchangeClient
    _trading_protocol_id: str

    def __init__(self, private_key: str):
        self._account = Account.from_key(private_key)
        self._exchange = ExchangeClient()
        self._login()

    def _login(self):
        nonce = self._exchange.generate_login_nonce()
        message = self._generate_eip4361_message(self._account, nonce)
        signature = signing.sign_message(self._account, message.encode("ascii"))

        login_submission = LoginSubmission(
            message=message, signature=Web3.to_hex(signature)
        )
        exchange_parameters = self._exchange.login(login_submission)

        self._trading_protocol_id = exchange_parameters.trading_protocol_id

    @staticmethod
    def _generate_eip4361_message(account: LocalAccount, nonce: str) -> str:
        message = SiweMessage(
            domain=EXCHANGE_DOMAIN,
            address=account.address,
            uri=config.EXCHANGE_URL,
            version=siwe.VersionEnum.one,  # type: ignore
            chain_id=config.CHAIN_ID,
            issued_at=ISO8601Datetime.from_datetime(datetime.now()),
            nonce=nonce,
            statement=None,
        )
        return message.prepare_message()
