"""FinalSettlementFacet contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import hexbytes
import web3
from web3 import types
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

    @property
    def FSPFinalized(self) -> contract.ContractEvent:
        """Binding for `event FSPFinalized` on the FinalSettlementFacet contract."""
        return self._contract.events.FSPFinalized

    @property
    def FeeCollected(self) -> contract.ContractEvent:
        """Binding for `event FeeCollected` on the FinalSettlementFacet contract."""
        return self._contract.events.FeeCollected

    @property
    def FeeDispersed(self) -> contract.ContractEvent:
        """Binding for `event FeeDispersed` on the FinalSettlementFacet contract."""
        return self._contract.events.FeeDispersed

    @property
    def FinalSettlementCloseout(self) -> contract.ContractEvent:
        """Binding for `event FinalSettlementCloseout` on the FinalSettlementFacet contract."""
        return self._contract.events.FinalSettlementCloseout

    @property
    def PositionUpdated(self) -> contract.ContractEvent:
        """Binding for `event PositionUpdated` on the FinalSettlementFacet contract."""
        return self._contract.events.PositionUpdated

    def final_settlement_id(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `FINAL_SETTLEMENT_ID` on the FinalSettlementFacet contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.FINAL_SETTLEMENT_ID().call(
            block_identifier=block_identifier
        )
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
        block_identifier: types.BlockIdentifier = "latest",
    ) -> typing.Tuple[int, bool]:
        """Binding for `getFsp` on the FinalSettlementFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        bool
        """
        return_value = self._contract.functions.getFsp(
            product_id,
        ).call(block_identifier=block_identifier)
        return (
            int(return_value[0]),
            bool(return_value[1]),
        )

    def get_fsp_finalization_time(
        self,
        product_id: hexbytes.HexBytes,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `getFspFinalizationTime` on the FinalSettlementFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.getFspFinalizationTime(
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)

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
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `openInterest` on the FinalSettlementFacet contract.

        Parameters
        ----------
        product_id : hexbytes.HexBytes
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.openInterest(
            product_id,
        ).call(block_identifier=block_identifier)
        return int(return_value)


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "type": "function",
            "name": "FINAL_SETTLEMENT_ID",
            "inputs": [],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "finalizeFsp",
            "inputs": [
                {"name": "productID", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "int256", "internalType": "int256"}],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "getFsp",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [
                {"name": "fsp", "type": "int256", "internalType": "int256"},
                {"name": "finalized", "type": "bool", "internalType": "bool"},
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "getFspFinalizationTime",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "initiateFinalSettlement",
            "inputs": [
                {"name": "productID", "type": "bytes32", "internalType": "bytes32"},
                {"name": "accounts", "type": "address[]", "internalType": "address[]"},
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "openInterest",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "event",
            "name": "FSPFinalized",
            "inputs": [
                {
                    "name": "productID",
                    "type": "bytes32",
                    "indexed": True,
                    "internalType": "bytes32",
                },
                {
                    "name": "fsp",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "FeeCollected",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "capitalAmount",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "id",
                    "type": "uint256",
                    "indexed": False,
                    "internalType": "uint256",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "FeeDispersed",
            "inputs": [
                {
                    "name": "recipient",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "capitalAmount",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "id",
                    "type": "uint256",
                    "indexed": False,
                    "internalType": "uint256",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "FinalSettlementCloseout",
            "inputs": [
                {
                    "name": "productID",
                    "type": "bytes32",
                    "indexed": True,
                    "internalType": "bytes32",
                },
                {
                    "name": "accountLength",
                    "type": "uint256",
                    "indexed": False,
                    "internalType": "uint256",
                },
                {
                    "name": "closedBy",
                    "type": "address",
                    "indexed": False,
                    "internalType": "address",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "PositionUpdated",
            "inputs": [
                {
                    "name": "marginAccountId",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address",
                },
                {
                    "name": "positionId",
                    "type": "bytes32",
                    "indexed": True,
                    "internalType": "bytes32",
                },
                {
                    "name": "costBasis",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "price",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "quantity",
                    "type": "int256",
                    "indexed": False,
                    "internalType": "int256",
                },
                {
                    "name": "id",
                    "type": "uint256",
                    "indexed": False,
                    "internalType": "uint256",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "error",
            "name": "FSPAlreadyFinalized",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
        },
        {
            "type": "error",
            "name": "FSPNotFound",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
        },
        {
            "type": "error",
            "name": "FSPTimeNotReached",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"},
                {"name": "currentTime", "type": "uint256", "internalType": "uint256"},
                {
                    "name": "earliestFSPSubmissionTime",
                    "type": "uint256",
                    "internalType": "uint256",
                },
            ],
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
            "name": "InvalidOracleAddress",
            "inputs": [
                {"name": "oracleAddress", "type": "address", "internalType": "address"}
            ],
        },
        {
            "type": "error",
            "name": "MAECheckFailed",
            "inputs": [
                {"name": "marginAccount", "type": "address", "internalType": "address"}
            ],
        },
        {
            "type": "error",
            "name": "MismatchedFSPAccountQuantities",
            "inputs": [
                {"name": "checksum", "type": "int256", "internalType": "int256"},
                {
                    "name": "expectedChecksum",
                    "type": "int256",
                    "internalType": "int256",
                },
            ],
        },
        {
            "type": "error",
            "name": "NotFound",
            "inputs": [
                {"name": "parameter", "type": "string", "internalType": "string"}
            ],
        },
        {
            "type": "error",
            "name": "ProductNotInFinalSettlement",
            "inputs": [
                {"name": "productId", "type": "bytes32", "internalType": "bytes32"}
            ],
        },
        {
            "type": "error",
            "name": "SafeCastOverflowedUintToInt",
            "inputs": [{"name": "value", "type": "uint256", "internalType": "uint256"}],
        },
    ],
)
