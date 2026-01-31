# Public API sources (examples)

Each example below includes a sample endpoint and a matching ApiSpecJSONPath
snippet. Verify the endpoint response and terms of use before finalizing.

## Open-Meteo (weather, no key for non-commercial)

Sample endpoint:

`https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=temperature_2m_max&timezone=UTC`

ApiSpecJSONPath:

```json
{
  "standard": "JSONPath",
  "spec_variant": "underlying-history",
  "url": "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=temperature_2m_max&timezone=UTC",
  "date_path": "$.daily.time[*]",
  "value_path": "$.daily.temperature_2m_max[*]",
  "date_format_type": "iso_8601",
  "timezone": "UTC"
}
```

Notes:
- Returns ISO 8601 dates in `daily.time`.
- Ensure daily arrays align (same length).

## Climate Monitor (climate, public)

Sample endpoint:

`https://climatemonitor.info/api/public/v1/co2/monthly_gl`

ApiSpecJSONPath:

```json
{
  "standard": "JSONPath",
  "spec_variant": "underlying-history",
  "url": "https://climatemonitor.info/api/public/v1/co2/monthly_gl",
  "date_path": "$.data.readings[*].label",
  "value_path": "$.data.readings[*].value",
  "date_format_type": "iso_8601",
  "timezone": "UTC"
}
```

Notes:
- Response is JSend; data lives under `data.readings`.
- Labels are ISO 8601 dates in the example payloads.

## World Bank Indicators API (economic, public)

Sample endpoint:

`https://api.worldbank.org/v2/country/USA/indicator/FP.CPI.TOTL?format=json&per_page=1000`

ApiSpecJSONPath:

```json
{
  "standard": "JSONPath",
  "spec_variant": "underlying-history",
  "url": "https://api.worldbank.org/v2/country/USA/indicator/FP.CPI.TOTL?format=json&per_page=1000",
  "date_path": "$[1][*].date",
  "value_path": "$[1][*].value",
  "date_format_type": "custom",
  "date_format_custom": "%Y",
  "timezone": "UTC",
  "max_pages": 1
}
```

Notes:
- The `date` field is a year string (YYYY). Use a custom format.
- Set `per_page` high to avoid pagination and keep `max_pages` small.

## CoinGecko Market Chart (crypto, public with rate limits)

Sample endpoint:

`https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=90`

ApiSpecJSONPath:

```json
{
  "standard": "JSONPath",
  "spec_variant": "underlying-history",
  "url": "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=90",
  "date_path": "$.prices[*][0]",
  "value_path": "$.prices[*][1]",
  "date_format_type": "unix_timestamp",
  "timestamp_scale": 1000,
  "timezone": "UTC"
}
```

Notes:
- Timestamps are milliseconds since epoch.
- Check current API terms and rate limits; free access may be limited.
