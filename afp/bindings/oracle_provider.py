"""OracleProvider contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import hexbytes
import web3
from web3.contract import contract


class OracleProvider:
    """OracleProvider contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed OracleProvider contract.
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
        """Binding for `event Initialized` on the OracleProvider contract."""
        return self._contract.events.Initialized

    @property
    def OwnershipTransferred(self) -> contract.ContractEvent:
        """Binding for `event OwnershipTransferred` on the OracleProvider contract."""
        return self._contract.events.OwnershipTransferred

    @property
    def PriceSubmitted(self) -> contract.ContractEvent:
        """Binding for `event PriceSubmitted` on the OracleProvider contract."""
        return self._contract.events.PriceSubmitted

    @property
    def Upgraded(self) -> contract.ContractEvent:
        """Binding for `event Upgraded` on the OracleProvider contract."""
        return self._contract.events.Upgraded

    def upgrade_interface_version(
        self,
    ) -> str:
        """Binding for `UPGRADE_INTERFACE_VERSION` on the OracleProvider contract.

        Returns
        -------
        str
        """
        return_value = self._contract.functions.UPGRADE_INTERFACE_VERSION().call()
        return str(return_value)

    def get_admin(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `getAdmin` on the OracleProvider contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.getAdmin().call()
        return eth_typing.ChecksumAddress(return_value)

    def initialize(
        self,
        _product_registry: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `initialize` on the OracleProvider contract.

        Parameters
        ----------
        _product_registry : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.initialize(
            _product_registry,
        )

    def is_admin_active(
        self,
    ) -> bool:
        """Binding for `isAdminActive` on the OracleProvider contract.

        Returns
        -------
        bool
        """
        return_value = self._contract.functions.isAdminActive().call()
        return bool(return_value)

    def owner(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `owner` on the OracleProvider contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.owner().call()
        return eth_typing.ChecksumAddress(return_value)

    def product_registry(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `productRegistry` on the OracleProvider contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.productRegistry().call()
        return eth_typing.ChecksumAddress(return_value)

    def proxiable_uuid(
        self,
    ) -> hexbytes.HexBytes:
        """Binding for `proxiableUUID` on the OracleProvider contract.

        Returns
        -------
        hexbytes.HexBytes
        """
        return_value = self._contract.functions.proxiableUUID().call()
        return hexbytes.HexBytes(return_value)

    def renounce_ownership(
        self,
    ) -> contract.ContractFunction:
        """Binding for `renounceOwnership` on the OracleProvider contract.

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.renounceOwnership()

    def resolve(
        self,
        product_id: hexbytes.HexBytes,
        key1: hexbytes.HexBytes,
    ) -> int:
        """Binding for `resolve` on the OracleProvider contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        key1 : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.resolve(
            product_id,
            key1,
        ).call()
        return int(return_value)

    def set_active(
        self,
        active: bool,
    ) -> contract.ContractFunction:
        """Binding for `setActive` on the OracleProvider contract.

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
        admin: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `setAdmin` on the OracleProvider contract.

        Parameters
        ----------
        admin : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.setAdmin(
            admin,
        )

    def submit(
        self,
        key: hexbytes.HexBytes,
        fsp: int,
    ) -> contract.ContractFunction:
        """Binding for `submit` on the OracleProvider contract.

        Parameters
        ----------
        key : hexbytes.HexBytes
        fsp : int

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.submit(
            key,
            fsp,
        )

    def transfer_ownership(
        self,
        new_owner: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `transferOwnership` on the OracleProvider contract.

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
        """Binding for `upgradeToAndCall` on the OracleProvider contract.

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
                {"internalType": "address", "name": "implementation", "type": "address"}
            ],
            "name": "ERC1967InvalidImplementation",
            "type": "error",
        },
        {"inputs": [], "name": "ERC1967NonPayable", "type": "error"},
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "FSPNotFound",
            "type": "error",
        },
        {"inputs": [], "name": "FailedCall", "type": "error"},
        {"inputs": [], "name": "InvalidInitialization", "type": "error"},
        {
            "inputs": [
                {"internalType": "enum ProductState", "name": "state", "type": "uint8"}
            ],
            "name": "InvalidProductState",
            "type": "error",
        },
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
                    "internalType": "bytes32",
                    "name": "key",
                    "type": "bytes32",
                },
                {
                    "indexed": False,
                    "internalType": "int256",
                    "name": "fsp",
                    "type": "int256",
                },
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "submitter",
                    "type": "address",
                },
            ],
            "name": "PriceSubmitted",
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
            "name": "getAdmin",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_productRegistry",
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
            "name": "isAdminActive",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"},
                {"internalType": "bytes", "name": "", "type": "bytes"},
            ],
            "name": "resolve",
            "outputs": [{"internalType": "int256", "name": "", "type": "int256"}],
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
            "inputs": [{"internalType": "address", "name": "admin", "type": "address"}],
            "name": "setAdmin",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "key", "type": "bytes32"},
                {"internalType": "int256", "name": "fsp", "type": "int256"},
            ],
            "name": "submit",
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
    ],
)
