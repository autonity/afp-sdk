"""ProductRegistryFacet contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import hexbytes
import web3
from web3 import types
from web3.contract import contract

from .types import (
    ExpirySpecification,
    ProductMetadata,
    OracleSpecification,
    BaseProduct,
    MarginSpecification,
    FuturesProductV1,
    PredictionProductV1,
)


class ProductRegistryFacet:
    """ProductRegistryFacet contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed ProductRegistryFacet contract.
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

    def expiry_specification(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> ExpirySpecification:
        """Binding for `expirySpecification` on the ProductRegistryFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        ExpirySpecification
        """
        return_value = self._contract.functions.expirySpecification(
            product_id,
        ).call(block_identifier=block_identifier)
        return ExpirySpecification(int(return_value[0]), int(return_value[1]))

    def futures_product_v1(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> FuturesProductV1:
        """Binding for `futuresProductV1` on the ProductRegistryFacet contract.

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
        """Binding for `id` on the ProductRegistryFacet contract.

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

    def mmr(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `mmr` on the ProductRegistryFacet contract.

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

    def prediction_product_v1(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> PredictionProductV1:
        """Binding for `predictionProductV1` on the ProductRegistryFacet contract.

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

    def products(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.Tuple[int, BaseProduct]:
        """Binding for `products` on the ProductRegistryFacet contract.

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

    def register_future_product(
        self,
        product: FuturesProductV1,
    ) -> contract.ContractFunction:
        """Binding for `registerFutureProduct` on the ProductRegistryFacet contract.

        Parameters
        ----------
        product : FuturesProductV1

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
        )

    def register_prediction_product(
        self,
        product: PredictionProductV1,
    ) -> contract.ContractFunction:
        """Binding for `registerPredictionProduct` on the ProductRegistryFacet contract.

        Parameters
        ----------
        product : PredictionProductV1

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
        )

    def state(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `state` on the ProductRegistryFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.state(
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def type_of(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `typeOf` on the ProductRegistryFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.typeOf(
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "type": "function",
            "name": "expirySpecification",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [
                {
                    "name": "",
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
                }
            ],
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
            "stateMutability": "pure",
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
                }
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
                }
            ],
            "outputs": [{"name": "", "type": "bytes32", "internalType": "bytes32"}],
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
            "name": "typeOf",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [
                {"name": "", "type": "uint8", "internalType": "enum ProductType"}
            ],
            "stateMutability": "view",
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
            "name": "InvalidPriceRange",
            "inputs": [
                {"name": "minPrice", "type": "int256", "internalType": "int256"},
                {"name": "maxPrice", "type": "int256", "internalType": "int256"},
            ],
        },
        {
            "type": "error",
            "name": "InvalidProductId",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
        },
        {
            "type": "error",
            "name": "InvalidStartTime",
            "inputs": [
                {"name": "startTime", "type": "uint256", "internalType": "uint256"},
                {
                    "name": "blockTimestamp",
                    "type": "uint256",
                    "internalType": "uint256",
                },
            ],
        },
        {
            "type": "error",
            "name": "NotImplemented",
            "inputs": [{"name": "feature", "type": "string", "internalType": "string"}],
        },
        {
            "type": "error",
            "name": "ProductExists",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
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
