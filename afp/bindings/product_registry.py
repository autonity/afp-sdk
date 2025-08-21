"""ProductRegistry contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import enum
import typing
from dataclasses import dataclass

import eth_typing
import hexbytes
import web3
from web3.contract import contract


class ProductState(enum.IntEnum):
    """Port of `enum ProductState` on the ProductRegistry contract."""

    NOT_EXIST = 0
    PENDING = 1
    LIVE = 2
    TRADEOUT = 3
    FINAL_SETTLEMENT = 4
    EXPIRED = 5


@dataclass
class ProductMetadata:
    """Port of `struct ProductMetadata` on the IProductRegistry contract."""

    builder: eth_typing.ChecksumAddress
    symbol: str
    description: str


@dataclass
class OracleSpecification:
    """Port of `struct OracleSpecification` on the IProductRegistry contract."""

    oracle_address: eth_typing.ChecksumAddress
    fsv_decimals: int
    fsp_alpha: int
    fsp_beta: int
    fsv_calldata: hexbytes.HexBytes


@dataclass
class Product:
    """Port of `struct Product` on the IProductRegistry contract."""

    metadata: ProductMetadata
    oracle_spec: OracleSpecification
    price_quotation: str
    collateral_asset: eth_typing.ChecksumAddress
    start_time: int
    earliest_fsp_submission_time: int
    unit_value: int
    initial_margin_requirement: int
    maintenance_margin_requirement: int
    offer_price_buffer: int
    auction_bounty: int
    tradeout_interval: int
    tick_size: int
    extended_metadata: str


class ProductRegistry:
    """ProductRegistry contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed ProductRegistry contract.
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
        """Binding for `event Initialized` on the ProductRegistry contract."""
        return self._contract.events.Initialized

    @property
    def OwnershipTransferred(self) -> contract.ContractEvent:
        """Binding for `event OwnershipTransferred` on the ProductRegistry contract."""
        return self._contract.events.OwnershipTransferred

    @property
    def ProductRegistered(self) -> contract.ContractEvent:
        """Binding for `event ProductRegistered` on the ProductRegistry contract."""
        return self._contract.events.ProductRegistered

    @property
    def Upgraded(self) -> contract.ContractEvent:
        """Binding for `event Upgraded` on the ProductRegistry contract."""
        return self._contract.events.Upgraded

    def upgrade_interface_version(
        self,
    ) -> str:
        """Binding for `UPGRADE_INTERFACE_VERSION` on the ProductRegistry contract.

        Returns
        -------
        str
        """
        return_value = self._contract.functions.UPGRADE_INTERFACE_VERSION().call()
        return str(return_value)

    def auction_bounty(
        self,
        product_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `auctionBounty` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.auctionBounty(
            product_id,
        ).call()
        return int(return_value)

    def clearing(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `clearing` on the ProductRegistry contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.clearing().call()
        return eth_typing.ChecksumAddress(return_value)

    def collateral_asset(
        self,
        product_id: hexbytes.HexBytes,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `collateralAsset` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.collateralAsset(
            product_id,
        ).call()
        return eth_typing.ChecksumAddress(return_value)

    def earliest_fsp_submission_time(
        self,
        product_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `earliestFSPSubmissionTime` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.earliestFSPSubmissionTime(
            product_id,
        ).call()
        return int(return_value)

    def id(
        self,
        product: Product,
    ) -> hexbytes.HexBytes:
        """Binding for `id` on the ProductRegistry contract.

        Parameters
        ----------
        product : Product

        Returns
        -------
        hexbytes.HexBytes
        """
        return_value = self._contract.functions.id(
            (
                (
                    product.metadata.builder,
                    product.metadata.symbol,
                    product.metadata.description,
                ),
                (
                    product.oracle_spec.oracle_address,
                    product.oracle_spec.fsv_decimals,
                    product.oracle_spec.fsp_alpha,
                    product.oracle_spec.fsp_beta,
                    product.oracle_spec.fsv_calldata,
                ),
                product.price_quotation,
                product.collateral_asset,
                product.start_time,
                product.earliest_fsp_submission_time,
                product.unit_value,
                product.initial_margin_requirement,
                product.maintenance_margin_requirement,
                product.offer_price_buffer,
                product.auction_bounty,
                product.tradeout_interval,
                product.tick_size,
                product.extended_metadata,
            ),
        ).call()
        return hexbytes.HexBytes(return_value)

    def imr(
        self,
        product_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `imr` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.imr(
            product_id,
        ).call()
        return int(return_value)

    def initialize(
        self,
    ) -> contract.ContractFunction:
        """Binding for `initialize` on the ProductRegistry contract.

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.initialize()

    def mmr(
        self,
        product_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `mmr` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.mmr(
            product_id,
        ).call()
        return int(return_value)

    def offer_price_buffer(
        self,
        product_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `offerPriceBuffer` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.offerPriceBuffer(
            product_id,
        ).call()
        return int(return_value)

    def oracle_specification(
        self,
        product_id: hexbytes.HexBytes,
    ) -> OracleSpecification:
        """Binding for `oracleSpecification` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        OracleSpecification
        """
        return_value = self._contract.functions.oracleSpecification(
            product_id,
        ).call()
        return OracleSpecification(
            eth_typing.ChecksumAddress(return_value[0]),
            int(return_value[1]),
            int(return_value[2]),
            int(return_value[3]),
            hexbytes.HexBytes(return_value[4]),
        )

    def owner(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `owner` on the ProductRegistry contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.owner().call()
        return eth_typing.ChecksumAddress(return_value)

    def point_value(
        self,
        product_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `pointValue` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.pointValue(
            product_id,
        ).call()
        return int(return_value)

    def products(
        self,
        product_id: hexbytes.HexBytes,
    ) -> Product:
        """Binding for `products` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        Product
        """
        return_value = self._contract.functions.products(
            product_id,
        ).call()
        return Product(
            ProductMetadata(
                eth_typing.ChecksumAddress(return_value[0][0]),
                str(return_value[0][1]),
                str(return_value[0][2]),
            ),
            OracleSpecification(
                eth_typing.ChecksumAddress(return_value[1][0]),
                int(return_value[1][1]),
                int(return_value[1][2]),
                int(return_value[1][3]),
                hexbytes.HexBytes(return_value[1][4]),
            ),
            str(return_value[2]),
            eth_typing.ChecksumAddress(return_value[3]),
            int(return_value[4]),
            int(return_value[5]),
            int(return_value[6]),
            int(return_value[7]),
            int(return_value[8]),
            int(return_value[9]),
            int(return_value[10]),
            int(return_value[11]),
            int(return_value[12]),
            str(return_value[13]),
        )

    def proxiable_uuid(
        self,
    ) -> hexbytes.HexBytes:
        """Binding for `proxiableUUID` on the ProductRegistry contract.

        Returns
        -------
        hexbytes.HexBytes
        """
        return_value = self._contract.functions.proxiableUUID().call()
        return hexbytes.HexBytes(return_value)

    def register(
        self,
        product: Product,
    ) -> contract.ContractFunction:
        """Binding for `register` on the ProductRegistry contract.

        Parameters
        ----------
        product : Product

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.register(
            (
                (
                    product.metadata.builder,
                    product.metadata.symbol,
                    product.metadata.description,
                ),
                (
                    product.oracle_spec.oracle_address,
                    product.oracle_spec.fsv_decimals,
                    product.oracle_spec.fsp_alpha,
                    product.oracle_spec.fsp_beta,
                    product.oracle_spec.fsv_calldata,
                ),
                product.price_quotation,
                product.collateral_asset,
                product.start_time,
                product.earliest_fsp_submission_time,
                product.unit_value,
                product.initial_margin_requirement,
                product.maintenance_margin_requirement,
                product.offer_price_buffer,
                product.auction_bounty,
                product.tradeout_interval,
                product.tick_size,
                product.extended_metadata,
            ),
        )

    def renounce_ownership(
        self,
    ) -> contract.ContractFunction:
        """Binding for `renounceOwnership` on the ProductRegistry contract.

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.renounceOwnership()

    def set_clearing(
        self,
        clearing_: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `setClearing` on the ProductRegistry contract.

        Parameters
        ----------
        clearing_ : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.setClearing(
            clearing_,
        )

    def state(
        self,
        product_id: hexbytes.HexBytes,
    ) -> ProductState:
        """Binding for `state` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        ProductState
        """
        return_value = self._contract.functions.state(
            product_id,
        ).call()
        return ProductState(return_value)

    def tick_size(
        self,
        product_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `tickSize` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.tickSize(
            product_id,
        ).call()
        return int(return_value)

    def transfer_ownership(
        self,
        new_owner: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `transferOwnership` on the ProductRegistry contract.

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
        """Binding for `upgradeToAndCall` on the ProductRegistry contract.

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
        {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
        {
            "inputs": [
                {"internalType": "address", "name": "target", "type": "address"}
            ],
            "name": "AddressEmptyCode",
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
        {
            "inputs": [
                {"internalType": "uint256", "name": "startTime", "type": "uint256"},
                {
                    "internalType": "uint256",
                    "name": "earliestFSPSubmissionTime",
                    "type": "uint256",
                },
            ],
            "name": "InvalidFSPSubmissionTime",
            "type": "error",
        },
        {"inputs": [], "name": "InvalidInitialization", "type": "error"},
        {
            "inputs": [
                {"internalType": "uint16", "name": "imr", "type": "uint16"},
                {"internalType": "uint16", "name": "mmr", "type": "uint16"},
            ],
            "name": "InvalidMarginRequirement",
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
                {"internalType": "uint256", "name": "startTime", "type": "uint256"},
                {
                    "internalType": "uint256",
                    "name": "blockTimestamp",
                    "type": "uint256",
                },
            ],
            "name": "InvalidStartTime",
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
                    "internalType": "address",
                    "name": "builder",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "bytes32",
                    "name": "productId",
                    "type": "bytes32",
                },
            ],
            "name": "ProductRegistered",
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
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "auctionBounty",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "clearing",
            "outputs": [
                {
                    "internalType": "contract IClearingSubset",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "collateralAsset",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "earliestFSPSubmissionTime",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "components": [
                        {
                            "components": [
                                {
                                    "internalType": "address",
                                    "name": "builder",
                                    "type": "address",
                                },
                                {
                                    "internalType": "string",
                                    "name": "symbol",
                                    "type": "string",
                                },
                                {
                                    "internalType": "string",
                                    "name": "description",
                                    "type": "string",
                                },
                            ],
                            "internalType": "struct IProductRegistry.ProductMetadata",
                            "name": "metadata",
                            "type": "tuple",
                        },
                        {
                            "components": [
                                {
                                    "internalType": "address",
                                    "name": "oracleAddress",
                                    "type": "address",
                                },
                                {
                                    "internalType": "uint8",
                                    "name": "fsvDecimals",
                                    "type": "uint8",
                                },
                                {
                                    "internalType": "int256",
                                    "name": "fspAlpha",
                                    "type": "int256",
                                },
                                {
                                    "internalType": "int256",
                                    "name": "fspBeta",
                                    "type": "int256",
                                },
                                {
                                    "internalType": "bytes",
                                    "name": "fsvCalldata",
                                    "type": "bytes",
                                },
                            ],
                            "internalType": "struct IProductRegistry.OracleSpecification",
                            "name": "oracleSpec",
                            "type": "tuple",
                        },
                        {
                            "internalType": "string",
                            "name": "priceQuotation",
                            "type": "string",
                        },
                        {
                            "internalType": "address",
                            "name": "collateralAsset",
                            "type": "address",
                        },
                        {
                            "internalType": "uint256",
                            "name": "startTime",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "earliestFSPSubmissionTime",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "unitValue",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint16",
                            "name": "initialMarginRequirement",
                            "type": "uint16",
                        },
                        {
                            "internalType": "uint16",
                            "name": "maintenanceMarginRequirement",
                            "type": "uint16",
                        },
                        {
                            "internalType": "uint64",
                            "name": "offerPriceBuffer",
                            "type": "uint64",
                        },
                        {
                            "internalType": "uint64",
                            "name": "auctionBounty",
                            "type": "uint64",
                        },
                        {
                            "internalType": "uint32",
                            "name": "tradeoutInterval",
                            "type": "uint32",
                        },
                        {"internalType": "uint8", "name": "tickSize", "type": "uint8"},
                        {
                            "internalType": "string",
                            "name": "extendedMetadata",
                            "type": "string",
                        },
                    ],
                    "internalType": "struct IProductRegistry.Product",
                    "name": "product",
                    "type": "tuple",
                }
            ],
            "name": "id",
            "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "stateMutability": "pure",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "imr",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "initialize",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "mmr",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "offerPriceBuffer",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "oracleSpecification",
            "outputs": [
                {
                    "components": [
                        {
                            "internalType": "address",
                            "name": "oracleAddress",
                            "type": "address",
                        },
                        {
                            "internalType": "uint8",
                            "name": "fsvDecimals",
                            "type": "uint8",
                        },
                        {
                            "internalType": "int256",
                            "name": "fspAlpha",
                            "type": "int256",
                        },
                        {"internalType": "int256", "name": "fspBeta", "type": "int256"},
                        {
                            "internalType": "bytes",
                            "name": "fsvCalldata",
                            "type": "bytes",
                        },
                    ],
                    "internalType": "struct IProductRegistry.OracleSpecification",
                    "name": "",
                    "type": "tuple",
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
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "pointValue",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "products",
            "outputs": [
                {
                    "components": [
                        {
                            "components": [
                                {
                                    "internalType": "address",
                                    "name": "builder",
                                    "type": "address",
                                },
                                {
                                    "internalType": "string",
                                    "name": "symbol",
                                    "type": "string",
                                },
                                {
                                    "internalType": "string",
                                    "name": "description",
                                    "type": "string",
                                },
                            ],
                            "internalType": "struct IProductRegistry.ProductMetadata",
                            "name": "metadata",
                            "type": "tuple",
                        },
                        {
                            "components": [
                                {
                                    "internalType": "address",
                                    "name": "oracleAddress",
                                    "type": "address",
                                },
                                {
                                    "internalType": "uint8",
                                    "name": "fsvDecimals",
                                    "type": "uint8",
                                },
                                {
                                    "internalType": "int256",
                                    "name": "fspAlpha",
                                    "type": "int256",
                                },
                                {
                                    "internalType": "int256",
                                    "name": "fspBeta",
                                    "type": "int256",
                                },
                                {
                                    "internalType": "bytes",
                                    "name": "fsvCalldata",
                                    "type": "bytes",
                                },
                            ],
                            "internalType": "struct IProductRegistry.OracleSpecification",
                            "name": "oracleSpec",
                            "type": "tuple",
                        },
                        {
                            "internalType": "string",
                            "name": "priceQuotation",
                            "type": "string",
                        },
                        {
                            "internalType": "address",
                            "name": "collateralAsset",
                            "type": "address",
                        },
                        {
                            "internalType": "uint256",
                            "name": "startTime",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "earliestFSPSubmissionTime",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "unitValue",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint16",
                            "name": "initialMarginRequirement",
                            "type": "uint16",
                        },
                        {
                            "internalType": "uint16",
                            "name": "maintenanceMarginRequirement",
                            "type": "uint16",
                        },
                        {
                            "internalType": "uint64",
                            "name": "offerPriceBuffer",
                            "type": "uint64",
                        },
                        {
                            "internalType": "uint64",
                            "name": "auctionBounty",
                            "type": "uint64",
                        },
                        {
                            "internalType": "uint32",
                            "name": "tradeoutInterval",
                            "type": "uint32",
                        },
                        {"internalType": "uint8", "name": "tickSize", "type": "uint8"},
                        {
                            "internalType": "string",
                            "name": "extendedMetadata",
                            "type": "string",
                        },
                    ],
                    "internalType": "struct IProductRegistry.Product",
                    "name": "",
                    "type": "tuple",
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
            "inputs": [
                {
                    "components": [
                        {
                            "components": [
                                {
                                    "internalType": "address",
                                    "name": "builder",
                                    "type": "address",
                                },
                                {
                                    "internalType": "string",
                                    "name": "symbol",
                                    "type": "string",
                                },
                                {
                                    "internalType": "string",
                                    "name": "description",
                                    "type": "string",
                                },
                            ],
                            "internalType": "struct IProductRegistry.ProductMetadata",
                            "name": "metadata",
                            "type": "tuple",
                        },
                        {
                            "components": [
                                {
                                    "internalType": "address",
                                    "name": "oracleAddress",
                                    "type": "address",
                                },
                                {
                                    "internalType": "uint8",
                                    "name": "fsvDecimals",
                                    "type": "uint8",
                                },
                                {
                                    "internalType": "int256",
                                    "name": "fspAlpha",
                                    "type": "int256",
                                },
                                {
                                    "internalType": "int256",
                                    "name": "fspBeta",
                                    "type": "int256",
                                },
                                {
                                    "internalType": "bytes",
                                    "name": "fsvCalldata",
                                    "type": "bytes",
                                },
                            ],
                            "internalType": "struct IProductRegistry.OracleSpecification",
                            "name": "oracleSpec",
                            "type": "tuple",
                        },
                        {
                            "internalType": "string",
                            "name": "priceQuotation",
                            "type": "string",
                        },
                        {
                            "internalType": "address",
                            "name": "collateralAsset",
                            "type": "address",
                        },
                        {
                            "internalType": "uint256",
                            "name": "startTime",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "earliestFSPSubmissionTime",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "unitValue",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint16",
                            "name": "initialMarginRequirement",
                            "type": "uint16",
                        },
                        {
                            "internalType": "uint16",
                            "name": "maintenanceMarginRequirement",
                            "type": "uint16",
                        },
                        {
                            "internalType": "uint64",
                            "name": "offerPriceBuffer",
                            "type": "uint64",
                        },
                        {
                            "internalType": "uint64",
                            "name": "auctionBounty",
                            "type": "uint64",
                        },
                        {
                            "internalType": "uint32",
                            "name": "tradeoutInterval",
                            "type": "uint32",
                        },
                        {"internalType": "uint8", "name": "tickSize", "type": "uint8"},
                        {
                            "internalType": "string",
                            "name": "extendedMetadata",
                            "type": "string",
                        },
                    ],
                    "internalType": "struct IProductRegistry.Product",
                    "name": "product",
                    "type": "tuple",
                }
            ],
            "name": "register",
            "outputs": [],
            "stateMutability": "nonpayable",
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
                {
                    "internalType": "contract IClearingSubset",
                    "name": "clearing_",
                    "type": "address",
                }
            ],
            "name": "setClearing",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "state",
            "outputs": [
                {"internalType": "enum ProductState", "name": "", "type": "uint8"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "tickSize",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
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
