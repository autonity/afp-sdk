# Development

The package uses [`uv`](https://docs.astral.sh/uv/) as project manager.

- Install dependencies with the `uv sync` command.
- Execute linters with the `uv run poe lint` command.
- Run tests with the `uv run poe test` command.
- Check distributions before release with the `uv run poe check-dist` command.
- Generate markdown API documentation with the `uv run poe doc-gen` command.

## Product Specification

A product specification is represented as a single JSON object, but it is stored
at two different places:

- The object under the `product` attribute is uploaded to the Product Registry contract.
- The other nested objects constitute the extended metadata and are uploaded to IPFS.
- The `extendedMetadata` property of the on-chain product specification stores
  the root CID of the IPFS DAG.

### Updating Extended Metadata Schemas

Extended metadata schemas are versioned and an IPFS CID is associated with each
version of each schema. For each schema there is also a matching Pydantic model
in the `afp.schemas` module.

When extended metadata schemas are updated, the related model updates should be
backwards-compatible to make sure existing products that use old schemas can be still
be downloaded from IPFS and parsed.

To modify models in backwards-compatible way, e.g. when the `OracleFallback` schema
is updated from v0.2.0 to v0.2.1, do the following:

- Make a private duplicate of the Pydantic model that needs to be updated, e.g.
  duplicate `OracleFallback` as `_OracleFallbackV020`.
- Modify the fields of the public model (`OracleFallback`) to match the updated
  schema.
- Update `OracleFallback.SCHEMA_CID` to the CID of the updated schema. Keep the
  old CID in `_OracleFallbackV020.SCHEMA_CID`.

With the above changes, if a product is downloaded that still uses the old
`OracleFallback` schema then it will be parsed using the `_OracleFallbackV020`
model, however users will see the updated `OracleFallback` schema as part of the
public API.
