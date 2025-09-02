## [v0.2.1] - 2025-09-02

### Added

- Add SystemViewer contract bindings ([#15](https://github.com/autonity/afp-sdk/pull/15))

### Changed

- Change the data type of Trade ID from integer to string ([#14](https://github.com/autonity/afp-sdk/pull/14))

## [v0.2.0] - 2025-09-02

### Changed

- Validate limit price to make sure it conforms to the product's tick size ([#12](https://github.com/autonity/afp-sdk/pull/12))
- Update Clearing System contract bindings for Autonity Bakerloo (Nile) Testnet deployment as of 2025-09-02 ([#13](https://github.com/autonity/afp-sdk/pull/13))

### Added

- Add optional `rounding` argument to `afp.Trading.create_intent` ([#12](https://github.com/autonity/afp-sdk/pull/12))

## [v0.1.2] - 2025-08-28

### Fixed

- Fix oracle specification decimal parsing in `afp.Builder.create_product` ([#9](https://github.com/autonity/afp-sdk/pull/9))

## [v0.1.1] - 2025-08-28

### Fixed

- Fix incorrect parameter type in `afp.bindings.ClearingDiamond.mutializeLosses` ([#8](https://github.com/autonity/afp-sdk/pull/8))

## [v0.1.0] - 2025-08-22

_First release._

[v0.2.1]: https://github.com/autonity/afp-sdk/releases/tag/v0.2.1
[v0.2.0]: https://github.com/autonity/afp-sdk/releases/tag/v0.2.0
[v0.1.2]: https://github.com/autonity/afp-sdk/releases/tag/v0.1.2
[v0.1.1]: https://github.com/autonity/afp-sdk/releases/tag/v0.1.1
[v0.1.0]: https://github.com/autonity/afp-sdk/releases/tag/v0.1.0
