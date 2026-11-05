---
type: Reference
title: GDX breadth calculation
description: US-listed GDX constituent breadth, calculated from daily bars and refreshed only in weekly report runs.
status: draft
tags: [breadth, methodology, custom, GDX]
generated:
  by: codex/market-report-poc
  at: "2026-11-04T22:50:06Z"
market_report:
  symbol: CUSTOM:GDX-SMA50
  section: themes
  cadence: weekly
  universe_scope: US-listed GDX constituents
  implementation_status: report_available
  evidence_status: exploratory
  enabled: false
---
# Calculation

The reusable `calculate_breadth` helper in package module `situational_awareness.breadth` accepts
symbol identifiers, daily closing histories, an SMA window, and optional
inclusive start/end dates. The CLI is `custom-breadth`.

For each security with a current price and sufficient history, compare its
close with the simple average of its latest N observations, including the
current close. Count above, below, and equal separately. Above percentage is
100 times the above count divided by all eligible securities, including equals.
An equality tolerance of 1e-12 relative to the average handles floating-point noise.

# Availability and dates

Calculate over all supplied history before applying the output start date,
so warmup can use observations before the requested period. The first N-1
observations are ineligible. Do not forward-fill prices on missing days.
An explicit null close resets the security's warmup. Missing session dates
do not reset it; the SMA counts available observations, not calendar days.
For TradingView snapshots, supported exchange timezones determine session
dates before combining histories; this prevents Australian bars from shifting
to the previous UTC day. Explicit per-symbol `session_timezones` can override
these defaults. Other snapshots default to UTC date labels.
Output dates are the union of supplied session dates. Timestamps use UTC
midnight as a date label, not an executable trade timestamp.

The denominator varies with availability. Record coverage and missing counts
daily. `--min-coverage` can suppress percentages below a specified fraction
of the fixed universe; raw counts remain available. Default 0 permits partial
coverage when at least one security qualifies. No eligible securities means
a null percentage. Entirely absent histories appear in universe metadata.

# Snapshot contract

The result has `schema_version`, `provider`, `fetched_at`, and a `series`
mapping, matching the outer shape of existing report snapshots. Each bar's
`c` is percentage above; `o`, `h`, `l`, and `v` are null because this is a
close-only statistic. Additional fields store counts, coverage, and below/equal
percentages. It is not an intraday OHLC index or a reproduction of MMOH/MMOF's
undocumented provider methodology.

# GDX universe

The [GDX holdings snapshot](/sectors/gdx.md) supplies 59 security ticker labels;
cash and Other/Cash are excluded. Use a complete explicit symbol map for
provider exchange-qualified identifiers. Issuer labels are not assumed to be
valid TradingView symbols, and missing mappings fail rather than guessing.

Keep one listing per economic constituent. The helper equal-weights stocks,
not fund allocation weights. Apply today's constituent list to historical
prices only with the fixed-universe label: it introduces survivorship and
membership bias and is not historical GDX portfolio breadth. Inception dates,
holidays, mixed exchanges, currencies, and data gaps can change coverage.
The 59 securities should not be conflated with the issuer's reported 65 holdings.

# Report scope and cadence

The report uses only the US-listed subset of the fixed GDX holdings, selected
through the same symbol map and US-exchange filter as the gold-miners theme.
Foreign listings are excluded from the denominator, not counted as unavailable.
This subset differs from historical full-international GDX breadth; do not join
or compare the two series as if their universes were identical. The full issuer
holdings table remains a reference, not a foreign-price download instruction.

GDX breadth is a **weekly study** calculated from daily closing prices and a
50-session SMA; weekly refresh cadence does not turn the SMA into 50 weeks.
Both daily and weekly reports show the same saved study, a Weekly badge and the
last observation date. Daily reports do not recalculate or overwrite the snapshot.
Only `market-report --weekly` updates it. The default local file is
`data/gdx-breadth-us-sma50.json`; `--gdx-breadth PATH` can select another US-only
snapshot. A legacy snapshot containing foreign symbols is not displayed.

A fresh TradingView weekly run shares the US stock bars already needed by theme
returns; it does not fetch a second international GDX basket. A snapshot-provider
weekly run recalculates from one complete stored provider/download batch, without
network calls. Missing inputs retain the previous snapshot with an availability
note. Alpaca also requires a complete stored US subset for weekly calculation.

Weekly and daily reports have separate output filenames. Record the snapshot
update time separately from its last market observation, and preserve input bar
hashes, provider, fetch time, download date, fixed membership date and subset scope.
Minimum eligible coverage is 80% of the selected US universe; percentages are
suppressed below that cutoff. No predictive threshold has been validated.

# Limits

The planned event study is tracked in [GDX research TODOs](/sectors/gdx.md#research-todos).
The generic custom-breadth helper can still accept explicit research universes;
the report itself uses US listings only.
