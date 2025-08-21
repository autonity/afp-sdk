from itertools import chain

from web3 import Web3

from .. import config
from . import (
    auctioneer_facet,
    bankruptcy_facet,
    clearing_facet,
    final_settlement_facet,
    margin_account_registry,
    mark_price_tracker_facet,
    oracle_provider,
    product_registry,
)

# In order to include a facet in the ClearingDiamond facade:
# 1. Add its ABI to CLEARING_DIAMOND_ABI
# 2. Set its contract binding as a superclass of ClearingDiamond

CLEARING_DIAMOND_ABI = list(
    chain(
        auctioneer_facet.ABI,
        bankruptcy_facet.ABI,
        clearing_facet.ABI,
        final_settlement_facet.ABI,
        mark_price_tracker_facet.ABI,
    )
)


class ClearingDiamond(
    auctioneer_facet.AuctioneerFacet,
    bankruptcy_facet.BankruptcyFacet,
    clearing_facet.ClearingFacet,
    final_settlement_facet.FinalSettlementFacet,
    mark_price_tracker_facet.MarkPriceTrackerFacet,
):
    """ClearingDiamond contract binding.

    Includes all functions inherited from various facets.

    Parameters
    ----------
    w3 : web3.Web3
    """

    def __init__(self, w3: Web3):
        self._contract = w3.eth.contract(
            address=config.CLEARING_DIAMOND_ADDRESS, abi=CLEARING_DIAMOND_ABI
        )


class MarginAccountRegistry(margin_account_registry.MarginAccountRegistry):
    """MarginAccountRegistry contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    """

    def __init__(self, w3: Web3):
        super().__init__(w3, config.MARGIN_ACCOUNT_REGISTRY_ADDRESS)


class OracleProvider(oracle_provider.OracleProvider):
    """OracleProvider contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    """

    def __init__(self, w3: Web3):
        super().__init__(w3, config.ORACLE_PROVIDER_ADDRESS)


class ProductRegistry(product_registry.ProductRegistry):
    """ProductRegistry contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    """

    def __init__(self, w3: Web3):
        super().__init__(w3, config.PRODUCT_REGISTRY_ADDRESS)
