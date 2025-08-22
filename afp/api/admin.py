from .. import validators
from ..decorators import refresh_token_on_expiry
from ..schemas import ExchangeProductSubmission
from .base import ExchangeAPI


class Admin(ExchangeAPI):
    """API for AutEx administration, restricted to AutEx admins.

    Authenticates with the exchange on creation.

    Parameters
    ----------
    private_key : str
        The private key of the exchange adminstrator account.

    Raises
    ------
    afp.exceptions.AuthenticationError
        If the exchange rejects the login attempt.
    """

    @refresh_token_on_expiry
    def approve_product(self, product_id: str) -> None:
        """Approves a product for trading on the exchange.

        Parameters
        ----------
        product_id : str

        Raises
        ------
        afp.exceptions.AuthorizationError
            If the configured account is not an exchange administrator.
        """
        product = ExchangeProductSubmission(id=product_id)
        self._exchange.approve_product(product)

    @refresh_token_on_expiry
    def delist_product(self, product_id: str) -> None:
        """Delists a product from the exchange.

        New order submissions of this product will be rejected.

        Parameters
        ----------
        product_id : str

        Raises
        ------
        afp.exceptions.AuthorizationError
            If the configured account is not an exchange administrator.
        """
        value = validators.validate_hexstr32(product_id)
        self._exchange.delist_product(value)
