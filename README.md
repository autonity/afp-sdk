# Autonomous Futures Protocol Python SDK

Decentralized clearing and creation of Forecast Futures on any timeseries.

![CI](https://github.com/autonity/afp-sdk/actions/workflows/ci.yml/badge.svg)

## Installation

This library is published on PyPI as the [afp-sdk](https://pypi.org/project/afp-sdk/)
package. It can be installed in a virtualenv with:

```py
pip install afp-sdk
```

## Documentation

See [afp.autonity.org](https://afp.autonity.org/) for the Autonomous Futures Protocol
documentation, including the Python SDK reference.

## Overview

The `afp` package consists of the following:

- `afp` top-level module: High-level API for interacting with the AFP Clearing
  System and the AutEx exchange.
- `afp.bindings` submodule: Low-level API that provides typed Python bindings
  for the Clearing System smart contracts.

## Configuration

By default the SDK communicates with the AFP Clearing System contracts on
Autonity Mainnet, and the AutEx Exchange. Connection parameters can be
overridden via the `afp.AFP` constructor and environment variables; see the
documentation of the `afp.AFP` class for the available parameters.

## Usage

### Preparation

In order to trade in the AFP system, traders need to prepare the following:

- The ID of a product to be traded.
- The address of the product's collateral token.
- An Autonity account for managing the margin account. It needs to hold a
  balance in ATN (for paying gas fee) and in the product's collateral token.
- An Autonity account for signing intents and submitting trades to the
  exchange. The two accounts can be the same.
- The address of an Autonity RPC provider. They can be found on
  [Chainlist](https://chainlist.org/?search=autonity).

We can store those in the following constants (using random example IDs):

```py
import os

PRODUCT_ID = "0x38d502bb683f53ec7c3d7a14b4aa47ac717659e121426131c0189c15bf4b9460"
COLLATERAL_ASSET = "0xD1A1e4035a164cF42228A8aAaBC2c0Ac9e49687B"
PRIVATE_KEY = os.environ["PRIVATE_KEY"]
AUTONITY_RPC_URL = "https://bakerloo.autonity-apis.com"
```

### Configuration

An application instance can be created with the `afp.AFP()` constructor. An instance
is associated with a trading venue and a margin account.

The required constructor arguments are the RPC provider URL and the authenticator of
the blockchain account that manages the margin account.

An "authenticator" is a service that implements the `afp.Authenticator` protocol.
Available options are `afp.PrivateKeyAuthenticator` that reads the private key
from a constructor argument, and `afp.KeyfileAuthenticator` that reads the private
key from an encrypted keyfile.

```py
import afp

app = afp.AFP(
    rpc_url=AUTONITY_RPC_URL,
    authenticator=afp.PrivateKeyAuthenticator(PRIVATE_KEY),
)
```

### Margin Account API

Margin accounts can be managed via the `MarginAccount` session object. It
connects to the specified Autonity RPC provider and communicates with the
Clearing System smart contracts.

```py
margin_account = app.MarginAccount()
```

Collateral can be deposited into the margin account with `margin_account.deposit()`.

```py
from decimal import Decimal

margin_account.deposit(COLLATERAL_ASSET, Decimal("100.00"))
print(margin_account.capital(COLLATERAL_ASSET))
```

### Trading API

Functions of the trading API can be accessed via the `Trading` session object.
It communicates with the AutEx exchange and authenticates on creation with the
intent account's private key. The intent account authenticator is optional, it
defaults to the authenticator set in the `AFP` constructor.

```py
trading = app.Trading()
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

- Install dependencies with the `uv sync` command.
- Execute linters with the `uv run poe lint` command.
- Run tests with the `uv run poe test` command.
- Check distributions before release with the `uv run poe check-dist` command.
- Generate markdown API documentation with the `uv run poe doc-gen` command.
