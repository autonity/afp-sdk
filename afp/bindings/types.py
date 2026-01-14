import enum
import typing
from dataclasses import dataclass

import eth_typing
import hexbytes


class Side(enum.IntEnum):
    """Port of `enum Side` on the ClearingFacet contract."""

    BID = 0
    ASK = 1


class ProductState(enum.IntEnum):
    """Port of `enum ProductState` on the ProductRegistry contract."""

    NOT_EXIST = 0
    PENDING = 1
    LIVE = 2
    TRADEOUT = 3
    FINAL_SETTLEMENT = 4
    EXPIRED = 5


@dataclass
class ClearingConfig:
    """Port of `struct ClearingConfig` on the AdminFacet contract."""

    clearing_fee_rate: int
    max_trading_fee_rate: int


@dataclass
class MarkPriceConfig:
    """Port of `struct MarkPriceConfig` on the AdminFacet contract."""

    mark_price_interval: int


@dataclass
class FinalSettlementConfig:
    """Port of `struct FinalSettlementConfig` on the AdminFacet contract."""

    closeout_fee_rate: int
    closeout_reward_rate: int


@dataclass
class ProductConfig:
    """Port of `struct ProductConfig` on the AdminFacet contract."""

    clearing_payout_ratio: int
    maintenance_deposit_interval: int
    min_product_maintenance_fee: int


@dataclass
class Config:
    """Port of `struct Config` on the AdminFacet contract."""

    clearing_config: ClearingConfig
    mark_price_config: MarkPriceConfig
    final_settlement_config: FinalSettlementConfig
    product_config: ProductConfig


@dataclass
class IntentData:
    """Port of `struct IntentData` on the ClearingFacet contract."""

    nonce: int
    trading_protocol_id: eth_typing.ChecksumAddress
    product_id: hexbytes.HexBytes
    limit_price: int
    quantity: int
    max_trading_fee_rate: int
    good_until: int
    side: Side
    referral: eth_typing.ChecksumAddress


@dataclass
class Intent:
    """Port of `struct Intent` on the ClearingFacet contract."""

    margin_account_id: eth_typing.ChecksumAddress
    intent_account_id: eth_typing.ChecksumAddress
    hash: hexbytes.HexBytes
    data: IntentData
    signature: hexbytes.HexBytes


@dataclass
class Trade:
    """Port of `struct Trade` on the ClearingFacet contract."""

    product_id: hexbytes.HexBytes
    protocol_id: eth_typing.ChecksumAddress
    trade_id: int
    price: int
    timestamp: int
    quantity: int
    accounts: typing.List[eth_typing.ChecksumAddress]
    quantities: typing.List[int]
    fee_rates: typing.List[int]
    intents: typing.List[Intent]


@dataclass
class Settlement:
    """Port of `struct Settlement` on the MarginAccountFacet contract."""

    product_id: hexbytes.HexBytes
    quantity: int
    price: int


@dataclass
class MarginData:
    """Port of `struct MarginData` on the IMarginAccountFacet contract."""

    capital: int
    mae: int
    mmu: int
    pnl: int


@dataclass
class PositionData:
    """Port of `struct PositionData` on the MarginAccountFacet contract."""

    product_id: hexbytes.HexBytes
    quantity: int
    cost_basis: int
    maintenance_margin: int
    pnl: int


@dataclass
class ExpirySpecification:
    """Port of `struct ExpirySpecification` on the ProductRegistryFacet contract."""

    earliest_fsp_submission_time: int
    tradeout_interval: int


@dataclass
class ProductMetadata:
    """Port of `struct ProductMetadata` on the ProductRegistryFacet contract."""

    builder: eth_typing.ChecksumAddress
    symbol: str
    description: str


@dataclass
class OracleSpecification:
    """Port of `struct OracleSpecification` on the ProductRegistryFacet contract."""

    oracle_address: eth_typing.ChecksumAddress
    fsv_decimals: int
    fsp_alpha: int
    fsp_beta: int
    fsv_calldata: hexbytes.HexBytes


@dataclass
class BaseProduct:
    """Port of `struct BaseProduct` on the ProductRegistryFacet contract."""

    metadata: ProductMetadata
    oracle_spec: OracleSpecification
    collateral_asset: eth_typing.ChecksumAddress
    start_time: int
    point_value: int
    price_decimals: int
    extended_metadata: str


@dataclass
class MarginSpecification:
    """Port of `struct MarginSpecification` on the ProductRegistryFacet contract."""

    imr: int
    mmr: int


@dataclass
class FuturesProductV1:
    """Port of `struct FuturesProductV1` on the ProductRegistryFacet contract."""

    base: BaseProduct
    expiry_spec: ExpirySpecification
    margin_spec: MarginSpecification


@dataclass
class PredictionProductV1:
    """Port of `struct PredictionProductV1` on the ProductRegistryFacet contract."""

    base: BaseProduct
    expiry_spec: ExpirySpecification
    max_price: int
    min_price: int
