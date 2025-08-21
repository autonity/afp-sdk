"""FinalSettlementFacet contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import hexbytes
import web3
from web3.contract import contract


class FinalSettlementFacet:
    """FinalSettlementFacet contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed FinalSettlementFacet contract.
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

    def closeout_fee_rate(
        self,
    ) -> int:
        """Binding for `CLOSEOUT_FEE_RATE` on the FinalSettlementFacet contract.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.CLOSEOUT_FEE_RATE().call()
        return int(return_value)

    def closeout_reward_rate(
        self,
    ) -> int:
        """Binding for `CLOSEOUT_REWARD_RATE` on the FinalSettlementFacet contract.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.CLOSEOUT_REWARD_RATE().call()
        return int(return_value)

    def finalize_fsp(
        self,
        product_id: hexbytes.HexBytes,
    ) -> contract.ContractFunction:
        """Binding for `finalizeFsp` on the FinalSettlementFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.finalizeFsp(
            product_id,
        )

    def get_fsp(
        self,
        product_id: hexbytes.HexBytes,
    ) -> typing.Tuple[int, bool]:
        """Binding for `getFsp` on the FinalSettlementFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        int
        bool
        """
        return_value = self._contract.functions.getFsp(
            product_id,
        ).call()
        return (
            int(return_value[0]),
            bool(return_value[1]),
        )

    def initiate_final_settlement(
        self,
        product_id: hexbytes.HexBytes,
        accounts: typing.List[eth_typing.ChecksumAddress],
    ) -> contract.ContractFunction:
        """Binding for `initiateFinalSettlement` on the FinalSettlementFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        accounts : typing.List[eth_typing.ChecksumAddress]

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.initiateFinalSettlement(
            product_id,
            accounts,
        )

    def open_interest(
        self,
        product_id: hexbytes.HexBytes,
    ) -> int:
        """Binding for `openInterest` on the FinalSettlementFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes

        Returns
        -------
        int
        """
        return_value = self._contract.functions.openInterest(
            product_id,
        ).call()
        return int(return_value)


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "FSPAlreadyFinalized",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "FSPNotFound",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"},
                {"internalType": "uint256", "name": "currentTime", "type": "uint256"},
                {
                    "internalType": "uint256",
                    "name": "earliestFSPSubmissionTime",
                    "type": "uint256",
                },
            ],
            "name": "FSPTimeNotReached",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "fspAccount", "type": "address"}
            ],
            "name": "InvalidFSPAccount",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "oracleAddress", "type": "address"}
            ],
            "name": "InvalidOracleAddress",
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
                {"internalType": "int256", "name": "checksum", "type": "int256"},
                {
                    "internalType": "int256",
                    "name": "expectedChecksum",
                    "type": "int256",
                },
            ],
            "name": "MismatchedFSPAccountQuantities",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "ProductNotInFinalSettlement",
            "type": "error",
        },
        {
            "inputs": [],
            "name": "CLOSEOUT_FEE_RATE",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "pure",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "CLOSEOUT_REWARD_RATE",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "pure",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productID", "type": "bytes32"}
            ],
            "name": "finalizeFsp",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "getFsp",
            "outputs": [
                {"internalType": "uint256", "name": "fsp", "type": "uint256"},
                {"internalType": "bool", "name": "finalized", "type": "bool"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productID", "type": "bytes32"},
                {"internalType": "address[]", "name": "accounts", "type": "address[]"},
            ],
            "name": "initiateFinalSettlement",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "openInterest",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
    ],
)
