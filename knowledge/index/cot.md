---
type: Metric
title: S&P 500 and Nasdaq futures positioning
description: Weekly CFTC consolidated futures-only trader positions with daily continuous E-mini price context.
tags: [COT, futures, SPY, Nasdaq, positioning]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-11-04T20:46:07Z"
sources:
  - id: cftc-history
    resource: https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm
    title: Official CFTC historical TFF futures-only archives
  - id: cftc-current
    resource: https://www.cftc.gov/dea/futures/financial_lf.htm
    title: Current CFTC TFF futures-only report
  - id: ofr-tff
    resource: https://www.financialresearch.gov/hedge-fund-monitor/datasets/tff/
    title: OFR explanation of TFF categories and consolidated contracts
market_report:
  section: cot
  implementation_status: metrics_available
  evidence_status: descriptive
  enabled: false
---
# Scope and calculation

Use only CFTC consolidated futures-only codes `13874+` (S&P 500) and `20974+`
(Nasdaq-100). Preserve the five groups: dealers, asset managers, leveraged funds,
other reportables and non-reportable positions. Net contracts equal gross longs
minus gross shorts; preserve gross values and open interest.[^cftc-current]
Consolidation covers multiple fungible contract sizes, so these series are not
interchangeable with an E-mini-only or futures-and-options-combined series.[^ofr-tff]

# Report display and interpretation

Each market has one combined chart: daily continuous E-mini candles above weekly
net-position bars, on separate axes, plus a one- or two-sentence interpretation.
The default view is 12 months. Colors identify groups; positive bars are net long
and negative bars net short. Every market labels its latest position date and
price date separately. Positioning is plotted on Tuesday observation dates,
normally published later that week; historical charts are not trading backtests.

ES1!/NQ1! prices are context for consolidated positioning, not exactly the same
contract universe. Continuous-contract rolls can affect price comparisons.
TradingView bars opening at or after 17:00 Chicago time are assigned the following
session date. Raw OHLCV remains in the ordinary dated bar store. Price-derived
returns and predictive positioning rules are not implemented here.

Position counts do not alone establish sentiment, crowding or an actionable
reversal: hedging and relative-value strategies may offset positions elsewhere.
A 12-month chart does not establish a validated historical extreme.

# Storage and refresh

Download the prior and current calendar-year CFTC TFF futures-only ZIP archives
with `uv run cot.py --refresh`. Preserve source files, actual fetch timestamps,
URLs and SHA-256 hashes under `data/cot/<download-date>/`.[^cftc-history]
The derived snapshot records all weekly values for both indexes. Duplicate
conflicts fail validation; source net-reconciliation residuals of up to five
contracts are retained without forcing equality, while larger residuals fail.

Snapshot report runs read stored COT data and prices. Fresh TradingView report
runs additionally refresh ES/NQ price bars and check the CFTC archives, reusing
same-download-day archives unless `cot.py --refresh` is explicitly used. A failed
CFTC refresh is reported and retains the stored snapshot. This weekly dataset
has a separate source and cadence from daily prices and earnings caches.

# TODOs

- [ ] Download historical COT data for S&P 500 and Nasdaq-100 futures and create long-term historical charts.
  - Check the earliest available coverage for each market and retain source archives, fetch timestamps and hashes.
  - Document contract-consolidation and trader-classification changes before joining older history.
  - Add selectable chart lookbacks while keeping weekly position dates distinct from publication dates.

[^cftc-history]: CFTC historical compressed report page; TFF futures-only text archives for 2025 and 2026 retrieved 2026-11-04.
[^cftc-current]: Current official report observed 2026-11-04, with positions as of 2026-10-27.
[^ofr-tff]: US Treasury OFR explains report categories and consolidation of fungible contracts.
