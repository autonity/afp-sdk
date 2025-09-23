from .. import validators
from ..decorators import refresh_token_on_expiry
from ..enums import ListingState
from ..schemas import ExchangeProductListingSubmission, ExchangeProductUpdateSubmission
from .base import ExchangeAPI


class Admin(ExchangeAPI):
    """API for AutEx administration, restricted to AutEx admins."""

    @refresh_token_on_expiry
    def list_product(self, product_id: str) -> None:
        """Lists a product on the exchange.

        The product is in private state after listing until it is revealed to the public.

        Parameters
        ----------
        product_id : str

        Raises
        ------
        afp.exceptions.AuthorizationError
            If the configured account is not an exchange administrator.
        """
        product_listing = ExchangeProductListingSubmission(id=product_id)
        self._exchange.list_product(product_listing)

    @refresh_token_on_expiry
    def reveal_product(self, product_id: str) -> None:
        """Makes a product publicly available for trading on the exchange.

        Parameters
        ----------
        product_id : str

        Raises
        ------
        afp.exceptions.AuthorizationError
            If the configured account is not an exchange administrator.
        """
        product_update = ExchangeProductUpdateSubmission(
            listing_state=ListingState.PUBLIC
        )
        self._exchange.update_product_listing(
            validators.validate_hexstr32(product_id), product_update
        )

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
        product_update = ExchangeProductUpdateSubmission(
            listing_state=ListingState.DELISTED
        )
        self._exchange.update_product_listing(
            validators.validate_hexstr32(product_id), product_update
        )
