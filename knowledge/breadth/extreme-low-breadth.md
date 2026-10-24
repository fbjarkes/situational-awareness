---
type: Market Insight
title: Extreme low breadth
description: Below-20 breadth hypothesis with preliminary individual-indicator crossing evidence.
tags: [breadth, MMOH, MMOF, research]
status: draft
generated:
  by: codex/market-report-poc
sources:
  - id: crossing-study
    resource: /references/breadth-crossing-study.md
    title: Exploratory breadth downward-crossing event study
  - id: project-hypothesis
    resource: /references/project-decisions.md
    title: Project discussion and proposed hypotheses
market_report:
  section: breadth
  evidence_status: exploratory
  enabled: false
  priority: high
  condition:
    indicators: [INDEX:MMOH, INDEX:MMOF]
    field: close
    match: all
    operator: below
    threshold: 20
    require_same_observation_date: true
  interpretation: Both breadth indicators are below 20; this proposed extreme-low signal has not been historically validated.
---
# Hypothesis

The user proposed that MMOH/MMOF values below 20 are rare and may identify
attractive buying opportunities.[^project-hypothesis] Preliminary individual
crossing results are recorded below; rarity and a robust trading edge remain unestablished.

# Preliminary evidence

An exploratory study covers 2002-01-02 through 2026-10-23 and tests each index
separately crossing from at-or-above to below 30, 25, and 20.[^crossing-study]
For below-20 crossings, mean 50-session SPY price returns were 4.68% for MMOH
(32 events) and 5.19% for MMOF (40 events), versus 1.80% unconditionally.
At 200 sessions, means were 10.21% and 8.73%, versus 7.74% unconditionally.

These tests do not validate this file's both-below condition. See the
[full study](/references/breadth-crossing-study.md) for all requested horizons,
medians, win rates, methodology, snapshot hashes, and limitations.

# Scope

This candidate condition requires both [MMOH](/breadth/mmoh.md) and
[MMOF](/breadth/mmof.md) to be strictly below 20 on the same observation date.
The original observation did not settle whether either or both must qualify;
this is a proposed research variant, not a confirmed user requirement.

# Validation plan

1. Verify indicator definitions and obtain sufficient historical coverage.
2. Test each indicator separately, either indicator, and both together.
3. Define episodes so consecutive low readings do not inflate independent sample counts.
4. Measure frequency, forward benchmark returns, and interim drawdowns at declared horizons.
5. Compare with unconditional outcomes, account for overlapping samples, and test across market regimes.

# Limitations

The study is descriptive: events overlap and cluster, dividends and execution
costs are excluded, and signal-close returns assume no execution delay.
No independent verification or statistical significance test is recorded.
Low readings alone do not establish a trade recommendation.
Keep this rule disabled until evidence and report wording have been reviewed.

[^project-hypothesis]: User-proposed observation recorded in the project decisions reference.

[^crossing-study]: Reproducible exploratory SPY price-return study using downloaded TradingView daily observations.
