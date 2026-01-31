# Validation checklist

Use this list to preflight a product before pinning or PR submission.

## Forecastathon rules

- Builder address is registered for Forecastathon.
- startTime is at least two full working days after PR submission.
- Correct oracleAddress and collateralAsset for the selected network.
- Only one environment per PR (bakerloo or mainnet).
- Product is unleveraged with explicit minPrice and maxPrice.
- Extended metadata is pinned on IPFS as DAG-CBOR.
- API source is reachable and freely accessible.

## On-chain product (PredictionProductV1)

- minPrice < maxPrice.
- startTime < earliestFSPSubmissionTime.
- builder and contract addresses are valid checksummed EVM addresses.
- symbol matches required pattern if time series.

## Extended metadata

- outcome_space.fsp_type matches outcome_point.fsp_type.
- outcome_space.base_case and edge_cases have non-empty condition and
  fsp_resolution strings.
- Template variables in conditions resolve against outcome_point.
- oracle_fallback.fallback_time >= earliestFSPSubmissionTime + 7 days.
- oracle_fallback.fallback_fsp within [minPrice, maxPrice].
- OracleConfig and ApiSpec fields are present when used.

## Time series symbol format

Symbols encode the release date and frequency. Month codes:
F=Jan, G=Feb, H=Mar, J=Apr, K=May, M=Jun, N=Jul, Q=Aug, U=Sep, V=Oct,
X=Nov, Z=Dec.

Patterns (prefix is 1-8 uppercase letters):

- daily: PREFIXDDMYY (DD day, M month code, YY year)
- weekly/fortnightly: PREFIXWW WYY (ISO week number)
- semimonthly: PREFIX1MYY or PREFIX2MYY (1 = days 1-15, 2 = days 16+)
- monthly/quarterly: PREFIXMYY
- yearly: PREFIXYYYY

Release date in outcome_point must match the symbol date encoding.
