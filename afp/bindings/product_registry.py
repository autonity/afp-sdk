"""ProductRegistry contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import hexbytes
import web3
from web3 import types
from web3.contract import contract

from .types import (
    ProductState,
    ExpirySpecification,
    ProductMetadata,
    OracleSpecification,
    BaseProduct,
    MarginSpecification,
    FuturesProductV1,
    PredictionProductV1,
)


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
        block_identifier: types.BlockIdentifier = "latest",
    ) -> str:
        """Binding for `UPGRADE_INTERFACE_VERSION` on the ProductRegistry contract.

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

    def claim_builder_rewards(
        self,
        product_id: hexbytes.HexBytes,
    ) -> contract.ContractFunction:
        """Binding for `claimBuilderRewards` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.claimBuilderRewards(
            product_id,
        )

    def clearing(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `clearing` on the ProductRegistry contract.

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
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `collateralAsset` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.collateralAsset(
            product_id,
        ).call(block_identifier=block_identifier)
        return eth_typing.ChecksumAddress(return_value)

    def earliest_fsp_submission_time(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `earliestFSPSubmissionTime` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.earliestFSPSubmissionTime(
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def futures_product_v1(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> FuturesProductV1:
        """Binding for `futuresProductV1` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        FuturesProductV1
        """
        return_value = self._contract.functions.futuresProductV1(
            product_id,
        ).call(block_identifier=block_identifier)
        return FuturesProductV1(
            BaseProduct(
                ProductMetadata(
                    eth_typing.ChecksumAddress(return_value[0][0][0]),
                    str(return_value[0][0][1]),
                    str(return_value[0][0][2]),
                ),
                OracleSpecification(
                    eth_typing.ChecksumAddress(return_value[0][1][0]),
                    int(return_value[0][1][1]),
                    int(return_value[0][1][2]),
                    int(return_value[0][1][3]),
                    hexbytes.HexBytes(return_value[0][1][4]),
                ),
                eth_typing.ChecksumAddress(return_value[0][2]),
                int(return_value[0][3]),
                int(return_value[0][4]),
                int(return_value[0][5]),
                str(return_value[0][6]),
            ),
            ExpirySpecification(int(return_value[1][0]), int(return_value[1][1])),
            MarginSpecification(int(return_value[2][0]), int(return_value[2][1])),
        )

    def id(
        self,
        product: BaseProduct,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> hexbytes.HexBytes:
        """Binding for `id` on the ProductRegistry contract.

        Parameters
        ----------
        product : BaseProduct
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

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
                product.collateral_asset,
                product.start_time,
                product.point_value,
                product.price_decimals,
                product.extended_metadata,
            ),
        ).call(block_identifier=block_identifier)
        return hexbytes.HexBytes(return_value)

    def increase_builder_stake(
        self,
        product_id: hexbytes.HexBytes,
        fee: int,
    ) -> contract.ContractFunction:
        """Binding for `increaseBuilderStake` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        fee : int

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.increaseBuilderStake(
            product_id,
            fee,
        )

    def initialize(
        self,
        clearing_: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `initialize` on the ProductRegistry contract.

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

    def max_price(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `maxPrice` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.maxPrice(
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def min_price(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `minPrice` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.minPrice(
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def mmr(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `mmr` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.mmr(
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def oracle_specification(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> OracleSpecification:
        """Binding for `oracleSpecification` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        OracleSpecification
        """
        return_value = self._contract.functions.oracleSpecification(
            product_id,
        ).call(block_identifier=block_identifier)
        return OracleSpecification(
            eth_typing.ChecksumAddress(return_value[0]),
            int(return_value[1]),
            int(return_value[2]),
            int(return_value[3]),
            hexbytes.HexBytes(return_value[4]),
        )

    def owner(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `owner` on the ProductRegistry contract.

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

    def point_value(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `pointValue` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.pointValue(
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def prediction_product_v1(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> PredictionProductV1:
        """Binding for `predictionProductV1` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        PredictionProductV1
        """
        return_value = self._contract.functions.predictionProductV1(
            product_id,
        ).call(block_identifier=block_identifier)
        return PredictionProductV1(
            BaseProduct(
                ProductMetadata(
                    eth_typing.ChecksumAddress(return_value[0][0][0]),
                    str(return_value[0][0][1]),
                    str(return_value[0][0][2]),
                ),
                OracleSpecification(
                    eth_typing.ChecksumAddress(return_value[0][1][0]),
                    int(return_value[0][1][1]),
                    int(return_value[0][1][2]),
                    int(return_value[0][1][3]),
                    hexbytes.HexBytes(return_value[0][1][4]),
                ),
                eth_typing.ChecksumAddress(return_value[0][2]),
                int(return_value[0][3]),
                int(return_value[0][4]),
                int(return_value[0][5]),
                str(return_value[0][6]),
            ),
            ExpirySpecification(int(return_value[1][0]), int(return_value[1][1])),
            int(return_value[2]),
            int(return_value[3]),
        )

    def price_decimals(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `priceDecimals` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.priceDecimals(
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def product_treasury(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `productTreasury` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.productTreasury(
            product_id,
        ).call(block_identifier=block_identifier)
        return eth_typing.ChecksumAddress(return_value)

    def products(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.Tuple[int, BaseProduct]:
        """Binding for `products` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        BaseProduct
        """
        return_value = self._contract.functions.products(
            product_id,
        ).call(block_identifier=block_identifier)
        return (
            int(return_value[0]),
            BaseProduct(
                ProductMetadata(
                    eth_typing.ChecksumAddress(return_value[1][0][0]),
                    str(return_value[1][0][1]),
                    str(return_value[1][0][2]),
                ),
                OracleSpecification(
                    eth_typing.ChecksumAddress(return_value[1][1][0]),
                    int(return_value[1][1][1]),
                    int(return_value[1][1][2]),
                    int(return_value[1][1][3]),
                    hexbytes.HexBytes(return_value[1][1][4]),
                ),
                eth_typing.ChecksumAddress(return_value[1][2]),
                int(return_value[1][3]),
                int(return_value[1][4]),
                int(return_value[1][5]),
                str(return_value[1][6]),
            ),
        )

    def proxiable_uuid(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> hexbytes.HexBytes:
        """Binding for `proxiableUUID` on the ProductRegistry contract.

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

    def register_future_product(
        self,
        product: FuturesProductV1,
        initial_builder_stake: int,
    ) -> contract.ContractFunction:
        """Binding for `registerFutureProduct` on the ProductRegistry contract.

        Parameters
        ----------
        product : FuturesProductV1
        initial_builder_stake : int

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.registerFutureProduct(
            (
                (
                    (
                        product.base.metadata.builder,
                        product.base.metadata.symbol,
                        product.base.metadata.description,
                    ),
                    (
                        product.base.oracle_spec.oracle_address,
                        product.base.oracle_spec.fsv_decimals,
                        product.base.oracle_spec.fsp_alpha,
                        product.base.oracle_spec.fsp_beta,
                        product.base.oracle_spec.fsv_calldata,
                    ),
                    product.base.collateral_asset,
                    product.base.start_time,
                    product.base.point_value,
                    product.base.price_decimals,
                    product.base.extended_metadata,
                ),
                (
                    product.expiry_spec.earliest_fsp_submission_time,
                    product.expiry_spec.tradeout_interval,
                ),
                (product.margin_spec.imr, product.margin_spec.mmr),
            ),
            initial_builder_stake,
        )

    def register_prediction_product(
        self,
        product: PredictionProductV1,
        initial_builder_stake: int,
    ) -> contract.ContractFunction:
        """Binding for `registerPredictionProduct` on the ProductRegistry contract.

        Parameters
        ----------
        product : PredictionProductV1
        initial_builder_stake : int

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.registerPredictionProduct(
            (
                (
                    (
                        product.base.metadata.builder,
                        product.base.metadata.symbol,
                        product.base.metadata.description,
                    ),
                    (
                        product.base.oracle_spec.oracle_address,
                        product.base.oracle_spec.fsv_decimals,
                        product.base.oracle_spec.fsp_alpha,
                        product.base.oracle_spec.fsp_beta,
                        product.base.oracle_spec.fsv_calldata,
                    ),
                    product.base.collateral_asset,
                    product.base.start_time,
                    product.base.point_value,
                    product.base.price_decimals,
                    product.base.extended_metadata,
                ),
                (
                    product.expiry_spec.earliest_fsp_submission_time,
                    product.expiry_spec.tradeout_interval,
                ),
                product.max_price,
                product.min_price,
            ),
            initial_builder_stake,
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

    def state(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> ProductState:
        """Binding for `state` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        ProductState
        """
        return_value = self._contract.functions.state(
            product_id,
        ).call(block_identifier=block_identifier)
        return ProductState(return_value)

    def tick_size(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `tickSize` on the ProductRegistry contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.tickSize(
            product_id,
        ).call(block_identifier=block_identifier)
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
        {
            "type": "function",
            "name": "UPGRADE_INTERFACE_VERSION",
            "inputs": [],
            "outputs": [{"name": "", "type": "string", "internalType": "string"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "claimBuilderRewards",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "clearing",
            "inputs": [],
            "outputs": [
                {
                    "name": "",
                    "type": "address",
                    "internalType": "contract IProductRegistryFacet",
                }
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "collateralAsset",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "address", "internalType": "address"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "earliestFSPSubmissionTime",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "futuresProductV1",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [
                {
                    "name": "",
                    "type": "tuple",
                    "internalType": "struct FuturesProductV1",
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
                            "name": "marginSpec",
                            "type": "tuple",
                            "internalType": "struct MarginSpecification",
                            "components": [
                                {
                                    "name": "imr",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "mmr",
                                    "type": "uint256",
                                    "internalType": "uint256",
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
            "name": "id",
            "inputs": [
                {
                    "name": "product",
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
                }
            ],
            "outputs": [{"name": "", "type": "bytes32", "internalType": "bytes32"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "increaseBuilderStake",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"},
                {"name": "fee", "type": "uint256", "internalType": "uint256"},
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "initialize",
            "inputs": [
                {
                    "name": "clearing_",
                    "type": "address",
                    "internalType": "contract IProductRegistryFacet",
                }
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "maxPrice",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "int256", "internalType": "int256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "minPrice",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "int256", "internalType": "int256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "mmr",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "oracleSpecification",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [
                {
                    "name": "",
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
                        {"name": "fspBeta", "type": "int256", "internalType": "int256"},
                        {
                            "name": "fsvCalldata",
                            "type": "bytes",
                            "internalType": "bytes",
                        },
                    ],
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
            "name": "pointValue",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "predictionProductV1",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [
                {
                    "name": "",
                    "type": "tuple",
                    "internalType": "struct PredictionProductV1",
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
            "name": "priceDecimals",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "productTreasury",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "address", "internalType": "address"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "products",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [
                {"name": "", "type": "uint8", "internalType": "enum ProductType"},
                {
                    "name": "",
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
            "name": "registerFutureProduct",
            "inputs": [
                {
                    "name": "product",
                    "type": "tuple",
                    "internalType": "struct FuturesProductV1",
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
                            "name": "marginSpec",
                            "type": "tuple",
                            "internalType": "struct MarginSpecification",
                            "components": [
                                {
                                    "name": "imr",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "mmr",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                            ],
                        },
                    ],
                },
                {
                    "name": "initialBuilderStake",
                    "type": "uint256",
                    "internalType": "uint256",
                },
            ],
            "outputs": [{"name": "", "type": "bytes32", "internalType": "bytes32"}],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "registerPredictionProduct",
            "inputs": [
                {
                    "name": "product",
                    "type": "tuple",
                    "internalType": "struct PredictionProductV1",
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
                },
                {
                    "name": "initialBuilderStake",
                    "type": "uint256",
                    "internalType": "uint256",
                },
            ],
            "outputs": [{"name": "", "type": "bytes32", "internalType": "bytes32"}],
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
            "name": "state",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [
                {"name": "", "type": "uint8", "internalType": "enum ProductState"}
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "tickSize",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
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
            "name": "ProductRegistered",
            "inputs": [
                {
                    "name": "builder",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "productId",
                    "type": "bytes32",
                    "indexed": False,
                    "internalType": "bytes32",
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
