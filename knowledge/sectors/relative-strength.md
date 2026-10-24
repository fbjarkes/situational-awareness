---
type: Metric
title: Sector relative strength
description: Proposed sector ETF excess-return calculation over one, three, and six months.
tags: [sectors, SPDR, relative-strength]
status: draft
generated:
  by: codex/market-report-poc
sources:
  - id: project-design
    resource: /references/project-decisions.md
    title: Proposed sector analysis design
market_report:
  section: sectors
  implementation_status: planned
  benchmark: SPY
  horizons_months: [1, 3, 6]
  columns: [Sector, RS-1, RS-3, RS-6]
  units: percentage_points
  method: return_difference
  adjustment_policy: pending
---
# Proposed definition

For this project, RS is proposed as sector ETF return minus SPY return over
one, three, or six calendar months.[^project-design] This is a local metric
definition, not a claim that all providers define relative strength this way.

For horizon n:

```text
RS-n = 100 * ((sector_end / sector_start - 1)
            - (benchmark_end / benchmark_start - 1))
```

Positive values indicate sector outperformance under this definition.

# Date alignment

Use a common end session for the benchmark and all sectors. Subtract n
calendar months from that session date, clamping month-end dates, then use
the last common available session on or before the target date. Missing or
insufficient history produces an unavailable cell rather than a zero.

# Data decisions pending

Confirm the SPDR sector instrument universe, benchmark, provider, maximum
acceptable session lag, and adjustment policy before implementation.
All inputs must use the same policy. Dividend-adjusted total returns are
preferred for this proposed comparison; split-only prices must be labeled
as price returns rather than total returns.

# Presentation

One sector table with RS-1, RS-3, and RS-6 in percentage points, followed by
one or two sentences identifying leadership and lagging sectors.
Calculations and table generation are not yet implemented.

[^project-design]: The user requested RS-1/RS-3/RS-6; the benchmark and formula are the proposed implementation design.
