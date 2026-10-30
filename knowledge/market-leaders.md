---
type: Metric
title: Market leaders
description: Top ten theme stocks ranked by weighted multi-period relative price performance versus SPY.
tags: [market-leaders, relative-strength, stocks, themes]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-30T22:13:23Z"
sources:
  - id: memberships
    resource: /themes/theme-memberships.md
    title: Authoritative current theme stock memberships and separate fund exposures
  - id: rs-method
    resource: /references/theme-returns.md
    title: Shared relative price ratio and horizon conventions
market_report:
  section: market-leaders
  implementation_status: metrics_available
  evidence_status: descriptive
  enabled: false
  weights:
    1W: 0.25
    1M: 0.25
    3M: 0.25
    6M: 0.25
---
# Universe

Compare all US-listed stocks in current theme memberships, including core stocks
and extended candidates; deduplicate securities across themes. Exclude ETFs and
other separately tracked funds. Include the US-listed subset of the existing GDX
holdings when its explicit symbol map is available. Display each leader's theme
memberships alongside its ticker.[^memberships]

# Score

For each horizon, compute `RS_h = 100 * ((1 + stock_return_h) /
(1 + SPY_return_h) - 1)`, with fractional returns inside the formula.
The composite score is `sum(weight_h * RS_h) / sum(weight_h)` for 1W, 1M, 3M,
and 6M. Initial weights are 25% each; these are project defaults, not optimized
or validated coefficients. Positive scores indicate average relative
outperformance; this score is a percentage, not a percentile or 1–99 rating.
Sort descending and display the top ten; break exact ties by canonical symbol.
The top ten may include negative scores if the entire universe lags SPY.

1W means five trading-session intervals. Calendar-month horizons use the last
SPY session on or before the anniversary. Stock and benchmark use the same
start and end dates and split-adjusted USD price bars, excluding dividends.
Retain corporate-identity cutoffs, including reused SPCX and PURR tickers.
Require complete stock and benchmark histories for every horizon; exclude
ineligible stocks and report the reasons instead of redistributing weights.
No missing-bar forward filling is permitted.[^rs-method]

# Interpretation and reproducibility

Display one table with composite RS and its four component RS values, followed
by one or two descriptive sentences. Record provider, download batch, common
observation/start dates, weights, benchmark returns, input hashes, memberships,
eligible count, and excluded stocks in report JSON. Unavailable stored histories
remain excluded; do not silently fetch or mix providers/batches.

Current theme membership creates selection and survivorship bias. Overlapping
periods and overlapping theme exposures are correlated. This descriptive screen
does not establish forward returns, risk-adjusted superiority, or a buying rule;
`enabled: false` refers to unvalidated trading rules, not the descriptive table.

[^memberships]: Current project stock membership records, including optional extended candidates and linked GDX holdings; not historical point-in-time membership.
[^rs-method]: Shared project price-ratio and calendar-alignment definitions; descriptive calculations are not an independently validated market claim.
