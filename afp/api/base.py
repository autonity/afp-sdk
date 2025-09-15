from abc import ABC
from datetime import datetime
from functools import cache
from urllib.parse import urlparse
from typing import cast

from eth_typing.evm import ChecksumAddress
from siwe import ISO8601Datetime, SiweMessage, siwe  # type: ignore (untyped library)
from web3 import Web3, HTTPProvider
from web3.contract.contract import ContractFunction
from web3.types import TxParams

from ..auth import Authenticator
from ..config import Config
from ..bindings.erc20 import ERC20
from ..exceptions import ConfigurationError
from ..exchange import ExchangeClient
from ..schemas import LoginSubmission, Transaction


class BaseAPI(ABC):
    _authenticator: Authenticator
    _config: Config

    def __init__(self, config: Config, authenticator: Authenticator | None = None):
        self._config = config

        if authenticator is None:
            if config.authenticator is None:
                raise ConfigurationError("Authenticator not specified")
            self._authenticator = config.authenticator
        else:
            self._authenticator = authenticator

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(authenticator={repr(self._authenticator)})"


class ClearingSystemAPI(BaseAPI, ABC):
    _config: Config
    _w3: Web3

    def __init__(self, config: Config, authenticator: Authenticator | None = None):
        super().__init__(config, authenticator)

        if self._config.rpc_url is None:
            raise ConfigurationError("RPC URL not specified")

        self._w3 = Web3(HTTPProvider(self._config.rpc_url))
        self._w3.eth.default_account = self._authenticator.address

    def _transact(self, func: ContractFunction) -> Transaction:
        tx_count = self._w3.eth.get_transaction_count(self._authenticator.address)
        tx_params = {
            "from": self._authenticator.address,
            "nonce": tx_count,
            "gasLimit": self._config.gas_limit,
            "maxFeePerGas": self._config.max_fee_per_gas,
            "maxPriorityFeePerGas": self._config.max_priority_fee_per_gas,
        }

        prepared_tx = func.build_transaction(
            cast(TxParams, {k: v for k, v in tx_params.items() if v is not None})
        )
        signed_tx = self._authenticator.sign_transaction(prepared_tx)
        tx_hash = self._w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = self._w3.eth.wait_for_transaction_receipt(
            tx_hash, timeout=self._config.timeout_seconds
        )

        return Transaction(
            hash=tx_hash.to_0x_hex(),
            data=dict(prepared_tx),
            receipt=dict(tx_receipt),
        )

    @cache
    def _decimals(self, collateral_asset: ChecksumAddress) -> int:
        token_contract = ERC20(self._w3, collateral_asset)
        return token_contract.decimals()


class ExchangeAPI(BaseAPI, ABC):
    _exchange: ExchangeClient
    _trading_protocol_id: str

    def __init__(
        self,
        config: Config,
        authenticator: Authenticator | None = None,
        exchange_url: str | None = None,
    ):
        if exchange_url is None:
            exchange_url = config.exchange_url

        super().__init__(config, authenticator)
        self._exchange = ExchangeClient(exchange_url)
        self._login()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(authenticator={repr(self._authenticator)}, "
            f"exchange={repr(self._exchange)})"
        )

    def _login(self):
        nonce = self._exchange.generate_login_nonce()
        message = self._generate_eip4361_message(nonce)
        signature = self._authenticator.sign_message(message.encode("ascii"))

        login_submission = LoginSubmission(
            message=message, signature=Web3.to_hex(signature)
        )
        exchange_parameters = self._exchange.login(login_submission)

        self._trading_protocol_id = exchange_parameters.trading_protocol_id

    def _generate_eip4361_message(self, nonce: str) -> str:
        message = SiweMessage(
            domain=urlparse(self._config.exchange_url).netloc,
            address=self._authenticator.address,
            uri=self._config.exchange_url,
            version=siwe.VersionEnum.one,  # type: ignore
            chain_id=self._config.chain_id,
            issued_at=ISO8601Datetime.from_datetime(datetime.now()),
            nonce=nonce,
            statement=None,
        )
        return message.prepare_message()
