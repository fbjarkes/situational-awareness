---
type: Reference
title: Artificial intelligence
description: Companies supplying or commercializing AI capabilities and infrastructure.
tags: [themes, ai]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-29T23:43:42Z"
sources:
  - id: nebius-cloud
    resource: https://nebius.com/about
    title: Nebius issuer AI-cloud platform and Nasdaq NBIS listing, consulted 2026-10-30
  - id: nebius-group
    resource: https://nebius.com/newsroom/nebius-reports-second-quarter-2026-financial-results
    title: Nebius issuer Q2 2026 results and other group activities, consulted 2026-10-30
  - id: coreweave-cloud
    resource: https://coreweave.com/why-coreweave
    title: CoreWeave issuer specialized GPU cloud description and Nasdaq CRWV listing, consulted 2026-10-30
  - id: iren-cloud
    resource: https://www.sec.gov/Archives/edgar/data/1878848/000187884826000052/iren-20260630.htm
    title: IREN fiscal 2026 Form 10-K, AI Cloud/mining business mix and transition, consulted 2026-10-30
  - id: iren-results
    resource: https://iren.gcs-web.com/news-releases/news-release-details/iren-reports-fy26-results
    title: IREN issuer results dated 2026-08-27; fiscal 2026 segment revenue and Nasdaq IREN, consulted 2026-10-30
  - id: provider-framework
    resource: https://www.msci.com/our-solutions/indexes/thematic-investing/themes-and-sub-themes
    title: Provider thematic classification framework
  - id: project-taxonomy
    resource: /themes/themes.md
    title: Project theme registry and proposed taxonomy
theme:
  id: ai
  classification: structural_theme
  tracking_status: proposed
  memberships: /themes/theme-memberships.md
  subthemes:
    - id: ai-hyperscalers-platforms
      title: Hyperscalers and AI platforms
    - id: ai-neoclouds
      title: Neoclouds and specialized AI cloud
    - id: ai-compute-infrastructure
      title: Compute infrastructure
    - id: ai-memory-and-hbm
      title: Memory and HBM
    - id: ai-lithography
      title: Lithography
    - id: ai-advanced-packaging
      title: Advanced packaging
    - id: ai-inspection-and-metrology
      title: Inspection and metrology
    - id: ai-photonics-and-optical-interconnects
      title: Photonics and optical interconnects
    - id: ai-switching-and-networking
      title: Switching and networking
    - id: ai-data-centers
      title: Data centers
    - id: ai-cooling
      title: Cooling
    - id: ai-power-delivery
      title: Power delivery
    - id: ai-software-platforms-and-agents
      title: Software platforms and agents
---
# Scope

Companies supplying or commercializing AI capabilities and infrastructure. This is a proposed project universe, not an industry classification
or a claim of current market leadership.

# Classification and subthemes

Provider frameworks support the broad thematic approach.[^provider-framework]
The names, boundaries, and subdivisions below are the project's first-draft
synthesis, not a provider's official membership rules.[^project-taxonomy]

- Hyperscalers and AI platforms
- Neoclouds and specialized AI cloud
- Compute infrastructure
- Memory and HBM
- Lithography
- Advanced packaging
- Inspection and metrology
- Photonics and optical interconnects
- Switching and networking
- Data centers
- Cooling
- Power delivery
- Software platforms and agents

# Membership criteria

Lithography here means equipment enabling semiconductor production for AI
infrastructure. AI applied to lithography is a separate exposure rationale;
record it explicitly rather than treating the two as equivalent. Photonics
covers optical components and interconnects supporting AI systems, not every
company selling optical products. Power and cooling membership likewise needs
evidence of AI/data-center exposure rather than a generic equipment label.

Require documented products, services, revenue, or investment exposure relevant
to the scope. Marketing references alone do not establish membership. Record
exposure as core, diversified, or indirect, supported by a source and rationale.
Membership can overlap other themes and subthemes.

# Initial neocloud universe

The [shared membership table](/themes/theme-memberships.md) records three
US-listed core-universe candidates under `ai-neoclouds`:

| Ticker | Company | AI exposure role | Business-mix context |
|---|---|---|---|
| NBIS | Nebius Group | Direct supplier | Specialized AI-cloud platform; group also has other businesses/interests. [^nebius-cloud] [^nebius-group] |
| CRWV | CoreWeave | Direct supplier | GPU cloud, storage, networking, and software for AI workloads. [^coreweave-cloud] |
| IREN | IREN Limited | Direct supplier | AI-cloud/mining transition; diversified exposure at the reviewed reporting date. [^iren-cloud] [^iren-results] |

US-listed foreign issuers are eligible; exclude OTC and foreign-only listings.
Core-universe role does not imply a pure-play revenue threshold. The exposure
classification is a provisional project judgment; review dates do not establish
historical membership. Current provider symbols must be resolved before execution.
Other AI segments remain unpopulated; do not automatically import their members
from Semiconductors, Healthcare, Robotics, or Electrification without AI evidence.

# Cloud boundaries and classification dimensions

Neoclouds provide specialized AI compute/cloud services. Distinguish them from
broad hyperscalers/AI platforms and from landlords leasing data-center space,
GPU designers, and power/cooling suppliers. A supplier can have multiple roles,
but owning a data center alone does not establish an AI-cloud service business.
The separate `ai-hyperscalers-platforms` category is reserved for broader cloud
and platform providers; it is not silently merged into the neocloud peer group.

Exposure role is independent of product subtheme and business mix: `direct_supplier`
sells AI-related capabilities, `adopter` applies AI internally to another business,
and `indirect_enabler` supplies supporting infrastructure. Initial selection
focuses on documented suppliers; merely using AI does not establish membership.
The role table above is qualitative, not a ranking or revenue-weighted breakdown.

IREN reported FY2026 AI Cloud revenue of $128.8 million versus $578.2 million
from Bitcoin mining.[^iren-results] Its filing describes an ongoing transition
with a target of substantially completing the change by 2026 year-end; this is a
plan, not a completed outcome.[^iren-cloud] Reassess realized revenue mix at each
review. Contracted ARR, operating run-rate ARR, and recognized period revenue
are different measures and must not be substituted for one another.

IREN's mining history does not automatically add it to the separately curated
[Crypto](/themes/crypto-blockchain.md) universe. Add a dated relationship only
when explicitly selecting that exposure. Likewise, do not treat legacy Nebius
issuer history as an unchanged AI-cloud business; record restructurings and
business transitions before historical research.

# Interpretation and research

Use [shared methodology](/themes/methodology.md) for weighting, calendars,
coverage, and RS. Compare a stock with its narrow peers and its parent theme
separately; this concept enables no trading rule.

Compare neocloud RS against the selected neocloud peers and, once populated,
the deduplicated AI parent basket. Exclude the tested stock and disclose peer
coverage. Do not label a three-stock neocloud basket as the full AI industry.
No RS calculation, report section, or data download is enabled by this update.

The authoritative [within-theme RS research checklist](/themes/themes.md#research-todos)
is maintained once in the registry.

[^provider-framework]: Provider framework consulted during project taxonomy research on 2026-10-28; supports broad categories, not every proposed subdivision.
[^project-taxonomy]: User-approved first-draft organization, 2026-10-28; membership and predictive effects remain unvalidated.

[^nebius-cloud]: Nebius issuer AI-cloud platform and Nasdaq NBIS listing; consulted 2026-10-30.
[^nebius-group]: Nebius issuer Q2 2026 results and other group activities; consulted 2026-10-30.
[^coreweave-cloud]: CoreWeave issuer specialized GPU cloud description and Nasdaq CRWV listing; consulted 2026-10-30.
[^iren-cloud]: IREN fiscal 2026 Form 10-K, AI Cloud/mining business mix and transition; consulted 2026-10-30.
[^iren-results]: IREN issuer results dated 2026-08-27; fiscal 2026 segment revenue and Nasdaq IREN; consulted 2026-10-30.
