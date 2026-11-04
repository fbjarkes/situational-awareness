---
type: Metric
title: Consumer discretionary versus staples price ratio
description: RSPD divided by RSPS as a descriptive equal-weight sector-leadership study in Ratios.
tags: [breadth, relative-strength, RSPD, RSPS, sectors]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-11-04T22:26:27Z"
sources:
  - id: rspd-issuer
    resource: https://www.invesco.com/us-rest/contentdetail?contentId=1e0c7c23dbd92610VgnVCM1000006e36b50aRCRD&dnsName=us
    title: Invesco RSPD fund factsheet
  - id: rsps-issuer
    resource: https://www.invesco.com/content/dam/invesco/us/en/product-documents/etf/fact-sheet/rsps-invesco-s-p-500-equal-weight-consumer-staples-etf-us.pdf
    title: Invesco RSPS fund factsheet
market_report:
  section: ratios
  implementation_status: metrics_available
  evidence_status: descriptive
  enabled: false
---
# Definition

RSPD is the Invesco S&P 500 Equal Weight Consumer Discretionary ETF.[^rspd-issuer]
RSPS is the Invesco S&P 500 Equal Weight Consumer Staples ETF.[^rsps-issuer]
The ratio is `RSPD close / RSPS close` for matching US trading sessions.
Use TradingView `AMEX:RSPD` and `AMEX:RSPS` (US funds, not a same-ticker overseas
product). Read a complete pair from one download date and provider; do not
forward-fill missing dates or divide by zero. Preserve gaps in the chart.

# Interpretation

A rising ratio means discretionary has outperformed staples on a price basis;
a falling ratio means the opposite. Both funds can rise or fall together.
This describes relative cyclical-versus-defensive leadership, not a count of
participating stocks, and the raw ratio's level 1 is not a signal threshold.
The chart is displayed in the separate Ratios section; MMOH/MMOF remain in
Market Breadth because they measure stock participation. No predictive or contrarian trading rule is validated.

# Report and provenance

Display one chart and one or two interpretation sentences. The chart uses the
ratio-specific lookback (default 36 calendar months), with latest paired close and one-calendar-month ratio change
when available (last paired session on/before the anniversary). Exclude future
observations relative to the report date; label intraday observations.
Prices are provider-adjusted price closes and exclude dividend total returns;
different distributions can affect comparisons. Preserve raw OHLCV through
`situational_awareness.bar_store.save_bars` and retain input hashes, provider,
fetch time, download date, and latest common observation date in report JSON.
Stored runs use the latest complete paired batch. Fresh TradingView runs download
both ETFs along with other daily report symbols. Alpaca runs read a complete
stored Alpaca pair when available and otherwise show unavailable.

[^rspd-issuer]: Invesco RSPD factsheet, consulted 2026-11-04; equal-weight S&P 500 consumer discretionary sector exposure and quarterly rebalancing.
[^rsps-issuer]: Invesco RSPS factsheet, consulted 2026-11-04; equal-weight S&P 500 consumer staples sector exposure and quarterly rebalancing.

# Chart window configuration

`RATIO_LOOKBACK_MONTHS=36` in the project `.env` sets a three-year chart window.
Process environment overrides the file; `--ratio-lookback MONTHS` overrides both.
The setting is independent of the other report charts. Fresh TradingView runs
request enough history; stored runs flag incomplete histories without downloading.
