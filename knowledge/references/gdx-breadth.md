---
type: Reference
title: GDX breadth calculation
description: Equal-weight daily above/below SMA methodology for a supplied security universe.
status: draft
tags: [breadth, methodology, custom, GDX]
generated:
  by: codex/market-report-poc
  at: 2026-10-25T19:25:19Z
market_report:
  symbol: CUSTOM:GDX-SMA50
  section: gdx_breadth
  implementation_status: report_available
  evidence_status: exploratory
  enabled: false
---
# Calculation

The reusable `calculate_breadth` helper in repository file `breadth.py` accepts
symbol identifiers, daily closing histories, an SMA window, and optional
inclusive start/end dates. The CLI is `custom-breadth.py`.

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

# Limits

The planned event study is tracked in [GDX research TODOs](/sectors/gdx.md#research-todos).

The GDX report defaults to a 50-day SMA, the 2026-10-22 fixed universe, and
minimum coverage 0.8. It shows daily coverage and suppresses percentages below
that cutoff. Generate the local snapshot with:

```powershell
uv run custom-breadth.py --holdings-md knowledge/sectors/gdx.md --symbol-map data/gdx-symbol-map.json --ma 50 --min-coverage 0.8 --universe-as-of 2026-10-22 --name CUSTOM:GDX-SMA50 --download-date 2026-10-25 --output data/gdx-breadth-sma50.json
```

The daily report includes this snapshot automatically when present; use
`--gdx-breadth PATH` to select another. It does not refresh constituent data.

Raw histories are stored per symbol under `data/research/day/<download-date>/`,
using Stockholm download dates and Windows-safe percent-encoded filenames.
The helper defaults to the latest complete batch; `--download-date` pins it.
Live downloads save each symbol automatically to the same store. Derived
breadth JSON retains input file paths and hashes for reproducibility.

The live downloader pages all available daily history from the configured
TradingView MCP endpoint; standalone authentication is still required.
Inputs must have consistent price-adjustment treatment; splits can distort
an SMA if unadjusted. Provider notices and input hashes are retained.
For live downloads, today's bar can still be forming: use a completed-session
`--end` date when closing-only breadth is required. The helper has no exchange
calendar or historical constituent membership service. No predictive threshold
or trading rule has been validated for this custom series.
