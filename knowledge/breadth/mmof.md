---
type: Metric
title: MMOF
description: Percentage of stocks above their 150-day average, as labeled by TradingView.
resource: https://www.tradingview.com/symbols/INDEX-MMOF/
tags: [breadth, MMOF]
status: draft
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-10-26T12:00:00Z"
market_report:
  symbol: INDEX:MMOF
  section: breadth
  definition_status: partially_confirmed
  average_horizon_days: 150
  units: percent
  expected_range: [0, 100]
  universe_status: undocumented_in_consulted_source
  evidence_status: exploratory
  studied_crossing_thresholds: [30, 25, 20]
  insight_source: /references/breadth-crossing-study.md
  data_providers:
    tradingview:
      status: available
      symbol: INDEX:MMOF
    alpaca:
      status: unavailable
      reason: TradingView-calculated breadth index; Alpaca market data covers US-listed stocks and ETFs only.
      checked_at: "2026-10-26"
      details: /references/data-providers.md
sources:
  - id: crossing-study
    resource: /references/breadth-crossing-study.md
    title: Exploratory breadth downward-crossing event study
  - id: data-providers
    resource: /references/data-providers.md
    title: Market data providers and symbol availability
  - id: tradingview-symbol
    resource: https://www.tradingview.com/symbols/INDEX-MMOF/
    title: TradingView MMOF symbol overview
---
# Usage

The PoC fetches daily closing observations for `INDEX:MMOF` and displays them
alongside [MMOH](/breadth/mmoh.md).

# Provider availability

`INDEX:MMOF` is available only from TradingView. Alpaca has no equivalent symbol;
an Alpaca asset lookup for `MMOF` returned not found on
2026-10-26.[^data-providers] Reports run with `--provider alpaca` read this series
from a stored TradingView batch and label the substitution, or show the
section as unavailable when no such batch exists.

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

# Historical crossing insights

The [breadth study](/references/breadth-crossing-study.md) tested this index
individually over 2002-01-02 through 2026-10-23. A signal occurs when the
previous available close is at or above a threshold and the current close
is strictly below it; returns run from that session's SPY close.[^crossing-study]

Below-20 crossings had 40 mature events. Mean SPY price return at 50 trading
sessions was 5.19% with 78% positive outcomes, versus a 1.80% unconditional
mean. At 200 sessions, the mean was 8.73%, median 10.43%, and positive-return
frequency 75%, versus a 7.74% unconditional mean.[^crossing-study]

Within this sample, below-20 crossings had higher mean returns than below-25
or below-30 crossings at 30, 50, 100, and 200 sessions. Below-30 crossings
underperformed the unconditional mean at every tested horizon. This suggests
the threshold and holding horizon matter; it does not establish a trading edge.

# Evidence limitations

These results apply to downward crossings, not every day below a threshold,
and do not test both indices together. Repeated crossings cluster and return
windows overlap; no significance or out-of-sample test was performed.
Prices exclude dividends and returns assume entry at the signal-session close.
The worst below-20 200-session return was approximately -32.94%; this is a
terminal return, not maximum interim drawdown.[^crossing-study]

# Related insights

[Extreme low breadth](/breadth/extreme-low-breadth.md) is a research hypothesis,
not an established interpretation of this metric.

The [extreme-low hypothesis](/breadth/extreme-low-breadth.md) remains disabled.
Rarity, execution feasibility, and independent validation remain open questions.

[^tradingview-symbol]: TradingView symbol overview, consulted 2026-10-25; community ideas are not provider methodology.

[^crossing-study]: Exploratory TradingView-based SPY price-return event study; full tables, assumptions, and snapshot provenance are recorded in the linked research result. Worst terminal returns are in the local summary CSV.

[^data-providers]: Provider coverage reference; records the Alpaca lookup and the report's substitution policy.
