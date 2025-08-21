"""MarginAccountRegistry contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import hexbytes
import web3
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
    ) -> str:
        """Binding for `UPGRADE_INTERFACE_VERSION` on the MarginAccountRegistry contract.

        Returns
        -------
        str
        """
        return_value = self._contract.functions.UPGRADE_INTERFACE_VERSION().call()
        return str(return_value)

    def clearing(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `clearing` on the MarginAccountRegistry contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.clearing().call()
        return eth_typing.ChecksumAddress(return_value)

    def get_admin(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `getAdmin` on the MarginAccountRegistry contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.getAdmin().call()
        return eth_typing.ChecksumAddress(return_value)

    def get_margin_account(
        self,
        collateral_asset: eth_typing.ChecksumAddress,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `getMarginAccount` on the MarginAccountRegistry contract.

        Parameters
        ----------
        collateral_asset : eth_typing.ChecksumAddress

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.getMarginAccount(
            collateral_asset,
        ).call()
        return eth_typing.ChecksumAddress(return_value)

    def initialize(
        self,
        _clearing: eth_typing.ChecksumAddress,
        _valuation: eth_typing.ChecksumAddress,
        _product_registry: eth_typing.ChecksumAddress,
        beacon_: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `initialize` on the MarginAccountRegistry contract.

        Parameters
        ----------
        _clearing : eth_typing.ChecksumAddress
        _valuation : eth_typing.ChecksumAddress
        _product_registry : eth_typing.ChecksumAddress
        beacon_ : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.initialize(
            _clearing,
            _valuation,
            _product_registry,
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

    def is_admin_active(
        self,
    ) -> bool:
        """Binding for `isAdminActive` on the MarginAccountRegistry contract.

        Returns
        -------
        bool
        """
        return_value = self._contract.functions.isAdminActive().call()
        return bool(return_value)

    def margin_accounts(
        self,
        key0: eth_typing.ChecksumAddress,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `marginAccounts` on the MarginAccountRegistry contract.

        Parameters
        ----------
        key0 : eth_typing.ChecksumAddress

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.marginAccounts(
            key0,
        ).call()
        return eth_typing.ChecksumAddress(return_value)

    def owner(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `owner` on the MarginAccountRegistry contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.owner().call()
        return eth_typing.ChecksumAddress(return_value)

    def product_registry(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `productRegistry` on the MarginAccountRegistry contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.productRegistry().call()
        return eth_typing.ChecksumAddress(return_value)

    def proxiable_uuid(
        self,
    ) -> hexbytes.HexBytes:
        """Binding for `proxiableUUID` on the MarginAccountRegistry contract.

        Returns
        -------
        hexbytes.HexBytes
        """
        return_value = self._contract.functions.proxiableUUID().call()
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

    def set_active(
        self,
        active: bool,
    ) -> contract.ContractFunction:
        """Binding for `setActive` on the MarginAccountRegistry contract.

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
        """Binding for `setAdmin` on the MarginAccountRegistry contract.

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

    def valuation(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `valuation` on the MarginAccountRegistry contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.valuation().call()
        return eth_typing.ChecksumAddress(return_value)


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "inputs": [
                {"internalType": "address", "name": "target", "type": "address"}
            ],
            "name": "AddressEmptyCode",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "bytes4", "name": "selector", "type": "bytes4"},
                {"internalType": "address", "name": "sender", "type": "address"},
            ],
            "name": "AdminControlledNotAuthorized",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "string", "name": "parameter", "type": "string"}
            ],
            "name": "AlreadyExists",
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
        {"inputs": [], "name": "NotInitialized", "type": "error"},
        {"inputs": [], "name": "NotInitializing", "type": "error"},
        {
            "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
            "name": "OwnableInvalidOwner",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "account", "type": "address"}
            ],
            "name": "OwnableUnauthorizedAccount",
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
                    "internalType": "address",
                    "name": "collateralAsset",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "marginAccount",
                    "type": "address",
                },
            ],
            "name": "MarginAccountCreated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "previousOwner",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address",
                },
            ],
            "name": "OwnershipTransferred",
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
            "name": "UPGRADE_INTERFACE_VERSION",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
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
            "name": "getAdmin",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "collateralAsset",
                    "type": "address",
                }
            ],
            "name": "getMarginAccount",
            "outputs": [
                {
                    "internalType": "contract IMarginAccount",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "_clearing", "type": "address"},
                {"internalType": "address", "name": "_valuation", "type": "address"},
                {
                    "internalType": "address",
                    "name": "_productRegistry",
                    "type": "address",
                },
                {"internalType": "address", "name": "beacon_", "type": "address"},
            ],
            "name": "initialize",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "collateralAsset",
                    "type": "address",
                }
            ],
            "name": "initializeMarginAccount",
            "outputs": [
                {
                    "internalType": "contract IMarginAccount",
                    "name": "",
                    "type": "address",
                }
            ],
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
            "inputs": [{"internalType": "address", "name": "", "type": "address"}],
            "name": "marginAccounts",
            "outputs": [
                {
                    "internalType": "contract IMarginAccount",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "owner",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "productRegistry",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
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
            "inputs": [],
            "name": "renounceOwnership",
            "outputs": [],
            "stateMutability": "nonpayable",
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
                {"internalType": "address", "name": "newOwner", "type": "address"}
            ],
            "name": "transferOwnership",
            "outputs": [],
            "stateMutability": "nonpayable",
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
            "inputs": [],
            "name": "valuation",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
    ],
)
