from typing import Any, cast

from eth_abi.packed import encode_packed
from eth_account import messages
from eth_typing.evm import ChecksumAddress
from eth_account.signers.local import LocalAccount
from hexbytes import HexBytes
from web3 import Web3

from . import config
from .bindings import clearing_facet
from .schemas import IntentData, OrderSide


ORDER_SIDE_MAPPING: dict[OrderSide, int] = {
    OrderSide.BID: clearing_facet.Side.BID.value,
    OrderSide.ASK: clearing_facet.Side.ASK.value,
}


def generate_intent_hash(
    intent_data: IntentData,
    margin_account_id: ChecksumAddress,
    intent_account_id: ChecksumAddress,
    tick_size: int,
) -> HexBytes:
    types = [
        "address",  # margin_account_id
        "address",  # intent_account_id
        "uint256",  # nonce
        "address",  # trading_protocol_id
        "bytes32",  # product_id
        "uint256",  # limit_price
        "uint256",  # quantity
        "uint256",  # max_trading_fee_rate
        "uint256",  # good_until_time
        "uint8",  # side
    ]
    values: list[Any] = [
        margin_account_id,
        intent_account_id,
        intent_data.nonce,
        cast(ChecksumAddress, intent_data.trading_protocol_id),
        HexBytes(intent_data.product_id),
        int(intent_data.limit_price * 10**tick_size),
        intent_data.quantity,
        int(intent_data.max_trading_fee_rate * config.FEE_RATE_MULTIPLIER),
        int(intent_data.good_until_time.timestamp()),
        ORDER_SIDE_MAPPING[intent_data.side],
    ]
    return Web3.keccak(encode_packed(types, values))


def generate_order_cancellation_hash(nonce: int, intent_hash: str) -> HexBytes:
    types = ["uint256", "bytes32"]
    values: list[Any] = [nonce, HexBytes(intent_hash)]
    return Web3.keccak(encode_packed(types, values))


def generate_product_id(builder: LocalAccount, symbol: str) -> HexBytes:
    types = ["address", "string"]
    values: list[Any] = [builder.address, symbol]
    return Web3.keccak(encode_packed(types, values))


def sign_message(account: LocalAccount, message: bytes) -> HexBytes:
    eip191_message = messages.encode_defunct(message)
    signed_message = account.sign_message(eip191_message)
    return signed_message.signature
