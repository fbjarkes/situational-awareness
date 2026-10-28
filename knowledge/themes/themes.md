---
type: Reference
title: Themes
description: Registry of active project themes and proposed within-theme relative-strength research.
tags: [themes, constituents, relative-strength]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-28T21:55:00Z"
sources:
  - id: gdx-concept
    resource: /sectors/gdx.md
    title: GDX definition, dated holdings, and report context
  - id: user-proposal
    resource: User request in this project chat, 2026-10-28
    title: Theme registry and within-theme RS-high research proposal
market_report:
  section: themes
  implementation_status: registry_only
  evidence_status: exploratory
  enabled: false
---
# Active themes

Active means covered by this project, not a claim about current market leadership.
Gold miners is the only theme currently represented in the report.[^gdx-concept]

| Theme ID | Theme | Proxy | Knowledge | Ticker manifest |
|---|---|---|---|---|
| gold-miners | Gold miners | AMEX:GDX | [GDX](/sectors/gdx.md) | [Gold miners universe](/themes/theme-tickers.md#gold-miners) |

Add future themes here with a stable ID, scope, and an entry in the shared
[ticker manifest](/themes/theme-tickers.md). Theme membership can overlap;
retain dated membership and provider symbol mappings separately from raw bars.

# Proposed relative strength

The user proposes tracking a stock making a new relative-strength high within
its own theme.[^user-proposal] The following is a research design, not a finding
or an implemented report signal.

Proposed RS series: `100 * stock_normalized_price / peer_index`, where both
series start at 1 on the same session. The peer index compounds the equal-weight
daily returns of the selected theme members, excluding the stock being tested.
A stock's high nominal share price must not give it more benchmark weight.
Rising RS indicates outperformance of the selected peers under this definition.

Use matched sessions and a single provider and adjustment policy. Do not silently
forward-fill missing prices or change the peer universe when data is missing.
Specify minimum coverage, rebalancing, exchange-calendar alignment, and treatment
of delistings before computing results. Current fixed holdings create survivorship
bias when applied to earlier history.

# Research TODOs

- [ ] Study stocks making new relative-strength highs against their own theme and measure subsequent returns.
  - Proposed event: RS closes strictly above its preceding 20, 50, or 252 trading-session values; evaluate lookbacks separately and require full warmup.
  - Benchmark: equal-weight theme peers excluding the tested stock, using dated membership and a documented rebalancing policy.
  - Horizons: 10, 20, 30, 50, 100, and 200 trading sessions after the event close; measure stock returns and excess returns versus the peer benchmark.
  - Baseline: unconditional returns for the same eligible stocks, dates, and horizons; report theme and market-regime breakdowns.
  - Report sample sizes, mean, median, positive frequency, worst interim drawdowns, incomplete horizons, and coverage.
  - Separate all qualifying days from first breakout events and non-overlapping samples; account for clustering across stocks in the same theme.
  - Record inputs, download dates, hashes, adjustment and dividend policy, membership/survivorship bias, calendar alignment, execution assumptions, costs, and multiple-testing limitations.

# TODOs

- [ ] Implement a reusable stock-versus-group RS utility after documenting the benchmark and missing-data contract.
  - Proposed interface: `relative_strength(symbol, group_symbols, period, ...)`, reading bars through `bar_store.load_bars` from one explicit batch and provider.
  - Return a dated RS series, new-high flags, eligible peer counts, and input provenance; exclude the tested stock and reject an empty peer group.
  - Verify scale invariance, self-exclusion, aligned dates, missing-history handling, and strict new-high behavior before enabling report output.

[^gdx-concept]: Existing GDX knowledge concept and report context; consulted 2026-10-28.
[^user-proposal]: User-requested research idea, recorded 2026-10-28; no study conducted.
