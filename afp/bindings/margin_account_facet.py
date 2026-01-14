"""MarginAccountFacet contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import hexbytes
import web3
from web3 import types
from web3.contract import contract

from .types import Settlement, MarginData, PositionData


class MarginAccountFacet:
    """MarginAccountFacet contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed MarginAccountFacet contract.
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
    def PositionUpdated(self) -> contract.ContractEvent:
        """Binding for `event PositionUpdated` on the MarginAccountFacet contract."""
        return self._contract.events.PositionUpdated

    def authorize(
        self,
        owner: eth_typing.ChecksumAddress,
        intent_account: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `authorize` on the MarginAccountFacet contract.

        Parameters
        ----------
        owner : eth_typing.ChecksumAddress
        intent_account : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.authorize(
            owner,
            intent_account,
        )

    def collateral(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `collateral` on the MarginAccountFacet contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.collateral().call(
            block_identifier=block_identifier
        )
        return eth_typing.ChecksumAddress(return_value)

    def deposit(
        self,
        owner: eth_typing.ChecksumAddress,
        amount: int,
    ) -> contract.ContractFunction:
        """Binding for `deposit` on the MarginAccountFacet contract.

        Parameters
        ----------
        owner : eth_typing.ChecksumAddress
        amount : int

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.deposit(
            owner,
            amount,
        )

    def estimate_additional_margin(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        settlement: Settlement,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `estimateAdditionalMargin` on the MarginAccountFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        settlement : Settlement
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.estimateAdditionalMargin(
            margin_account_id,
            (settlement.product_id, settlement.quantity, settlement.price),
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def is_authorized(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        intent_account: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> bool:
        """Binding for `isAuthorized` on the MarginAccountFacet contract.

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
        return_value = self._contract.functions.isAuthorized(
            margin_account_id,
            intent_account,
        ).call(block_identifier=block_identifier)
        return bool(return_value)

    def mae_check(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        settlement: Settlement,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> bool:
        """Binding for `maeCheck` on the MarginAccountFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        settlement : Settlement
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        bool
        """
        return_value = self._contract.functions.maeCheck(
            margin_account_id,
            (settlement.product_id, settlement.quantity, settlement.price),
        ).call(block_identifier=block_identifier)
        return bool(return_value)

    def margin_data(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> MarginData:
        """Binding for `marginData` on the MarginAccountFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        MarginData
        """
        return_value = self._contract.functions.marginData(
            margin_account_id,
        ).call(block_identifier=block_identifier)
        return MarginData(
            int(return_value[0]),
            int(return_value[1]),
            int(return_value[2]),
            int(return_value[3]),
        )

    def position(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> PositionData:
        """Binding for `position` on the MarginAccountFacet contract.

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
        return_value = self._contract.functions.position(
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

    def products_by_margin_account(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[hexbytes.HexBytes]:
        """Binding for `products` on the MarginAccountFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[hexbytes.HexBytes]
        """
        return_value = self._contract.functions.products(
            margin_account_id,
        ).call(block_identifier=block_identifier)
        return [
            hexbytes.HexBytes(return_value_elem) for return_value_elem in return_value
        ]

    def revoke(
        self,
        owner: eth_typing.ChecksumAddress,
        intent_account: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `revoke` on the MarginAccountFacet contract.

        Parameters
        ----------
        owner : eth_typing.ChecksumAddress
        intent_account : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.revoke(
            owner,
            intent_account,
        )

    def state_after_settlement(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        settlement: Settlement,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.Tuple[int, int]:
        """Binding for `stateAfterSettlement` on the MarginAccountFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        settlement : Settlement
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        int
        """
        return_value = self._contract.functions.stateAfterSettlement(
            margin_account_id,
            (settlement.product_id, settlement.quantity, settlement.price),
        ).call(block_identifier=block_identifier)
        return (
            int(return_value[0]),
            int(return_value[1]),
        )

    def withdraw(
        self,
        owner: eth_typing.ChecksumAddress,
        amount: int,
    ) -> contract.ContractFunction:
        """Binding for `withdraw` on the MarginAccountFacet contract.

        Parameters
        ----------
        owner : eth_typing.ChecksumAddress
        amount : int

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.withdraw(
            owner,
            amount,
        )


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "type": "function",
            "name": "authorize",
            "inputs": [
                {"name": "owner", "type": "address", "internalType": "address"},
                {"name": "intentAccount", "type": "address", "internalType": "address"},
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "collateral",
            "inputs": [],
            "outputs": [{"name": "", "type": "address", "internalType": "address"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "deposit",
            "inputs": [
                {"name": "owner", "type": "address", "internalType": "address"},
                {"name": "amount", "type": "uint256", "internalType": "uint256"},
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "estimateAdditionalMargin",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                },
                {
                    "name": "settlement",
                    "type": "tuple",
                    "internalType": "struct Settlement",
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
                        {"name": "price", "type": "int256", "internalType": "int256"},
                    ],
                },
            ],
            "outputs": [
                {
                    "name": "additionalMargin",
                    "type": "uint256",
                    "internalType": "uint256",
                }
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "isAuthorized",
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
            "name": "maeCheck",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                },
                {
                    "name": "settlement",
                    "type": "tuple",
                    "internalType": "struct Settlement",
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
                        {"name": "price", "type": "int256", "internalType": "int256"},
                    ],
                },
            ],
            "outputs": [
                {"name": "checkPassed", "type": "bool", "internalType": "bool"}
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "marginData",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                }
            ],
            "outputs": [
                {
                    "name": "",
                    "type": "tuple",
                    "internalType": "struct IMarginAccountFacet.MarginData",
                    "components": [
                        {"name": "capital", "type": "int256", "internalType": "int256"},
                        {"name": "mae", "type": "int256", "internalType": "int256"},
                        {"name": "mmu", "type": "uint256", "internalType": "uint256"},
                        {"name": "pnl", "type": "int256", "internalType": "int256"},
                    ],
                }
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "position",
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
            "name": "products",
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
            "name": "revoke",
            "inputs": [
                {"name": "owner", "type": "address", "internalType": "address"},
                {"name": "intentAccount", "type": "address", "internalType": "address"},
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "stateAfterSettlement",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "internalType": "address",
                },
                {
                    "name": "settlement",
                    "type": "tuple",
                    "internalType": "struct Settlement",
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
                        {"name": "price", "type": "int256", "internalType": "int256"},
                    ],
                },
            ],
            "outputs": [
                {"name": "maeAfter", "type": "int256", "internalType": "int256"},
                {"name": "mmuAfter", "type": "uint256", "internalType": "uint256"},
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "withdraw",
            "inputs": [
                {"name": "owner", "type": "address", "internalType": "address"},
                {"name": "amount", "type": "uint256", "internalType": "uint256"},
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
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
        {"type": "error", "name": "EVWMA_NotInitialized", "inputs": []},
        {
            "type": "error",
            "name": "InsufficientBalance",
            "inputs": [
                {"name": "account", "type": "address", "internalType": "address"},
                {"name": "balance", "type": "uint256", "internalType": "uint256"},
                {"name": "required", "type": "uint256", "internalType": "uint256"},
            ],
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
            "name": "SafeCastOverflowedIntToUint",
            "inputs": [{"name": "value", "type": "int256", "internalType": "int256"}],
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
    ],
)
