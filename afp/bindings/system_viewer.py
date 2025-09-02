"""SystemViewer contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import enum
import typing
from dataclasses import dataclass

import eth_typing
import hexbytes
import web3
from web3.contract import contract


class ProductState(enum.IntEnum):
    """Port of `enum ProductState` on the SystemViewer contract."""

    NOT_EXIST = 0
    PENDING = 1
    LIVE = 2
    TRADEOUT = 3
    FINAL_SETTLEMENT = 4
    EXPIRED = 5


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


@dataclass
class UserMarginAccountData:
    """Port of `struct UserMarginAccountData` on the ISystemViewer contract."""

    collateral_asset: eth_typing.ChecksumAddress
    margin_account_id: eth_typing.ChecksumAddress
    mae: int
    mmu: int
    positions: typing.List[PositionData]


class SystemViewer:
    """SystemViewer contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed SystemViewer contract.
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
        """Binding for `event Initialized` on the SystemViewer contract."""
        return self._contract.events.Initialized

    @property
    def OwnershipTransferred(self) -> contract.ContractEvent:
        """Binding for `event OwnershipTransferred` on the SystemViewer contract."""
        return self._contract.events.OwnershipTransferred

    @property
    def Upgraded(self) -> contract.ContractEvent:
        """Binding for `event Upgraded` on the SystemViewer contract."""
        return self._contract.events.Upgraded

    def upgrade_interface_version(
        self,
    ) -> str:
        """Binding for `UPGRADE_INTERFACE_VERSION` on the SystemViewer contract.

        Returns
        -------
        str
        """
        return_value = self._contract.functions.UPGRADE_INTERFACE_VERSION().call()
        return str(return_value)

    def clearing(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `clearing` on the SystemViewer contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.clearing().call()
        return eth_typing.ChecksumAddress(return_value)

    def initialize(
        self,
        _clearing: eth_typing.ChecksumAddress,
        _product_registry: eth_typing.ChecksumAddress,
        _margin_account_registry: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `initialize` on the SystemViewer contract.

        Parameters
        ----------
        _clearing : eth_typing.ChecksumAddress
        _product_registry : eth_typing.ChecksumAddress
        _margin_account_registry : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.initialize(
            _clearing,
            _product_registry,
            _margin_account_registry,
        )

    def mae_by_collateral_asset(
        self,
        collateral_asset: eth_typing.ChecksumAddress,
        accounts: typing.List[eth_typing.ChecksumAddress],
    ) -> typing.List[int]:
        """Binding for `maeByCollateralAsset` on the SystemViewer contract.

        Parameters
        ----------
        collateral_asset : eth_typing.ChecksumAddress
        accounts : typing.List[eth_typing.ChecksumAddress]

        Returns
        -------
        typing.List[int]
        """
        return_value = self._contract.functions.maeByCollateralAsset(
            collateral_asset,
            accounts,
        ).call()
        return [int(return_value_elem) for return_value_elem in return_value]

    def mae_by_collateral_assets(
        self,
        collateral_assets: typing.List[eth_typing.ChecksumAddress],
        accounts: typing.List[eth_typing.ChecksumAddress],
    ) -> typing.List[int]:
        """Binding for `maeByCollateralAssets` on the SystemViewer contract.

        Parameters
        ----------
        collateral_assets : typing.List[eth_typing.ChecksumAddress]
        accounts : typing.List[eth_typing.ChecksumAddress]

        Returns
        -------
        typing.List[int]
        """
        return_value = self._contract.functions.maeByCollateralAssets(
            collateral_assets,
            accounts,
        ).call()
        return [int(return_value_elem) for return_value_elem in return_value]

    def mae_checks_by_collateral_asset(
        self,
        collateral_asset: eth_typing.ChecksumAddress,
        accounts: typing.List[eth_typing.ChecksumAddress],
        settlements: typing.List[Settlement],
    ) -> typing.Tuple[typing.List[bool], typing.List[int], typing.List[int]]:
        """Binding for `maeChecksByCollateralAsset` on the SystemViewer contract.

        Parameters
        ----------
        collateral_asset : eth_typing.ChecksumAddress
        accounts : typing.List[eth_typing.ChecksumAddress]
        settlements : typing.List[Settlement]

        Returns
        -------
        typing.List[bool]
        typing.List[int]
        typing.List[int]
        """
        return_value = self._contract.functions.maeChecksByCollateralAsset(
            collateral_asset,
            accounts,
            [(item.position_id, item.quantity, item.price) for item in settlements],
        ).call()
        return (
            [bool(return_value0_elem) for return_value0_elem in return_value[0]],
            [int(return_value1_elem) for return_value1_elem in return_value[1]],
            [int(return_value2_elem) for return_value2_elem in return_value[2]],
        )

    def margin_account_registry(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `marginAccountRegistry` on the SystemViewer contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.marginAccountRegistry().call()
        return eth_typing.ChecksumAddress(return_value)

    def owner(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `owner` on the SystemViewer contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.owner().call()
        return eth_typing.ChecksumAddress(return_value)

    def positions_by_collateral_asset(
        self,
        collateral_asset: eth_typing.ChecksumAddress,
        accounts: typing.List[eth_typing.ChecksumAddress],
    ) -> typing.List[typing.List[PositionData]]:
        """Binding for `positionsByCollateralAsset` on the SystemViewer contract.

        Parameters
        ----------
        collateral_asset : eth_typing.ChecksumAddress
        accounts : typing.List[eth_typing.ChecksumAddress]

        Returns
        -------
        typing.List[typing.List[PositionData]]
        """
        return_value = self._contract.functions.positionsByCollateralAsset(
            collateral_asset,
            accounts,
        ).call()
        return [
            [
                PositionData(
                    hexbytes.HexBytes(return_value_elem[0]),
                    int(return_value_elem[1]),
                    int(return_value_elem[2]),
                    int(return_value_elem[3]),
                    int(return_value_elem[4]),
                )
                for return_value_elem in return_value_list0
            ]
            for return_value_list0 in return_value
        ]

    def positions_by_collateral_assets(
        self,
        collateral_assets: typing.List[eth_typing.ChecksumAddress],
        accounts: typing.List[eth_typing.ChecksumAddress],
    ) -> typing.List[typing.List[PositionData]]:
        """Binding for `positionsByCollateralAssets` on the SystemViewer contract.

        Parameters
        ----------
        collateral_assets : typing.List[eth_typing.ChecksumAddress]
        accounts : typing.List[eth_typing.ChecksumAddress]

        Returns
        -------
        typing.List[typing.List[PositionData]]
        """
        return_value = self._contract.functions.positionsByCollateralAssets(
            collateral_assets,
            accounts,
        ).call()
        return [
            [
                PositionData(
                    hexbytes.HexBytes(return_value_elem[0]),
                    int(return_value_elem[1]),
                    int(return_value_elem[2]),
                    int(return_value_elem[3]),
                    int(return_value_elem[4]),
                )
                for return_value_elem in return_value_list0
            ]
            for return_value_list0 in return_value
        ]

    def product_details(
        self,
        product_ids: typing.List[hexbytes.HexBytes],
    ) -> typing.List[Product]:
        """Binding for `productDetails` on the SystemViewer contract.

        Parameters
        ----------
        product_ids : typing.List[hexbytes.HexBytes]

        Returns
        -------
        typing.List[Product]
        """
        return_value = self._contract.functions.productDetails(
            product_ids,
        ).call()
        return [
            Product(
                ProductMetadata(
                    eth_typing.ChecksumAddress(return_value_elem[0][0]),
                    str(return_value_elem[0][1]),
                    str(return_value_elem[0][2]),
                ),
                OracleSpecification(
                    eth_typing.ChecksumAddress(return_value_elem[1][0]),
                    int(return_value_elem[1][1]),
                    int(return_value_elem[1][2]),
                    int(return_value_elem[1][3]),
                    hexbytes.HexBytes(return_value_elem[1][4]),
                ),
                str(return_value_elem[2]),
                eth_typing.ChecksumAddress(return_value_elem[3]),
                int(return_value_elem[4]),
                int(return_value_elem[5]),
                int(return_value_elem[6]),
                int(return_value_elem[7]),
                int(return_value_elem[8]),
                int(return_value_elem[9]),
                int(return_value_elem[10]),
                int(return_value_elem[11]),
                int(return_value_elem[12]),
                str(return_value_elem[13]),
            )
            for return_value_elem in return_value
        ]

    def product_registry(
        self,
    ) -> eth_typing.ChecksumAddress:
        """Binding for `productRegistry` on the SystemViewer contract.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.productRegistry().call()
        return eth_typing.ChecksumAddress(return_value)

    def product_states(
        self,
        product_ids: typing.List[hexbytes.HexBytes],
    ) -> typing.List[ProductState]:
        """Binding for `productStates` on the SystemViewer contract.

        Parameters
        ----------
        product_ids : typing.List[hexbytes.HexBytes]

        Returns
        -------
        typing.List[ProductState]
        """
        return_value = self._contract.functions.productStates(
            product_ids,
        ).call()
        return [ProductState(return_value_elem) for return_value_elem in return_value]

    def proxiable_uuid(
        self,
    ) -> hexbytes.HexBytes:
        """Binding for `proxiableUUID` on the SystemViewer contract.

        Returns
        -------
        hexbytes.HexBytes
        """
        return_value = self._contract.functions.proxiableUUID().call()
        return hexbytes.HexBytes(return_value)

    def renounce_ownership(
        self,
    ) -> contract.ContractFunction:
        """Binding for `renounceOwnership` on the SystemViewer contract.

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
        """Binding for `transferOwnership` on the SystemViewer contract.

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
        """Binding for `upgradeToAndCall` on the SystemViewer contract.

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

    def user_margin_data_by_collateral_asset(
        self,
        collateral_asset: eth_typing.ChecksumAddress,
        accounts: typing.List[eth_typing.ChecksumAddress],
    ) -> typing.List[UserMarginAccountData]:
        """Binding for `userMarginDataByCollateralAsset` on the SystemViewer contract.

        Parameters
        ----------
        collateral_asset : eth_typing.ChecksumAddress
        accounts : typing.List[eth_typing.ChecksumAddress]

        Returns
        -------
        typing.List[UserMarginAccountData]
        """
        return_value = self._contract.functions.userMarginDataByCollateralAsset(
            collateral_asset,
            accounts,
        ).call()
        return [
            UserMarginAccountData(
                eth_typing.ChecksumAddress(return_value_elem[0]),
                eth_typing.ChecksumAddress(return_value_elem[1]),
                int(return_value_elem[2]),
                int(return_value_elem[3]),
                [
                    PositionData(
                        hexbytes.HexBytes(return_value_elem4_elem[0]),
                        int(return_value_elem4_elem[1]),
                        int(return_value_elem4_elem[2]),
                        int(return_value_elem4_elem[3]),
                        int(return_value_elem4_elem[4]),
                    )
                    for return_value_elem4_elem in return_value_elem[4]
                ],
            )
            for return_value_elem in return_value
        ]

    def user_margin_data_by_collateral_assets(
        self,
        collateral_assets: typing.List[eth_typing.ChecksumAddress],
        accounts: typing.List[eth_typing.ChecksumAddress],
    ) -> typing.List[UserMarginAccountData]:
        """Binding for `userMarginDataByCollateralAssets` on the SystemViewer contract.

        Parameters
        ----------
        collateral_assets : typing.List[eth_typing.ChecksumAddress]
        accounts : typing.List[eth_typing.ChecksumAddress]

        Returns
        -------
        typing.List[UserMarginAccountData]
        """
        return_value = self._contract.functions.userMarginDataByCollateralAssets(
            collateral_assets,
            accounts,
        ).call()
        return [
            UserMarginAccountData(
                eth_typing.ChecksumAddress(return_value_elem[0]),
                eth_typing.ChecksumAddress(return_value_elem[1]),
                int(return_value_elem[2]),
                int(return_value_elem[3]),
                [
                    PositionData(
                        hexbytes.HexBytes(return_value_elem4_elem[0]),
                        int(return_value_elem4_elem[1]),
                        int(return_value_elem4_elem[2]),
                        int(return_value_elem4_elem[3]),
                        int(return_value_elem4_elem[4]),
                    )
                    for return_value_elem4_elem in return_value_elem[4]
                ],
            )
            for return_value_elem in return_value
        ]

    def valuations(
        self,
        product_ids: typing.List[hexbytes.HexBytes],
    ) -> typing.List[int]:
        """Binding for `valuations` on the SystemViewer contract.

        Parameters
        ----------
        product_ids : typing.List[hexbytes.HexBytes]

        Returns
        -------
        typing.List[int]
        """
        return_value = self._contract.functions.valuations(
            product_ids,
        ).call()
        return [int(return_value_elem) for return_value_elem in return_value]


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
                {"internalType": "address", "name": "implementation", "type": "address"}
            ],
            "name": "ERC1967InvalidImplementation",
            "type": "error",
        },
        {"inputs": [], "name": "ERC1967NonPayable", "type": "error"},
        {"inputs": [], "name": "FailedCall", "type": "error"},
        {"inputs": [], "name": "InvalidInitialization", "type": "error"},
        {
            "inputs": [{"internalType": "string", "name": "reason", "type": "string"}],
            "name": "InvalidParameters",
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
            "outputs": [
                {
                    "internalType": "contract IClearingDiamond",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "contract IClearingDiamond",
                    "name": "_clearing",
                    "type": "address",
                },
                {
                    "internalType": "contract IProductRegistry",
                    "name": "_productRegistry",
                    "type": "address",
                },
                {
                    "internalType": "contract IMarginAccountRegistry",
                    "name": "_marginAccountRegistry",
                    "type": "address",
                },
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
                },
                {"internalType": "address[]", "name": "accounts", "type": "address[]"},
            ],
            "name": "maeByCollateralAsset",
            "outputs": [
                {"internalType": "int256[]", "name": "results", "type": "int256[]"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address[]",
                    "name": "collateralAssets",
                    "type": "address[]",
                },
                {"internalType": "address[]", "name": "accounts", "type": "address[]"},
            ],
            "name": "maeByCollateralAssets",
            "outputs": [
                {"internalType": "int256[]", "name": "results", "type": "int256[]"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "collateralAsset",
                    "type": "address",
                },
                {"internalType": "address[]", "name": "accounts", "type": "address[]"},
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
            "name": "maeChecksByCollateralAsset",
            "outputs": [
                {"internalType": "bool[]", "name": "results", "type": "bool[]"},
                {"internalType": "int256[]", "name": "maeAfter", "type": "int256[]"},
                {"internalType": "uint256[]", "name": "mmuAfter", "type": "uint256[]"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "marginAccountRegistry",
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
            "name": "owner",
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
                },
                {"internalType": "address[]", "name": "accounts", "type": "address[]"},
            ],
            "name": "positionsByCollateralAsset",
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
                    "internalType": "struct IMarginAccount.PositionData[][]",
                    "name": "results",
                    "type": "tuple[][]",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address[]",
                    "name": "collateralAssets",
                    "type": "address[]",
                },
                {"internalType": "address[]", "name": "accounts", "type": "address[]"},
            ],
            "name": "positionsByCollateralAssets",
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
                    "internalType": "struct IMarginAccount.PositionData[][]",
                    "name": "results",
                    "type": "tuple[][]",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32[]", "name": "productIds", "type": "bytes32[]"}
            ],
            "name": "productDetails",
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
                    "internalType": "struct IProductRegistry.Product[]",
                    "name": "details",
                    "type": "tuple[]",
                }
            ],
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
                {"internalType": "bytes32[]", "name": "productIds", "type": "bytes32[]"}
            ],
            "name": "productStates",
            "outputs": [
                {
                    "internalType": "enum ProductState[]",
                    "name": "states",
                    "type": "uint8[]",
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
            "inputs": [
                {
                    "internalType": "address",
                    "name": "collateralAsset",
                    "type": "address",
                },
                {"internalType": "address[]", "name": "accounts", "type": "address[]"},
            ],
            "name": "userMarginDataByCollateralAsset",
            "outputs": [
                {
                    "components": [
                        {
                            "internalType": "address",
                            "name": "collateralAsset",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "marginAccountId",
                            "type": "address",
                        },
                        {"internalType": "int256", "name": "mae", "type": "int256"},
                        {"internalType": "uint256", "name": "mmu", "type": "uint256"},
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
                                {
                                    "internalType": "int256",
                                    "name": "pnl",
                                    "type": "int256",
                                },
                            ],
                            "internalType": "struct IMarginAccount.PositionData[]",
                            "name": "positions",
                            "type": "tuple[]",
                        },
                    ],
                    "internalType": "struct ISystemViewer.UserMarginAccountData[]",
                    "name": "data",
                    "type": "tuple[]",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address[]",
                    "name": "collateralAssets",
                    "type": "address[]",
                },
                {"internalType": "address[]", "name": "accounts", "type": "address[]"},
            ],
            "name": "userMarginDataByCollateralAssets",
            "outputs": [
                {
                    "components": [
                        {
                            "internalType": "address",
                            "name": "collateralAsset",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "marginAccountId",
                            "type": "address",
                        },
                        {"internalType": "int256", "name": "mae", "type": "int256"},
                        {"internalType": "uint256", "name": "mmu", "type": "uint256"},
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
                                {
                                    "internalType": "int256",
                                    "name": "pnl",
                                    "type": "int256",
                                },
                            ],
                            "internalType": "struct IMarginAccount.PositionData[]",
                            "name": "positions",
                            "type": "tuple[]",
                        },
                    ],
                    "internalType": "struct ISystemViewer.UserMarginAccountData[]",
                    "name": "data",
                    "type": "tuple[]",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32[]", "name": "productIds", "type": "bytes32[]"}
            ],
            "name": "valuations",
            "outputs": [
                {"internalType": "uint256[]", "name": "prices", "type": "uint256[]"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
    ],
)
