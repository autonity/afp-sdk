import os
from typing import cast
from unittest.mock import Mock

from eth_account.datastructures import SignedTransaction
from eth_typing.evm import ChecksumAddress
from hexbytes import HexBytes
from web3.types import TxParams

os.environ = {}

from afp import auth


NULL_ADDRESS = cast(ChecksumAddress, "0x0000000000000000000000000000000000000000")


class AuthenticatorStub(auth.Authenticator):
    address = NULL_ADDRESS

    def sign_message(self, message: bytes) -> HexBytes:
        return HexBytes("0x")

    def sign_transaction(self, params: TxParams) -> SignedTransaction:
        return cast(SignedTransaction, Mock(raw_transaction=HexBytes("0x")))
