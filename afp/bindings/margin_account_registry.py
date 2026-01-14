"""MarginAccountRegistry contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import hexbytes
import web3
from web3 import types
from web3.contract import contract


class MarginAccountRegistry:
    """MarginAccountRegistry contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed MarginAccountRegistry contract.
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
        """Binding for `event Initialized` on the MarginAccountRegistry contract."""
        return self._contract.events.Initialized

    @property
    def MarginAccountCreated(self) -> contract.ContractEvent:
        """Binding for `event MarginAccountCreated` on the MarginAccountRegistry contract."""
        return self._contract.events.MarginAccountCreated

    @property
    def OwnershipTransferred(self) -> contract.ContractEvent:
        """Binding for `event OwnershipTransferred` on the MarginAccountRegistry contract."""
        return self._contract.events.OwnershipTransferred

    @property
    def Upgraded(self) -> contract.ContractEvent:
        """Binding for `event Upgraded` on the MarginAccountRegistry contract."""
        return self._contract.events.Upgraded

    def upgrade_interface_version(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> str:
        """Binding for `UPGRADE_INTERFACE_VERSION` on the MarginAccountRegistry contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        str
        """
        return_value = self._contract.functions.UPGRADE_INTERFACE_VERSION().call(
            block_identifier=block_identifier
        )
        return str(return_value)

    def beacon(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `beacon` on the MarginAccountRegistry contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.beacon().call(
            block_identifier=block_identifier
        )
        return eth_typing.ChecksumAddress(return_value)

    def clearing(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `clearing` on the MarginAccountRegistry contract.

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

    def get_margin_account(
        self,
        collateral_asset: eth_typing.ChecksumAddress,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `getMarginAccount` on the MarginAccountRegistry contract.

        Parameters
        ----------
        collateral_asset : eth_typing.ChecksumAddress
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.getMarginAccount(
            collateral_asset,
        ).call(block_identifier=block_identifier)
        return eth_typing.ChecksumAddress(return_value)

    def initialize(
        self,
        clearing_: eth_typing.ChecksumAddress,
        beacon_: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `initialize` on the MarginAccountRegistry contract.

        Parameters
        ----------
        clearing_ : eth_typing.ChecksumAddress
        beacon_ : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.initialize(
            clearing_,
            beacon_,
        )

    def initialize_margin_account(
        self,
        collateral_asset: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `initializeMarginAccount` on the MarginAccountRegistry contract.

        Parameters
        ----------
        collateral_asset : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.initializeMarginAccount(
            collateral_asset,
        )

    def owner(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `owner` on the MarginAccountRegistry contract.

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

    def proxiable_uuid(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> hexbytes.HexBytes:
        """Binding for `proxiableUUID` on the MarginAccountRegistry contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        hexbytes.HexBytes
        """
        return_value = self._contract.functions.proxiableUUID().call(
            block_identifier=block_identifier
        )
        return hexbytes.HexBytes(return_value)

    def renounce_ownership(
        self,
    ) -> contract.ContractFunction:
        """Binding for `renounceOwnership` on the MarginAccountRegistry contract.

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.renounceOwnership()

    def transfer_ownership(
        self,
        new_owner: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `transferOwnership` on the MarginAccountRegistry contract.

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

    def upgrade_to_and_call(
        self,
        new_implementation: eth_typing.ChecksumAddress,
        data: hexbytes.HexBytes,
    ) -> contract.ContractFunction:
        """Binding for `upgradeToAndCall` on the MarginAccountRegistry contract.

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


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "type": "function",
            "name": "UPGRADE_INTERFACE_VERSION",
            "inputs": [],
            "outputs": [{"name": "", "type": "string", "internalType": "string"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "beacon",
            "inputs": [],
            "outputs": [{"name": "", "type": "address", "internalType": "address"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "clearing",
            "inputs": [],
            "outputs": [{"name": "", "type": "address", "internalType": "address"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "getMarginAccount",
            "inputs": [
                {
                    "name": "collateralAsset",
                    "type": "address",
                    "internalType": "address",
                }
            ],
            "outputs": [
                {
                    "name": "",
                    "type": "address",
                    "internalType": "contract IMarginAccount",
                }
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "initialize",
            "inputs": [
                {"name": "clearing_", "type": "address", "internalType": "address"},
                {"name": "beacon_", "type": "address", "internalType": "address"},
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "initializeMarginAccount",
            "inputs": [
                {
                    "name": "collateralAsset",
                    "type": "address",
                    "internalType": "address",
                }
            ],
            "outputs": [
                {
                    "name": "",
                    "type": "address",
                    "internalType": "contract IMarginAccount",
                }
            ],
            "stateMutability": "nonpayable",
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
            "name": "proxiableUUID",
            "inputs": [],
            "outputs": [{"name": "", "type": "bytes32", "internalType": "bytes32"}],
            "stateMutability": "view",
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
            "name": "transferOwnership",
            "inputs": [
                {"name": "newOwner", "type": "address", "internalType": "address"}
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "upgradeToAndCall",
            "inputs": [
                {
                    "name": "newImplementation",
                    "type": "address",
                    "internalType": "address",
                },
                {"name": "data", "type": "bytes", "internalType": "bytes"},
            ],
            "outputs": [],
            "stateMutability": "payable",
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
            "name": "MarginAccountCreated",
            "inputs": [
                {
                    "name": "collateralAsset",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "marginAccount",
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
            "name": "Upgraded",
            "inputs": [
                {
                    "name": "implementation",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                }
            ],
            "anonymous": False,
        },
        {
            "type": "error",
            "name": "AddressEmptyCode",
            "inputs": [
                {"name": "target", "type": "address", "internalType": "address"}
            ],
        },
        {"type": "error", "name": "AlreadyInitialized", "inputs": []},
        {
            "type": "error",
            "name": "ERC1967InvalidImplementation",
            "inputs": [
                {"name": "implementation", "type": "address", "internalType": "address"}
            ],
        },
        {"type": "error", "name": "ERC1967NonPayable", "inputs": []},
        {"type": "error", "name": "FailedCall", "inputs": []},
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
        {"type": "error", "name": "UUPSUnauthorizedCallContext", "inputs": []},
        {
            "type": "error",
            "name": "UUPSUnsupportedProxiableUUID",
            "inputs": [{"name": "slot", "type": "bytes32", "internalType": "bytes32"}],
        },
    ],
)
