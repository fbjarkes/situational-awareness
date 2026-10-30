---
type: Metric
title: Market leaders
description: Top ten theme stocks ranked by weighted relative price performance versus SPY and proximity to their 52-week closing highs.
tags: [market-leaders, relative-strength, stocks, themes]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-30T22:33:06Z"
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
    1W: 0.20
    1M: 0.20
    3M: 0.20
    6M: 0.20
  proximity_weight: 0.20
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
The composite score is `sum(weight_h * RS_h) + proximity_weight * distance`,
with weights summing to one. Each return period has 20% weight; proximity has
20% weight. `distance = 100 * (latest close / trailing_high_close - 1)` is zero
at the high and negative below it. The high is the highest split-adjusted close
in the trailing 252 SPY trading sessions, including the latest observation.
Require a valid close for every one of those sessions; shorter listings or gaps
are excluded instead of using a since-listing high. Record the high close,
window start, distance, and return-only RS alongside the composite in JSON.
This is a project scoring convention, not optimized or validated coefficients.
The composite is expressed in points, not a pure relative-return percentage,
percentile, or 1–99 rating. A negative score can reflect the proximity penalty
even when the stock outperformed SPY.
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

Display one table with composite score, distance from the 52-week closing high, and four component RS values, followed
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
