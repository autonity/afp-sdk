"""MarginAccount contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing
from dataclasses import dataclass

import eth_typing
import hexbytes
import web3
from web3.contract import contract


@dataclass
class Settlement:
    """Port of `struct Settlement` on the IMarginAccount contract."""

    position_id: hexbytes.HexBytes
    quantity: int
    price: int


@dataclass
class PositionData:
    """Port of `struct PositionData` on the IMarginAccount contract."""

    position_id: hexbytes.HexBytes
    quantity: int
    cost_basis: int
    maintenance_margin: int
    pnl: int


class MarginAccount:
    """MarginAccount contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed MarginAccount contract.
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
        """Binding for `event FeeCollected` on the MarginAccount contract."""
        return self._contract.events.FeeCollected

    @property
    def FeeDispersed(self) -> contract.ContractEvent:
        """Binding for `event FeeDispersed` on the MarginAccount contract."""
        return self._contract.events.FeeDispersed

    @property
    def Initialized(self) -> contract.ContractEvent:
        """Binding for `event Initialized` on the MarginAccount contract."""
        return self._contract.events.Initialized

    @property
    def PositionUpdated(self) -> contract.ContractEvent:
        """Binding for `event PositionUpdated` on the MarginAccount contract."""
        return self._contract.events.PositionUpdated

    def authorize(
        self,
        intent_account: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `authorize` on the MarginAccount contract.

        Parameters
        ----------
        intent_account : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.authorize(
            intent_account,
        )

    def authorized(
        self,
        margin_account: eth_typing.ChecksumAddress,
        intent_account: eth_typing.ChecksumAddress,
    ) -> bool:
        """Binding for `authorized` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress
        intent_account : eth_typing.ChecksumAddress

        Returns
        -------
        bool
        """
        return_value = self._contract.functions.authorized(
            margin_account,
            intent_account,
        ).call()
        return bool(return_value)

    def batch_mae_check(
        self,
        margin_account: eth_typing.ChecksumAddress,
        settlements: typing.List[Settlement],
        mark_price_if_settled: typing.List[int],
    ) -> typing.Tuple[bool, int, int]:
        """Binding for `batchMaeCheck` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress
        settlements : typing.List[Settlement]
        mark_price_if_settled : typing.List[int]

        Returns
        -------
        bool
        int
        int
        """
        return_value = self._contract.functions.batchMaeCheck(
            margin_account,
            [(item.position_id, item.quantity, item.price) for item in settlements],
            mark_price_if_settled,
        ).call()
        return (
            bool(return_value[0]),
            int(return_value[1]),
            int(return_value[2]),
        )

    def batch_settle(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        settlements: typing.List[Settlement],
    ) -> contract.ContractFunction:
        """Binding for `batchSettle` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        settlements : typing.List[Settlement]

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.batchSettle(
            margin_account_id,
            [(item.position_id, item.quantity, item.price) for item in settlements],
        )

    def capital(
        self,
        margin_account: eth_typing.ChecksumAddress,
    ) -> int:
        """Binding for `capital` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress

        Returns
        -------
        int
        """
        return_value = self._contract.functions.capital(
            margin_account,
        ).call()
        return int(return_value)

    def clearing(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `clearing` on the MarginAccount contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.clearing().call()
        return eth_typing.ChecksumAddress(return_value)

    def collateral_asset(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `collateralAsset` on the MarginAccount contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.collateralAsset().call()
        return eth_typing.ChecksumAddress(return_value)

    def collateral_token(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `collateralToken` on the MarginAccount contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.collateralToken().call()
        return eth_typing.ChecksumAddress(return_value)

    def collect_fee(
        self,
        margin_account: eth_typing.ChecksumAddress,
        capital_amount: int,
    ) -> contract.ContractFunction:
        """Binding for `collectFee` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress
        capital_amount : int

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.collectFee(
            margin_account,
            capital_amount,
        )

    def deposit(
        self,
        amount: int,
    ) -> contract.ContractFunction:
        """Binding for `deposit` on the MarginAccount contract.

        Parameters
        ----------
        amount : int

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.deposit(
            amount,
        )

    def disperse_fees(
        self,
        recipients: typing.List[eth_typing.ChecksumAddress],
        capital_amounts: typing.List[int],
    ) -> contract.ContractFunction:
        """Binding for `disperseFees` on the MarginAccount contract.

        Parameters
        ----------
        recipients : typing.List[eth_typing.ChecksumAddress]
        capital_amounts : typing.List[int]

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.disperseFees(
            recipients,
            capital_amounts,
        )

    def estimate_liquidation_price(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        product_id: hexbytes.HexBytes,
        price: int,
        quantity: int,
    ) -> int:
        """Binding for `estimateLiquidationPrice` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        product_id : hexbytes.HexBytes
        price : int
        quantity : int

        Returns
        -------
        int
        """
        return_value = self._contract.functions.estimateLiquidationPrice(
            margin_account_id,
            product_id,
            price,
            quantity,
        ).call()
        return int(return_value)

    def estimate_liquidation_price_for_position(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        position_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `estimateLiquidationPriceForPosition` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        position_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.estimateLiquidationPriceForPosition(
            margin_account_id,
            position_id,
        ).call()
        return int(return_value)

    def initialize(
        self,
        _collateral_token: eth_typing.ChecksumAddress,
        _valuation: eth_typing.ChecksumAddress,
        _product_registry: eth_typing.ChecksumAddress,
        _clearing: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `initialize` on the MarginAccount contract.

        Parameters
        ----------
        _collateral_token : eth_typing.ChecksumAddress
        _valuation : eth_typing.ChecksumAddress
        _product_registry : eth_typing.ChecksumAddress
        _clearing : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.initialize(
            _collateral_token,
            _valuation,
            _product_registry,
            _clearing,
        )

    def mae(
        self,
        margin_account: eth_typing.ChecksumAddress,
    ) -> int:
        """Binding for `mae` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress

        Returns
        -------
        int
        """
        return_value = self._contract.functions.mae(
            margin_account,
        ).call()
        return int(return_value)

    def mae_and_mmu_after_batch_trade(
        self,
        margin_account: eth_typing.ChecksumAddress,
        settlements: typing.List[Settlement],
        mark_price_if_settled: typing.List[int],
    ) -> typing.Tuple[int, int]:
        """Binding for `maeAndMmuAfterBatchTrade` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress
        settlements : typing.List[Settlement]
        mark_price_if_settled : typing.List[int]

        Returns
        -------
        int
        int
        """
        return_value = self._contract.functions.maeAndMmuAfterBatchTrade(
            margin_account,
            [(item.position_id, item.quantity, item.price) for item in settlements],
            mark_price_if_settled,
        ).call()
        return (
            int(return_value[0]),
            int(return_value[1]),
        )

    def mae_check(
        self,
        margin_account: eth_typing.ChecksumAddress,
        settlement: Settlement,
        mark_price_if_settled: int,
    ) -> typing.Tuple[bool, int, int]:
        """Binding for `maeCheck` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress
        settlement : Settlement
        mark_price_if_settled : int

        Returns
        -------
        bool
        int
        int
        """
        return_value = self._contract.functions.maeCheck(
            margin_account,
            (settlement.position_id, settlement.quantity, settlement.price),
            mark_price_if_settled,
        ).call()
        return (
            bool(return_value[0]),
            int(return_value[1]),
            int(return_value[2]),
        )

    def mma(
        self,
        margin_account: eth_typing.ChecksumAddress,
    ) -> int:
        """Binding for `mma` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress

        Returns
        -------
        int
        """
        return_value = self._contract.functions.mma(
            margin_account,
        ).call()
        return int(return_value)

    def mmu(
        self,
        margin_account: eth_typing.ChecksumAddress,
    ) -> int:
        """Binding for `mmu` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress

        Returns
        -------
        int
        """
        return_value = self._contract.functions.mmu(
            margin_account,
        ).call()
        return int(return_value)

    def pnl(
        self,
        margin_account: eth_typing.ChecksumAddress,
    ) -> int:
        """Binding for `pnl` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress

        Returns
        -------
        int
        """
        return_value = self._contract.functions.pnl(
            margin_account,
        ).call()
        return int(return_value)

    def position_age(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        position_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `positionAge` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        position_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.positionAge(
            margin_account_id,
            position_id,
        ).call()
        return int(return_value)

    def position_count(
        self,
        margin_account: eth_typing.ChecksumAddress,
    ) -> int:
        """Binding for `positionCount` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress

        Returns
        -------
        int
        """
        return_value = self._contract.functions.positionCount(
            margin_account,
        ).call()
        return int(return_value)

    def position_data(
        self,
        margin_account: eth_typing.ChecksumAddress,
        position_id: hexbytes.HexBytes,
    ) -> PositionData:
        """Binding for `positionData` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress
        position_id : hexbytes.HexBytes

        Returns
        -------
        PositionData
        """
        return_value = self._contract.functions.positionData(
            margin_account,
            position_id,
        ).call()
        return PositionData(
            hexbytes.HexBytes(return_value[0]),
            int(return_value[1]),
            int(return_value[2]),
            int(return_value[3]),
            int(return_value[4]),
        )

    def position_pn_l(
        self,
        margin_account: eth_typing.ChecksumAddress,
        position_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `positionPnL` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress
        position_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.positionPnL(
            margin_account,
            position_id,
        ).call()
        return int(return_value)

    def position_quantity(
        self,
        margin_account: eth_typing.ChecksumAddress,
        position_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `positionQuantity` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress
        position_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.positionQuantity(
            margin_account,
            position_id,
        ).call()
        return int(return_value)

    def positions(
        self,
        margin_account: eth_typing.ChecksumAddress,
    ) -> typing.List[hexbytes.HexBytes]:
        """Binding for `positions` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress

        Returns
        -------
        typing.List[hexbytes.HexBytes]
        """
        return_value = self._contract.functions.positions(
            margin_account,
        ).call()
        return [
            hexbytes.HexBytes(return_value_elem) for return_value_elem in return_value
        ]

    def product_registry(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `productRegistry` on the MarginAccount contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.productRegistry().call()
        return eth_typing.ChecksumAddress(return_value)

    def revoke_authorization(
        self,
        intent_account: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `revokeAuthorization` on the MarginAccount contract.

        Parameters
        ----------
        intent_account : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.revokeAuthorization(
            intent_account,
        )

    def settle(
        self,
        margin_account: eth_typing.ChecksumAddress,
        intent_account: eth_typing.ChecksumAddress,
        settlement: Settlement,
    ) -> contract.ContractFunction:
        """Binding for `settle` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress
        intent_account : eth_typing.ChecksumAddress
        settlement : Settlement

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.settle(
            margin_account,
            intent_account,
            (settlement.position_id, settlement.quantity, settlement.price),
        )

    def valuation(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `valuation` on the MarginAccount contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.valuation().call()
        return eth_typing.ChecksumAddress(return_value)

    def withdraw(
        self,
        amount: int,
    ) -> contract.ContractFunction:
        """Binding for `withdraw` on the MarginAccount contract.

        Parameters
        ----------
        amount : int

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.withdraw(
            amount,
        )

    def withdrawable(
        self,
        margin_account: eth_typing.ChecksumAddress,
    ) -> int:
        """Binding for `withdrawable` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress

        Returns
        -------
        int
        """
        return_value = self._contract.functions.withdrawable(
            margin_account,
        ).call()
        return int(return_value)


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "inputs": [
                {"internalType": "uint256", "name": "dispersed", "type": "uint256"},
                {"internalType": "int256", "name": "collected", "type": "int256"},
            ],
            "name": "FeeInvariantViolated",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "account", "type": "address"},
                {"internalType": "uint256", "name": "balance", "type": "uint256"},
                {"internalType": "uint256", "name": "required", "type": "uint256"},
            ],
            "name": "InsufficientBalance",
            "type": "error",
        },
        {"inputs": [], "name": "InvalidInitialization", "type": "error"},
        {
            "inputs": [
                {"internalType": "string", "name": "paramName", "type": "string"}
            ],
            "name": "InvalidParameter",
            "type": "error",
        },
        {"inputs": [], "name": "NotInitializing", "type": "error"},
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"},
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"},
            ],
            "name": "PositionNotFound",
            "type": "error",
        },
        {
            "inputs": [{"internalType": "address", "name": "token", "type": "address"}],
            "name": "SafeERC20FailedOperation",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "account", "type": "address"}
            ],
            "name": "Unauthorized",
            "type": "error",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "int256",
                    "name": "capitalAmount",
                    "type": "int256",
                },
            ],
            "name": "FeeCollected",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "recipient",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "capitalAmount",
                    "type": "uint256",
                },
            ],
            "name": "FeeDispersed",
            "type": "event",
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
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "bytes32",
                    "name": "positionId",
                    "type": "bytes32",
                },
                {
                    "indexed": False,
                    "internalType": "int256",
                    "name": "totalQuantity",
                    "type": "int256",
                },
                {
                    "indexed": False,
                    "internalType": "int256",
                    "name": "costBasis",
                    "type": "int256",
                },
            ],
            "name": "PositionUpdated",
            "type": "event",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "intentAccount", "type": "address"}
            ],
            "name": "authorize",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"},
                {"internalType": "address", "name": "intentAccount", "type": "address"},
            ],
            "name": "authorized",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"},
                {
                    "components": [
                        {
                            "internalType": "bytes32",
                            "name": "positionId",
                            "type": "bytes32",
                        },
                        {
                            "internalType": "int256",
                            "name": "quantity",
                            "type": "int256",
                        },
                        {"internalType": "uint256", "name": "price", "type": "uint256"},
                    ],
                    "internalType": "struct IMarginAccount.Settlement[]",
                    "name": "settlements",
                    "type": "tuple[]",
                },
                {
                    "internalType": "uint256[]",
                    "name": "markPriceIfSettled",
                    "type": "uint256[]",
                },
            ],
            "name": "batchMaeCheck",
            "outputs": [
                {"internalType": "bool", "name": "checkPassed", "type": "bool"},
                {"internalType": "int256", "name": "maeAfter", "type": "int256"},
                {"internalType": "uint256", "name": "mmuAfter", "type": "uint256"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {
                    "components": [
                        {
                            "internalType": "bytes32",
                            "name": "positionId",
                            "type": "bytes32",
                        },
                        {
                            "internalType": "int256",
                            "name": "quantity",
                            "type": "int256",
                        },
                        {"internalType": "uint256", "name": "price", "type": "uint256"},
                    ],
                    "internalType": "struct IMarginAccount.Settlement[]",
                    "name": "settlements",
                    "type": "tuple[]",
                },
            ],
            "name": "batchSettle",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"}
            ],
            "name": "capital",
            "outputs": [{"internalType": "int256", "name": "", "type": "int256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "clearing",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "collateralAsset",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "collateralToken",
            "outputs": [
                {"internalType": "contract IERC20", "name": "", "type": "address"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"},
                {"internalType": "int256", "name": "capitalAmount", "type": "int256"},
            ],
            "name": "collectFee",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "amount", "type": "uint256"}
            ],
            "name": "deposit",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address[]",
                    "name": "recipients",
                    "type": "address[]",
                },
                {
                    "internalType": "uint256[]",
                    "name": "capitalAmounts",
                    "type": "uint256[]",
                },
            ],
            "name": "disperseFees",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountId",
                    "type": "address",
                },
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"},
                {"internalType": "uint256", "name": "price", "type": "uint256"},
                {"internalType": "int256", "name": "quantity", "type": "int256"},
            ],
            "name": "estimateLiquidationPrice",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountId",
                    "type": "address",
                },
                {"internalType": "bytes32", "name": "positionId", "type": "bytes32"},
            ],
            "name": "estimateLiquidationPriceForPosition",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_collateralToken",
                    "type": "address",
                },
                {"internalType": "address", "name": "_valuation", "type": "address"},
                {
                    "internalType": "address",
                    "name": "_productRegistry",
                    "type": "address",
                },
                {"internalType": "address", "name": "_clearing", "type": "address"},
            ],
            "name": "initialize",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"}
            ],
            "name": "mae",
            "outputs": [{"internalType": "int256", "name": "", "type": "int256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"},
                {
                    "components": [
                        {
                            "internalType": "bytes32",
                            "name": "positionId",
                            "type": "bytes32",
                        },
                        {
                            "internalType": "int256",
                            "name": "quantity",
                            "type": "int256",
                        },
                        {"internalType": "uint256", "name": "price", "type": "uint256"},
                    ],
                    "internalType": "struct IMarginAccount.Settlement[]",
                    "name": "settlements",
                    "type": "tuple[]",
                },
                {
                    "internalType": "uint256[]",
                    "name": "markPriceIfSettled",
                    "type": "uint256[]",
                },
            ],
            "name": "maeAndMmuAfterBatchTrade",
            "outputs": [
                {"internalType": "int256", "name": "maeAfter", "type": "int256"},
                {"internalType": "uint256", "name": "mmuAfter", "type": "uint256"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"},
                {
                    "components": [
                        {
                            "internalType": "bytes32",
                            "name": "positionId",
                            "type": "bytes32",
                        },
                        {
                            "internalType": "int256",
                            "name": "quantity",
                            "type": "int256",
                        },
                        {"internalType": "uint256", "name": "price", "type": "uint256"},
                    ],
                    "internalType": "struct IMarginAccount.Settlement",
                    "name": "settlement",
                    "type": "tuple",
                },
                {
                    "internalType": "uint256",
                    "name": "markPriceIfSettled",
                    "type": "uint256",
                },
            ],
            "name": "maeCheck",
            "outputs": [
                {"internalType": "bool", "name": "checkPassed", "type": "bool"},
                {"internalType": "int256", "name": "maeAfter", "type": "int256"},
                {"internalType": "uint256", "name": "mmuAfter", "type": "uint256"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"}
            ],
            "name": "mma",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"}
            ],
            "name": "mmu",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"}
            ],
            "name": "pnl",
            "outputs": [{"internalType": "int256", "name": "", "type": "int256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountId",
                    "type": "address",
                },
                {"internalType": "bytes32", "name": "positionId", "type": "bytes32"},
            ],
            "name": "positionAge",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"}
            ],
            "name": "positionCount",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"},
                {"internalType": "bytes32", "name": "positionId", "type": "bytes32"},
            ],
            "name": "positionData",
            "outputs": [
                {
                    "components": [
                        {
                            "internalType": "bytes32",
                            "name": "positionId",
                            "type": "bytes32",
                        },
                        {
                            "internalType": "int256",
                            "name": "quantity",
                            "type": "int256",
                        },
                        {
                            "internalType": "int256",
                            "name": "costBasis",
                            "type": "int256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "maintenanceMargin",
                            "type": "uint256",
                        },
                        {"internalType": "int256", "name": "pnl", "type": "int256"},
                    ],
                    "internalType": "struct IMarginAccount.PositionData",
                    "name": "",
                    "type": "tuple",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"},
                {"internalType": "bytes32", "name": "positionId", "type": "bytes32"},
            ],
            "name": "positionPnL",
            "outputs": [{"internalType": "int256", "name": "", "type": "int256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"},
                {"internalType": "bytes32", "name": "positionId", "type": "bytes32"},
            ],
            "name": "positionQuantity",
            "outputs": [{"internalType": "int256", "name": "", "type": "int256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"}
            ],
            "name": "positions",
            "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "productRegistry",
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
            "inputs": [
                {"internalType": "address", "name": "intentAccount", "type": "address"}
            ],
            "name": "revokeAuthorization",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"},
                {"internalType": "address", "name": "intentAccount", "type": "address"},
                {
                    "components": [
                        {
                            "internalType": "bytes32",
                            "name": "positionId",
                            "type": "bytes32",
                        },
                        {
                            "internalType": "int256",
                            "name": "quantity",
                            "type": "int256",
                        },
                        {"internalType": "uint256", "name": "price", "type": "uint256"},
                    ],
                    "internalType": "struct IMarginAccount.Settlement",
                    "name": "settlement",
                    "type": "tuple",
                },
            ],
            "name": "settle",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "valuation",
            "outputs": [
                {"internalType": "contract IValuation", "name": "", "type": "address"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "amount", "type": "uint256"}
            ],
            "name": "withdraw",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"}
            ],
            "name": "withdrawable",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
    ],
)
