"""SystemViewer contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import enum
import typing
from dataclasses import dataclass

import eth_typing
import hexbytes
import web3
from web3 import types
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
    """Port of `struct Settlement` on the SystemViewer contract."""

    product_id: hexbytes.HexBytes
    quantity: int
    price: int


@dataclass
class PositionData:
    """Port of `struct PositionData` on the SystemViewer contract."""

    product_id: hexbytes.HexBytes
    quantity: int
    cost_basis: int
    maintenance_margin: int
    pnl: int


@dataclass
class ProductMetadata:
    """Port of `struct ProductMetadata` on the SystemViewer contract."""

    builder: eth_typing.ChecksumAddress
    symbol: str
    description: str


@dataclass
class OracleSpecification:
    """Port of `struct OracleSpecification` on the SystemViewer contract."""

    oracle_address: eth_typing.ChecksumAddress
    fsv_decimals: int
    fsp_alpha: int
    fsp_beta: int
    fsv_calldata: hexbytes.HexBytes


@dataclass
class BaseProduct:
    """Port of `struct BaseProduct` on the SystemViewer contract."""

    metadata: ProductMetadata
    oracle_spec: OracleSpecification
    collateral_asset: eth_typing.ChecksumAddress
    start_time: int
    point_value: int
    price_decimals: int
    extended_metadata: str


@dataclass
class ExpirySpecification:
    """Port of `struct ExpirySpecification` on the SystemViewer contract."""

    earliest_fsp_submission_time: int
    tradeout_interval: int


@dataclass
class PredictionProductV1:
    """Port of `struct PredictionProductV1` on the SystemViewer contract."""

    base: BaseProduct
    expiry_spec: ExpirySpecification
    max_price: int
    min_price: int


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
        block_identifier: types.BlockIdentifier = "latest",
    ) -> str:
        """Binding for `UPGRADE_INTERFACE_VERSION` on the SystemViewer contract.

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

    def clearing(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `clearing` on the SystemViewer contract.

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
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[int]:
        """Binding for `maeByCollateralAsset` on the SystemViewer contract.

        Parameters
        ----------
        collateral_asset : eth_typing.ChecksumAddress
        accounts : typing.List[eth_typing.ChecksumAddress]
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[int]
        """
        return_value = self._contract.functions.maeByCollateralAsset(
            collateral_asset,
            accounts,
        ).call(block_identifier=block_identifier)
        return [int(return_value_elem) for return_value_elem in return_value]

    def mae_by_collateral_assets(
        self,
        collateral_assets: typing.List[eth_typing.ChecksumAddress],
        accounts: typing.List[eth_typing.ChecksumAddress],
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[int]:
        """Binding for `maeByCollateralAssets` on the SystemViewer contract.

        Parameters
        ----------
        collateral_assets : typing.List[eth_typing.ChecksumAddress]
        accounts : typing.List[eth_typing.ChecksumAddress]
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[int]
        """
        return_value = self._contract.functions.maeByCollateralAssets(
            collateral_assets,
            accounts,
        ).call(block_identifier=block_identifier)
        return [int(return_value_elem) for return_value_elem in return_value]

    def mae_checks(
        self,
        accounts: typing.List[eth_typing.ChecksumAddress],
        settlements: typing.List[Settlement],
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.Tuple[typing.List[bool], typing.List[int], typing.List[int]]:
        """Binding for `maeChecks` on the SystemViewer contract.

        Parameters
        ----------
        accounts : typing.List[eth_typing.ChecksumAddress]
        settlements : typing.List[Settlement]
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[bool]
        typing.List[int]
        typing.List[int]
        """
        return_value = self._contract.functions.maeChecks(
            accounts,
            [(item.product_id, item.quantity, item.price) for item in settlements],
        ).call(block_identifier=block_identifier)
        return (
            [bool(return_value0_elem) for return_value0_elem in return_value[0]],
            [int(return_value1_elem) for return_value1_elem in return_value[1]],
            [int(return_value2_elem) for return_value2_elem in return_value[2]],
        )

    def margin_account_registry(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `marginAccountRegistry` on the SystemViewer contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.marginAccountRegistry().call(
            block_identifier=block_identifier
        )
        return eth_typing.ChecksumAddress(return_value)

    def owner(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `owner` on the SystemViewer contract.

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

    def position_quantities_by_product_id(
        self,
        product_id: hexbytes.HexBytes,
        accounts: typing.List[eth_typing.ChecksumAddress],
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[int]:
        """Binding for `positionQuantitiesByProductId` on the SystemViewer contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        accounts : typing.List[eth_typing.ChecksumAddress]
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[int]
        """
        return_value = self._contract.functions.positionQuantitiesByProductId(
            product_id,
            accounts,
        ).call(block_identifier=block_identifier)
        return [int(return_value_elem) for return_value_elem in return_value]

    def position_quantities_by_product_ids(
        self,
        product_ids: typing.List[hexbytes.HexBytes],
        accounts: typing.List[eth_typing.ChecksumAddress],
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[int]:
        """Binding for `positionQuantitiesByProductIds` on the SystemViewer contract.

        Parameters
        ----------
        product_ids : typing.List[hexbytes.HexBytes]
        accounts : typing.List[eth_typing.ChecksumAddress]
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[int]
        """
        return_value = self._contract.functions.positionQuantitiesByProductIds(
            product_ids,
            accounts,
        ).call(block_identifier=block_identifier)
        return [int(return_value_elem) for return_value_elem in return_value]

    def positions_by_collateral_asset(
        self,
        collateral_asset: eth_typing.ChecksumAddress,
        accounts: typing.List[eth_typing.ChecksumAddress],
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[typing.List[PositionData]]:
        """Binding for `positionsByCollateralAsset` on the SystemViewer contract.

        Parameters
        ----------
        collateral_asset : eth_typing.ChecksumAddress
        accounts : typing.List[eth_typing.ChecksumAddress]
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[typing.List[PositionData]]
        """
        return_value = self._contract.functions.positionsByCollateralAsset(
            collateral_asset,
            accounts,
        ).call(block_identifier=block_identifier)
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
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[typing.List[PositionData]]:
        """Binding for `positionsByCollateralAssets` on the SystemViewer contract.

        Parameters
        ----------
        collateral_assets : typing.List[eth_typing.ChecksumAddress]
        accounts : typing.List[eth_typing.ChecksumAddress]
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[typing.List[PositionData]]
        """
        return_value = self._contract.functions.positionsByCollateralAssets(
            collateral_assets,
            accounts,
        ).call(block_identifier=block_identifier)
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
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[PredictionProductV1]:
        """Binding for `productDetails` on the SystemViewer contract.

        Parameters
        ----------
        product_ids : typing.List[hexbytes.HexBytes]
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[PredictionProductV1]
        """
        return_value = self._contract.functions.productDetails(
            product_ids,
        ).call(block_identifier=block_identifier)
        return [
            PredictionProductV1(
                BaseProduct(
                    ProductMetadata(
                        eth_typing.ChecksumAddress(return_value_elem[0][0][0]),
                        str(return_value_elem[0][0][1]),
                        str(return_value_elem[0][0][2]),
                    ),
                    OracleSpecification(
                        eth_typing.ChecksumAddress(return_value_elem[0][1][0]),
                        int(return_value_elem[0][1][1]),
                        int(return_value_elem[0][1][2]),
                        int(return_value_elem[0][1][3]),
                        hexbytes.HexBytes(return_value_elem[0][1][4]),
                    ),
                    eth_typing.ChecksumAddress(return_value_elem[0][2]),
                    int(return_value_elem[0][3]),
                    int(return_value_elem[0][4]),
                    int(return_value_elem[0][5]),
                    str(return_value_elem[0][6]),
                ),
                ExpirySpecification(
                    int(return_value_elem[1][0]), int(return_value_elem[1][1])
                ),
                int(return_value_elem[2]),
                int(return_value_elem[3]),
            )
            for return_value_elem in return_value
        ]

    def product_registry(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `productRegistry` on the SystemViewer contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.productRegistry().call(
            block_identifier=block_identifier
        )
        return eth_typing.ChecksumAddress(return_value)

    def product_states(
        self,
        product_ids: typing.List[hexbytes.HexBytes],
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[ProductState]:
        """Binding for `productStates` on the SystemViewer contract.

        Parameters
        ----------
        product_ids : typing.List[hexbytes.HexBytes]
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[ProductState]
        """
        return_value = self._contract.functions.productStates(
            product_ids,
        ).call(block_identifier=block_identifier)
        return [ProductState(return_value_elem) for return_value_elem in return_value]

    def proxiable_uuid(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> hexbytes.HexBytes:
        """Binding for `proxiableUUID` on the SystemViewer contract.

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
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[UserMarginAccountData]:
        """Binding for `userMarginDataByCollateralAsset` on the SystemViewer contract.

        Parameters
        ----------
        collateral_asset : eth_typing.ChecksumAddress
        accounts : typing.List[eth_typing.ChecksumAddress]
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[UserMarginAccountData]
        """
        return_value = self._contract.functions.userMarginDataByCollateralAsset(
            collateral_asset,
            accounts,
        ).call(block_identifier=block_identifier)
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
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[UserMarginAccountData]:
        """Binding for `userMarginDataByCollateralAssets` on the SystemViewer contract.

        Parameters
        ----------
        collateral_assets : typing.List[eth_typing.ChecksumAddress]
        accounts : typing.List[eth_typing.ChecksumAddress]
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[UserMarginAccountData]
        """
        return_value = self._contract.functions.userMarginDataByCollateralAssets(
            collateral_assets,
            accounts,
        ).call(block_identifier=block_identifier)
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
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.List[int]:
        """Binding for `valuations` on the SystemViewer contract.

        Parameters
        ----------
        product_ids : typing.List[hexbytes.HexBytes]
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        typing.List[int]
        """
        return_value = self._contract.functions.valuations(
            product_ids,
        ).call(block_identifier=block_identifier)
        return [int(return_value_elem) for return_value_elem in return_value]


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
            "name": "clearing",
            "inputs": [],
            "outputs": [{"name": "", "type": "address", "internalType": "address"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "initialize",
            "inputs": [
                {"name": "_clearing", "type": "address", "internalType": "address"},
                {
                    "name": "_productRegistry",
                    "type": "address",
                    "internalType": "contract IProductRegistry",
                },
                {
                    "name": "_marginAccountRegistry",
                    "type": "address",
                    "internalType": "contract IMarginAccountRegistry",
                },
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "maeByCollateralAsset",
            "inputs": [
                {
                    "name": "collateralAsset",
                    "type": "address",
                    "internalType": "address",
                },
                {"name": "accounts", "type": "address[]", "internalType": "address[]"},
            ],
            "outputs": [
                {"name": "results", "type": "int256[]", "internalType": "int256[]"}
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "maeByCollateralAssets",
            "inputs": [
                {
                    "name": "collateralAssets",
                    "type": "address[]",
                    "internalType": "address[]",
                },
                {"name": "accounts", "type": "address[]", "internalType": "address[]"},
            ],
            "outputs": [
                {"name": "results", "type": "int256[]", "internalType": "int256[]"}
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "maeChecks",
            "inputs": [
                {"name": "accounts", "type": "address[]", "internalType": "address[]"},
                {
                    "name": "settlements",
                    "type": "tuple[]",
                    "internalType": "struct Settlement[]",
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
                {"name": "results", "type": "bool[]", "internalType": "bool[]"},
                {"name": "maeAfter", "type": "int256[]", "internalType": "int256[]"},
                {"name": "mmuAfter", "type": "uint256[]", "internalType": "uint256[]"},
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "marginAccountRegistry",
            "inputs": [],
            "outputs": [
                {
                    "name": "",
                    "type": "address",
                    "internalType": "contract IMarginAccountRegistry",
                }
            ],
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
            "name": "positionQuantitiesByProductId",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"},
                {"name": "accounts", "type": "address[]", "internalType": "address[]"},
            ],
            "outputs": [
                {"name": "quantity", "type": "int256[]", "internalType": "int256[]"}
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "positionQuantitiesByProductIds",
            "inputs": [
                {
                    "name": "productIds",
                    "type": "bytes32[]",
                    "internalType": "bytes32[]",
                },
                {"name": "accounts", "type": "address[]", "internalType": "address[]"},
            ],
            "outputs": [
                {"name": "quantity", "type": "int256[]", "internalType": "int256[]"}
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "positionsByCollateralAsset",
            "inputs": [
                {
                    "name": "collateralAsset",
                    "type": "address",
                    "internalType": "address",
                },
                {"name": "accounts", "type": "address[]", "internalType": "address[]"},
            ],
            "outputs": [
                {
                    "name": "results",
                    "type": "tuple[][]",
                    "internalType": "struct PositionData[][]",
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
            "name": "positionsByCollateralAssets",
            "inputs": [
                {
                    "name": "collateralAssets",
                    "type": "address[]",
                    "internalType": "address[]",
                },
                {"name": "accounts", "type": "address[]", "internalType": "address[]"},
            ],
            "outputs": [
                {
                    "name": "results",
                    "type": "tuple[][]",
                    "internalType": "struct PositionData[][]",
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
            "name": "productDetails",
            "inputs": [
                {"name": "productIds", "type": "bytes32[]", "internalType": "bytes32[]"}
            ],
            "outputs": [
                {
                    "name": "details",
                    "type": "tuple[]",
                    "internalType": "struct PredictionProductV1[]",
                    "components": [
                        {
                            "name": "base",
                            "type": "tuple",
                            "internalType": "struct BaseProduct",
                            "components": [
                                {
                                    "name": "metadata",
                                    "type": "tuple",
                                    "internalType": "struct ProductMetadata",
                                    "components": [
                                        {
                                            "name": "builder",
                                            "type": "address",
                                            "internalType": "address",
                                        },
                                        {
                                            "name": "symbol",
                                            "type": "string",
                                            "internalType": "string",
                                        },
                                        {
                                            "name": "description",
                                            "type": "string",
                                            "internalType": "string",
                                        },
                                    ],
                                },
                                {
                                    "name": "oracleSpec",
                                    "type": "tuple",
                                    "internalType": "struct OracleSpecification",
                                    "components": [
                                        {
                                            "name": "oracleAddress",
                                            "type": "address",
                                            "internalType": "address",
                                        },
                                        {
                                            "name": "fsvDecimals",
                                            "type": "uint8",
                                            "internalType": "uint8",
                                        },
                                        {
                                            "name": "fspAlpha",
                                            "type": "int256",
                                            "internalType": "int256",
                                        },
                                        {
                                            "name": "fspBeta",
                                            "type": "int256",
                                            "internalType": "int256",
                                        },
                                        {
                                            "name": "fsvCalldata",
                                            "type": "bytes",
                                            "internalType": "bytes",
                                        },
                                    ],
                                },
                                {
                                    "name": "collateralAsset",
                                    "type": "address",
                                    "internalType": "address",
                                },
                                {
                                    "name": "startTime",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "pointValue",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "priceDecimals",
                                    "type": "uint8",
                                    "internalType": "uint8",
                                },
                                {
                                    "name": "extendedMetadata",
                                    "type": "string",
                                    "internalType": "string",
                                },
                            ],
                        },
                        {
                            "name": "expirySpec",
                            "type": "tuple",
                            "internalType": "struct ExpirySpecification",
                            "components": [
                                {
                                    "name": "earliestFSPSubmissionTime",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "tradeoutInterval",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                            ],
                        },
                        {
                            "name": "maxPrice",
                            "type": "int256",
                            "internalType": "int256",
                        },
                        {
                            "name": "minPrice",
                            "type": "int256",
                            "internalType": "int256",
                        },
                    ],
                }
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "productRegistry",
            "inputs": [],
            "outputs": [
                {
                    "name": "",
                    "type": "address",
                    "internalType": "contract IProductRegistry",
                }
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "productStates",
            "inputs": [
                {"name": "productIds", "type": "bytes32[]", "internalType": "bytes32[]"}
            ],
            "outputs": [
                {
                    "name": "states",
                    "type": "uint8[]",
                    "internalType": "enum ProductState[]",
                }
            ],
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
            "type": "function",
            "name": "userMarginDataByCollateralAsset",
            "inputs": [
                {
                    "name": "collateralAsset",
                    "type": "address",
                    "internalType": "address",
                },
                {"name": "accounts", "type": "address[]", "internalType": "address[]"},
            ],
            "outputs": [
                {
                    "name": "data",
                    "type": "tuple[]",
                    "internalType": "struct ISystemViewer.UserMarginAccountData[]",
                    "components": [
                        {
                            "name": "collateralAsset",
                            "type": "address",
                            "internalType": "address",
                        },
                        {
                            "name": "marginAccountId",
                            "type": "address",
                            "internalType": "address",
                        },
                        {"name": "mae", "type": "int256", "internalType": "int256"},
                        {"name": "mmu", "type": "uint256", "internalType": "uint256"},
                        {
                            "name": "positions",
                            "type": "tuple[]",
                            "internalType": "struct PositionData[]",
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
                                {
                                    "name": "pnl",
                                    "type": "int256",
                                    "internalType": "int256",
                                },
                            ],
                        },
                    ],
                }
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "userMarginDataByCollateralAssets",
            "inputs": [
                {
                    "name": "collateralAssets",
                    "type": "address[]",
                    "internalType": "address[]",
                },
                {"name": "accounts", "type": "address[]", "internalType": "address[]"},
            ],
            "outputs": [
                {
                    "name": "data",
                    "type": "tuple[]",
                    "internalType": "struct ISystemViewer.UserMarginAccountData[]",
                    "components": [
                        {
                            "name": "collateralAsset",
                            "type": "address",
                            "internalType": "address",
                        },
                        {
                            "name": "marginAccountId",
                            "type": "address",
                            "internalType": "address",
                        },
                        {"name": "mae", "type": "int256", "internalType": "int256"},
                        {"name": "mmu", "type": "uint256", "internalType": "uint256"},
                        {
                            "name": "positions",
                            "type": "tuple[]",
                            "internalType": "struct PositionData[]",
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
                                {
                                    "name": "pnl",
                                    "type": "int256",
                                    "internalType": "int256",
                                },
                            ],
                        },
                    ],
                }
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "valuations",
            "inputs": [
                {"name": "productIds", "type": "bytes32[]", "internalType": "bytes32[]"}
            ],
            "outputs": [
                {"name": "prices", "type": "int256[]", "internalType": "int256[]"}
            ],
            "stateMutability": "view",
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
        {
            "type": "error",
            "name": "InvalidParameters",
            "inputs": [{"name": "reason", "type": "string", "internalType": "string"}],
        },
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
