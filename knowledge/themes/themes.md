---
type: Reference
title: Themes
description: Registry of active and proposed project themes and within-theme relative-strength research.
tags: [themes, constituents, relative-strength]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-29T23:32:00Z"
sources:
  - id: gdx-concept
    resource: /sectors/gdx.md
    title: GDX definition, dated holdings, and report context
  - id: user-proposal
    resource: User request in this project chat, 2026-10-28
    title: Theme registry and within-theme RS-high research proposal
themes:
  - id: semiconductors
    title: Semiconductors
    concept: /themes/semiconductors.md
    classification: industry_basket
    tracking_status: proposed
  - id: crypto-blockchain
    title: Crypto and blockchain
    concept: /themes/crypto-blockchain.md
    classification: structural_theme
    tracking_status: proposed
  - id: batteries
    title: Batteries
    concept: /themes/batteries.md
    classification: structural_theme
    tracking_status: proposed
  - id: drones
    title: Drones
    concept: /themes/drones.md
    classification: structural_theme
    tracking_status: proposed
  - id: ai
    title: Artificial intelligence
    concept: /themes/artificial-intelligence.md
    classification: structural_theme
    tracking_status: proposed
  - id: robotics
    title: Robotics and automation
    concept: /themes/robotics-automation.md
    classification: structural_theme
    tracking_status: proposed
  - id: cybersecurity
    title: Cybersecurity
    concept: /themes/cybersecurity.md
    classification: structural_theme
    tracking_status: proposed
  - id: quantum
    title: Quantum computing
    concept: /themes/quantum-computing.md
    classification: structural_theme
    tracking_status: proposed
  - id: space
    title: Space and satellites
    concept: /themes/space-economy.md
    classification: structural_theme
    tracking_status: proposed
  - id: defense-tech
    title: Defense technology
    concept: /themes/defense-technology.md
    classification: structural_theme
    tracking_status: proposed
  - id: mobility
    title: Future mobility
    concept: /themes/future-mobility.md
    classification: structural_theme
    tracking_status: proposed
  - id: digital-finance
    title: Digital finance
    concept: /themes/digital-finance.md
    classification: structural_theme
    tracking_status: proposed
  - id: health-innovation
    title: Healthcare technology and innovation
    concept: /themes/healthcare-innovation.md
    classification: structural_theme
    tracking_status: proposed
  - id: longevity
    title: Longevity and metabolic health
    concept: /themes/longevity-metabolic-health.md
    classification: structural_theme
    tracking_status: proposed
  - id: electrification
    title: Electrification and grid modernization
    concept: /themes/electrification-grid.md
    classification: structural_theme
    tracking_status: proposed
  - id: nuclear
    title: Nuclear energy
    concept: /themes/nuclear-energy.md
    classification: structural_theme
    tracking_status: proposed
  - id: renewables
    title: Clean energy and renewables
    concept: /themes/renewable-energy.md
    classification: structural_theme
    tracking_status: proposed
  - id: resource-efficiency
    title: Resource efficiency and circular economy
    concept: /themes/resource-efficiency.md
    classification: structural_theme
    tracking_status: proposed
  - id: food-agtech
    title: Food and agricultural innovation
    concept: /themes/food-agriculture-innovation.md
    classification: structural_theme
    tracking_status: proposed
  - id: supply-resilience
    title: Supply-chain resilience and reshoring
    concept: /themes/supply-chain-resilience.md
    classification: structural_theme
    tracking_status: proposed
  - id: gold-miners
    title: Gold miners
    concept: /sectors/gdx.md
    classification: industry_basket
    tracking_status: active
market_report:
  section: themes
  implementation_status: registry_only
  evidence_status: exploratory
  enabled: false
---
# Theme registry

Document status (draft, stable, deprecated) describes knowledge maturity.
Tracking status (proposed, active, inactive) describes project coverage.
Active does not mean currently outperforming. IDs and classification fields are
project extensions, not OKF standard fields.

| Theme ID | Theme | Tracking status | Classification | Knowledge |
|---|---|---|---|---|
| drones | Drones | proposed | structural_theme | [Concept](/themes/drones.md) |
| ai | Artificial intelligence | proposed | structural_theme | [Concept](/themes/artificial-intelligence.md) |
| robotics | Robotics and automation | proposed | structural_theme | [Concept](/themes/robotics-automation.md) |
| cybersecurity | Cybersecurity | proposed | structural_theme | [Concept](/themes/cybersecurity.md) |
| quantum | Quantum computing | proposed | structural_theme | [Concept](/themes/quantum-computing.md) |
| space | Space and satellites | proposed | structural_theme | [Concept](/themes/space-economy.md) |
| defense-tech | Defense technology | proposed | structural_theme | [Concept](/themes/defense-technology.md) |
| mobility | Future mobility | proposed | structural_theme | [Concept](/themes/future-mobility.md) |
| semiconductors | Semiconductors | proposed | industry_basket | [Concept](/themes/semiconductors.md) |
| crypto-blockchain | Crypto and blockchain | proposed | structural_theme | [Concept](/themes/crypto-blockchain.md) |
| digital-finance | Digital finance | proposed | structural_theme | [Concept](/themes/digital-finance.md) |
| health-innovation | Healthcare technology and innovation | proposed | structural_theme | [Concept](/themes/healthcare-innovation.md) |
| longevity | Longevity and metabolic health | proposed | structural_theme | [Concept](/themes/longevity-metabolic-health.md) |
| electrification | Electrification and grid modernization | proposed | structural_theme | [Concept](/themes/electrification-grid.md) |
| nuclear | Nuclear energy | proposed | structural_theme | [Concept](/themes/nuclear-energy.md) |
| batteries | Batteries | proposed | structural_theme | [Concept](/themes/batteries.md) |
| renewables | Clean energy and renewables | proposed | structural_theme | [Concept](/themes/renewable-energy.md) |
| resource-efficiency | Resource efficiency and circular economy | proposed | structural_theme | [Concept](/themes/resource-efficiency.md) |
| food-agtech | Food and agricultural innovation | proposed | structural_theme | [Concept](/themes/food-agriculture-innovation.md) |
| supply-resilience | Supply-chain resilience and reshoring | proposed | structural_theme | [Concept](/themes/supply-chain-resilience.md) |
| gold-miners | Gold miners | active | industry_basket | [GDX](/sectors/gdx.md) |

The broad themes draw on provider thematic frameworks; the exact subdivisions
are a proposed project synthesis. These drafts do not establish stock membership
or implement new report sections. Gold miners remains the existing report basket.[^gdx-concept]

# Shared conventions

All theme stock universes use US exchange-listed stocks only, including eligible
US-listed foreign issuers and ADRs. Exclude foreign-only and OTC listings.
Apply this filter to linked holdings before constructing peer groups; see
[methodology](/themes/methodology.md). This scope records the user's instruction
of 2026-10-29 and does not imply that a global ETF proxy has a US-only portfolio.

[Theme memberships](/themes/theme-memberships.md) is the shared relationship
manifest, including links to existing dated holdings. Stocks may belong to
multiple subthemes and themes; deduplicate within parent-theme calculations.

[Methodology](/themes/methodology.md) defines membership evidence, peer exclusion,
equal weighting, date alignment, and proposed 5- and 10-session RS returns.
RS calculation period and new-high lookback are separate parameters.
The user's research proposal remains exploratory.[^user-proposal]

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
  - Support 5- and 10-session rolling RS returns initially, alongside the normalized RS series; expose a separate `high_lookback` parameter for new-high flags.
  - Return a dated RS series, new-high flags, eligible peer counts, and input provenance; exclude the tested stock and reject an empty peer group.
  - Verify scale invariance, self-exclusion, aligned dates, missing-history handling, and strict new-high behavior before enabling report output.

[^gdx-concept]: Existing GDX knowledge concept and report context; consulted 2026-10-28.
[^user-proposal]: User-requested research idea, recorded 2026-10-28; no study conducted.
