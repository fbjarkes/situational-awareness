---
type: Metric
title: SPY
description: US-listed S&P 500 ETF used as the project's broad US equity benchmark; holdings snapshot dated 2026-10-22.
resource: https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy
tags: [SPY, S&P 500, index, benchmark, equities]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-28"
sources:
  - id: ssga-daily-holdings
    resource: https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx
    title: State Street SPY daily holdings file
  - id: holdings-snapshot
    resource: /index/spy-holdings.md
    title: SPY holdings as of 2026-10-22
  - id: data-providers
    resource: /references/data-providers.md
    title: Market data providers and symbol availability
  - id: crossing-study
    resource: /references/breadth-crossing-study.md
    title: Exploratory breadth downward-crossing event study
  - id: user-ideas
    resource: TODO.md (local, untracked), consulted 2026-10-26
    title: User's daily-report ideas for SPY
market_report:
  symbol: AMEX:SPY
  section: sp500
  instrument_scope: US-listed ETF
  tracks: S&P 500
  currency: USD
  definition_status: partially_confirmed
  evidence_status: exploratory
  implementation_status: metrics_available
  report_metrics: [distance_from_sma200_pct, distance_from_sma50_pct, cons_days_above_sma50, cons_days_below_sma50, cons_down_days]
  enabled: false
  holdings_snapshot: /index/spy-holdings.md
  data_providers:
    tradingview:
      status: available
      symbol: AMEX:SPY
    alpaca:
      status: available
      symbol: SPY
      checked_at: "2026-10-26"
---
# Definition

SPY is the US-listed State Street SPDR S&P 500 ETF Trust; the issuer's
holdings file names the fund this way under ticker SPY.[^ssga-daily-holdings]
It is an exchange-traded fund holding S&P 500 securities, not the S&P 500
index itself. Fund prices include fees and tracking differences, and price
returns exclude dividends unless a total-return series is used.

# Symbols and data

TradingView resolves SPY as `AMEX:SPY`; the breadth study used that series
with split-adjusted, dividend-unadjusted daily prices.[^crossing-study]
Alpaca returned SPY daily bars on 2026-10-26 under the plain ticker `SPY`.[^data-providers]
Do not mix the two providers in one price history.

# Constituents

The [SPY holdings snapshot](/index/spy-holdings.md) lists 503 listed securities
as of 2026-10-22, retrieved 2026-10-26, plus cash and one non-standard
row.[^holdings-snapshot] Several issuers have more than one share class, so
there are fewer than 503 companies. Holdings change; treat the list as dated.

# Use in this project

- Benchmark for the proposed [sector relative strength](/sectors/relative-strength.md) calculation.
- Forward-return series in the [breadth crossing study](/references/breadth-crossing-study.md).
- S&P 500 report section: the SPY metrics below; sector relative strength is planned.

# Report metrics

The report's SPY card shows descriptive readings for the latest session,
computed by `price_stats.py` from stored daily closes:

- **Distance from 200-day / 50-day SMA:** `100 * (close / SMA - 1)`, in percent.
- **Consecutive days above or below the 50-day SMA:** sessions ending at the
  latest close with the close strictly above (or below) the SMA ending that
  session. A close equal to the SMA ends the streak. The card shows whichever
  side is active.
- **Consecutive down days:** sessions ending at the latest close with a close
  strictly below the previous close. An unchanged close ends the streak.

SMAs are simple and include the current close. A streak that reaches the
start of the downloaded history is shown with "≥", since it may be longer.
A latest bar fetched before 16:00 ET is intraday and labelled as such.
No thresholds are applied: these readings are not signals until the
studies below are recorded.

# Research TODOs

- [ ] Study SPY forward returns when at least 50% of S&P 500 constituents make a new 20-day high.
  - Proposed definition: a constituent's close strictly exceeds its preceding 20 trading-session closes; confirm closing highs versus intraday highs before running the study.
  - Trigger: qualifying constituents represent at least 50% of the point-in-time constituent universe; disclose missing histories and coverage rather than shrinking the denominator silently.
  - Horizons: 10, 20, 30, 50, 100, and 200 trading sessions after the signal-session close.
  - Baseline: unconditional SPY returns over the same sample and horizons, with a consistent adjustment and dividend policy.
  - Report: sample sizes, mean, median, positive frequency, and worst interim drawdown; disclose incomplete forward horizons.
  - Overlap: report all qualifying sessions and separately first crossings from below 50%, including a non-overlapping event sample.
  - Biases: prefer point-in-time membership, account for multiple share classes and delistings, and document survivorship bias if current holdings are used historically; disclose close-based execution assumptions and costs.
- [ ] Study SPY forward returns by distance from the 200-day SMA.
  - Buckets: below -10%, -10% to -5%, -5% to 0%, 0% to +5%, +5% to +10%, above +10%.
  - Horizons: 10, 20, and 50 trading sessions from the signal-session close.
  - Baseline: unconditional SPY returns over the same sample and horizons.
  - Report per bucket: N, mean, median, positive frequency, and worst interim drawdown.
  - Overlap: daily observations overlap heavily; also report a non-overlapping subsample.
  - Biases: single provider, split-adjusted price returns without dividends, regime clustering.
- [ ] Study SPY forward returns by consecutive days above the 50-day SMA.
  - Streak buckets: 1-5, 6-20, 21-50, and more than 50 sessions; also the first close below after 20+ sessions above.
  - Horizons: 10, 20, and 50 trading sessions from the signal-session close.
  - Baseline: unconditional SPY returns over the same sample and horizons.
  - Report per bucket: N, mean, median, positive frequency, and worst interim drawdown.
  - Overlap: consecutive days in one streak are not independent; count distinct streaks.
  - Biases: same as the 200-day study; streak length depends on history start.
- [ ] Study SPY forward returns after consecutive down days.
  - Thresholds: exactly 2, 3, 4, and 5 or more consecutive down closes.
  - Horizons: 1, 2, 3, 5, and 10 trading sessions from the signal-session close.
  - Baseline: unconditional SPY returns over the same sample and horizons.
  - Report: N, mean, median, positive frequency, worst interim drawdown, and results by decade.
  - Overlap: count a streak once at each threshold it reaches; note that longer streaks are subsets.
  - Biases: close-to-close entry is not executable at the signal close; no costs; split-adjusted price only.

# Proposed analysis

The user's remaining idea, recorded as a proposal, not a tested finding:[^user-ideas]
mean-reversion context such as "yesterday was a 50-day low, today is a
5-day high", with forward returns over the next one to five sessions.

# Open questions

The issuer's fund page was not consulted for this draft. Fund objective,
inception date, listing exchange, legal structure, expense ratio, and
dividend treatment remain to be recorded from the issuer.

# TODOs

- [ ] Record SPY fund facts from the issuer's overview page and factsheet.
  - Objective, inception, exchange, structure, expense ratio, dividend frequency, with as-of dates.

[^ssga-daily-holdings]: State Street daily holdings file, downloaded 2026-10-26 09:19:45 UTC; holdings as of 2026-10-22.
[^holdings-snapshot]: Counts and treatment of non-standard rows are documented in the holdings concept.
[^data-providers]: Alpaca get_stock_bars through the connected MCP tool, 2026-10-26.
[^crossing-study]: Breadth study inputs and adjustment statement.
[^user-ideas]: Ideas listed under "Index to include" in the user's local TODO.md.
