# Autonomous Futures System Python SDK

## Installation

The library can be installed in a virtualenv with:

```py
pip install afp-sdk
```

## Usage

### Preparation

In order to use the Futures System, traders need to prepare the following:

- The ID of a product to be traded.
- An Autonity account for managing the margin account. It needs to hold a
  balance in ATN (for paying gas fee) and in the product's collateral token.
- An Autonity account for signing intents.
- The address of an Autonity RPC provider. They can be found on
  [Chainlist](https://chainlist.org/?search=autonity&testnets=true).

We can store those in the following constants (using random example IDs):

```py
import os

PRODUCT_ID = "0x38d502bb683f53ec7c3d7a14b4aa47ac717659e121426131c0189c15bf4b9460"
MARGIN_ACCOUNT_ID = "0x214D8030d65d80586a84AD9C7acfa349D7301785"
MARGIN_ACCOUNT_PRIVATE_KEY = os.environ["MARGIN_ACCOUNT_PRIVATE_KEY"]
INTENT_ACCOUNT_ID = "0x32424b0E17F1084070cF432621d4F73bF4B0b997"
INTENT_ACCOUNT_PRIVATE_KEY = os.environ["INTENT_ACCOUNT_PRIVATE_KEY"]
AUTONITY_RPC_URL = "https://bakerloo.autonity-apis.com"
```

### Clearing API

The functions of the clearing API can be accessed via the `afp.Clearing`
session object. It connects to the specified Autonity RPC provider and
communicates with smart contracts related to the specified product.

```py
import afp

clearing = afp.Clearing(MARGIN_ACCOUNT_PRIVATE_KEY, AUTONITY_RPC_URL, PRODUCT_ID)
```

Collateral can be deposited into the margin account with
`clearing.deposit_into_margin_account()`.

```py
from decimal import Decimal

clearing.deposit_into_margin_account(Decimal("100.00"))
print(clearing.get_capital())
```

The intent account should be authorized to submit orders.

```py
clearing.authorize(INTENT_ACCOUNT_ID)
```

### Trading API

The functions of the trading API can be accessed via the `afp.Trading` session
object. It communicates with the exchange and authenticates on creation with
the intent account's private key.

```py
trading = afp.Trading(INTENT_ACCOUNT_PRIVATE_KEY)
```

To start trading a product, its parameters shall be retrieved from the server.

```py
product = trading.product(PRODUCT_ID)
```

Intents can be created with `trading.create_intent()`. Intent creation involves
hashing and signing the intent data. (The intent account's address is derived
from the private key specified in the `Trading` constructor.)

```py
from datetime import datetime, timedelta
from decimal import Decimal

intent = trading.create_intent(
    margin_account_id=MARGIN_ACCOUNT_ID,
    product=product,
    side="bid",
    limit_price=Decimal("1.23"),
    quantity=2,
    max_trading_fee_rate=Decimal("0.1"),
    good_until_time=datetime.now() + timedelta(hours=1),
)
```

The intent expressing a limit order can then be submitted to the exchange with
`trading.submit_limit_order()` that returns the accepted order, or raises
`afp.exceptions.OrderRejected` if the exchange rejects the order.

```py
order = trading.submit_limit_order(intent)
```

The exchange can be polled to get order fills with `trading.order_fills()`.

```py
from time import sleep

sleep(1)
print(trading.order_fills(product_id=PRODUCT_ID))
```

See further code examples in the [examples](./examples/) directory.

## API Reference

### Admin API

```py
admin = afp.Admin(admin_account_private_key)

admin.approve_product(product_id)
admin.delist_product(product_id)
```

### Builder API

```py
builder = afp.Builder(builder_account_private_key, autonity_rpc_url)

builder.create_product(symbol, description, start_time, oracle_address,
                       fsp_precision, alpha, beta, fsp_calldata,
                       earliest_fsp_submission_time, collateral_asset,
                       tick_size, unit_value, initial_margin_requirement,
                       maintenance_margin_requirement, clearing_fee_rate,
                       tradeout_interval, extended_metadata)
builder.register_product(product)

builder.product_state(product_id)
```

### Clearing API

```py
clearing = afp.Clearing(margin_account_private_key, autonity_rpc_url)

clearing.authorize(collateral_asset, intent_account_id)
clearing.deposit_into_margin_account(collateral_asset, amount)
clearing.withdraw_from_margin_account(collateral_asset, amount)
clearing.initiate_final_settlement(product_id, accounts)

clearing.collateral_asset(product_id)
clearing.product_state(product_id)

clearing.capital(collateral_asset)
clearing.maintenance_margin_available(collateral_asset)
clearing.maintenance_margin_used(collateral_asset)
clearing.margin_account_equity(collateral_asset)
clearing.position(collateral_asset, position_id)
clearing.positions(collateral_asset)
clearing.profit_and_loss(collateral_asset)
clearing.withdrawable_amount(collateral_asset)
```

### Trading API

```py
trading = afp.Trading(intent_account_private_key)

trading.create_intent(product, side, limit_price, quantity, max_trading_fee_rate,
                      good_until_time, [margin_account_id])
trading.submit_limit_order(intent)
trading.submit_cancel_order(intent_hash)

trading.products()
trading.product(product_id)
trading.market_depth(product_id)
trading.iter_market_depth(product_id)
trading.open_orders()
trading.order(intent_hash)
trading.order_fills([product_id], [intent_hash], [start], [end])
trading.iter_order_fills([product_id], [intent_hash])
```

### Liquidation API

```py
liquidation = afp.Liquidation(liquidator_account_private_key)

liquidation.request_liquidation(margin_account_id, collateral_asset)
liquidation.create_bid(product_id, price, quantity, side)
liquidation.submit_bids(margin_account_id, collateral_asset, bids)

liquidation.auction_data(margin_account_id, collateral_asset)
```

### Bindings API

```py
afp.bindings.ClearingDiamond(w3)
afp.bindings.MarginAccount(w3, address)
afp.bindings.MarginAccountRegistry(w3)
afp.bindings.OracleProvider(w3)
afp.bindings.ProductRegistry(w3)
afp.bindings.TradingProtocol(w3, address)
```

## Development

The package uses [`uv`](https://docs.astral.sh/uv/) as project manager.

- Dependecies can be installed with the `uv sync` command.
- Linters can be executed with the `uv run poe lint` command.
- Tests can be executed with the `uv run poe test` command.
- Distributions can be checked before release with the `uv run poe check-dist` command.
