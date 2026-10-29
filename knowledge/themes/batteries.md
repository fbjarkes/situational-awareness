---
type: Reference
title: Batteries
description: US-listed companies in battery materials, cell technology, and storage systems.
tags: [themes, batteries, storage, electrification]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-29T23:14:13Z"
sources:
  - id: lit-holdings
    resource: https://www.globalxetfs.com/funds/lit/
    title: Global X LIT mandate and holdings dated 2026-10-28, consulted 2026-10-30
  - id: enovix-batteries
    resource: https://ir.enovix.com/news-releases/news-release-details/enovixs-taa-compliant-battery-manufacturing-strengthens-position
    title: Enovix issuer battery description and Nasdaq ENVX listing, 2026-09-01, consulted 2026-10-30
  - id: quantumscape-batteries
    resource: https://www.quantumscape.com/quantumscape-announces-plans-for-100-mwh-solid-state-battery-production-line-for-ai-data-centers-aerospace-and-defense/
    title: QuantumScape issuer solid-state battery development and Nasdaq QS listing, 2026-10-21, consulted 2026-10-30
  - id: eos-batteries
    resource: https://investors.eose.com/news-releases/news-release-details/eos-energy-enterprises-announces-preliminary-third-quarter-2026
    title: Eos issuer zinc storage systems and Nasdaq EOSE listing, 2026-10-19, consulted 2026-10-30
  - id: fluence-batteries
    resource: https://ir.fluenceenergy.com/news-releases/news-release-details/fluence-secures-long-term-battery-supply-through-multiyear
    title: Fluence issuer battery-system integration and Nasdaq FLNC listing, 2026-09-24, consulted 2026-10-30
  - id: enersys-batteries
    resource: https://www.sec.gov/Archives/edgar/data/1289308/000128930826000009/exhibit991-closureoftjmxma.htm
    title: EnerSys issuer stored-energy and battery manufacturing description, NYSE ENS, 2026-03-25, consulted 2026-10-30

theme:
  id: batteries
  classification: structural_theme
  tracking_status: proposed
  memberships: /themes/theme-memberships.md
  subthemes:
    - id: batteries-materials
      title: Battery materials
    - id: batteries-cells
      title: Cells and battery technologies
    - id: batteries-systems
      title: Battery systems and integration
market_report:
  section: themes
  implementation_status: universe_recorded
  evidence_status: exploratory
  enabled: false
---
# Scope and boundaries

Battery materials, electrochemical cells, and battery-based storage systems
for vehicles, stationary storage, industrial equipment, and electronics.
Restrict membership to US exchange listings, including eligible foreign issuers
and ADRs; exclude foreign-only and OTC listings. This project theme does not
require exclusively lithium-ion technology.

[Clean energy](/themes/renewable-energy.md) concerns renewable generation and
its supply chain; batteries can support renewable systems but also serve other
applications. Battery membership alone is not a clean-energy or emissions claim.
The theme also overlaps [Electrification and grid](/themes/electrification-grid.md)
and [Future mobility](/themes/future-mobility.md). Preserve explicit relationships
and deduplicate securities within each parent theme.

# Initial universe

The authoritative [shared table](/themes/theme-memberships.md) records:

| US ticker | Company | Inclusion basis | Role |
|---|---|---|---|
| ALB | Albemarle | Battery-materials value-chain exposure; LIT holding. [^lit-holdings] | Core |
| ENVX | Enovix | Advanced lithium-ion batteries. [^enovix-batteries] | Core |
| QS | QuantumScape | Solid-state battery development. [^quantumscape-batteries] | Core |
| EOSE | Eos Energy Enterprises | Zinc-based storage systems. [^eos-batteries] | Core |
| FLNC | Fluence Energy | Battery storage-system integration. [^fluence-batteries] | Core |
| ENS | EnerSys | Industrial stored-energy and battery systems. [^enersys-batteries] | Core |
| TSLA | Tesla | Optional broader battery ecosystem exposure; LIT holding. [^lit-holdings] | Extended |

Core/extended and exposure labels are provisional project judgments. A system
integrator need not manufacture its own cells. Separate materials producers,
cell developers, mature manufacturers, and integrators when comparing peers;
commercial maturity and chemistry differ. QS is recorded as Nasdaq-listed,
consistent with its October 2026 issuer release.[^quantumscape-batteries]
Record current provider resolution and corporate actions before execution.
Review dates do not establish historical membership.

# Proxy and research

LIT is a proposed lithium-value-chain comparison proxy; its global holdings and
lithium focus differ from this US-only, multi-chemistry selection.[^lit-holdings]
It is not a stock peer-group member. Issuer plans do not establish commercial
scale, future demand, technical superiority, or investment returns.
Use [shared methodology](/themes/methodology.md) and the authoritative
[RS research checklist](/themes/themes.md#research-todos). No new report signal
or trading rule is enabled.

[^lit-holdings]: Global X LIT mandate and holdings dated 2026-10-28; consulted 2026-10-30.
[^enovix-batteries]: Enovix issuer battery description and Nasdaq ENVX listing, 2026-09-01; consulted 2026-10-30.
[^quantumscape-batteries]: QuantumScape issuer solid-state battery development and Nasdaq QS listing, 2026-10-21; consulted 2026-10-30.
[^eos-batteries]: Eos issuer zinc storage systems and Nasdaq EOSE listing, 2026-10-19; consulted 2026-10-30.
[^fluence-batteries]: Fluence issuer battery-system integration and Nasdaq FLNC listing, 2026-09-24; consulted 2026-10-30.
[^enersys-batteries]: EnerSys issuer stored-energy and battery manufacturing description, NYSE ENS, 2026-03-25; consulted 2026-10-30.
