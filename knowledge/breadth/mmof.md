---
type: Metric
title: MMOF
description: Percentage of stocks above their 150-day average, as labeled by TradingView.
resource: https://www.tradingview.com/symbols/INDEX-MMOF/
tags: [breadth, MMOF]
status: draft
generated:
  by: codex/market-report-poc
market_report:
  symbol: INDEX:MMOF
  section: breadth
  definition_status: partially_confirmed
  average_horizon_days: 150
  units: percent
  expected_range: [0, 100]
  universe_status: undocumented_in_consulted_source
sources:
  - id: tradingview-symbol
    resource: https://www.tradingview.com/symbols/INDEX-MMOF/
    title: TradingView MMOF symbol overview
---
# Usage

The PoC fetches daily closing observations for `INDEX:MMOF` and displays them
alongside [MMOH](/breadth/mmoh.md).

# Definition

TradingView labels MMOF as the percentage of stocks above their
150-day average.[^tradingview-symbol] The horizon and percentage unit are
confirmed by that label; the complete methodology remains unresolved.

# Interpretation

As a percentage, a value of 20 represents 20% of the included stocks above
the specified average. Changes are measured in percentage points.
Higher readings indicate broader participation above that average.
A reading below 50 means fewer than half qualify; 50 is a mathematical
midpoint, not a validated trading threshold.

# Methodology gaps

The consulted overview does not establish the stock universe, average type,
eligibility rules, treatment of equality or missing prices, constituent
changes, or publication schedule. Do not assume an S&P 500 universe or a
simple moving average without further documentation.

# Related insights

[Extreme low breadth](/breadth/extreme-low-breadth.md) is a research hypothesis,
not an established interpretation of this metric.

Rarity and subsequent returns require historical testing.

[^tradingview-symbol]: TradingView symbol overview, consulted 2026-10-25; community ideas are not provider methodology.
