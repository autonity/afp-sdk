"""MarkPriceTrackerFacet contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import hexbytes
import web3
from web3 import types
from web3.contract import contract


class MarkPriceTrackerFacet:
    """MarkPriceTrackerFacet contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed MarkPriceTrackerFacet contract.
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

    def valuation(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `valuation` on the MarkPriceTrackerFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.valuation(
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

    def valuation_after_trade(
        self,
        product_id: hexbytes.HexBytes,
        price: int,
        quantity: int,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `valuationAfterTrade` on the MarkPriceTrackerFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        price : int
        quantity : int
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.valuationAfterTrade(
            product_id,
            price,
            quantity,
        ).call(block_identifier=block_identifier)
        return int(return_value)


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "type": "function",
            "name": "valuation",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "int256", "internalType": "int256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "valuationAfterTrade",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"},
                {"name": "price", "type": "int256", "internalType": "int256"},
                {"name": "quantity", "type": "uint256", "internalType": "uint256"},
            ],
            "outputs": [{"name": "", "type": "int256", "internalType": "int256"}],
            "stateMutability": "view",
        },
        {"type": "error", "name": "EVWMA_NotInitialized", "inputs": []},
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
    ],
)
