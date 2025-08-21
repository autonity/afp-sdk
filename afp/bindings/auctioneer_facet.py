"""AuctioneerFacet contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import enum
import typing
from dataclasses import dataclass

import eth_typing
import hexbytes
import web3
from web3.contract import contract


class Side(enum.IntEnum):
    """Port of `enum Side` on the AuctioneerFacet contract."""

    BID = 0
    ASK = 1


@dataclass
class AuctionConfig:
    """Port of `struct AuctionConfig` on the IAuctioneer contract."""

    restoration_buffer: int
    liquidation_duration: int


@dataclass
class AuctionData:
    """Port of `struct AuctionData` on the IAuctioneer contract."""

    start_block: int
    mae_at_initiation: int
    mmu_at_initiation: int
    mae_now: int
    mmu_now: int


@dataclass
class BidData:
    """Port of `struct BidData` on the IAuctioneer contract."""

    product_id: hexbytes.HexBytes
    price: int
    quantity: int
    side: Side


class AuctioneerFacet:
    """AuctioneerFacet contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed AuctioneerFacet contract.
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
    def Auctioned(self) -> contract.ContractEvent:
        """Binding for `event Auctioned` on the AuctioneerFacet contract."""
        return self._contract.events.Auctioned

    @property
    def LiquidationStarted(self) -> contract.ContractEvent:
        """Binding for `event LiquidationStarted` on the AuctioneerFacet contract."""
        return self._contract.events.LiquidationStarted

    @property
    def LiquidationTerminated(self) -> contract.ContractEvent:
        """Binding for `event LiquidationTerminated` on the AuctioneerFacet contract."""
        return self._contract.events.LiquidationTerminated

    def auction_config(
        self,
    ) -> AuctionConfig:
        """Binding for `auctionConfig` on the AuctioneerFacet contract.

        Returns
        -------
        AuctionConfig
        """
        return_value = self._contract.functions.auctionConfig().call()
        return AuctionConfig(int(return_value[0]), int(return_value[1]))

    def auction_data(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        collateral: eth_typing.ChecksumAddress,
    ) -> AuctionData:
        """Binding for `auctionData` on the AuctioneerFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        collateral : eth_typing.ChecksumAddress

        Returns
        -------
        AuctionData
        """
        return_value = self._contract.functions.auctionData(
            margin_account_id,
            collateral,
        ).call()
        return AuctionData(
            int(return_value[0]),
            int(return_value[1]),
            int(return_value[2]),
            int(return_value[3]),
            int(return_value[4]),
        )

    def bid_auction(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        collateral_token: eth_typing.ChecksumAddress,
        bids: typing.List[BidData],
    ) -> contract.ContractFunction:
        """Binding for `bidAuction` on the AuctioneerFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        collateral_token : eth_typing.ChecksumAddress
        bids : typing.List[BidData]

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.bidAuction(
            margin_account_id,
            collateral_token,
            [
                (item.product_id, item.price, item.quantity, int(item.side))
                for item in bids
            ],
        )

    def can_terminate_auctions(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        collateral: eth_typing.ChecksumAddress,
    ) -> bool:
        """Binding for `canTerminateAuctions` on the AuctioneerFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        collateral : eth_typing.ChecksumAddress

        Returns
        -------
        bool
        """
        return_value = self._contract.functions.canTerminateAuctions(
            margin_account_id,
            collateral,
        ).call()
        return bool(return_value)

    def is_liquidatable(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        collateral_token: eth_typing.ChecksumAddress,
    ) -> bool:
        """Binding for `isLiquidatable` on the AuctioneerFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        collateral_token : eth_typing.ChecksumAddress

        Returns
        -------
        bool
        """
        return_value = self._contract.functions.isLiquidatable(
            margin_account_id,
            collateral_token,
        ).call()
        return bool(return_value)

    def is_liquidating(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        collateral_token: eth_typing.ChecksumAddress,
    ) -> bool:
        """Binding for `isLiquidating` on the AuctioneerFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        collateral_token : eth_typing.ChecksumAddress

        Returns
        -------
        bool
        """
        return_value = self._contract.functions.isLiquidating(
            margin_account_id,
            collateral_token,
        ).call()
        return bool(return_value)

    def mae_check_on_bid(
        self,
        liquidator_margin_account_id: eth_typing.ChecksumAddress,
        liquidating_margin_account_id: eth_typing.ChecksumAddress,
        collateral: eth_typing.ChecksumAddress,
        bids: typing.List[BidData],
    ) -> typing.Tuple[bool, bool]:
        """Binding for `maeCheckOnBid` on the AuctioneerFacet contract.

        Parameters
        ----------
        liquidator_margin_account_id : eth_typing.ChecksumAddress
        liquidating_margin_account_id : eth_typing.ChecksumAddress
        collateral : eth_typing.ChecksumAddress
        bids : typing.List[BidData]

        Returns
        -------
        bool
        bool
        """
        return_value = self._contract.functions.maeCheckOnBid(
            liquidator_margin_account_id,
            liquidating_margin_account_id,
            collateral,
            [
                (item.product_id, item.price, item.quantity, int(item.side))
                for item in bids
            ],
        ).call()
        return (
            bool(return_value[0]),
            bool(return_value[1]),
        )

    def max_mae_offered(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        collateral: eth_typing.ChecksumAddress,
        mmu_decreased: int,
    ) -> int:
        """Binding for `maxMaeOffered` on the AuctioneerFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        collateral : eth_typing.ChecksumAddress
        mmu_decreased : int

        Returns
        -------
        int
        """
        return_value = self._contract.functions.maxMaeOffered(
            margin_account_id,
            collateral,
            mmu_decreased,
        ).call()
        return int(return_value)

    def request_liquidation(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        collateral_token: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `requestLiquidation` on the AuctioneerFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        collateral_token : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.requestLiquidation(
            margin_account_id,
            collateral_token,
        )

    def terminate_auctions(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        collateral: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `terminateAuctions` on the AuctioneerFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        collateral : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.terminateAuctions(
            margin_account_id,
            collateral,
        )

    def validate_auctions(
        self,
        margin_account_id: eth_typing.ChecksumAddress,
        collateral_token: eth_typing.ChecksumAddress,
        bids: typing.List[BidData],
    ) -> bool:
        """Binding for `validateAuctions` on the AuctioneerFacet contract.

        Parameters
        ----------
        margin_account_id : eth_typing.ChecksumAddress
        collateral_token : eth_typing.ChecksumAddress
        bids : typing.List[BidData]

        Returns
        -------
        bool
        """
        return_value = self._contract.functions.validateAuctions(
            margin_account_id,
            collateral_token,
            [
                (item.product_id, item.price, item.quantity, int(item.side))
                for item in bids
            ],
        ).call()
        return bool(return_value)


ABI = typing.cast(
    eth_typing.ABI,
    [
        {"inputs": [], "name": "AuctionBidFailed", "type": "error"},
        {"inputs": [], "name": "AuctionBountyFeeTooHigh", "type": "error"},
        {
            "inputs": [
                {"internalType": "string", "name": "paramName", "type": "string"}
            ],
            "name": "InvalidParameter",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "enum ProductState", "name": "state", "type": "uint8"}
            ],
            "name": "InvalidProductState",
            "type": "error",
        },
        {"inputs": [], "name": "Liquidating", "type": "error"},
        {"inputs": [], "name": "LiquidationRequestFailed", "type": "error"},
        {
            "inputs": [
                {"internalType": "address", "name": "marginAccount", "type": "address"}
            ],
            "name": "MAECheckFailed",
            "type": "error",
        },
        {"inputs": [], "name": "MaeOverMmuRateExceeded", "type": "error"},
        {
            "inputs": [
                {"internalType": "bytes32", "name": "productId", "type": "bytes32"}
            ],
            "name": "NoTradeData",
            "type": "error",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "account", "type": "address"}
            ],
            "name": "Unauthorized",
            "type": "error",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "liquidatingMarginAccountID",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "liquidatorMarginAccountID",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "bytes32",
                    "name": "productId",
                    "type": "bytes32",
                },
                {
                    "indexed": False,
                    "internalType": "int256",
                    "name": "quantity",
                    "type": "int256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "price",
                    "type": "uint256",
                },
            ],
            "name": "Auctioned",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "collateralToken",
                    "type": "address",
                },
            ],
            "name": "LiquidationStarted",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "collateralToken",
                    "type": "address",
                },
            ],
            "name": "LiquidationTerminated",
            "type": "event",
        },
        {
            "inputs": [],
            "name": "auctionConfig",
            "outputs": [
                {
                    "components": [
                        {
                            "internalType": "uint64",
                            "name": "restorationBuffer",
                            "type": "uint64",
                        },
                        {
                            "internalType": "uint256",
                            "name": "liquidationDuration",
                            "type": "uint256",
                        },
                    ],
                    "internalType": "struct IAuctioneer.AuctionConfig",
                    "name": "",
                    "type": "tuple",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {"internalType": "address", "name": "collateral", "type": "address"},
            ],
            "name": "auctionData",
            "outputs": [
                {
                    "components": [
                        {
                            "internalType": "uint256",
                            "name": "startBlock",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "maeAtInitiation",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "mmuAtInitiation",
                            "type": "uint256",
                        },
                        {"internalType": "int256", "name": "maeNow", "type": "int256"},
                        {
                            "internalType": "uint256",
                            "name": "mmuNow",
                            "type": "uint256",
                        },
                    ],
                    "internalType": "struct IAuctioneer.AuctionData",
                    "name": "",
                    "type": "tuple",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "collateralToken",
                    "type": "address",
                },
                {
                    "components": [
                        {
                            "internalType": "bytes32",
                            "name": "productID",
                            "type": "bytes32",
                        },
                        {"internalType": "uint256", "name": "price", "type": "uint256"},
                        {
                            "internalType": "uint256",
                            "name": "quantity",
                            "type": "uint256",
                        },
                        {"internalType": "enum Side", "name": "side", "type": "uint8"},
                    ],
                    "internalType": "struct IAuctioneer.BidData[]",
                    "name": "bids",
                    "type": "tuple[]",
                },
            ],
            "name": "bidAuction",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {"internalType": "address", "name": "collateral", "type": "address"},
            ],
            "name": "canTerminateAuctions",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "collateralToken",
                    "type": "address",
                },
            ],
            "name": "isLiquidatable",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "collateralToken",
                    "type": "address",
                },
            ],
            "name": "isLiquidating",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "liquidatorMarginAccountID",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "liquidatingMarginAccountID",
                    "type": "address",
                },
                {"internalType": "address", "name": "collateral", "type": "address"},
                {
                    "components": [
                        {
                            "internalType": "bytes32",
                            "name": "productID",
                            "type": "bytes32",
                        },
                        {"internalType": "uint256", "name": "price", "type": "uint256"},
                        {
                            "internalType": "uint256",
                            "name": "quantity",
                            "type": "uint256",
                        },
                        {"internalType": "enum Side", "name": "side", "type": "uint8"},
                    ],
                    "internalType": "struct IAuctioneer.BidData[]",
                    "name": "bids",
                    "type": "tuple[]",
                },
            ],
            "name": "maeCheckOnBid",
            "outputs": [
                {"internalType": "bool", "name": "maeCheckFailed", "type": "bool"},
                {
                    "internalType": "bool",
                    "name": "maeOverMmuRateExceeded",
                    "type": "bool",
                },
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {"internalType": "address", "name": "collateral", "type": "address"},
                {"internalType": "uint256", "name": "mmuDecreased", "type": "uint256"},
            ],
            "name": "maxMaeOffered",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "collateralToken",
                    "type": "address",
                },
            ],
            "name": "requestLiquidation",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {"internalType": "address", "name": "collateral", "type": "address"},
            ],
            "name": "terminateAuctions",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "marginAccountID",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "collateralToken",
                    "type": "address",
                },
                {
                    "components": [
                        {
                            "internalType": "bytes32",
                            "name": "productID",
                            "type": "bytes32",
                        },
                        {"internalType": "uint256", "name": "price", "type": "uint256"},
                        {
                            "internalType": "uint256",
                            "name": "quantity",
                            "type": "uint256",
                        },
                        {"internalType": "enum Side", "name": "side", "type": "uint8"},
                    ],
                    "internalType": "struct IAuctioneer.BidData[]",
                    "name": "bids",
                    "type": "tuple[]",
                },
            ],
            "name": "validateAuctions",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
    ],
)
