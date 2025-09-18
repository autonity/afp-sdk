import json
import os
from typing import Protocol, cast

from eth_account.account import Account
from eth_account.datastructures import SignedTransaction
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount
from eth_account.types import TransactionDictType
from eth_typing.evm import ChecksumAddress
from hexbytes import HexBytes
from web3.types import TxParams


class Authenticator(Protocol):
    address: ChecksumAddress

    def sign_message(self, message: bytes) -> HexBytes: ...

    def sign_transaction(self, params: TxParams) -> SignedTransaction: ...


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
        The password for decrypting the keyfile.
    """

    def __init__(self, key_file: str, password: str) -> None:
        with open(os.path.expanduser(key_file), encoding="utf8") as f:
            key_data = json.load(f)

        private_key = Account.decrypt(key_data, password=password)
        super().__init__(private_key.to_0x_hex())
