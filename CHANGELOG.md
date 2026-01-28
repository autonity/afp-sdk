## [v0.6.0] - 2026-01-28

### Added

- Add Python 3.14 support ([#45](https://github.com/autonity/afp-sdk/pull/45))
- Add Prediction Product schemas to `afp.schemas` module for product creation ([#45](https://github.com/autonity/afp-sdk/pull/45))
- Add `Product.pin()` method for extended metadata IPFS upload an pinning ([#46](https://github.com/autonity/afp-sdk/pull/46))
- Add `Product.validate()` and `Product.validate_json()` methods for importing and validating product specifications ([#46](https://github.com/autonity/afp-sdk/pull/46))
- Add `Product.dump()` and `Product.dump_json()` methods for exporting product specifications ([#46](https://github.com/autonity/afp-sdk/pull/46))
- Add `Product.get()` method for downloading product specifications from Autonity & IPFS ([#46](https://github.com/autonity/afp-sdk/pull/46))

### Changed

- Update `Product.register()` method signature with the `initial_builder_stake` attribute ([#45](https://github.com/autonity/afp-sdk/pull/45))
- Update the AutEx exchange interface ([#42](https://github.com/autonity/afp-sdk/pull/42))
- Update contract bindings for the updated Clearing System interface ([#42](https://github.com/autonity/afp-sdk/pull/42))
- Update default contract addresses ([5948faa](https://github.com/autonity/afp-sdk/commit/5948faa1882a1ee1237936525df6534043b30f03))

### Removed

- Remove Python 3.11 support ([#45](https://github.com/autonity/afp-sdk/pull/45))
- Remove the `Product.create()` method ([#45](https://github.com/autonity/afp-sdk/pull/45))
- Remove deprecated methods `Trading.open_orders()`, `Product.create_product()`, `Product.register_product()` and `Product.product_state()` ([#41](https://github.com/autonity/afp-sdk/pull/41))

## [v0.5.4] - 2025-11-05

### Added

- Add `afp.exceptions.RateLimitExceeded` exception type ([#37](https://github.com/autonity/afp-sdk/pull/37))
- Add trading fee rate to `afp.schemas.OrderFill` structure ([#39](https://github.com/autonity/afp-sdk/pull/39))

### Changed

- Update for interface changes in the AutEx exchange ([#36](https://github.com/autonity/afp-sdk/pull/36))

## [v0.5.3] - 2025-10-29

### Added

- Add `Trading.ohlcv()` and `Trading.iter_ohlcv()` methods for querying OHLCV time series data ([#34](https://github.com/autonity/afp-sdk/pull/34))

### Changed

- Change `Trading.orders()`, `Trading.order_fills()` and `Trading.iter_order_fills()` to allow filtering items by intent account ID ([#33](https://github.com/autonity/afp-sdk/pull/33))

## [v0.5.2] - 2025-10-04

### Added

- Add `Trading.orders()` method for filtering orders based on multiple criteria ([#26](https://github.com/autonity/afp-sdk/pull/26))
- Add `trade_states` argument to `Trading.order_fills()` ([#26](https://github.com/autonity/afp-sdk/pull/26))

### Changed

- Change `Trading.products()`, `Trading.orders()` and `Trading.order_fills()` to retrieve items in batches ([#31](https://github.com/autonity/afp-sdk/pull/31))

### Fixed

- Raise `afp.exceptions.ExchangeError` for AutEx internal server errors instead of `afp.exceptions.ValidationError` ([#32](https://github.com/autonity/afp-sdk/pull/32))

### Removed

- Flag `Trading.open_orders()` method for deprecation. ([#26](https://github.com/autonity/afp-sdk/pull/26))

## [v0.5.1] - 2025-09-23

### Added

- Add `Admin.list_product()` and `Admin.reveal_product()` methods for the new 2-stage product listing process ([#28](https://github.com/autonity/afp-sdk/pull/28))
- Add `Product.create()`, `Product.register()` and `Product.state()` as short aliases for existing methods ([#27](https://github.com/autonity/afp-sdk/pull/27))

### Changed

- Flag `Product.create_product()`, `Product.register_product()` and `Product.product_state()` methods for deprecation ([#27](https://github.com/autonity/afp-sdk/pull/27))

### Removed

- Remove `Admin.approve_product()` method ([#28](https://github.com/autonity/afp-sdk/pull/28))

## [v0.5.0] - 2025-09-18

### Added

- Add key file authentication. ([#22](https://github.com/autonity/afp-sdk/pull/22))

### Changed

- Complete rework of the API and configuration management with breaking non backwards compatible changes. See the API reference. ([#22](https://github.com/autonity/afp-sdk/pull/22))

## [v0.4.0] - 2025-09-17

### Added

- Add `product_id` argument to `Trading.open_orders()` for filtering orders by product ([#21](https://github.com/autonity/afp-sdk/pull/21))
- Add new contract events to contract bindings ([#21](https://github.com/autonity/afp-sdk/pull/21))

### Removed

- Remove the `offer_price_buffer` product parameter from `Builder.create_product()` ([#23](https://github.com/autonity/afp-sdk/pull/23))

## [v0.3.0] - 2025-09-05

_First public release for Forecastathon._

[v0.6.0]: https://github.com/autonity/afp-sdk/releases/tag/v0.6.0
[v0.5.4]: https://github.com/autonity/afp-sdk/releases/tag/v0.5.4
[v0.5.3]: https://github.com/autonity/afp-sdk/releases/tag/v0.5.3
[v0.5.2]: https://github.com/autonity/afp-sdk/releases/tag/v0.5.2
[v0.5.1]: https://github.com/autonity/afp-sdk/releases/tag/v0.5.1
[v0.5.0]: https://github.com/autonity/afp-sdk/releases/tag/v0.5.0
[v0.4.0]: https://github.com/autonity/afp-sdk/releases/tag/v0.4.0
[v0.3.0]: https://github.com/autonity/afp-sdk/releases/tag/v0.3.0
