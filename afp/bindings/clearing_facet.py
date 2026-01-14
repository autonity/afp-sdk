"""ClearingFacet contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import hexbytes
import web3
from web3 import types
from web3.contract import contract


from .types import Trade


class ClearingFacet:
    """ClearingFacet contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed ClearingFacet contract.
    """

    _contract: contract.Contract

    def __init__(
        self,
        w3: web3.Web3,
        address: eth_typing.ChecksumAddress,
    ):
        self._contract = w3.eth.contract(
            address=address,
            abi=ABI,
        )

    @property
    def FeeCollected(self) -> contract.ContractEvent:
        """Binding for `event FeeCollected` on the ClearingFacet contract."""
        return self._contract.events.FeeCollected

    @property
    def FeeDispersed(self) -> contract.ContractEvent:
        """Binding for `event FeeDispersed` on the ClearingFacet contract."""
        return self._contract.events.FeeDispersed

    @property
    def PositionUpdated(self) -> contract.ContractEvent:
        """Binding for `event PositionUpdated` on the ClearingFacet contract."""
        return self._contract.events.PositionUpdated

    @property
    def TradeExecuted(self) -> contract.ContractEvent:
        """Binding for `event TradeExecuted` on the ClearingFacet contract."""
        return self._contract.events.TradeExecuted

    def estimate_fees(
        self,
        key0: hexbytes.HexBytes,
        key1: int,
        key2: int,
        key3: int,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.Tuple[int, int]:
        """Binding for `estimateFees` on the ClearingFacet contract.

        Parameters
        ----------
        key0 : hexbytes.HexBytes
        key1 : int
        key2 : int
        key3 : int
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        int
        """
        return_value = self._contract.functions.estimateFees(
            key0,
            key1,
            key2,
            key3,
        ).call(block_identifier=block_identifier)
        return (
            int(return_value[0]),
            int(return_value[1]),
        )

    def execute(
        self,
        trade: Trade,
        fallback_on_failure: bool,
    ) -> contract.ContractFunction:
        """Binding for `execute` on the ClearingFacet contract.

        Parameters
        ----------
        trade : Trade
        fallback_on_failure : bool

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.execute(
            (
                trade.product_id,
                trade.protocol_id,
                trade.trade_id,
                trade.price,
                trade.timestamp,
                trade.quantity,
                trade.accounts,
                trade.quantities,
                trade.fee_rates,
                [
                    (
                        trade_item.margin_account_id,
                        trade_item.intent_account_id,
                        trade_item.hash,
                        (
                            trade_item.data.nonce,
                            trade_item.data.trading_protocol_id,
                            trade_item.data.product_id,
                            trade_item.data.limit_price,
                            trade_item.data.quantity,
                            trade_item.data.max_trading_fee_rate,
                            trade_item.data.good_until,
                            int(trade_item.data.side),
                            trade_item.data.referral,
                        ),
                        trade_item.signature,
                    )
                    for trade_item in trade.intents
                ],
            ),
            fallback_on_failure,
        )


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "type": "function",
            "name": "estimateFees",
            "inputs": [
                {"name": "", "type": "bytes32", "internalType": "bytes32"},
                {"name": "", "type": "uint256", "internalType": "uint256"},
                {"name": "", "type": "uint256", "internalType": "uint256"},
                {"name": "", "type": "int256", "internalType": "int256"},
            ],
            "outputs": [
                {"name": "", "type": "uint256", "internalType": "uint256"},
                {"name": "", "type": "int256", "internalType": "int256"},
            ],
            "stateMutability": "pure",
        },
        {
            "type": "function",
            "name": "execute",
            "inputs": [
                {
                    "name": "trade",
                    "type": "tuple",
                    "internalType": "struct Trade",
                    "components": [
                        {
                            "name": "productId",
                            "type": "bytes32",
                            "internalType": "bytes32",
                        },
                        {
                            "name": "protocolId",
                            "type": "address",
                            "internalType": "address",
                        },
                        {
                            "name": "tradeId",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                        {"name": "price", "type": "int256", "internalType": "int256"},
                        {
                            "name": "timestamp",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                        {
                            "name": "quantity",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                        {
                            "name": "accounts",
                            "type": "address[]",
                            "internalType": "address[]",
                        },
                        {
                            "name": "quantities",
                            "type": "uint256[]",
                            "internalType": "uint256[]",
                        },
                        {
                            "name": "feeRates",
                            "type": "int32[]",
                            "internalType": "int32[]",
                        },
                        {
                            "name": "intents",
                            "type": "tuple[]",
                            "internalType": "struct Intent[]",
                            "components": [
                                {
                                    "name": "marginAccountId",
                                    "type": "address",
                                    "internalType": "address",
                                },
                                {
                                    "name": "intentAccountId",
                                    "type": "address",
                                    "internalType": "address",
                                },
                                {
                                    "name": "hash",
                                    "type": "bytes32",
                                    "internalType": "bytes32",
                                },
                                {
                                    "name": "data",
                                    "type": "tuple",
                                    "internalType": "struct IntentData",
                                    "components": [
                                        {
                                            "name": "nonce",
                                            "type": "uint256",
                                            "internalType": "uint256",
                                        },
                                        {
                                            "name": "tradingProtocolId",
                                            "type": "address",
                                            "internalType": "address",
                                        },
                                        {
                                            "name": "productId",
                                            "type": "bytes32",
                                            "internalType": "bytes32",
                                        },
                                        {
                                            "name": "limitPrice",
                                            "type": "int256",
                                            "internalType": "int256",
                                        },
                                        {
                                            "name": "quantity",
                                            "type": "uint256",
                                            "internalType": "uint256",
                                        },
                                        {
                                            "name": "maxTradingFeeRate",
                                            "type": "uint32",
                                            "internalType": "uint32",
                                        },
                                        {
                                            "name": "goodUntil",
                                            "type": "uint256",
                                            "internalType": "uint256",
                                        },
                                        {
                                            "name": "side",
                                            "type": "uint8",
                                            "internalType": "enum Side",
                                        },
                                        {
                                            "name": "referral",
                                            "type": "address",
                                            "internalType": "address",
                                        },
                                    ],
                                },
                                {
                                    "name": "signature",
                                    "type": "bytes",
                                    "internalType": "bytes",
                                },
                            ],
                        },
                    ],
                },
                {"name": "fallbackOnFailure", "type": "bool", "internalType": "bool"},
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "event",
            "name": "FeeCollected",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "capitalAmount",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "id",
                    "type": "uint256",
                    "indexed": False,
                    "internalType": "uint256",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "FeeDispersed",
            "inputs": [
                {
                    "name": "recipient",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "capitalAmount",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "id",
                    "type": "uint256",
                    "indexed": False,
                    "internalType": "uint256",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "PositionUpdated",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "positionId",
                    "type": "bytes32",
                    "indexed": True,
                    "internalType": "bytes32",
                },
                {
                    "name": "costBasis",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "price",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "quantity",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "id",
                    "type": "uint256",
                    "indexed": False,
                    "internalType": "uint256",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "TradeExecuted",
            "inputs": [
                {
                    "name": "productId",
                    "type": "bytes32",
                    "indexed": True,
                    "internalType": "bytes32",
                },
                {
                    "name": "protocolId",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "id",
                    "type": "uint256",
                    "indexed": False,
                    "internalType": "uint256",
                },
                {
                    "name": "price",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "quantity",
                    "type": "uint256",
                    "indexed": False,
                    "internalType": "uint256",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "error",
            "name": "DuplicateMarginAccount",
            "inputs": [
                {"name": "marginAccount", "type": "address", "internalType": "address"}
            ],
        },
        {"type": "error", "name": "ECDSAInvalidSignature", "inputs": []},
        {
            "type": "error",
            "name": "ECDSAInvalidSignatureLength",
            "inputs": [
                {"name": "length", "type": "uint256", "internalType": "uint256"}
            ],
        },
        {
            "type": "error",
            "name": "ECDSAInvalidSignatureS",
            "inputs": [{"name": "s", "type": "bytes32", "internalType": "bytes32"}],
        },
        {
            "type": "error",
            "name": "IntentFullySpent",
            "inputs": [
                {"name": "intentAccount", "type": "address", "internalType": "address"}
            ],
        },
        {
            "type": "error",
            "name": "InvalidFeeSum",
            "inputs": [{"name": "feeSum", "type": "int256", "internalType": "int256"}],
        },
        {
            "type": "error",
            "name": "InvalidFieldAccess",
            "inputs": [
                {
                    "name": "productType",
                    "type": "uint8",
                    "internalType": "enum ProductType",
                },
                {"name": "field", "type": "string", "internalType": "string"},
            ],
        },
        {
            "type": "error",
            "name": "InvalidIntent",
            "inputs": [
                {"name": "parameter", "type": "string", "internalType": "string"}
            ],
        },
        {
            "type": "error",
            "name": "InvalidParameter",
            "inputs": [
                {"name": "paramName", "type": "string", "internalType": "string"}
            ],
        },
        {
            "type": "error",
            "name": "InvalidProductState",
            "inputs": [
                {"name": "state", "type": "uint8", "internalType": "enum ProductState"}
            ],
        },
        {
            "type": "error",
            "name": "InvalidSignature",
            "inputs": [
                {"name": "signer", "type": "address", "internalType": "address"},
                {
                    "name": "expectedSigner",
                    "type": "address",
                    "internalType": "address",
                },
            ],
        },
        {
            "type": "error",
            "name": "InvalidTradeIntents",
            "inputs": [
                {"name": "length", "type": "uint256", "internalType": "uint256"}
            ],
        },
        {
            "type": "error",
            "name": "InvalidTradePrice",
            "inputs": [{"name": "price", "type": "int256", "internalType": "int256"}],
        },
        {
            "type": "error",
            "name": "MAECheckFailed",
            "inputs": [
                {"name": "marginAccount", "type": "address", "internalType": "address"}
            ],
        },
        {
            "type": "error",
            "name": "MismatchedTrade",
            "inputs": [
                {"name": "buySide", "type": "uint256", "internalType": "uint256"},
                {"name": "sellSide", "type": "uint256", "internalType": "uint256"},
            ],
        },
        {
            "type": "error",
            "name": "NotFound",
            "inputs": [
                {"name": "parameter", "type": "string", "internalType": "string"}
            ],
        },
        {
            "type": "error",
            "name": "PRBMath_MulDiv18_Overflow",
            "inputs": [
                {"name": "x", "type": "uint256", "internalType": "uint256"},
                {"name": "y", "type": "uint256", "internalType": "uint256"},
            ],
        },
        {
            "type": "error",
            "name": "PRBMath_MulDiv_Overflow",
            "inputs": [
                {"name": "x", "type": "uint256", "internalType": "uint256"},
                {"name": "y", "type": "uint256", "internalType": "uint256"},
                {"name": "denominator", "type": "uint256", "internalType": "uint256"},
            ],
        },
        {"type": "error", "name": "PRBMath_SD59x18_Div_InputTooSmall", "inputs": []},
        {
            "type": "error",
            "name": "PRBMath_SD59x18_Div_Overflow",
            "inputs": [
                {"name": "x", "type": "int256", "internalType": "SD59x18"},
                {"name": "y", "type": "int256", "internalType": "SD59x18"},
            ],
        },
        {
            "type": "error",
            "name": "PRBMath_SD59x18_Exp2_InputTooBig",
            "inputs": [{"name": "x", "type": "int256", "internalType": "SD59x18"}],
        },
        {
            "type": "error",
            "name": "PRBMath_SD59x18_Exp_InputTooBig",
            "inputs": [{"name": "x", "type": "int256", "internalType": "SD59x18"}],
        },
        {"type": "error", "name": "PRBMath_SD59x18_Mul_InputTooSmall", "inputs": []},
        {
            "type": "error",
            "name": "PRBMath_SD59x18_Mul_Overflow",
            "inputs": [
                {"name": "x", "type": "int256", "internalType": "SD59x18"},
                {"name": "y", "type": "int256", "internalType": "SD59x18"},
            ],
        },
        {
            "type": "error",
            "name": "SafeCastOverflowedUintToInt",
            "inputs": [{"name": "value", "type": "uint256", "internalType": "uint256"}],
        },
        {
            "type": "error",
            "name": "Unauthorized",
            "inputs": [
                {"name": "account", "type": "address", "internalType": "address"}
            ],
        },
        {
            "type": "error",
            "name": "UnauthorizedTradeSubmitter",
            "inputs": [
                {"name": "needed", "type": "address", "internalType": "address"},
                {"name": "got", "type": "address", "internalType": "address"},
            ],
        },
    ],
)
