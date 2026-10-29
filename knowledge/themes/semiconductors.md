---
type: Reference
title: Semiconductors
description: US-listed semiconductor ecosystem organized by product subtheme, business model, and end-market exposure.
tags: [themes, semiconductors, chips, equipment, design-ip]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-29T23:32:00Z"
sources:
  - id: smh-universe
    resource: https://www.vaneck.com/us/en/investments/semiconductor-etf-smh/holdings
    title: VanEck SMH issuer holdings dated 2026-10-28; universe evidence, not project classifications, consulted 2026-10-30
  - id: smhx-model
    resource: https://www.vaneck.com/us/en/investments/fabless-semiconductor-etf-smhx/holdings
    title: VanEck SMHX fabless semiconductor fund; business-model context, consulted 2026-10-30
  - id: nvda-semis
    resource: https://www.nvidia.com/en-us/about-nvidia/
    title: NVIDIA issuer accelerated computing, AI, and graphics description, consulted 2026-10-30
  - id: amd-semis
    resource: https://www.amd.com/en/corporate.html
    title: AMD issuer compute, graphics, accelerators, and embedded portfolio, consulted 2026-10-30
  - id: txn-semis
    resource: https://www.ti.com/about-ti.html
    title: Texas Instruments issuer analog/embedded products and manufacturing, consulted 2026-10-30
  - id: adi-semis
    resource: https://www.analog.com/en/who-we-are.html
    title: Analog Devices issuer analog portfolio and hybrid manufacturing network, consulted 2026-10-30
  - id: mchp-semis
    resource: https://www.microchip.com/en-us/about/corporate-overview
    title: Microchip issuer embedded control, manufacturing, and market description, consulted 2026-10-30
  - id: qcom-semis
    resource: https://www.qualcomm.com/company
    title: Qualcomm issuer processors, modems, connectivity, and licensing context, consulted 2026-10-30
  - id: mrvl-semis
    resource: https://www.marvell.com/company.html
    title: Marvell issuer compute, connectivity, and storage portfolio, consulted 2026-10-30
  - id: mu-semis
    resource: https://www.micron.com/about
    title: Micron issuer memory/storage products and markets, consulted 2026-10-30
  - id: tsm-semis
    resource: https://www.tsmc.com/english/aboutTSMC
    title: TSMC issuer dedicated foundry services, consulted 2026-10-30
  - id: gfs-semis
    resource: https://investors.gf.com/
    title: GlobalFoundries issuer manufacturing and end-market description, consulted 2026-10-30
  - id: amat-semis
    resource: https://www.appliedmaterials.com/us/en/about.html
    title: Applied Materials issuer semiconductor equipment description, consulted 2026-10-30
  - id: lrcx-semis
    resource: https://www.lamresearch.com/company/
    title: Lam Research issuer semiconductor manufacturing processes and equipment, consulted 2026-10-30
  - id: klac-semis
    resource: https://www.kla.com/company
    title: KLA issuer process control and semiconductor manufacturing solutions, consulted 2026-10-30
  - id: asml-semis
    resource: https://www.asml.com/en/company
    title: ASML issuer lithography and related equipment, consulted 2026-10-30
  - id: snps-semis
    resource: https://www.synopsys.com/company.html
    title: Synopsys issuer EDA, IP, and system-design products, consulted 2026-10-30
  - id: cdns-semis
    resource: https://www.cadence.com/en_US/home/company.html
    title: Cadence issuer computational software, chip design, and IP, consulted 2026-10-30
  - id: arm-semis
    resource: https://www.arm.com/company
    title: Arm issuer IP licensing and Arm-designed compute silicon portfolio, consulted 2026-10-30
  - id: semis-project
    resource: User-approved semiconductor taxonomy in this project chat, 2026-10-30
    title: Seven-subtheme project design and separate business/end-market attributes, consulted 2026-10-30

theme:
  id: semiconductors
  classification: industry_basket
  tracking_status: proposed
  memberships: /themes/theme-memberships.md
  security_profiles: /themes/semiconductor-profiles.md
  subthemes:
    - id: semis-compute
      title: AI accelerators and compute
    - id: semis-analog-embedded
      title: Analog and embedded
    - id: semis-connectivity
      title: Connectivity and communications
    - id: semis-memory
      title: Memory and storage chips
    - id: semis-foundries
      title: Foundries
    - id: semis-equipment
      title: Manufacturing equipment
    - id: semis-design-ip
      title: Chip-design software and IP
market_report:
  section: themes
  implementation_status: universe_recorded
  evidence_status: exploratory
  enabled: false
---
# Scope

US exchange-listed semiconductor companies and their equipment/design ecosystem.
US-listed foreign issuers and ADRs/ADSs are eligible; exclude foreign-only and OTC
listings. Keep chipmakers distinguishable from equipment and design enablers.
The seven-subtheme taxonomy is a user-approved project design, not an official
industry classification.[^semis-project]

# Product subthemes

| Subtheme | Initial US-listed candidates |
|---|---|
| AI accelerators and compute | NVDA, AMD |
| Analog and embedded | TXN, ADI, MCHP |
| Connectivity and communications | AVGO, QCOM, MRVL |
| Memory and storage chips | MU |
| Foundries | TSM, GFS |
| Manufacturing equipment | AMAT, LRCX, KLAC, ASML |
| Chip-design software and IP | SNPS, CDNS, ARM |

[Theme memberships](/themes/theme-memberships.md) is authoritative for security-to-
subtheme relationships. [Semiconductor profiles](/themes/semiconductor-profiles.md)
stores the separate business-model and end-market attributes, one row per security.
Most names appear in the dated SMH holdings; GFS is supported by its issuer
reference.[^smh-universe][^gfs-semis] This is a custom initial list, not an SMH
replication or exhaustive industry universe.

# NVDA versus TXN

NVDA is assigned to compute, with a fabless business-model label and indicative
data-center/consumer/automotive exposure. TXN is assigned to analog/embedded,
with an integrated-manufacturer label and industrial/automotive exposure among
its markets.[^nvda-semis][^txn-semis][^smhx-model] Thus a shared parent does not
make them interchangeable narrow peers. End-market tags are qualitative and
non-exclusive, not ranked revenue shares.

# Universe choices for research

- `ecosystem`: union of all semiconductor theme memberships, deduplicated by company.
- `chipmakers`: the same union filtered to profiles whose ecosystem roles include
  `chipmaker`; includes fabless designers, integrated manufacturers, and foundries.
- `subtheme`: explicit membership in one product subtheme, with its selected peers
  recorded; multiple memberships are allowed where supported.

Run stock-versus-group RS against both the narrow subtheme and the selected parent
universe, excluding the tested stock and deduplicating overlapping relationships.
Use the shared 5- and 10-session rolling RS convention; keep new-high lookback
separate. A group containing only the tested stock is unavailable, not zero RS:
MU currently has no other memory peer in this initial list. Do not silently borrow
members from a broader theme to fill that gap. These universe selectors are
research contracts; no selector or RS runtime is implemented by this update.

# Classification limits

These are provisional project assignments informed by issuer descriptions and
fund context. They do not establish revenue concentration or validated trading
signals. Product subthemes are not exclusive: custom compute can overlap
connectivity, and analog companies may supply embedded/connectivity products.
Business models can also overlap and change. ADI describes a hybrid internal and
external manufacturing network; integrated manufacturing does not mean every
chip is made internally.[^adi-semis] Arm's current site includes both licensed
IP and Arm-designed compute silicon, so its profile records IP and fabless roles
rather than treating it as software-only.[^arm-semis] Reassess such boundary
cases using current disclosures before research.

Review dates are not historical membership starts. Check current US listing,
provider-qualified symbols, corporate actions, and dated business mix before
execution; historical use of this current list introduces survivorship bias.
SMH is a proposed broad comparison proxy, not an exact match to any of these
custom scopes. ETFs do not enter company breadth or peer denominators.
Use [shared methodology](/themes/methodology.md) and the authoritative
[RS research checklist](/themes/themes.md#research-todos). No report section,
new signal, data download, or trading hypothesis is enabled.

[^smh-universe]: VanEck SMH issuer holdings dated 2026-10-28; universe evidence, not project classifications; consulted 2026-10-30.
[^smhx-model]: VanEck SMHX fabless semiconductor fund; business-model context; consulted 2026-10-30.
[^nvda-semis]: NVIDIA issuer accelerated computing, AI, and graphics description; consulted 2026-10-30.
[^amd-semis]: AMD issuer compute, graphics, accelerators, and embedded portfolio; consulted 2026-10-30.
[^txn-semis]: Texas Instruments issuer analog/embedded products and manufacturing; consulted 2026-10-30.
[^adi-semis]: Analog Devices issuer analog portfolio and hybrid manufacturing network; consulted 2026-10-30.
[^mchp-semis]: Microchip issuer embedded control, manufacturing, and market description; consulted 2026-10-30.
[^qcom-semis]: Qualcomm issuer processors, modems, connectivity, and licensing context; consulted 2026-10-30.
[^mrvl-semis]: Marvell issuer compute, connectivity, and storage portfolio; consulted 2026-10-30.
[^mu-semis]: Micron issuer memory/storage products and markets; consulted 2026-10-30.
[^tsm-semis]: TSMC issuer dedicated foundry services; consulted 2026-10-30.
[^gfs-semis]: GlobalFoundries issuer manufacturing and end-market description; consulted 2026-10-30.
[^amat-semis]: Applied Materials issuer semiconductor equipment description; consulted 2026-10-30.
[^lrcx-semis]: Lam Research issuer semiconductor manufacturing processes and equipment; consulted 2026-10-30.
[^klac-semis]: KLA issuer process control and semiconductor manufacturing solutions; consulted 2026-10-30.
[^asml-semis]: ASML issuer lithography and related equipment; consulted 2026-10-30.
[^snps-semis]: Synopsys issuer EDA, IP, and system-design products; consulted 2026-10-30.
[^cdns-semis]: Cadence issuer computational software, chip design, and IP; consulted 2026-10-30.
[^arm-semis]: Arm issuer IP licensing and Arm-designed compute silicon portfolio; consulted 2026-10-30.
[^semis-project]: Seven-subtheme project design and separate business/end-market attributes; consulted 2026-10-30.
