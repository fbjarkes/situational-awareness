---
type: Reference
title: Theme membership and relative-strength methodology
description: Proposed shared rules for overlapping stock themes and reproducible peer comparisons.
tags: [themes, methodology, relative-strength]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-29T22:33:06Z"
sources:
  - id: project-design
    resource: /themes/themes.md
    title: Theme registry and research design
---
# Status

These are project design conventions, not validated investment findings.
The RS utility and related research remain unimplemented.[^project-design]

# Membership

Theme stock universes are restricted to US exchange-listed securities, per the
user's 2026-10-29 instruction. US-listed foreign companies and exchange-listed
ADRs are eligible; foreign-only listings and OTC securities are excluded.
Use one eligible US listing per company. ETF proxies may hold international
stocks, but their holdings must be filtered before constructing a theme universe.
The legacy full GDX holdings and existing derived breadth remain dated source
artifacts; a US-only theme calculation must explicitly select eligible US rows
and disclose its different denominator.

Use stable theme and subtheme IDs. Store one relationship per security and
subtheme in [Theme memberships](/themes/theme-memberships.md). A security may
belong to several themes. Deduplicate securities within a parent-theme universe;
do not count each subtheme relationship as an additional stock. Resolve multiple
listings and share classes explicitly before computing company-level measures.

Each relationship needs a source, rationale, exposure classification (core,
diversified, indirect), review date, and membership validity dates when known.
Unknown validity dates stay unknown: a review date does not establish when a
company first acquired its exposure. Preserve past membership and source dates.
Keep document status separate from tracking status.

# Benchmark and weighting

For stock-versus-group RS, exclude the tested security from its own peer group.
Reject empty peer groups. Proposed benchmark: compound equal-weight daily peer
returns, rebalanced each common session across an explicitly selected fixed
universe for that calculation. Changes in membership require documented effective
dates. Do not average nominal stock prices.

Compute subtheme and parent-theme comparisons separately. Overlapping groups
are correlated; do not treat their research results as independent replications.

# Relative strength

Normalize stock price and peer index to 1 at a common initial session:
`RS_level = 100 * normalized_stock_price / normalized_peer_index`.

Initial rolling periods are 5 and 10 trading sessions:
`RS_n = 100 * ((stock_t / stock_t_minus_n) / (peer_t / peer_t_minus_n) - 1)`.
Units are percent relative return, not percentage-point return difference.
An n-session return requires n+1 aligned observations. Keep `period` separate
from `high_lookback`: a new RS-level high strictly exceeds the preceding
high-lookback observations; ties do not qualify. Require complete warmup.

# Inputs and missing data

Read bars through `bar_store.load_bars`, pinning one download batch and provider.
Use a consistent price adjustment and dividend policy and record input hashes.
Align by exchange-local session dates; international comparisons must disclose
asynchronous closes and possible look-ahead effects.

Initial strict policy: require all selected peers and the tested stock on each
required common session. Missing required observations make the result unavailable;
do not silently forward-fill or drop peers. Report selected/eligible counts.
Any relaxed minimum-coverage policy must be explicit and separately identified.

# Research reproducibility

Record membership snapshots, prices, fetch times, calculation settings, coverage,
baseline, sample sizes, event overlap, and interim drawdowns. Current holdings
applied historically introduce survivorship bias. State execution assumptions,
costs, missing/delisted-security treatment, and multiple-testing limitations.

The authoritative research checklist remains in
[Themes](/themes/themes.md#research-todos).

[^project-design]: Project conventions and user-requested theme RS research plan; not an executed study.
