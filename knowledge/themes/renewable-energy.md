---
type: Reference
title: Clean energy and renewables
description: Companies enabling renewable energy production and associated systems.
tags: [themes, renewables]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-29T23:14:13Z"
sources:
  - id: tan-holdings
    resource: https://www.invesco.com/us/en/financial-products/etfs/invesco-solar-etf.html
    title: Invesco TAN issuer holdings snapshot dated 2026-10-12, consulted 2026-10-30
  - id: provider-framework
    resource: https://www.msci.com/our-solutions/indexes/thematic-investing/themes-and-sub-themes
    title: Provider thematic classification framework
  - id: project-taxonomy
    resource: /themes/themes.md
    title: Project theme registry and proposed taxonomy
theme:
  id: renewables
  classification: structural_theme
  tracking_status: proposed
  memberships: /themes/theme-memberships.md
  subthemes:
    - id: renewables-solar
      title: Solar
    - id: renewables-wind
      title: Wind
    - id: renewables-hydrogen
      title: Hydrogen
    - id: renewables-energy-storage
      title: Energy storage
---
# Scope

Companies enabling renewable energy production and associated systems. This is a proposed project universe, not an industry classification
or a claim of current market leadership.

# Classification and subthemes

Provider frameworks support the broad thematic approach.[^provider-framework]
The names, boundaries, and subdivisions below are the project's first-draft
synthesis, not a provider's official membership rules.[^project-taxonomy]

- Solar
- Wind
- Hydrogen
- Energy storage

# Membership criteria

Require documented products, services, revenue, or investment exposure relevant
to the scope. Marketing references alone do not establish membership. Record
exposure as core, diversified, or indirect, supported by a source and rationale.
Membership can overlap other themes and subthemes.

# Clean Energy boundary

Clean Energy is the display name for this existing renewable-energy concept;
retain the `renewables` theme ID and file path to preserve existing links.
The initial universe focuses on renewable generation and its equipment supply
chain. [Nuclear energy](/themes/nuclear-energy.md) is separately tracked as
low-carbon generation. This project taxonomy is not a universal definition
of clean energy or a lifecycle-emissions certification.

[Batteries](/themes/batteries.md) is a distinct cross-cutting theme. Storage
shifts electricity across time; it is not itself a primary generation source,
and battery exposure alone does not establish renewable-energy exposure.
Companies can have explicit memberships in both themes where justified.

# Initial universe

The [shared membership table](/themes/theme-memberships.md) records seven core
candidates: FSLR (First Solar), NXT (Nextpower), ENPH (Enphase Energy), SEDG
(SolarEdge Technologies), RUN (Sunrun), ENLT (Enlight Renewable Energy), and
CWEN (Clearway Energy Class C). HASI (HA Sustainable Infrastructure Capital)
is an optional finance-related extension. All eight appear in the TAN issuer
holdings snapshot dated 2026-10-12.[^tan-holdings]

Only US exchange-listed securities are eligible, including foreign issuers.
Use CWEN as the chosen Clearway share class; do not also count CWEN.A as a
second company. This initial selection is solar-heavy and does not populate
all proposed wind or hydrogen subthemes. TAN is a solar comparison proxy,
not a benchmark for the entire clean-energy economy; it has global holdings
outside this US-only subset. Selection roles/exposure labels are provisional
project choices. Subthemes and current provider symbols require review before
execution; review dates do not establish historical membership. No new report
output or trading rule is enabled.

# Interpretation and research

Use [shared methodology](/themes/methodology.md) for weighting, calendars,
coverage, and RS. Compare a stock with its narrow peers and its parent theme
separately; this concept enables no trading rule.

The authoritative [within-theme RS research checklist](/themes/themes.md#research-todos)
is maintained once in the registry.

[^provider-framework]: Provider framework consulted during project taxonomy research on 2026-10-28; supports broad categories, not every proposed subdivision.
[^project-taxonomy]: User-approved first-draft organization, 2026-10-28; membership and predictive effects remain unvalidated.

[^tan-holdings]: Invesco TAN issuer holdings snapshot dated 2026-10-12; consulted 2026-10-30.
