---
type: Metric
title: S&P 500 versus small caps price ratio
description: SPY divided by IWM as a descriptive relative-leadership study.
tags: [breadth, relative-strength, SPY, IWM]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-11-04T22:20:22Z"
sources:
  - id: iwm-issuer
    resource: https://www.ishares.com/us/products/239710/ishares-russell-2000-etf
    title: Official IWM fund overview
market_report:
  section: ratios
  implementation_status: metrics_available
  evidence_status: descriptive
  enabled: false
---
# Definition

IWM provides exposure to US small-cap stocks through the Russell 2000 Index.[^iwm-issuer]
[SPY](/index/spy.md) represents the S&P 500. Calculate `SPY close / IWM close`
for matching US sessions, using TradingView `AMEX:SPY` and `AMEX:IWM`.

# Interpretation

A rising ratio means the S&P 500 outperforms Russell 2000 small caps on a price basis;
a falling ratio means the reverse. Both funds may still rise or fall together.
Rising SPY/IWM indicates large-cap leadership, not expanding small-cap participation. This is descriptive context, not a validated trading signal.

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

[^iwm-issuer]: Official issuer fund overview, consulted 2026-11-04.
