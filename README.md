# Autonity Futures Protocol Python SDK

## Installation

The library can be installed in a virtualenv with:

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
- An Autonity account for managing the margin account. It needs to hold a
  balance in ATN (for paying gas fee) and in the product's collateral token.
- An Autonity account for signing intents. The two accounts can be the same.
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

The intent account should be authorized to submit orders. This is only required
if the intent account and the margin account are different.

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

## Development

The package uses [`uv`](https://docs.astral.sh/uv/) as project manager.

- Dependecies can be installed with the `uv sync` command.
- Linters can be executed with the `uv run poe lint` command.
- Tests can be executed with the `uv run poe test` command.
- Distributions can be checked before release with the `uv run poe check-dist` command.
- Markdown API documentation can be generated with the `uv run poe doc-gen` command.
