---
type: Metric
title: VIX
description: Cboe S&P 500 implied-volatility index with a descriptive trailing closing-low metric.
resource: https://www.cboe.com/tradable_products/vix/faqs
tags: [VIX, S&P 500, index, volatility]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-26T10:37:53Z"
sources:
  - id: cboe-faq
    resource: https://www.cboe.com/tradable_products/vix/faqs
    title: Cboe VIX FAQ
  - id: cboe-volatility
    resource: https://www.cboe.com/tradable-products/volatility-trading/
    title: Cboe volatility trading and index interpretation
  - id: provider-reference
    resource: /references/data-providers.md
    title: Provider coverage and stored-series treatment
market_report:
  symbol: CBOE:VIX
  section: sp500
  definition_status: issuer_sourced
  implementation_status: metrics_available
  evidence_status: exploratory
  enabled: false
  report_metrics: [close, day_low]
  day_low_default_period: 365
  units: index_points
  data_providers:
    tradingview:
      status: available
      symbol: CBOE:VIX
    alpaca:
      status: unavailable
      reason: Spot volatility indices are outside Alpaca stock/ETF bar coverage.
---
# Definition

VIX measures expected S&P 500 volatility over a constant 30-day horizon,
inferred from SPX option bid/ask quotations. It is forward-looking implied
volatility, rather than realized historical volatility.[^cboe-faq]
The index is expressed as an annualized standard deviation; it describes
the magnitude of expected moves, not their direction.[^cboe-volatility]

# Report context

Display the spot index alongside [SPY](/index/spy.md) in the S&P 500 section.
Use `CBOE:VIX`, not a broker CFD, VIX futures contract, or volatility ETF.
The spot index cannot itself be bought and held.[^cboe-faq]
Do not infer an equity buying or selling rule from a low reading without
an appropriately documented study.

# Day low

This is a project-specific descriptive statistic, not a Cboe-defined metric.
It is the longest trailing window, ending at the latest observation, in
which that observation is strictly lower than every earlier close.
Count the latest observation in the window. Return zero if the latest
observation is higher than or equal to the previous close, or there is no
previous observation. An equal earlier close stops the window.

Examples, oldest to newest:

| Closes | Day low |
|---|---:|
| 12, 11, 10 | 3 |
| 10, 12, 11 | 2 |
| 12, 10, 11 | 0 |
| 12, 10, 10 | 0 |

`lowest_close(symbol, period)` in `price_utils.py` reads archived daily bars;
`lowest_close_period(closes, period)` in `price_stats.py` is the pure calculator.
Period caps the total number of observations searched, including the latest.
The report defaults to 365 trading sessions, not calendar days. A strict
new low across all 365 available closes returns 365. Reaching the start of
the window gives a lower bound; a longer history may support a larger span.
Insufficient history is disclosed rather than extrapolated. Utility calls
can omit period to search all available closes.

# Timing and limitations

Cboe describes a regular calculation session ending at 16:15 ET.[^cboe-faq]
A same-day observation fetched before that time is labeled intraday and its
day-low result provisional. This metric uses daily closes, not intraday lows.
Timestamps, provider revisions, missing sessions, and available-history depth
can affect results. Historical reports filter by observation date and do not
recreate old data revisions. No return-prediction claim is validated here.

Alpaca stock/ETF bars do not supply this spot index; a stored TradingView
substitution must retain its provider label.[^provider-reference]

[^cboe-faq]: Cboe VIX FAQ, consulted 2026-10-26.
[^cboe-volatility]: Cboe volatility trading overview, consulted 2026-10-26.
[^provider-reference]: Project provider reference; index coverage differs from US-stock/ETF coverage.
