from .auth import Authenticator, KeyfileAuthenticator, PrivateKeyAuthenticator
from .config import Config
from .api.admin import Admin
from .api.margin_account import MarginAccount
from .api.product import Product
from .api.trading import Trading
from .constants import defaults
from .exceptions import ConfigurationError
from .validators import validate_address


class AFP:
    """Application object for interacting with the AFP Clearing System and the AutEx
    exchange.

    Parameters
    ----------
    authenticator : afp.Authenticator, optional
        The default authenticator for signing transactions & messages. Can also be set
        with environment variables; use `AFP_PRIVATE_KEY` for private key
        authentication, `AFP_KEYFILE` and `AFP_KEYFILE_PASSWORD` for keyfile
        authentication.
    rpc_url : str, optional
        The URL of an Autonity RPC provider. Can also be set with the `AFP_RPC_URL`
        environment variable.
    exchange_url : str, optional
        The REST API base URL of the exchange. Defaults to the URL of the AutEx
        exchange. Its default value can be overridden with the `AFP_EXCHANGE_URL`
        environment variable.
    chain_id : str, optional
        The chain ID of the Autonity network. Defauls to the chain ID of Autonity
        Mainnet. Its default value can be overridden with the `AFP_CHAIN_ID` environment
        variable.
    gas_limit : int, optional
        The `gasLimit` parameter of blockchain transactions. Estimated with the
        `eth_estimateGas` JSON-RPC call if not specified. Its default value can be
        overridden with the `AFP_GAS_LIMIT` environment variable.
    max_fee_per_gas : int, optional
        The `maxFeePerGas` parameter of blockchain transactions in ton (wei) units.
        Defaults to `baseFeePerGas` from the return value of the `eth_getBlock` JSON-RPC
        call. Its default value can be overridden with the `AFP_MAX_FEE_PER_GAS`
        environment variable.
    max_priority_fee_per_gas : int, optional
        The `maxPriorityFeePerGas` parameter of blockchain transactions in ton (wei)
        units. Defaults to the return value of the `eth_maxPriorityFeePerGas` JSON-RPC
        call. Its default value can be overridden with the
        `AFP_MAX_PRIORITY_FEE_PER_GAS` environment variable.
    timeout_seconds: int, optional
        The number of seconds to wait for a blockchain transaction to be mined.
        Defaults to 10 seconds. Its default value can be overridden with the
        `AFP_TIMEOUT_SECONDS` environment variable.
    clearing_diamond_address : str, optional
        The address of the ClearingDiamond contract. Defaults to the Autonity Mainnet
        deployment address. Its default value can be overridden with the
        `AFP_CLEARING_DIAMOND_ADDRESS` environment variable.
    margin_account_registry_address : str, optional
        The address of the MarginAccountRegistry contract. Defaults to the Autonity
        Mainnet deployment address. Its default value can be overridden with the
        `AFP_MARGIN_ACCOUNT_REGISTRY_ADDRESS` environment variable.
    oracle_provider_address : str, optional
        The address of the OracleProvider contract. Defaults to the Autonity Mainnet
        deployment address. Its default value can be overridden with the
        `AFP_ORACLE_PROVIDER_ADDRESS` environment variable.
    product_registry_address: str, optional
        The address of the ProductRegistry contract. Defaults to the Autonity Mainnet
        deployment address. Its default value can be overridden with the
        `AFP_PRODUCT_REGISTRY_ADDRESS` environment variable.
    system_viewer_address: str, optional
        The address of the SystemViewer contract. Defaults to the Autonity Mainnet
        deployment address. Its default value can be overridden with the
        `AFP_SYSTEM_VIEWER_ADDRESS` environment variable.
    """

    config: Config

    def __init__(
        self,
        *,
        authenticator: Authenticator | None = None,
        rpc_url: str | None = defaults.RPC_URL,
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
        if authenticator is None:
            authenticator = _default_authenticator()

        self.config = Config(
            authenticator=authenticator,
            exchange_url=exchange_url,
            rpc_url=rpc_url,
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

    def MarginAccount(
        self, authenticator: Authenticator | None = None
    ) -> MarginAccount:
        """API for managing margin accounts.

        Parameters
        ----------
        authenticator : afp.Authenticator, optional
            Authenticator for signing transactions sent to the Clearing System.
            Defaults to the authenticator specified in the `AFP` constructor.
        """
        return MarginAccount(self.config, authenticator=authenticator)

    def Product(self, authenticator: Authenticator | None = None) -> Product:
        """API for managing products.

        Parameters
        ----------
        authenticator : afp.Authenticator, optional
            Authenticator for signing transactions sent to the Clearing System.
            Defaults to the authenticator specified in the `AFP` constructor.
        """
        return Product(self.config, authenticator=authenticator)

    # Exchange APIs

    def Admin(
        self,
        authenticator: Authenticator | None = None,
        exchange_url: str | None = None,
    ) -> Admin:
        """API for AutEx administration, restricted to AutEx admins.

        Authenticates with the exchange on creation.

        Parameters
        ----------
        authenticator : afp.Authenticator, optional
            Authenticator for authenticating with the AutEx exchange. Defaults to the
            authenticator specified in the `AFP` constructor.
        exchange_url: str, optional
            The REST API base URL of the exchange. Defaults to the value specified in
            the `AFP` constructor.

        Raises
        ------
        afp.exceptions.AuthenticationError
            If the exchange rejects the login attempt.
        """
        return Admin(
            self.config, authenticator=authenticator, exchange_url=exchange_url
        )

    def Trading(
        self,
        authenticator: Authenticator | None = None,
        exchange_url: str | None = None,
    ) -> Trading:
        """API for trading in the AutEx exchange.

        Authenticates with the exchange on creation.

        Parameters
        ----------
        authenticator : afp.Authenticator, optional
            Authenticator for signing intents and authenticating with the AutEx
            exchange. Defaults to the authenticator specified in the `AFP` constructor.
        exchange_url: str, optional
            The REST API base URL of the exchange. Defaults to the value specified in
            the `AFP` constructor.

        Raises
        ------
        afp.exceptions.AuthenticationError
            If the exchange rejects the login attempt.
        """
        return Trading(
            self.config, authenticator=authenticator, exchange_url=exchange_url
        )


def _default_authenticator() -> Authenticator | None:
    if defaults.PRIVATE_KEY is not None and defaults.KEYFILE is not None:
        raise ConfigurationError(
            "Only one of AFP_PRIVATE_KEY and AFP_KEYFILE environment "
            "variables should be specified"
        )
    if defaults.PRIVATE_KEY is not None:
        return PrivateKeyAuthenticator(defaults.PRIVATE_KEY)
    if defaults.KEYFILE is not None:
        return KeyfileAuthenticator(defaults.KEYFILE, defaults.KEYFILE_PASSWORD)
    return None
