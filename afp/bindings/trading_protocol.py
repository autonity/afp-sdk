"""TradingProtocol contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import enum
import typing
from dataclasses import dataclass

import eth_typing
import hexbytes
import web3
from web3.contract import contract


class Side(enum.IntEnum):
    """Port of `enum Side` on the TradingProtocol contract."""

    BID = 0
    ASK = 1


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


class TradingProtocol:
    """TradingProtocol contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed TradingProtocol contract.
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
    def Initialized(self) -> contract.ContractEvent:
        """Binding for `event Initialized` on the TradingProtocol contract."""
        return self._contract.events.Initialized

    @property
    def RoleAdminChanged(self) -> contract.ContractEvent:
        """Binding for `event RoleAdminChanged` on the TradingProtocol contract."""
        return self._contract.events.RoleAdminChanged

    @property
    def RoleGranted(self) -> contract.ContractEvent:
        """Binding for `event RoleGranted` on the TradingProtocol contract."""
        return self._contract.events.RoleGranted

    @property
    def RoleRevoked(self) -> contract.ContractEvent:
        """Binding for `event RoleRevoked` on the TradingProtocol contract."""
        return self._contract.events.RoleRevoked

    @property
    def Upgraded(self) -> contract.ContractEvent:
        """Binding for `event Upgraded` on the TradingProtocol contract."""
        return self._contract.events.Upgraded

    def default_admin_role(
        self,
    ) -> hexbytes.HexBytes:
        """Binding for `DEFAULT_ADMIN_ROLE` on the TradingProtocol contract.

        Returns
        -------
        hexbytes.HexBytes
        """
        return_value = self._contract.functions.DEFAULT_ADMIN_ROLE().call()
        return hexbytes.HexBytes(return_value)

    def trade_submitter_role(
        self,
    ) -> hexbytes.HexBytes:
        """Binding for `TRADE_SUBMITTER_ROLE` on the TradingProtocol contract.

        Returns
        -------
        hexbytes.HexBytes
        """
        return_value = self._contract.functions.TRADE_SUBMITTER_ROLE().call()
        return hexbytes.HexBytes(return_value)

    def upgrade_interface_version(
        self,
    ) -> str:
        """Binding for `UPGRADE_INTERFACE_VERSION` on the TradingProtocol contract.

        Returns
        -------
        str
        """
        return_value = self._contract.functions.UPGRADE_INTERFACE_VERSION().call()
        return str(return_value)

    def add_trade_submitter(
        self,
        submitter: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `addTradeSubmitter` on the TradingProtocol contract.

        Parameters
        ----------
        submitter : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.addTradeSubmitter(
            submitter,
        )

    def change_owner(
        self,
        new_owner: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `changeOwner` on the TradingProtocol contract.

        Parameters
        ----------
        new_owner : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.changeOwner(
            new_owner,
        )

    def deposit(
        self,
        margin_account_contract: eth_typing.ChecksumAddress,
        amount: int,
    ) -> contract.ContractFunction:
        """Binding for `deposit` on the TradingProtocol contract.

        Parameters
        ----------
        margin_account_contract : eth_typing.ChecksumAddress
        amount : int

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.deposit(
            margin_account_contract,
            amount,
        )

    def execute(
        self,
        trade: Trade,
        fallback_on_failure: bool,
    ) -> contract.ContractFunction:
        """Binding for `execute` on the TradingProtocol contract.

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

    def execute_sequence(
        self,
        trades: typing.List[Trade],
        fallback_on_failure: bool,
    ) -> contract.ContractFunction:
        """Binding for `executeSequence` on the TradingProtocol contract.

        Parameters
        ----------
        trades : typing.List[Trade]
        fallback_on_failure : bool

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.executeSequence(
            [
                (
                    item.product_id,
                    item.protocol_id,
                    item.trade_id,
                    item.price,
                    item.timestamp,
                    item.accounts,
                    item.quantities,
                    item.fee_rates,
                    [
                        (
                            item_item.margin_account_id,
                            item_item.intent_account_id,
                            item_item.hash,
                            (
                                item_item.data.nonce,
                                item_item.data.trading_protocol_id,
                                item_item.data.product_id,
                                item_item.data.limit_price,
                                item_item.data.quantity,
                                item_item.data.max_trading_fee_rate,
                                item_item.data.good_until,
                                int(item_item.data.side),
                            ),
                            item_item.signature,
                        )
                        for item_item in item.intents
                    ],
                )
                for item in trades
            ],
            fallback_on_failure,
        )

    def get_role_admin(
        self,
        role: hexbytes.HexBytes,
    ) -> hexbytes.HexBytes:
        """Binding for `getRoleAdmin` on the TradingProtocol contract.

        Parameters
        ----------
        role : hexbytes.HexBytes

        Returns
        -------
        hexbytes.HexBytes
        """
        return_value = self._contract.functions.getRoleAdmin(
            role,
        ).call()
        return hexbytes.HexBytes(return_value)

    def get_role_member(
        self,
        role: hexbytes.HexBytes,
        index: int,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `getRoleMember` on the TradingProtocol contract.

        Parameters
        ----------
        role : hexbytes.HexBytes
        index : int

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.getRoleMember(
            role,
            index,
        ).call()
        return eth_typing.ChecksumAddress(return_value)

    def get_role_member_count(
        self,
        role: hexbytes.HexBytes,
    ) -> int:
        """Binding for `getRoleMemberCount` on the TradingProtocol contract.

        Parameters
        ----------
        role : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.getRoleMemberCount(
            role,
        ).call()
        return int(return_value)

    def get_role_members(
        self,
        role: hexbytes.HexBytes,
    ) -> typing.List[eth_typing.ChecksumAddress]:
        """Binding for `getRoleMembers` on the TradingProtocol contract.

        Parameters
        ----------
        role : hexbytes.HexBytes

        Returns
        -------
        typing.List[eth_typing.ChecksumAddress]
        """
        return_value = self._contract.functions.getRoleMembers(
            role,
        ).call()
        return [
            eth_typing.ChecksumAddress(return_value_elem)
            for return_value_elem in return_value
        ]

    def grant_role(
        self,
        role: hexbytes.HexBytes,
        account: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `grantRole` on the TradingProtocol contract.

        Parameters
        ----------
        role : hexbytes.HexBytes
        account : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.grantRole(
            role,
            account,
        )

    def has_role(
        self,
        role: hexbytes.HexBytes,
        account: eth_typing.ChecksumAddress,
    ) -> bool:
        """Binding for `hasRole` on the TradingProtocol contract.

        Parameters
        ----------
        role : hexbytes.HexBytes
        account : eth_typing.ChecksumAddress

        Returns
        -------
        bool
        """
        return_value = self._contract.functions.hasRole(
            role,
            account,
        ).call()
        return bool(return_value)

    def initialize(
        self,
        clearing_address: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `initialize` on the TradingProtocol contract.

        Parameters
        ----------
        clearing_address : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.initialize(
            clearing_address,
        )

    def proxiable_uuid(
        self,
    ) -> hexbytes.HexBytes:
        """Binding for `proxiableUUID` on the TradingProtocol contract.

        Returns
        -------
        hexbytes.HexBytes
        """
        return_value = self._contract.functions.proxiableUUID().call()
        return hexbytes.HexBytes(return_value)

    def remove_trade_submitter(
        self,
        submitter: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `removeTradeSubmitter` on the TradingProtocol contract.

        Parameters
        ----------
        submitter : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.removeTradeSubmitter(
            submitter,
        )

    def renounce_role(
        self,
        role: hexbytes.HexBytes,
        caller_confirmation: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `renounceRole` on the TradingProtocol contract.

        Parameters
        ----------
        role : hexbytes.HexBytes
        caller_confirmation : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.renounceRole(
            role,
            caller_confirmation,
        )

    def revoke_role(
        self,
        role: hexbytes.HexBytes,
        account: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `revokeRole` on the TradingProtocol contract.

        Parameters
        ----------
        role : hexbytes.HexBytes
        account : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.revokeRole(
            role,
            account,
        )

    def supports_interface(
        self,
        interface_id: hexbytes.HexBytes,
    ) -> bool:
        """Binding for `supportsInterface` on the TradingProtocol contract.

        Parameters
        ----------
        interface_id : hexbytes.HexBytes

        Returns
        -------
        bool
        """
        return_value = self._contract.functions.supportsInterface(
            interface_id,
        ).call()
        return bool(return_value)

    def upgrade_to_and_call(
        self,
        new_implementation: eth_typing.ChecksumAddress,
        data: hexbytes.HexBytes,
    ) -> contract.ContractFunction:
        """Binding for `upgradeToAndCall` on the TradingProtocol contract.

        Parameters
        ----------
        new_implementation : eth_typing.ChecksumAddress
        data : hexbytes.HexBytes

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.upgradeToAndCall(
            new_implementation,
            data,
        )

    def withdraw(
        self,
        margin_account_contract: eth_typing.ChecksumAddress,
        amount: int,
    ) -> contract.ContractFunction:
        """Binding for `withdraw` on the TradingProtocol contract.

        Parameters
        ----------
        margin_account_contract : eth_typing.ChecksumAddress
        amount : int

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.withdraw(
            margin_account_contract,
            amount,
        )


ABI = typing.cast(
    eth_typing.ABI,
    [
        {"inputs": [], "name": "AccessControlBadConfirmation", "type": "error"},
        {
            "inputs": [
                {"internalType": "address", "name": "account", "type": "address"},
                {"internalType": "bytes32", "name": "neededRole", "type": "bytes32"},
            ],
            "name": "AccessControlUnauthorizedAccount",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "target", "type": "address"}
            ],
            "name": "AddressEmptyCode",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "implementation", "type": "address"}
            ],
            "name": "ERC1967InvalidImplementation",
            "type": "error",
        },
        {"inputs": [], "name": "ERC1967NonPayable", "type": "error"},
        {"inputs": [], "name": "FailedCall", "type": "error"},
        {"inputs": [], "name": "InvalidInitialization", "type": "error"},
        {"inputs": [], "name": "NotInitializing", "type": "error"},
        {
            "inputs": [{"internalType": "address", "name": "token", "type": "address"}],
            "name": "SafeERC20FailedOperation",
            "type": "error",
        },
        {"inputs": [], "name": "UUPSUnauthorizedCallContext", "type": "error"},
        {
            "inputs": [{"internalType": "bytes32", "name": "slot", "type": "bytes32"}],
            "name": "UUPSUnsupportedProxiableUUID",
            "type": "error",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "uint64",
                    "name": "version",
                    "type": "uint64",
                }
            ],
            "name": "Initialized",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "bytes32",
                    "name": "role",
                    "type": "bytes32",
                },
                {
                    "indexed": True,
                    "internalType": "bytes32",
                    "name": "previousAdminRole",
                    "type": "bytes32",
                },
                {
                    "indexed": True,
                    "internalType": "bytes32",
                    "name": "newAdminRole",
                    "type": "bytes32",
                },
            ],
            "name": "RoleAdminChanged",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "bytes32",
                    "name": "role",
                    "type": "bytes32",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "account",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "sender",
                    "type": "address",
                },
            ],
            "name": "RoleGranted",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "bytes32",
                    "name": "role",
                    "type": "bytes32",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "account",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "sender",
                    "type": "address",
                },
            ],
            "name": "RoleRevoked",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "implementation",
                    "type": "address",
                }
            ],
            "name": "Upgraded",
            "type": "event",
        },
        {
            "inputs": [],
            "name": "DEFAULT_ADMIN_ROLE",
            "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "TRADE_SUBMITTER_ROLE",
            "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "UPGRADE_INTERFACE_VERSION",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "submitter", "type": "address"}
            ],
            "name": "addTradeSubmitter",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "newOwner", "type": "address"}
            ],
            "name": "changeOwner",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountContract",
                    "type": "address",
                },
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
            ],
            "name": "deposit",
            "outputs": [],
            "stateMutability": "nonpayable",
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
                    "internalType": "struct IClearing.Trade[]",
                    "name": "trades",
                    "type": "tuple[]",
                },
                {"internalType": "bool", "name": "fallbackOnFailure", "type": "bool"},
            ],
            "name": "executeSequence",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "bytes32", "name": "role", "type": "bytes32"}],
            "name": "getRoleAdmin",
            "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                {"internalType": "uint256", "name": "index", "type": "uint256"},
            ],
            "name": "getRoleMember",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "bytes32", "name": "role", "type": "bytes32"}],
            "name": "getRoleMemberCount",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "bytes32", "name": "role", "type": "bytes32"}],
            "name": "getRoleMembers",
            "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                {"internalType": "address", "name": "account", "type": "address"},
            ],
            "name": "grantRole",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                {"internalType": "address", "name": "account", "type": "address"},
            ],
            "name": "hasRole",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "clearingAddress",
                    "type": "address",
                }
            ],
            "name": "initialize",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "proxiableUUID",
            "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "submitter", "type": "address"}
            ],
            "name": "removeTradeSubmitter",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                {
                    "internalType": "address",
                    "name": "callerConfirmation",
                    "type": "address",
                },
            ],
            "name": "renounceRole",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                {"internalType": "address", "name": "account", "type": "address"},
            ],
            "name": "revokeRole",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}
            ],
            "name": "supportsInterface",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "newImplementation",
                    "type": "address",
                },
                {"internalType": "bytes", "name": "data", "type": "bytes"},
            ],
            "name": "upgradeToAndCall",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountContract",
                    "type": "address",
                },
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
            ],
            "name": "withdraw",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ],
)
