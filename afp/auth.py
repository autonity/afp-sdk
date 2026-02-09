import atexit
import json
import os
from typing import Protocol, cast

import trezorlib.ethereum as trezor_eth
from eth_account.account import Account
from eth_account.datastructures import SignedTransaction
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount
from eth_account.types import TransactionDictType
from eth_account._utils.legacy_transactions import (
    encode_transaction,
    serializable_unsigned_transaction_from_dict,
)
from eth_typing.evm import ChecksumAddress
from eth_utils.conversions import to_int
from eth_utils.crypto import keccak
from hexbytes import HexBytes
from trezorlib.client import TrezorClient, TrezorClientUI, get_default_client
from trezorlib.tools import parse_path
from trezorlib.transport import DeviceIsBusy
from web3 import Web3
from web3.constants import CHECKSUM_ADDRESSS_ZERO
from web3.types import TxParams

from .constants import TREZOR_DEFAULT_PREFIX
from .exceptions import DeviceError


class Authenticator(Protocol):
    address: ChecksumAddress

    def sign_message(self, message: bytes) -> HexBytes: ...

    def sign_transaction(self, params: TxParams) -> SignedTransaction: ...


class NullAuthenticator(Authenticator):
    """Authenticator stub as placeholder for testing."""

    def __init__(self):
        self.address = CHECKSUM_ADDRESSS_ZERO

    def sign_message(self, message: bytes) -> HexBytes:
        raise NotImplementedError()

    def sign_transaction(self, params: TxParams) -> SignedTransaction:
        raise NotImplementedError()


class PrivateKeyAuthenticator(Authenticator):
    """Authenticates with a private key specified in a constructor argument.

    Parameters
    ----------
    private_key: str
        The private key of a blockchain account.
    """

    _account: LocalAccount

    def __init__(self, private_key: str) -> None:
        self._account = Account.from_key(private_key)
        self.address = self._account.address

    def sign_message(self, message: bytes) -> HexBytes:
        eip191_message = encode_defunct(message)
        signed_message = self._account.sign_message(eip191_message)
        return signed_message.signature

    def sign_transaction(self, params: TxParams) -> SignedTransaction:
        return self._account.sign_transaction(cast(TransactionDictType, params))

    def __repr__(self):
        return f"{self.__class__.__name__}(address='{self.address}')"


class KeyfileAuthenticator(PrivateKeyAuthenticator):
    """Authenticates with a private key read from an encrypted keyfile.

    Parameters
    ----------
    key_file : str
        The path to the keyfile.
    password : str
        The password for decrypting the keyfile. Defaults to no password.
    """

    def __init__(self, key_file: str, password: str = "") -> None:
        with open(os.path.expanduser(key_file), encoding="utf8") as f:
            key_data = json.load(f)

        private_key = Account.decrypt(key_data, password=password)
        super().__init__(private_key.to_0x_hex())


class TrezorAuthenticator(Authenticator):
    """Authenticates with a Trezor device.

    Parameters
    ----------
    path_or_index: str or int
        The full derivation path of the account, e.g. `m/44h/60h/0h/0/123`; or the
        index of the account at the default Trezor derivation prefix for Ethereum
        coins `m/44h/60h/0h/0`, e.g. `123`.
    passphrase: str
        The passphrase for the Trezor device. Defaults to no passphrase.
    """

    client: TrezorClient

    def __init__(self, path_or_index: str | int, passphrase: str = ""):
        if isinstance(path_or_index, int) or path_or_index.isdigit():
            path_str = f"{TREZOR_DEFAULT_PREFIX}/{int(path_or_index)}"
        else:
            path_str = path_or_index
        try:
            self.path = parse_path(path_str)
        except ValueError as exc:
            raise DeviceError(
                f"Invalid Trezor BIP32 derivation path '{path_str}'"
            ) from exc
        self.client = self._get_client(passphrase)
        atexit.register(self.client.end_session)

        address_str = trezor_eth.get_address(self.client, self.path)
        self.address = Web3.to_checksum_address(address_str)

    def sign_transaction(self, params: TxParams) -> SignedTransaction:
        assert "chainId" in params
        assert "gas" in params
        assert "nonce" in params
        assert "to" in params
        assert "value" in params
        data_bytes = HexBytes(params["data"] if "data" in params else b"")

        if "gasPrice" in params and params["gasPrice"]:
            v_int, r_bytes, s_bytes = trezor_eth.sign_tx(
                self.client,
                self.path,
                nonce=cast(int, params["nonce"]),
                gas_price=cast(int, params["gasPrice"]),
                gas_limit=params["gas"],
                to=cast(str, params["to"]),
                value=cast(int, params["value"]),
                data=data_bytes,
                chain_id=params["chainId"],
            )
        else:
            assert "maxFeePerGas" in params
            assert "maxPriorityFeePerGas" in params
            v_int, r_bytes, s_bytes = trezor_eth.sign_tx_eip1559(
                self.client,
                self.path,
                nonce=cast(int, params["nonce"]),
                gas_limit=params["gas"],
                to=cast(str, params["to"]),
                value=cast(int, params["value"]),
                data=data_bytes,
                chain_id=params["chainId"],
                max_gas_fee=int(params["maxFeePerGas"]),
                max_priority_fee=int(params["maxPriorityFeePerGas"]),
            )

        r_int = to_int(r_bytes)
        s_int = to_int(s_bytes)
        filtered_tx = dict((k, v) for (k, v) in params.items() if k not in ("from"))
        # In a LegacyTransaction, "type" is not a valid field. See EIP-2718.
        if "type" in filtered_tx and filtered_tx["type"] == "0x0":
            filtered_tx.pop("type")
        tx_unsigned = serializable_unsigned_transaction_from_dict(
            cast(TransactionDictType, filtered_tx)
        )
        tx_encoded = encode_transaction(tx_unsigned, vrs=(v_int, r_int, s_int))
        txhash = keccak(tx_encoded)
        return SignedTransaction(
            raw_transaction=HexBytes(tx_encoded),
            hash=HexBytes(txhash),
            r=r_int,
            s=s_int,
            v=v_int,
        )

    def sign_message(self, message: bytes) -> HexBytes:
        sigdata = trezor_eth.sign_message(
            self.client,
            self.path,
            message.decode("utf-8"),
        )
        return HexBytes(sigdata.signature)

    @staticmethod
    def _get_client(passphrase: str) -> TrezorClient:
        ui = _NonInteractiveTrezorUI(passphrase)
        try:
            return get_default_client(ui=ui)
        except DeviceIsBusy as exc:
            raise DeviceError("Device in use by another process") from exc
        except Exception as exc:
            raise DeviceError(
                "No Trezor device found; "
                "check device is connected, unlocked, and detected by OS"
            ) from exc


class _NonInteractiveTrezorUI(TrezorClientUI):
    """Replacement for the default TrezorClientUI of the Trezor library.

    Bringing up an interactive passphrase prompt is unwanted in the SDK;
    this implementation receives the passphrase as constructor argument.
    """
    _passphrase: str

    def __init__(self, passphrase: str) -> None:
        self._passphrase = passphrase

    def button_request(self, br: object) -> None:
        pass

    def get_pin(self, code: object) -> str:
        raise DeviceError("PIN entry on host is not supported")

    def get_passphrase(self, available_on_device: bool) -> str:
        return self._passphrase
