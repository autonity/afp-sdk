"""AdminFacet contract binding and data structures."""

# This module has been generated using pyabigen v0.2.16

import typing

import eth_typing
import web3
from web3 import types
from web3.contract import contract

from .types import ClearingConfig, MarkPriceConfig, FinalSettlementConfig, Config


class AdminFacet:
    """AdminFacet contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    address : eth_typing.ChecksumAddress
        The address of a deployed AdminFacet contract.
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
    def AddressUpdated(self) -> contract.ContractEvent:
        """Binding for `event AddressUpdated` on the AdminFacet contract."""
        return self._contract.events.AddressUpdated

    @property
    def ConfigUpdated(self) -> contract.ContractEvent:
        """Binding for `event ConfigUpdated` on the AdminFacet contract."""
        return self._contract.events.ConfigUpdated

    @property
    def OwnershipTransferred(self) -> contract.ContractEvent:
        """Binding for `event OwnershipTransferred` on the AdminFacet contract."""
        return self._contract.events.OwnershipTransferred

    def clearing_fee_rate(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `clearingFeeRate` on the AdminFacet contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.clearingFeeRate().call(
            block_identifier=block_identifier
        )
        return int(return_value)

    def closeout_fee_rate(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `closeoutFeeRate` on the AdminFacet contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.closeoutFeeRate().call(
            block_identifier=block_identifier
        )
        return int(return_value)

    def closeout_reward_rate(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `closeoutRewardRate` on the AdminFacet contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.closeoutRewardRate().call(
            block_identifier=block_identifier
        )
        return int(return_value)

    def config(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> Config:
        """Binding for `config` on the AdminFacet contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        Config
        """
        return_value = self._contract.functions.config().call(
            block_identifier=block_identifier
        )
        return Config(
            ClearingConfig(int(return_value[0][0]), int(return_value[0][1])),
            MarkPriceConfig(int(return_value[1][0])),
            FinalSettlementConfig(int(return_value[2][0]), int(return_value[2][1])),
        )

    def get_margin_account_registry(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `getMarginAccountRegistry` on the AdminFacet contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.getMarginAccountRegistry().call(
            block_identifier=block_identifier
        )
        return eth_typing.ChecksumAddress(return_value)

    def get_mark_price_interval(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `getMarkPriceInterval` on the AdminFacet contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.getMarkPriceInterval().call(
            block_identifier=block_identifier
        )
        return int(return_value)

    def get_product_registry(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `getProductRegistry` on the AdminFacet contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.getProductRegistry().call(
            block_identifier=block_identifier
        )
        return eth_typing.ChecksumAddress(return_value)

    def get_treasury(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `getTreasury` on the AdminFacet contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        eth_typing.ChecksumAddress
        """
        return_value = self._contract.functions.getTreasury().call(
            block_identifier=block_identifier
        )
        return eth_typing.ChecksumAddress(return_value)

    def initialize(
        self,
        treasury: eth_typing.ChecksumAddress,
        product_registry: eth_typing.ChecksumAddress,
        margin_account_registry: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `initialize` on the AdminFacet contract.

        Parameters
        ----------
        treasury : eth_typing.ChecksumAddress
        product_registry : eth_typing.ChecksumAddress
        margin_account_registry : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.initialize(
            treasury,
            product_registry,
            margin_account_registry,
        )

    def max_trading_fee_rate(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> int:
        """Binding for `maxTradingFeeRate` on the AdminFacet contract.

        Parameters
        ----------
        block_identifier : web3.types.BlockIdentifier
            The block identifier, defaults to the latest block.

        Returns
        -------
        int
        """
        return_value = self._contract.functions.maxTradingFeeRate().call(
            block_identifier=block_identifier
        )
        return int(return_value)

    def owner(
        self,
        block_identifier: types.BlockIdentifier = "latest",
    ) -> eth_typing.ChecksumAddress:
        """Binding for `owner` on the AdminFacet contract.

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

    def set_config(
        self,
        config_: Config,
    ) -> contract.ContractFunction:
        """Binding for `setConfig` on the AdminFacet contract.

        Parameters
        ----------
        config_ : Config

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.setConfig(
            (
                (
                    config_.clearing_config.clearing_fee_rate,
                    config_.clearing_config.max_trading_fee_rate,
                ),
                (config_.mark_price_config.mark_price_interval),
                (
                    config_.final_settlement_config.closeout_fee_rate,
                    config_.final_settlement_config.closeout_reward_rate,
                ),
            ),
        )

    def set_margin_account_registry(
        self,
        margin_account_registry: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `setMarginAccountRegistry` on the AdminFacet contract.

        Parameters
        ----------
        margin_account_registry : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.setMarginAccountRegistry(
            margin_account_registry,
        )

    def set_treasury(
        self,
        treasury: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `setTreasury` on the AdminFacet contract.

        Parameters
        ----------
        treasury : eth_typing.ChecksumAddress

        Returns
        -------
        web3.contract.contract.ContractFunction
            A contract function instance to be sent in a transaction.
        """
        return self._contract.functions.setTreasury(
            treasury,
        )

    def transfer_ownership(
        self,
        new_owner: eth_typing.ChecksumAddress,
    ) -> contract.ContractFunction:
        """Binding for `transferOwnership` on the AdminFacet contract.

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


ABI = typing.cast(
    eth_typing.ABI,
    [
        {
            "type": "function",
            "name": "clearingFeeRate",
            "inputs": [],
            "outputs": [{"name": "", "type": "uint32", "internalType": "uint32"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "closeoutFeeRate",
            "inputs": [],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "closeoutRewardRate",
            "inputs": [],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "config",
            "inputs": [],
            "outputs": [
                {
                    "name": "",
                    "type": "tuple",
                    "internalType": "struct Config",
                    "components": [
                        {
                            "name": "clearingConfig",
                            "type": "tuple",
                            "internalType": "struct ClearingConfig",
                            "components": [
                                {
                                    "name": "clearingFeeRate",
                                    "type": "uint32",
                                    "internalType": "uint32",
                                },
                                {
                                    "name": "maxTradingFeeRate",
                                    "type": "uint32",
                                    "internalType": "uint32",
                                },
                            ],
                        },
                        {
                            "name": "markPriceConfig",
                            "type": "tuple",
                            "internalType": "struct MarkPriceConfig",
                            "components": [
                                {
                                    "name": "markPriceInterval",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                }
                            ],
                        },
                        {
                            "name": "finalSettlementConfig",
                            "type": "tuple",
                            "internalType": "struct FinalSettlementConfig",
                            "components": [
                                {
                                    "name": "closeoutFeeRate",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "closeoutRewardRate",
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
            "name": "getMarginAccountRegistry",
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
            "name": "getMarkPriceInterval",
            "inputs": [],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "getProductRegistry",
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
            "name": "getTreasury",
            "inputs": [],
            "outputs": [{"name": "", "type": "address", "internalType": "address"}],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "initialize",
            "inputs": [
                {"name": "treasury", "type": "address", "internalType": "address"},
                {
                    "name": "productRegistry",
                    "type": "address",
                    "internalType": "address",
                },
                {
                    "name": "marginAccountRegistry",
                    "type": "address",
                    "internalType": "address",
                },
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "maxTradingFeeRate",
            "inputs": [],
            "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
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
            "name": "setConfig",
            "inputs": [
                {
                    "name": "config_",
                    "type": "tuple",
                    "internalType": "struct Config",
                    "components": [
                        {
                            "name": "clearingConfig",
                            "type": "tuple",
                            "internalType": "struct ClearingConfig",
                            "components": [
                                {
                                    "name": "clearingFeeRate",
                                    "type": "uint32",
                                    "internalType": "uint32",
                                },
                                {
                                    "name": "maxTradingFeeRate",
                                    "type": "uint32",
                                    "internalType": "uint32",
                                },
                            ],
                        },
                        {
                            "name": "markPriceConfig",
                            "type": "tuple",
                            "internalType": "struct MarkPriceConfig",
                            "components": [
                                {
                                    "name": "markPriceInterval",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                }
                            ],
                        },
                        {
                            "name": "finalSettlementConfig",
                            "type": "tuple",
                            "internalType": "struct FinalSettlementConfig",
                            "components": [
                                {
                                    "name": "closeoutFeeRate",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "closeoutRewardRate",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                            ],
                        },
                    ],
                }
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "setMarginAccountRegistry",
            "inputs": [
                {
                    "name": "marginAccountRegistry",
                    "type": "address",
                    "internalType": "address",
                }
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "setTreasury",
            "inputs": [
                {"name": "treasury", "type": "address", "internalType": "address"}
            ],
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
            "type": "event",
            "name": "AddressUpdated",
            "inputs": [
                {
                    "name": "name",
                    "type": "string",
                    "indexed": False,
                    "internalType": "string",
                },
                {
                    "name": "oldAddress",
                    "type": "address",
                    "indexed": False,
                    "internalType": "address",
                },
                {
                    "name": "newAddress",
                    "type": "address",
                    "indexed": False,
                    "internalType": "address",
                },
            ],
            "anonymous": False,
        },
        {
            "type": "event",
            "name": "ConfigUpdated",
            "inputs": [
                {
                    "name": "oldConfig",
                    "type": "tuple",
                    "indexed": False,
                    "internalType": "struct Config",
                    "components": [
                        {
                            "name": "clearingConfig",
                            "type": "tuple",
                            "internalType": "struct ClearingConfig",
                            "components": [
                                {
                                    "name": "clearingFeeRate",
                                    "type": "uint32",
                                    "internalType": "uint32",
                                },
                                {
                                    "name": "maxTradingFeeRate",
                                    "type": "uint32",
                                    "internalType": "uint32",
                                },
                            ],
                        },
                        {
                            "name": "markPriceConfig",
                            "type": "tuple",
                            "internalType": "struct MarkPriceConfig",
                            "components": [
                                {
                                    "name": "markPriceInterval",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                }
                            ],
                        },
                        {
                            "name": "finalSettlementConfig",
                            "type": "tuple",
                            "internalType": "struct FinalSettlementConfig",
                            "components": [
                                {
                                    "name": "closeoutFeeRate",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "closeoutRewardRate",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                            ],
                        },
                    ],
                },
                {
                    "name": "newConfig",
                    "type": "tuple",
                    "indexed": False,
                    "internalType": "struct Config",
                    "components": [
                        {
                            "name": "clearingConfig",
                            "type": "tuple",
                            "internalType": "struct ClearingConfig",
                            "components": [
                                {
                                    "name": "clearingFeeRate",
                                    "type": "uint32",
                                    "internalType": "uint32",
                                },
                                {
                                    "name": "maxTradingFeeRate",
                                    "type": "uint32",
                                    "internalType": "uint32",
                                },
                            ],
                        },
                        {
                            "name": "markPriceConfig",
                            "type": "tuple",
                            "internalType": "struct MarkPriceConfig",
                            "components": [
                                {
                                    "name": "markPriceInterval",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                }
                            ],
                        },
                        {
                            "name": "finalSettlementConfig",
                            "type": "tuple",
                            "internalType": "struct FinalSettlementConfig",
                            "components": [
                                {
                                    "name": "closeoutFeeRate",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "closeoutRewardRate",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                            ],
                        },
                    ],
                },
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
    ],
)
