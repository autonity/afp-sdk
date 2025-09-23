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

[v0.5.1]: https://github.com/autonity/afp-sdk/releases/tag/v0.5.1
[v0.5.0]: https://github.com/autonity/afp-sdk/releases/tag/v0.5.0
[v0.4.0]: https://github.com/autonity/afp-sdk/releases/tag/v0.4.0
[v0.3.0]: https://github.com/autonity/afp-sdk/releases/tag/v0.3.0
