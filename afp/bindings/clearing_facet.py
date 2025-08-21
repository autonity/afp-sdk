"""ClearingFacet contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import enum
import typing
from dataclasses import dataclass

import eth_typing
import hexbytes
import web3
from web3.contract import contract


class Side(enum.IntEnum):
    """Port of `enum Side` on the ClearingFacet contract."""

    BID = 0
    ASK = 1


@dataclass
class AuctionConfig:
    """Port of `struct AuctionConfig` on the IAuctioneer contract."""

    restoration_buffer: int
    liquidation_duration: int


@dataclass
class ClearingConfig:
    """Port of `struct ClearingConfig` on the IClearing contract."""

    clearing_fee_rate: int


@dataclass
class Config:
    """Port of `struct Config` on the IClearing contract."""

    auction_config: AuctionConfig
    clearing_config: ClearingConfig


@dataclass
class IntentData:
    """Port of `struct IntentData` on the IClearing contract."""

    nonce: int
    trading_protocol_id: eth_typing.ChecksumAddress
    product_id: hexbytes.HexBytes
    limit_price: int
    quantity: int
    max_trading_fee_rate: int
    good_until: int
    side: Side


@dataclass
class Intent:
    """Port of `struct Intent` on the IClearing contract."""

    margin_account_id: eth_typing.ChecksumAddress
    intent_account_id: eth_typing.ChecksumAddress
    hash: hexbytes.HexBytes
    data: IntentData
    signature: hexbytes.HexBytes


@dataclass
class Trade:
    """Port of `struct Trade` on the IClearing contract."""

    product_id: hexbytes.HexBytes
    protocol_id: eth_typing.ChecksumAddress
    trade_id: int
    price: int
    timestamp: int
    accounts: typing.List[eth_typing.ChecksumAddress]
    quantities: typing.List[int]
    fee_rates: typing.List[int]
    intents: typing.List[Intent]


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
    def TradeExecuted(self) -> contract.ContractEvent:
        """Binding for `event TradeExecuted` on the ClearingFacet contract."""
        return self._contract.events.TradeExecuted

    def max_trading_fee_rate(
        self,
    ) -> int:
        """Binding for `MAX_TRADING_FEE_RATE` on the ClearingFacet contract.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.MAX_TRADING_FEE_RATE().call()
        return int(return_value)

    def clearing_fee_rate(
        self,
    ) -> int:
        """Binding for `clearingFeeRate` on the ClearingFacet contract.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.clearingFeeRate().call()
        return int(return_value)

    def config(
        self,
    ) -> Config:
        """Binding for `config` on the ClearingFacet contract.

        Returns
        -------
        Config
        """
        return_value = self._contract.functions.config().call()
        return Config(
            AuctionConfig(int(return_value[0][0]), int(return_value[0][1])),
            ClearingConfig(int(return_value[1][0])),
        )

    def estimate_fees(
        self,
        product_id: hexbytes.HexBytes,
        price: int,
        quantity: int,
        trading_fee_rate: int,
    ) -> typing.Tuple[int, int]:
        """Binding for `estimateFees` on the ClearingFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        price : int
        quantity : int
        trading_fee_rate : int

        Returns
        -------
        int
        int
        """
        return_value = self._contract.functions.estimateFees(
            product_id,
            price,
            quantity,
            trading_fee_rate,
        ).call()
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
                        ),
                        trade_item.signature,
                    )
                    for trade_item in trade.intents
                ],
            ),
            fallback_on_failure,
        )

    def finalize_initialization(
        self,
        margin_account_registry: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `finalizeInitialization` on the ClearingFacet contract.

        Parameters
        ----------
        margin_account_registry : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.finalizeInitialization(
            margin_account_registry,
        )

    def get_admin(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `getAdmin` on the ClearingFacet contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.getAdmin().call()
        return eth_typing.ChecksumAddress(return_value)

    def get_margin_account_registry(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `getMarginAccountRegistry` on the ClearingFacet contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.getMarginAccountRegistry().call()
        return eth_typing.ChecksumAddress(return_value)

    def get_product_registry(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `getProductRegistry` on the ClearingFacet contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.getProductRegistry().call()
        return eth_typing.ChecksumAddress(return_value)

    def get_treasury(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `getTreasury` on the ClearingFacet contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.getTreasury().call()
        return eth_typing.ChecksumAddress(return_value)

    def hash_intent(
        self,
        intent: Intent,
    ) -> hexbytes.HexBytes:
        """Binding for `hashIntent` on the ClearingFacet contract.

        Parameters
        ----------
        intent : Intent

        Returns
        -------
        hexbytes.HexBytes
        """
        return_value = self._contract.functions.hashIntent(
            (
                intent.margin_account_id,
                intent.intent_account_id,
                intent.hash,
                (
                    intent.data.nonce,
                    intent.data.trading_protocol_id,
                    intent.data.product_id,
                    intent.data.limit_price,
                    intent.data.quantity,
                    intent.data.max_trading_fee_rate,
                    intent.data.good_until,
                    int(intent.data.side),
                ),
                intent.signature,
            ),
        ).call()
        return hexbytes.HexBytes(return_value)

    def initialize(
        self,
        _product_registry: eth_typing.ChecksumAddress,
        _treasury: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `initialize` on the ClearingFacet contract.

        Parameters
        ----------
        _product_registry : eth_typing.ChecksumAddress
        _treasury : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.initialize(
            _product_registry,
            _treasury,
        )

    def is_admin_active(
        self,
    ) -> bool:
        """Binding for `isAdminActive` on the ClearingFacet contract.

        Returns
        -------
        bool
        """
        return_value = self._contract.functions.isAdminActive().call()
        return bool(return_value)

    def set_active(
        self,
        active: bool,
    ) -> contract.ContractFunction:
        """Binding for `setActive` on the ClearingFacet contract.

        Parameters
        ----------
        active : bool

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.setActive(
            active,
        )

    def set_admin(
        self,
        new_admin: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `setAdmin` on the ClearingFacet contract.

        Parameters
        ----------
        new_admin : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.setAdmin(
            new_admin,
        )

    def set_config(
        self,
        _config: Config,
    ) -> contract.ContractFunction:
        """Binding for `setConfig` on the ClearingFacet contract.

        Parameters
        ----------
        _config : Config

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.setConfig(
            (
                (
                    _config.auction_config.restoration_buffer,
                    _config.auction_config.liquidation_duration,
                ),
                (_config.clearing_config.clearing_fee_rate),
            ),
        )

    def version(
        self,
    ) -> str:
        """Binding for `version` on the ClearingFacet contract.

        Returns
        -------
        str
        """
        return_value = self._contract.functions.version().call()
        return str(return_value)


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "inputs": [
                {"internalType": "bytes4", "name": "selector", "type": "bytes4"},
                {"internalType": "address", "name": "sender", "type": "address"},
            ],
            "name": "AdminControlledNotAuthorized",
            "type": "error",
        },
        {"inputs": [], "name": "AlreadyInitialized", "type": "error"},
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"}
            ],
            "name": "DuplicateMarginAccount",
            "type": "error",
        },
        {"inputs": [], "name": "ECDSAInvalidSignature", "type": "error"},
        {
            "inputs": [
                {"internalType": "uint256", "name": "length", "type": "uint256"}
            ],
            "name": "ECDSAInvalidSignatureLength",
            "type": "error",
        },
        {
            "inputs": [{"internalType": "bytes32", "name": "s", "type": "bytes32"}],
            "name": "ECDSAInvalidSignatureS",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "intentAccount", "type": "address"}
            ],
            "name": "IntentFullySpent",
            "type": "error",
        },
        {
            "inputs": [{"internalType": "int256", "name": "feeSum", "type": "int256"}],
            "name": "InvalidFeeSum",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "string", "name": "parameter", "type": "string"}
            ],
            "name": "InvalidIntent",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "string", "name": "paramName", "type": "string"}
            ],
            "name": "InvalidParameter",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "enum ProductState", "name": "state", "type": "uint8"}
            ],
            "name": "InvalidProductState",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "signer", "type": "address"},
                {
                    "internalType": "address",
                    "name": "expectedSigner",
                    "type": "address",
                },
            ],
            "name": "InvalidSignature",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "length", "type": "uint256"}
            ],
            "name": "InvalidTradeIntents",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"}
            ],
            "name": "MAECheckFailed",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "int256", "name": "feeRate", "type": "int256"},
                {"internalType": "uint256", "name": "maxFeeRate", "type": "uint256"},
            ],
            "name": "MaxFeeRateExceeded",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "buySide", "type": "uint256"},
                {"internalType": "uint256", "name": "sellSide", "type": "uint256"},
            ],
            "name": "MismatchedTrade",
            "type": "error",
        },
        {"inputs": [], "name": "QueueIsEmpty", "type": "error"},
        {
            "inputs": [
                {"internalType": "address", "name": "account", "type": "address"}
            ],
            "name": "Unauthorized",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "needed", "type": "address"},
                {"internalType": "address", "name": "got", "type": "address"},
            ],
            "name": "UnauthorizedTradeSubmitter",
            "type": "error",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "bytes32",
                    "name": "productID",
                    "type": "bytes32",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "protocolID",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "marginAccount",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "price",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "quantity",
                    "type": "uint256",
                },
            ],
            "name": "TradeExecuted",
            "type": "event",
        },
        {
            "inputs": [],
            "name": "MAX_TRADING_FEE_RATE",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "pure",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "clearingFeeRate",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "config",
            "outputs": [
                {
                    "components": [
                        {
                            "components": [
                                {
                                    "internalType": "uint64",
                                    "name": "restorationBuffer",
                                    "type": "uint64",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "liquidationDuration",
                                    "type": "uint256",
                                },
                            ],
                            "internalType": "struct IAuctioneer.AuctionConfig",
                            "name": "auctionConfig",
                            "type": "tuple",
                        },
                        {
                            "components": [
                                {
                                    "internalType": "uint32",
                                    "name": "clearingFeeRate",
                                    "type": "uint32",
                                }
                            ],
                            "internalType": "struct IClearing.ClearingConfig",
                            "name": "clearingConfig",
                            "type": "tuple",
                        },
                    ],
                    "internalType": "struct IClearing.Config",
                    "name": "",
                    "type": "tuple",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productID", "type": "bytes32"},
                {"internalType": "uint256", "name": "price", "type": "uint256"},
                {"internalType": "uint256", "name": "quantity", "type": "uint256"},
                {"internalType": "int256", "name": "tradingFeeRate", "type": "int256"},
            ],
            "name": "estimateFees",
            "outputs": [
                {"internalType": "uint256", "name": "clearingFee", "type": "uint256"},
                {"internalType": "int256", "name": "tradingFee", "type": "int256"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "components": [
                        {
                            "internalType": "bytes32",
                            "name": "productID",
                            "type": "bytes32",
                        },
                        {
                            "internalType": "address",
                            "name": "protocolID",
                            "type": "address",
                        },
                        {
                            "internalType": "uint256",
                            "name": "tradeID",
                            "type": "uint256",
                        },
                        {"internalType": "uint256", "name": "price", "type": "uint256"},
                        {
                            "internalType": "uint256",
                            "name": "timestamp",
                            "type": "uint256",
                        },
                        {
                            "internalType": "address[]",
                            "name": "accounts",
                            "type": "address[]",
                        },
                        {
                            "internalType": "uint256[]",
                            "name": "quantities",
                            "type": "uint256[]",
                        },
                        {
                            "internalType": "int256[]",
                            "name": "feeRates",
                            "type": "int256[]",
                        },
                        {
                            "components": [
                                {
                                    "internalType": "address",
                                    "name": "marginAccountID",
                                    "type": "address",
                                },
                                {
                                    "internalType": "address",
                                    "name": "intentAccountID",
                                    "type": "address",
                                },
                                {
                                    "internalType": "bytes32",
                                    "name": "hash",
                                    "type": "bytes32",
                                },
                                {
                                    "components": [
                                        {
                                            "internalType": "uint256",
                                            "name": "nonce",
                                            "type": "uint256",
                                        },
                                        {
                                            "internalType": "address",
                                            "name": "tradingProtocolID",
                                            "type": "address",
                                        },
                                        {
                                            "internalType": "bytes32",
                                            "name": "productID",
                                            "type": "bytes32",
                                        },
                                        {
                                            "internalType": "uint256",
                                            "name": "limitPrice",
                                            "type": "uint256",
                                        },
                                        {
                                            "internalType": "uint256",
                                            "name": "quantity",
                                            "type": "uint256",
                                        },
                                        {
                                            "internalType": "uint256",
                                            "name": "maxTradingFeeRate",
                                            "type": "uint256",
                                        },
                                        {
                                            "internalType": "uint256",
                                            "name": "goodUntil",
                                            "type": "uint256",
                                        },
                                        {
                                            "internalType": "enum Side",
                                            "name": "side",
                                            "type": "uint8",
                                        },
                                    ],
                                    "internalType": "struct IClearing.IntentData",
                                    "name": "data",
                                    "type": "tuple",
                                },
                                {
                                    "internalType": "bytes",
                                    "name": "signature",
                                    "type": "bytes",
                                },
                            ],
                            "internalType": "struct IClearing.Intent[]",
                            "name": "intents",
                            "type": "tuple[]",
                        },
                    ],
                    "internalType": "struct IClearing.Trade",
                    "name": "trade",
                    "type": "tuple",
                },
                {"internalType": "bool", "name": "fallbackOnFailure", "type": "bool"},
            ],
            "name": "execute",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountRegistry",
                    "type": "address",
                }
            ],
            "name": "finalizeInitialization",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getAdmin",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getMarginAccountRegistry",
            "outputs": [
                {
                    "internalType": "contract IMarginAccountRegistry",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getProductRegistry",
            "outputs": [
                {
                    "internalType": "contract IProductRegistry",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getTreasury",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "components": [
                        {
                            "internalType": "address",
                            "name": "marginAccountID",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "intentAccountID",
                            "type": "address",
                        },
                        {"internalType": "bytes32", "name": "hash", "type": "bytes32"},
                        {
                            "components": [
                                {
                                    "internalType": "uint256",
                                    "name": "nonce",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "address",
                                    "name": "tradingProtocolID",
                                    "type": "address",
                                },
                                {
                                    "internalType": "bytes32",
                                    "name": "productID",
                                    "type": "bytes32",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "limitPrice",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "quantity",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "maxTradingFeeRate",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "goodUntil",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "enum Side",
                                    "name": "side",
                                    "type": "uint8",
                                },
                            ],
                            "internalType": "struct IClearing.IntentData",
                            "name": "data",
                            "type": "tuple",
                        },
                        {"internalType": "bytes", "name": "signature", "type": "bytes"},
                    ],
                    "internalType": "struct IClearing.Intent",
                    "name": "intent",
                    "type": "tuple",
                }
            ],
            "name": "hashIntent",
            "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "stateMutability": "pure",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_productRegistry",
                    "type": "address",
                },
                {"internalType": "address", "name": "_treasury", "type": "address"},
            ],
            "name": "initialize",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "isAdminActive",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "bool", "name": "active", "type": "bool"}],
            "name": "setActive",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "newAdmin", "type": "address"}
            ],
            "name": "setAdmin",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "components": [
                        {
                            "components": [
                                {
                                    "internalType": "uint64",
                                    "name": "restorationBuffer",
                                    "type": "uint64",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "liquidationDuration",
                                    "type": "uint256",
                                },
                            ],
                            "internalType": "struct IAuctioneer.AuctionConfig",
                            "name": "auctionConfig",
                            "type": "tuple",
                        },
                        {
                            "components": [
                                {
                                    "internalType": "uint32",
                                    "name": "clearingFeeRate",
                                    "type": "uint32",
                                }
                            ],
                            "internalType": "struct IClearing.ClearingConfig",
                            "name": "clearingConfig",
                            "type": "tuple",
                        },
                    ],
                    "internalType": "struct IClearing.Config",
                    "name": "_config",
                    "type": "tuple",
                }
            ],
            "name": "setConfig",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "version",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "pure",
            "type": "function",
        },
    ],
)
