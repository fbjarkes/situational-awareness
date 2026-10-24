---
type: Market Insight
title: Extreme low breadth
description: Unvalidated below-20 breadth hypothesis.
tags: [breadth, MMOH, MMOF, research]
status: draft
generated:
  by: codex/market-report-poc
sources:
  - id: project-hypothesis
    resource: /references/project-decisions.md
    title: Project discussion and proposed hypotheses
market_report:
  section: breadth
  evidence_status: hypothesis
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
attractive buying opportunities.[^project-hypothesis] Neither rarity nor
subsequent performance has been established.

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

No empirical study or verification event is recorded. Low readings alone do
not establish timing, expected return, or a trade recommendation.
Keep this rule disabled until evidence and report wording have been reviewed.

[^project-hypothesis]: User-proposed observation recorded in the project decisions reference.
