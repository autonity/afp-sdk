# Autonomous Futures Protocol Python SDK

## Installation

This library is published on PyPI as the [afp-sdk](https://pypi.org/project/afp-sdk/)
package. It can be installed in a virtualenv with:

```py
pip install afp-sdk
```

## Overview

The `afp` package consists of the following:

- `afp` top-level module: High-level API for interacting with the Clearing
  System and the AutEx exchange.
- `afp.bindings` submodule: Low-level API that provides typed Python bindings
  for the Clearing System smart contracts.

## Usage

### Preparation

In order to use the AFP system, traders need to prepare the following:

- The ID of a product to be traded.
- The address of the product's collateral token.
- An Autonity account for managing the margin account. It needs to hold a
  balance in ATN (for paying gas fee) and in the product's collateral token.
- An Autonity account for signing intents. The two accounts can be the same.
- The address of an Autonity RPC provider. They can be found on
  [Chainlist](https://chainlist.org/?search=autonity&testnets=true).

We can store those in the following constants (using random example IDs):

```py
import os

PRODUCT_ID = "0x38d502bb683f53ec7c3d7a14b4aa47ac717659e121426131c0189c15bf4b9460"
COLLATERAL_ASSET = "0xD1A1e4035a164cF42228A8aAaBC2c0Ac9e49687B"
MARGIN_ACCOUNT_PRIVATE_KEY = os.environ["MARGIN_ACCOUNT_PRIVATE_KEY"]
INTENT_ACCOUNT_PRIVATE_KEY = os.environ["INTENT_ACCOUNT_PRIVATE_KEY"]
AUTONITY_RPC_URL = "https://bakerloo.autonity-apis.com"
```

Account IDs (addresses) may be retrieved from the private keys with `eth_account`:

```py
from eth_account import Account

MARGIN_ACCOUNT_ID = Account.from_key(MARGIN_ACCOUNT_PRIVATE_KEY).address
INTENT_ACCOUNT_ID = Account.from_key(INTENT_ACCOUNT_PRIVATE_KEY).address
```

### Clearing API

Functions of the Clearing API can be accessed via the `afp.Clearing`
session object. It connects to the specified Autonity RPC provider and
communicates with the Clearing System smart contracts.

```py
import afp

clearing = afp.Clearing(MARGIN_ACCOUNT_PRIVATE_KEY, AUTONITY_RPC_URL)
```

Collateral can be deposited into the margin account with
`clearing.deposit_into_margin_account()`.

```py
from decimal import Decimal

clearing.deposit_into_margin_account(COLLATERAL_ASSET, Decimal("100.00"))
print(clearing.capital(COLLATERAL_ASSET))
```

The intent account should be authorized to submit orders. This is only required
if the intent account and the margin account are different.

```py
clearing.authorize(COLLATERAL_ASSET, INTENT_ACCOUNT_ID)
```

### Trading API

The functions of the trading API can be accessed via the `afp.Trading` session
object. It communicates with the AutEx exchange and authenticates on creation with
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
`trading.submit_limit_order()` that returns the created order object.

```py
order = trading.submit_limit_order(intent)
print(order)
```

The exchange then performs various checks to ensure that the order is valid. To
ensure that the order has been accepted, its state can be polled with
`trading.order()`.

```py
order = trading.order(order.id)
print(order.state)
```

Fills of orders submitted by the authenticated intent account can be queried
with `trading.order_fills()`.

```py
fills = trading.order_fills(product_id=PRODUCT_ID)
print(fills)
```

See further code examples in the [examples](./examples/) directory.

## Development

The package uses [`uv`](https://docs.astral.sh/uv/) as project manager.

- Dependecies can be installed with the `uv sync` command.
- Linters can be executed with the `uv run poe lint` command.
- Tests can be executed with the `uv run poe test` command.
- Distributions can be checked before release with the `uv run poe check-dist` command.
- Markdown API documentation can be generated with the `uv run poe doc-gen` command.
