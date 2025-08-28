"""BankruptcyFacet contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing
from dataclasses import dataclass

import eth_typing
import hexbytes
import web3
from web3.contract import contract


@dataclass
class LAAData:
    """Port of `struct LAAData` on the IBankruptcy contract."""

    owner: eth_typing.ChecksumAddress
    quantity: int
    last_traded_timestamp: int
    position_age: int


@dataclass
class PositionLossData:
    """Port of `struct PositionLossData` on the IBankruptcy contract."""

    position_id: hexbytes.HexBytes
    bankrupt_account_u_pn_l: int
    bankrupt_account_quantity: int
    mark_price: int
    point_value: int
    tick_size: int
    laa_data: typing.List[LAAData]


class BankruptcyFacet:
    """BankruptcyFacet contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed BankruptcyFacet contract.
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

    def last_traded_timestamp(
        self,
        product_id: hexbytes.HexBytes,
        trader: eth_typing.ChecksumAddress,
    ) -> int:
        """Binding for `lastTradedTimestamp` on the BankruptcyFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        trader : eth_typing.ChecksumAddress

        Returns
        -------
        int
        """
        return_value = self._contract.functions.lastTradedTimestamp(
            product_id,
            trader,
        ).call()
        return int(return_value)

    def mutualize_losses(
        self,
        bankrupt_account_id: eth_typing.ChecksumAddress,
        collateral_token: eth_typing.ChecksumAddress,
        product_ids: typing.List[hexbytes.HexBytes],
        laas: typing.List[typing.List[eth_typing.ChecksumAddress]],
    ) -> contract.ContractFunction:
        """Binding for `mutualizeLosses` on the BankruptcyFacet contract.

        Parameters
        ----------
        bankrupt_account_id : eth_typing.ChecksumAddress
        collateral_token : eth_typing.ChecksumAddress
        product_ids : typing.List[hexbytes.HexBytes]
        laas : typing.List[typing.List[eth_typing.ChecksumAddress]]

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.mutualizeLosses(
            bankrupt_account_id,
            collateral_token,
            product_ids,
            laas,
        )

    def unique_trader_count(
        self,
        product_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `uniqueTraderCount` on the BankruptcyFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.uniqueTraderCount(
            product_id,
        ).call()
        return int(return_value)

    def validate_la_as(
        self,
        margin_account: eth_typing.ChecksumAddress,
        bankrupt_account: eth_typing.ChecksumAddress,
        product_id: hexbytes.HexBytes,
        product_owners: typing.List[eth_typing.ChecksumAddress],
    ) -> PositionLossData:
        """Binding for `validateLAAs` on the BankruptcyFacet contract.

        Parameters
        ----------
        margin_account : eth_typing.ChecksumAddress
        bankrupt_account : eth_typing.ChecksumAddress
        product_id : hexbytes.HexBytes
        product_owners : typing.List[eth_typing.ChecksumAddress]

        Returns
        -------
        PositionLossData
        """
        return_value = self._contract.functions.validateLAAs(
            margin_account,
            bankrupt_account,
            product_id,
            product_owners,
        ).call()
        return PositionLossData(
            hexbytes.HexBytes(return_value[0]),
            int(return_value[1]),
            int(return_value[2]),
            int(return_value[3]),
            int(return_value[4]),
            int(return_value[5]),
            [
                LAAData(
                    eth_typing.ChecksumAddress(return_value6_elem[0]),
                    int(return_value6_elem[1]),
                    int(return_value6_elem[2]),
                    int(return_value6_elem[3]),
                )
                for return_value6_elem in return_value[6]
            ],
        )


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "inputs": [
                {"internalType": "address", "name": "account", "type": "address"}
            ],
            "name": "AccountNotBankrupt",
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
                {"internalType": "int256", "name": "neededQuantity", "type": "int256"},
                {
                    "internalType": "int256",
                    "name": "totalLAAQuantity",
                    "type": "int256",
                },
            ],
            "name": "LAAQuantityMismatch",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "neededCount", "type": "uint256"},
                {
                    "internalType": "uint256",
                    "name": "totalLAASetCount",
                    "type": "uint256",
                },
            ],
            "name": "LAASetIncomplete",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "NoTradeData",
            "type": "error",
        },
        {"inputs": [], "name": "QueueIsEmpty", "type": "error"},
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"},
                {"internalType": "address", "name": "trader", "type": "address"},
            ],
            "name": "lastTradedTimestamp",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "bankruptAccountId",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "collateralToken",
                    "type": "address",
                },
                {
                    "internalType": "bytes32[]",
                    "name": "productIds",
                    "type": "bytes32[]",
                },
                {"internalType": "address[][]", "name": "laas", "type": "address[][]"},
            ],
            "name": "mutualizeLosses",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "uniqueTraderCount",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "contract IMarginAccount",
                    "name": "marginAccount",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "bankruptAccount",
                    "type": "address",
                },
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"},
                {
                    "internalType": "address[]",
                    "name": "productOwners",
                    "type": "address[]",
                },
            ],
            "name": "validateLAAs",
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
                            "name": "bankruptAccountUPnL",
                            "type": "int256",
                        },
                        {
                            "internalType": "int256",
                            "name": "bankruptAccountQuantity",
                            "type": "int256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "markPrice",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "pointValue",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "tickSize",
                            "type": "uint256",
                        },
                        {
                            "components": [
                                {
                                    "internalType": "address",
                                    "name": "owner",
                                    "type": "address",
                                },
                                {
                                    "internalType": "int256",
                                    "name": "quantity",
                                    "type": "int256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "lastTradedTimestamp",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "positionAge",
                                    "type": "uint256",
                                },
                            ],
                            "internalType": "struct IBankruptcy.LAAData[]",
                            "name": "laaData",
                            "type": "tuple[]",
                        },
                    ],
                    "internalType": "struct IBankruptcy.PositionLossData",
                    "name": "",
                    "type": "tuple",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
    ],
)
