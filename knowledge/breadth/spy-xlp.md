---
type: Metric
title: S&P 500 versus consumer staples price ratio
description: SPY divided by XLP as a descriptive relative-leadership study.
tags: [breadth, relative-strength, SPY, XLP]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-11-04T22:26:27Z"
sources:
  - id: xlp-issuer
    resource: https://www.ssga.com/us/en/intermediary/etfs/state-street-consumer-staples-select-sector-spdr-etf-xlp
    title: Official XLP fund overview
market_report:
  section: ratios
  implementation_status: metrics_available
  evidence_status: descriptive
  enabled: false
---
# Definition

XLP tracks the Consumer Staples Select Sector Index.[^xlp-issuer]
[SPY](/index/spy.md) represents the S&P 500. Calculate `SPY close / XLP close`
for matching US sessions, using TradingView `AMEX:SPY` and `AMEX:XLP`.

# Interpretation

A rising ratio means the S&P 500 outperforms consumer staples on a price basis;
a falling ratio means the reverse. Both funds may still rise or fall together.
Sector composition and weighting differ between the two funds. This is descriptive context, not a validated trading signal.

# Report and provenance

Use the shared `build_price_ratio` function and `ratio_card` renderer, exactly as
for [RSPD/RSPS](/breadth/rspd-rsps.md). Display one chart and one or two sentences,
with the latest paired reading and one-calendar-month change. Use one complete
provider/download batch, preserve missing-session gaps, exclude future observations,
and label provisional intraday values. The ratio is unrebased, excludes dividends,
and level 1 has no special signal meaning. Provider price adjustments can affect
comparisons; this is not dividend-adjusted total-return relative strength.

Archive raw prices through `bar_store.save_bars`; retain download date, fetch time,
provider, observation dates and input hashes in report JSON. Fresh TradingView runs
fetch both legs, sharing the SPY download across studies. Stored runs load the
latest complete pair; Alpaca requires an archived Alpaca pair or shows unavailable.

[^xlp-issuer]: Official issuer fund overview, consulted 2026-11-04.

# Chart window configuration

`RATIO_LOOKBACK_MONTHS=36` in the project `.env` sets a three-year chart window.
Process environment overrides the file; `--ratio-lookback MONTHS` overrides both.
The setting is independent of the other report charts. Fresh TradingView runs
request enough history; stored runs flag incomplete histories without downloading.
