"""MarkPriceTrackerFacet contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import hexbytes
import web3
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
    ) -> int:
        """Binding for `valuation` on the MarkPriceTrackerFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.valuation(
            product_id,
        ).call()
        return int(return_value)

    def valuation_after_trade(
        self,
        product_id: hexbytes.HexBytes,
        price: int,
        quantity: int,
    ) -> int:
        """Binding for `valuationAfterTrade` on the MarkPriceTrackerFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        price : int
        quantity : int

        Returns
        -------
        int
        """
        return_value = self._contract.functions.valuationAfterTrade(
            product_id,
            price,
            quantity,
        ).call()
        return int(return_value)


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "NoTradeData",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "valuation",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"},
                {"internalType": "uint256", "name": "price", "type": "uint256"},
                {"internalType": "uint256", "name": "quantity", "type": "uint256"},
            ],
            "name": "valuationAfterTrade",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
    ],
)
