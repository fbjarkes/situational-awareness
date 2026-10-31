---
type: Metric
title: SPY revenue growth screen
description: Descriptive screen for recorded SPY holdings with two latest consecutive quarters above 25 percent revenue growth year over year.
tags: [SPY, earnings, revenue, growth, screening]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-31T22:57:35Z"
sources:
  - id: holdings
    resource: /index/spy-holdings.md
    title: Recorded SPY holdings snapshot
market_report:
  section: spy-earnings
  implementation_status: metrics_available
  evidence_status: descriptive
  enabled: false
---
# Definition

Use the numbered listed securities in [SPY holdings](/index/spy-holdings.md).
Exclude cash/non-standard rows, preserve listed share classes, and resolve exact
tickers through a dated TradingView symbol map. This is a fixed holdings snapshot,
not a claim about today's official index membership.[^holdings]

Compare the latest two reported quarters, requiring consecutive, unique labels.
Both revenue YoY values must be strictly above 25%, calculated as
`100 * (quarter revenue / same quarter prior-year revenue - 1)`.
Require unique prior-year quarter labels and positive bases. Do not replace a
missing/failed latest pair with an older passing streak. Missing comparisons are
unassessable, not zero or failed screens. EPS is displayed but is not a filter.

# Output and limits

Display one row per matching security, with quarterly revenue/EPS YoY and actual
values. Rank by the lower revenue growth value of the latest pair, descending,
then canonical symbol. Record cache hashes, download times, holdings/map hashes,
coverage, and excluded securities in report JSON. Existing caches are reused
without expiry; no daily report run automatically downloads the full universe.

Provider duplicate quarter labels and incomplete histories limit coverage. Cached
financials can contain restatements, and fiscal labels/currency/EPS basis can be
unspecified. This is descriptive current-cache screening with membership and
selection bias, not point-in-time research or evidence of profitable trading.

[^holdings]: Issuer-reported SPY holdings snapshot as of 2026-10-22, retrieved 2026-10-26; see the linked dataset for source evidence.
