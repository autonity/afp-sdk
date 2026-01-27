"""MarginAccount contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import hexbytes
import web3
from web3 import types
from web3.contract import contract

from .types import PositionData


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
    def Deposit(self) -> contract.ContractEvent:
        """Binding for `event Deposit` on the MarginAccount contract."""
        return self._contract.events.Deposit

    @property
    def Initialized(self) -> contract.ContractEvent:
        """Binding for `event Initialized` on the MarginAccount contract."""
        return self._contract.events.Initialized

    @property
    def IntentAuthorized(self) -> contract.ContractEvent:
        """Binding for `event IntentAuthorized` on the MarginAccount contract."""
        return self._contract.events.IntentAuthorized

    @property
    def IntentRevoked(self) -> contract.ContractEvent:
        """Binding for `event IntentRevoked` on the MarginAccount contract."""
        return self._contract.events.IntentRevoked

    @property
    def OwnershipTransferred(self) -> contract.ContractEvent:
        """Binding for `event OwnershipTransferred` on the MarginAccount contract."""
        return self._contract.events.OwnershipTransferred

    @property
    def PositionUpdated(self) -> contract.ContractEvent:
        """Binding for `event PositionUpdated` on the MarginAccount contract."""
        return self._contract.events.PositionUpdated

    @property
    def Withdraw(self) -> contract.ContractEvent:
        """Binding for `event Withdraw` on the MarginAccount contract."""
        return self._contract.events.Withdraw

    def add_allowed(
        self,
        addr: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `addAllowed` on the MarginAccount contract.

        Parameters
        ----------
        addr : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.addAllowed(
            addr,
        )

    def admin(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `admin` on the MarginAccount contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.admin().call(
            block_identifier=block_identifier
        )
        return eth_typing.ChecksumAddress(return_value)

    def allowed(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[eth_typing.ChecksumAddress]:
        """Binding for `allowed` on the MarginAccount contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[eth_typing.ChecksumAddress]
        """
        return_value = self._contract.functions.allowed().call(
            block_identifier=block_identifier
        )
        return [
            eth_typing.ChecksumAddress(return_value_elem)
            for return_value_elem in return_value
        ]

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
        margin_account_id: eth_typing.ChecksumAddress,
        intent_account: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> bool:
        """Binding for `authorized` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        intent_account : eth_typing.ChecksumAddress
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        bool
        """
        return_value = self._contract.functions.authorized(
            margin_account_id,
            intent_account,
        ).call(block_identifier=block_identifier)
        return bool(return_value)

    def capital(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `capital` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.capital(
            margin_account_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def clearing(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `clearing` on the MarginAccount contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.clearing().call(
            block_identifier=block_identifier
        )
        return eth_typing.ChecksumAddress(return_value)

    def collateral_asset(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `collateralAsset` on the MarginAccount contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.collateralAsset().call(
            block_identifier=block_identifier
        )
        return eth_typing.ChecksumAddress(return_value)

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

    def deposit_for(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        amount: int,
    ) -> contract.ContractFunction:
        """Binding for `depositFor` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        amount : int

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.depositFor(
            margin_account_id,
            amount,
        )

    def initialize(
        self,
        clearing_: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `initialize` on the MarginAccount contract.

        Parameters
        ----------
        clearing_ : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.initialize(
            clearing_,
        )

    def mae(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `mae` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.mae(
            margin_account_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def mma(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `mma` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.mma(
            margin_account_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def mmu(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `mmu` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.mmu(
            margin_account_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def owner(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `owner` on the MarginAccount contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.owner().call(
            block_identifier=block_identifier
        )
        return eth_typing.ChecksumAddress(return_value)

    def pnl(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `pnl` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.pnl(
            margin_account_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def position_count(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `positionCount` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.positionCount(
            margin_account_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def position_data(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> PositionData:
        """Binding for `positionData` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        PositionData
        """
        return_value = self._contract.functions.positionData(
            margin_account_id,
            product_id,
        ).call(block_identifier=block_identifier)
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
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `positionPnL` on the MarginAccount contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.positionPnL(
            margin_account,
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def position_quantity(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `positionQuantity` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.positionQuantity(
            margin_account_id,
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def positions(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[hexbytes.HexBytes]:
        """Binding for `positions` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[hexbytes.HexBytes]
        """
        return_value = self._contract.functions.positions(
            margin_account_id,
        ).call(block_identifier=block_identifier)
        return [
            hexbytes.HexBytes(return_value_elem) for return_value_elem in return_value
        ]

    def remove_allowed(
        self,
        addr: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `removeAllowed` on the MarginAccount contract.

        Parameters
        ----------
        addr : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.removeAllowed(
            addr,
        )

    def renounce_ownership(
        self,
    ) -> contract.ContractFunction:
        """Binding for `renounceOwnership` on the MarginAccount contract.

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.renounceOwnership()

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

    def transfer_ownership(
        self,
        new_owner: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `transferOwnership` on the MarginAccount contract.

        Parameters
        ----------
        new_owner : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.transferOwnership(
            new_owner,
        )

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
        margin_account_id: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `withdrawable` on the MarginAccount contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.withdrawable(
            margin_account_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "type": "function",
            "name": "addAllowed",
            "inputs": [{"name": "addr", "type": "address", "internalType": "address"}],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "admin",
            "inputs": [],
            "outputs": [{"name": "", "type": "address", "internalType": "address"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "allowed",
            "inputs": [],
            "outputs": [{"name": "", "type": "address[]", "internalType": "address[]"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "authorize",
            "inputs": [
                {"name": "intentAccount", "type": "address", "internalType": "address"}
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "authorized",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                },
                {"name": "intentAccount", "type": "address", "internalType": "address"},
            ],
            "outputs": [{"name": "", "type": "bool", "internalType": "bool"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "capital",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                }
            ],
            "outputs": [{"name": "", "type": "int256", "internalType": "int256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "clearing",
            "inputs": [],
            "outputs": [
                {
                    "name": "",
                    "type": "address",
                    "internalType": "contract IMarginAccountFacet",
                }
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "collateralAsset",
            "inputs": [],
            "outputs": [{"name": "", "type": "address", "internalType": "address"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "deposit",
            "inputs": [
                {"name": "amount", "type": "uint256", "internalType": "uint256"}
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "depositFor",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                },
                {"name": "amount", "type": "uint256", "internalType": "uint256"},
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "initialize",
            "inputs": [
                {"name": "clearing_", "type": "address", "internalType": "address"}
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "mae",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                }
            ],
            "outputs": [{"name": "", "type": "int256", "internalType": "int256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "mma",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                }
            ],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "mmu",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                }
            ],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "owner",
            "inputs": [],
            "outputs": [{"name": "", "type": "address", "internalType": "address"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "pnl",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                }
            ],
            "outputs": [{"name": "", "type": "int256", "internalType": "int256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "positionCount",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                }
            ],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "positionData",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                },
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"},
            ],
            "outputs": [
                {
                    "name": "",
                    "type": "tuple",
                    "internalType": "struct PositionData",
                    "components": [
                        {
                            "name": "productId",
                            "type": "bytes32",
                            "internalType": "bytes32",
                        },
                        {
                            "name": "quantity",
                            "type": "int256",
                            "internalType": "int256",
                        },
                        {
                            "name": "costBasis",
                            "type": "int256",
                            "internalType": "int256",
                        },
                        {
                            "name": "maintenanceMargin",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                        {"name": "pnl", "type": "int256", "internalType": "int256"},
                    ],
                }
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "positionPnL",
            "inputs": [
                {"name": "marginAccount", "type": "address", "internalType": "address"},
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"},
            ],
            "outputs": [{"name": "", "type": "int256", "internalType": "int256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "positionQuantity",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                },
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"},
            ],
            "outputs": [{"name": "", "type": "int256", "internalType": "int256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "positions",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                }
            ],
            "outputs": [{"name": "", "type": "bytes32[]", "internalType": "bytes32[]"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "removeAllowed",
            "inputs": [{"name": "addr", "type": "address", "internalType": "address"}],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "renounceOwnership",
            "inputs": [],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "revokeAuthorization",
            "inputs": [
                {"name": "intentAccount", "type": "address", "internalType": "address"}
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "transferOwnership",
            "inputs": [
                {"name": "newOwner", "type": "address", "internalType": "address"}
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "withdraw",
            "inputs": [
                {"name": "amount", "type": "uint256", "internalType": "uint256"}
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "withdrawable",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                }
            ],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "event",
            "name": "Deposit",
            "inputs": [
                {
                    "name": "user",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "amount",
                    "type": "uint256",
                    "indexed": False,
                    "internalType": "uint256",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "Initialized",
            "inputs": [
                {
                    "name": "version",
                    "type": "uint64",
                    "indexed": False,
                    "internalType": "uint64",
                }
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "IntentAuthorized",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "intentAccount",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "IntentRevoked",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "intentAccount",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "OwnershipTransferred",
            "inputs": [
                {
                    "name": "previousOwner",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "newOwner",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
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
                    "name": "productId",
                    "type": "bytes32",
                    "indexed": True,
                    "internalType": "bytes32",
                },
                {
                    "name": "totalQuantity",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "costBasis",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "price",
                    "type": "uint256",
                    "indexed": False,
                    "internalType": "uint256",
                },
                {
                    "name": "quantity",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "Withdraw",
            "inputs": [
                {
                    "name": "user",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "amount",
                    "type": "uint256",
                    "indexed": False,
                    "internalType": "uint256",
                },
            ],
            "anonymous": False,
        },
        {"type": "error", "name": "InvalidInitialization", "inputs": []},
        {"type": "error", "name": "NotInitializing", "inputs": []},
        {
            "type": "error",
            "name": "OwnableInvalidOwner",
            "inputs": [{"name": "owner", "type": "address", "internalType": "address"}],
        },
        {
            "type": "error",
            "name": "OwnableUnauthorizedAccount",
            "inputs": [
                {"name": "account", "type": "address", "internalType": "address"}
            ],
        },
        {
            "type": "error",
            "name": "SafeCastOverflowedIntToUint",
            "inputs": [{"name": "value", "type": "int256", "internalType": "int256"}],
        },
        {
            "type": "error",
            "name": "SafeERC20FailedOperation",
            "inputs": [{"name": "token", "type": "address", "internalType": "address"}],
        },
        {
            "type": "error",
            "name": "Unauthorized",
            "inputs": [
                {"name": "account", "type": "address", "internalType": "address"}
            ],
        },
    ],
)
