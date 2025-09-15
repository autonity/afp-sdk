from .auth import Authenticator
from .config import Config
from .api.admin import Admin
from .api.builder import Builder
from .api.clearing import Clearing
from .api.liquidation import Liquidation
from .api.trading import Trading
from .constants import defaults
from .validators import validate_address


class AFP:
    """Application object for interacting with the AFP Clearing System and the AutEx
    exchange.

    Parameters
    ----------
    rpc_url : str, optional
        The URL of an Autonity RPC provider.
    authenticator : afp.Authenticator, optional
        The default authenticator for signing transactions & messages.
    exchange_url: str, optional
        The base REST API URL of the AutEx exchange.
    chain_id : str, optional
        The chain ID of the Autonity network.
    gas_limit : int, optional
        The `gasLimit` parameter of blockchain transactions. Estimated with
        the `eth_estimateGas` JSON-RPC method if not specified.
    max_fee_per_gas : int, optional
        The `maxFeePerGas` parameter of blockchain transactions in ton (wei) units.
    max_priority_fee_per_gas : int, optional
        The `maxPriorityFeePerGas` parameter of blockchain transactions in ton (wei)
        units.
    timeout_seconds: int, optional
        The number of seconds to wait for a blockchain transaction to be mined.
    clearing_diamond_address : str, optional
        The address of the ClearingDiamond contract.
    margin_account_registry_address : str, optional
        The address of the MarginAccountRegistry contract.
    oracle_provider_address : str, optional
        The address of the OracleProvider contract.
    product_registry_address: str, optional
        The address of the ProductRegistry contract.
    system_viewer_address: str, optional
        The address of the SystemViewer contract.
    """

    config: Config

    def __init__(
        self,
        rpc_url: str | None = None,
        authenticator: Authenticator | None = None,
        *,
        exchange_url: str = defaults.EXCHANGE_URL,
        chain_id: int = defaults.CHAIN_ID,
        gas_limit: int | None = defaults.GAS_LIMIT,
        max_fee_per_gas: int | None = defaults.MAX_FEE_PER_GAS,
        max_priority_fee_per_gas: int | None = defaults.MAX_PRIORITY_FEE_PER_GAS,
        timeout_seconds: int = defaults.TIMEOUT_SECONDS,
        clearing_diamond_address: str = defaults.CLEARING_DIAMOND_ADDRESS,
        margin_account_registry_address: str = defaults.MARGIN_ACCOUNT_REGISTRY_ADDRESS,
        oracle_provider_address: str = defaults.ORACLE_PROVIDER_ADDRESS,
        product_registry_address: str = defaults.PRODUCT_REGISTRY_ADDRESS,
        system_viewer_address: str = defaults.SYSTEM_VIEWER_ADDRESS,
    ) -> None:
        self.config = Config(
            rpc_url=rpc_url,
            authenticator=authenticator,
            exchange_url=exchange_url,
            chain_id=chain_id,
            gas_limit=gas_limit,
            max_fee_per_gas=max_fee_per_gas,
            max_priority_fee_per_gas=max_priority_fee_per_gas,
            timeout_seconds=timeout_seconds,
            clearing_diamond_address=validate_address(clearing_diamond_address),
            margin_account_registry_address=validate_address(
                margin_account_registry_address
            ),
            oracle_provider_address=validate_address(oracle_provider_address),
            product_registry_address=validate_address(product_registry_address),
            system_viewer_address=validate_address(system_viewer_address),
        )

    def __repr__(self) -> str:
        return f"AFP(config={repr(self.config)})"

    # Clearing APIs

    def Builder(self, authenticator: Authenticator | None = None) -> Builder:
        """API for building and submitting new products.

        Parameters
        ----------
        authenticator : afp.Authenticator, optional
            Authenticator for signing transactions sent to the Clearing System.
            Defaults to the authenticator specified in the `AFP` constructor.
        """
        return Builder(self.config, authenticator)

    def Clearing(self, authenticator: Authenticator | None = None) -> Clearing:
        """API for managing margin accounts.

        Parameters
        ----------
        authenticator : afp.Authenticator, optional
            Authenticator for signing transactions sent to the Clearing System.
            Defaults to the authenticator specified in the `AFP` constructor.
        """
        return Clearing(self.config, authenticator)

    def Liquidation(self, authenticator: Authenticator | None = None) -> Liquidation:
        """API for participating in liquidation auctions.

        Parameters
        ----------
        authenticator : afp.Authenticator, optional
            Authenticator for signing transactions sent to the Clearing System.
            Defaults to the authenticator specified in the `AFP` constructor.
        """
        return Liquidation(self.config, authenticator)

    # Exchange APIs

    def Admin(self, authenticator: Authenticator | None = None) -> Admin:
        """API for AutEx administration, restricted to AutEx admins.

        Authenticates with the exchange on creation.

        Parameters
        ----------
        authenticator : afp.Authenticator, optional
            Authenticator for authenticating with the AutEx exchange. Defaults to the
            authenticator specified in the `AFP` constructor.

        Raises
        ------
        afp.exceptions.AuthenticationError
            If the exchange rejects the login attempt.
        """
        return Admin(self.config, authenticator)

    def Trading(self, authenticator: Authenticator | None = None) -> Trading:
        """API for trading in the AutEx exchange.

        Authenticates with the exchange on creation.

        Parameters
        ----------
        authenticator : afp.Authenticator, optional
            Authenticator for signing intents and authenticating with the AutEx
            exchange. Defaults to the authenticator specified in the `AFP` constructor.

        Raises
        ------
        afp.exceptions.AuthenticationError
            If the exchange rejects the login attempt.
        """
        return Trading(self.config, authenticator)
