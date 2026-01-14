from itertools import chain

from eth_typing.evm import ChecksumAddress

from web3 import Web3

from . import (
    admin_facet,
    clearing_facet,
    final_settlement_facet,
    margin_account_facet,
    margin_account_registry,
    mark_price_tracker_facet,
    oracle_provider,
    product_registry,
    product_registry_facet,
    system_viewer,
)
from ..constants import defaults

# In order to include a facet in the ClearingDiamond facade:
# 1. Add its ABI to CLEARING_DIAMOND_ABI
# 2. Set its contract binding as a superclass of ClearingDiamond

CLEARING_DIAMOND_ABI = list(
    chain(
        admin_facet.ABI,
        clearing_facet.ABI,
        final_settlement_facet.ABI,
        margin_account_facet.ABI,
        mark_price_tracker_facet.ABI,
        product_registry_facet.ABI,
    )
)


class ClearingDiamond(
    admin_facet.AdminFacet,
    clearing_facet.ClearingFacet,
    final_settlement_facet.FinalSettlementFacet,
    margin_account_facet.MarginAccountFacet,
    mark_price_tracker_facet.MarkPriceTrackerFacet,
    product_registry_facet.ProductRegistryFacet,
):
    """ClearingDiamond contract binding.

    Includes all functions inherited from various facets.

    Parameters
    ----------
    w3 : web3.Web3
    """

    def __init__(
        self, w3: Web3, address: ChecksumAddress = defaults.CLEARING_DIAMOND_ADDRESS
    ):
        self._contract = w3.eth.contract(address=address, abi=CLEARING_DIAMOND_ABI)


class MarginAccountRegistry(margin_account_registry.MarginAccountRegistry):
    """MarginAccountRegistry contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    """

    def __init__(
        self,
        w3: Web3,
        address: ChecksumAddress = defaults.MARGIN_ACCOUNT_REGISTRY_ADDRESS,
    ):
        super().__init__(w3, address)


class OracleProvider(oracle_provider.OracleProvider):
    """OracleProvider contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    """

    def __init__(
        self, w3: Web3, address: ChecksumAddress = defaults.ORACLE_PROVIDER_ADDRESS
    ):
        super().__init__(w3, address)


class ProductRegistry(product_registry.ProductRegistry):
    """ProductRegistry contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    """

    def __init__(
        self, w3: Web3, address: ChecksumAddress = defaults.PRODUCT_REGISTRY_ADDRESS
    ):
        super().__init__(w3, address)


class SystemViewer(system_viewer.SystemViewer):
    """SystemViewer contract binding.

    Parameters
    ----------
    w3 : web3.Web3
    """

    def __init__(
        self, w3: Web3, address: ChecksumAddress = defaults.SYSTEM_VIEWER_ADDRESS
    ):
        super().__init__(w3, address)
