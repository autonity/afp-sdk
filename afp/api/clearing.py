from decimal import Decimal
from functools import cache

from eth_typing.evm import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from web3.exceptions import ContractCustomError

from .. import validators
from ..bindings import (
    ClearingDiamond,
    MarginAccount,
    MarginAccountRegistry,
    ProductRegistry,
)
from ..bindings.erc20 import ERC20
from ..bindings.facade import CLEARING_DIAMOND_ABI
from ..bindings.margin_account import ABI as MARGIN_CONTRACT_ABI
from ..bindings.margin_account_registry import ABI as MARGIN_ACCOUNT_REGISTRY_ABI
from ..bindings.product_registry import ABI as PRODUCT_REGISTRY_ABI
from ..decorators import convert_web3_error
from ..exceptions import NotFoundError
from ..schemas import Position
from .base import ClearingSystemAPI
from .builder import Builder


class Clearing(ClearingSystemAPI):
    """API for managing margin accounts.

    Parameters
    ----------
    private_key : str
        The private key of the blockchain account that manages the margin account.
    autonity_rpc_url : str
        The URL of a JSON-RPC provider for Autonity. (HTTPS only.)
    """

    ### Transactions ###

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def authorize(self, collateral_asset: str, intent_account_id: str) -> str:
        """Authorizes a blockchain account to submit intents to the clearing system
        using the margin account associated with the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.
        intent_account_id : str
            The address of the intent account.

        Returns
        -------
        str
            The hash of the transaction.
        """
        collateral_asset = validators.validate_address(collateral_asset)
        intent_account_id = validators.validate_address(intent_account_id)

        tx_hash = (
            self._margin_contract(collateral_asset)
            .authorize(intent_account_id)
            .transact()
        )
        self._w3.eth.wait_for_transaction_receipt(tx_hash)
        return Web3.to_hex(tx_hash)

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def deposit_into_margin_account(
        self, collateral_asset: str, amount: Decimal
    ) -> tuple[str, str]:
        """Deposits the specified amount of collateral tokens into the margin account
        associated with the collateral asset.

        First approves the token transfer with the collateral token, then executes the
        transfer.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.
        amount : Decimal
            The amount of collateral tokens to deposit.

        Returns
        -------
        str
            The hash of the approval transaction.
        str
            The hash of the deposit transaction.
        """
        collateral_asset = validators.validate_address(collateral_asset)
        token_amount = int(amount * 10 ** self._decimals(collateral_asset))
        token_contract = ERC20(self._w3, collateral_asset)

        tx1_hash = token_contract.approve(
            self._margin_contract(collateral_asset)._contract.address,  # type: ignore
            token_amount,
        ).transact()
        self._w3.eth.wait_for_transaction_receipt(tx1_hash)

        tx2_hash = (
            self._margin_contract(collateral_asset).deposit(token_amount).transact()
        )
        self._w3.eth.wait_for_transaction_receipt(tx2_hash)

        return (Web3.to_hex(tx1_hash), Web3.to_hex(tx2_hash))

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def withdraw_from_margin_account(
        self, collateral_asset: str, amount: Decimal
    ) -> str:
        """Withdraws the specified amount of collateral tokens from the margin account
        associated with the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.
        amount : Decimal
            The amount of collateral tokens to withdraw.

        Returns
        -------
        str
            The hash of the transaction.
        """
        collateral_asset = validators.validate_address(collateral_asset)
        token_amount = int(amount * 10 ** self._decimals(collateral_asset))
        tx_hash = (
            self._margin_contract(collateral_asset).withdraw(token_amount).transact()
        )
        self._w3.eth.wait_for_transaction_receipt(tx_hash)
        return Web3.to_hex(tx_hash)

    @convert_web3_error(CLEARING_DIAMOND_ABI)
    def initiate_final_settlement(self, product_id: str, accounts: list[str]) -> str:
        """Initiate final settlement (closeout) process for the specified accounts.

        The product must be in Final Settlement state. The accounts must hold non-zero
        positions in the product that offset each other (i.e. the sum of their position
        sizes is 0.)

        Parameters
        ----------
        product_id : str
            The ID of the product.
        accounts : list of str
            List of margin account IDs to initiate settlement for.

        Returns
        -------
        str
            The hash of the transaction.
        """
        product_id = validators.validate_hexstr32(product_id)
        addresses = [validators.validate_address(account) for account in accounts]

        clearing_contract = ClearingDiamond(self._w3)
        tx_hash = clearing_contract.initiate_final_settlement(
            HexBytes(product_id), addresses
        ).transact()
        self._w3.eth.wait_for_transaction_receipt(tx_hash)
        return Web3.to_hex(tx_hash)

    ### Views ###

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def capital(self, collateral_asset: str) -> Decimal:
        """Returns the amount of collateral tokens in the margin account associated
        with the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        Decimal
        """
        collateral_asset = validators.validate_address(collateral_asset)
        amount = self._margin_contract(collateral_asset).capital(self._account.address)
        return Decimal(amount) / 10 ** self._decimals(collateral_asset)

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def position(self, collateral_asset: str, position_id: str) -> Position:
        """Returns the parameters of a position in the margin account associated with
        the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.
        position_id: str
            The ID of the position.

        Returns
        -------
        afp.schemas.Position
        """
        validators.validate_hexstr32(position_id)
        data = self._margin_contract(collateral_asset).position_data(
            self._account.address, HexBytes(position_id)
        )
        decimals = self._decimals(collateral_asset)
        return Position(
            id=Web3.to_hex(data.position_id),
            quantity=data.quantity,
            cost_basis=Decimal(data.cost_basis) / 10**decimals,
            maintenance_margin=Decimal(data.maintenance_margin) / 10**decimals,
            pnl=Decimal(data.pnl) / 10**decimals,
        )

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def positions(self, collateral_asset: str) -> list[Position]:
        """Returns all positions in the margin account associated with the collateral
        asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        list of afp.schemas.Position
        """
        collateral_asset = validators.validate_address(collateral_asset)
        position_ids = self._margin_contract(collateral_asset).positions(
            self._account.address
        )
        return [self.position(collateral_asset, Web3.to_hex(id)) for id in position_ids]

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def margin_account_equity(self, collateral_asset: str) -> Decimal:
        """Returns the margin account equity in the margin account associated with the
        collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        Decimal
        """
        collateral_asset = validators.validate_address(collateral_asset)
        amount = self._margin_contract(collateral_asset).mae(self._account.address)
        return Decimal(amount) / 10 ** self._decimals(collateral_asset)

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def maintenance_margin_available(self, collateral_asset: str) -> Decimal:
        """Returns the maintenance margin available in the margin account associated
        with the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        Decimal
        """
        collateral_asset = validators.validate_address(collateral_asset)
        amount = self._margin_contract(collateral_asset).mma(self._account.address)
        return Decimal(amount) / 10 ** self._decimals(collateral_asset)

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def maintenance_margin_used(self, collateral_asset: str) -> Decimal:
        """Returns the maintenance margin used in the margin account associated with
        the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        Decimal
        """
        collateral_asset = validators.validate_address(collateral_asset)
        amount = self._margin_contract(collateral_asset).mmu(self._account.address)
        return Decimal(amount) / 10 ** self._decimals(collateral_asset)

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def profit_and_loss(self, collateral_asset: str) -> Decimal:
        """Returns the profit and loss in the margin account associated with the
        collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        Decimal
        """
        collateral_asset = validators.validate_address(collateral_asset)
        amount = self._margin_contract(collateral_asset).pnl(self._account.address)
        return Decimal(amount) / 10 ** self._decimals(collateral_asset)

    @convert_web3_error(MARGIN_CONTRACT_ABI)
    def withdrawable_amount(self, collateral_asset: str) -> Decimal:
        """Returns the amount of collateral tokens withdrawable from the margin account
        associated with the collateral asset.

        Parameters
        ----------
        collateral_asset : str
            The address of the collateral token.

        Returns
        -------
        Decimal
        """
        collateral_asset = validators.validate_address(collateral_asset)
        amount = self._margin_contract(collateral_asset).withdrawable(
            self._account.address
        )
        return Decimal(amount) / 10 ** self._decimals(collateral_asset)

    @convert_web3_error(PRODUCT_REGISTRY_ABI)
    def collateral_asset(self, product_id: str) -> str:
        """Returns the collateral asset of a product.

        Parameters
        ----------
        product_id : str
            The ID of the product.

        Returns
        -------
        str
        """
        product_registry_contract = ProductRegistry(self._w3)
        collateral_asset = product_registry_contract.collateral_asset(
            HexBytes(product_id)
        )
        if Web3.to_int(hexstr=collateral_asset) == 0:
            raise NotFoundError("Product not found in the product registry")
        return collateral_asset

    def product_state(self, product_id: str) -> str:
        """Returns the current state of a product.

        Parameters
        ----------
        product_id : str
            The ID of the product.

        Returns
        -------
        str
        """
        return Builder.product_state(self, product_id)

    ### Internal getters ###

    @cache
    @convert_web3_error(MARGIN_ACCOUNT_REGISTRY_ABI)
    def _margin_contract(self, collateral_asset: ChecksumAddress) -> MarginAccount:
        margin_account_registry_contract = MarginAccountRegistry(self._w3)
        try:
            margin_contract_address = (
                margin_account_registry_contract.get_margin_account(
                    Web3.to_checksum_address(collateral_asset)
                )
            )
        except ContractCustomError:
            raise NotFoundError("No margin account found for collateral asset")
        return MarginAccount(self._w3, margin_contract_address)
