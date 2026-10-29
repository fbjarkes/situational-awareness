---
type: Reference
title: Drones
description: US-listed companies supplying unmanned aerial systems, drone components, and related autonomy technologies.
tags: [themes, drones, autonomy, defense-tech]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-29T22:37:54Z"
sources:
  - id: avav-issuer
    resource: https://investor.avinc.com/news-events/press-releases
    title: AeroVironment issuer uncrewed-system releases, consulted 2026-10-29
  - id: ktos-issuer
    resource: https://ir.kratosdefense.com/investor-relations
    title: Kratos issuer unmanned systems and Nasdaq listing, consulted 2026-10-29
  - id: rcat-issuer
    resource: https://ir.redcatholdings.com/
    title: Red Cat issuer defense drone and robotics description, consulted 2026-10-29
  - id: ondas-issuer
    resource: https://www.ondas.com/
    title: Ondas issuer business description and Nasdaq ONDS listing, consulted 2026-10-29
  - id: umac-issuer
    resource: https://www.unusualmachines.com/
    title: Unusual Machines drone industry business, consulted 2026-10-29
  - id: umac-listing
    resource: https://www.sec.gov/Archives/edgar/data/1956955/000168316826000348/umac_8k.htm
    title: Unusual Machines January 2026 Form 8-K, NYSE American UMAC listing
  - id: dpro-release
    resource: https://www.nasdaq.com/press-release/draganfly-announces-closing-us-10-million-strategic-investment-2026-09-30
    title: Draganfly issuer release dated 2026-09-29, drone business and Nasdaq DPRO listing

theme:
  id: drones
  classification: structural_theme
  tracking_status: proposed
  memberships: /themes/theme-memberships.md
  subthemes:
    - id: drones-platforms
      title: Drone platforms
    - id: drones-components
      title: Components and enabling technology
    - id: drones-counter-uas
      title: Counter-drone systems
market_report:
  section: themes
  implementation_status: universe_recorded
  evidence_status: exploratory
  enabled: false
---
# Scope

Companies supplying aerial drones, unmanned aircraft systems, components,
and related autonomous or counter-drone technologies for military, commercial,
and public-safety uses. Restrict membership to US exchange-listed stocks;
US-listed foreign companies are eligible, while OTC and foreign-only listings
are excluded. This is a project theme, not an official industry classification.

# Initial universe

The authoritative [shared membership table](/themes/theme-memberships.md)
contains six initial candidates:

| Ticker | Company | Inclusion rationale |
|---|---|---|
| AVAV | AeroVironment | Uncrewed aerial systems. [^avav-issuer] |
| KTOS | Kratos Defense & Security Solutions | Unmanned systems within a broader defense business. [^ktos-issuer] |
| RCAT | Red Cat Holdings | Defense drone and robotic systems. [^rcat-issuer] |
| ONDS | Ondas | Autonomous drone systems and counter-UAS. [^ondas-issuer] |
| UMAC | Unusual Machines | Drone-industry products and components. [^umac-issuer] [^umac-listing] |
| DPRO | Draganfly | Drone solutions, systems, and technologies. [^dpro-release] |

All six are initial core-universe candidates; exposure labels are provisional
project judgments, not verified revenue thresholds. KTOS is marked diversified
because the cited issuer description spans multiple defense businesses.
Subtheme assignments and current provider-qualified symbols require review
before execution. Review dates do not establish historical membership.

# Overlap and research

This theme overlaps [Defense technology](/themes/defense-technology.md) and
[Robotics and automation](/themes/robotics-automation.md). AVAV, KTOS, and RCAT
already have separate defense memberships. Preserve both relationships and
deduplicate by security within each calculated universe. Membership in Drones
does not automatically assign a stock to any other theme.

Use [shared methodology](/themes/methodology.md) for weighting, peer exclusion,
coverage, and RS. Compare platform manufacturers and component suppliers
separately where appropriate. No dedicated ETF proxy is selected yet, and no
report output or trading rule is enabled. The authoritative
[within-theme RS research checklist](/themes/themes.md#research-todos) remains
in the registry.

[^avav-issuer]: AeroVironment issuer releases describing uncrewed systems; Nasdaq AVAV, consulted 2026-10-29.
[^ktos-issuer]: Kratos issuer investor relations; Nasdaq KTOS and unmanned/defense technologies, consulted 2026-10-29.
[^rcat-issuer]: Red Cat issuer investor relations; drone and robotic defense systems, consulted 2026-10-29.

[^ondas-issuer]: Ondas issuer description; Nasdaq ONDS and autonomous drones/counter-UAS, consulted 2026-10-29.
[^umac-issuer]: Unusual Machines issuer page; drone-industry products, consulted 2026-10-29.
[^umac-listing]: SEC Form 8-K dated 2026-01-15 lists UMAC on NYSE American; current provider symbol resolution required before execution.
[^dpro-release]: Draganfly issuer release dated 2026-09-29, distributed through Nasdaq; Nasdaq DPRO and drone systems/technology, consulted 2026-10-29.
