---
type: Dataset
title: Semiconductor security profiles
description: Separate business-model, ecosystem-role, and indicative end-market attributes for US-listed semiconductor theme members.
tags: [themes, semiconductors, classification, end-markets]
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

profile_schema:
  key: symbol
  list_separator: comma
  business_models: [fabless, integrated_manufacturer, foundry, equipment, software_ip, ip_licensing]
  ecosystem_roles: [chipmaker, equipment, design_ip]
  end_markets: [data_center, automotive, industrial, consumer, communications, semiconductor_manufacturing, semiconductor_design]
---
# Attributes

One row per selected US-listed security. Comma-separated values are sets; they
are not rankings or weights. This table is authoritative for these attributes;
subthemes live in [Theme memberships](/themes/theme-memberships.md).

All classifications are provisional project judgments based on the cited sources,
not independent verification of revenue shares. End markets are indicative,
non-exhaustive exposures. Equipment/design rows use their direct industry customer
as the end market, avoiding an unsupported claim about ultimate chip demand.
`chipmaker` includes contract foundries as well as designers and integrated
manufacturers. Multiple business models and ecosystem roles are allowed.

| Symbol | Company | Business models | Ecosystem roles | End markets | Reviewed | Sources |
|---|---|---|---|---|---|---|
| NASDAQ:NVDA | NVIDIA | fabless | chipmaker | data_center, consumer, automotive | 2026-10-30 | [^nvda-semis] [^smh-universe] |
| NASDAQ:AMD | Advanced Micro Devices | fabless | chipmaker | data_center, consumer, industrial | 2026-10-30 | [^amd-semis] [^smh-universe] |
| NASDAQ:TXN | Texas Instruments | integrated_manufacturer | chipmaker | industrial, automotive, consumer, communications | 2026-10-30 | [^txn-semis] [^smh-universe] |
| NASDAQ:ADI | Analog Devices | integrated_manufacturer | chipmaker | industrial, automotive, communications, consumer | 2026-10-30 | [^adi-semis] [^smh-universe] |
| NASDAQ:MCHP | Microchip Technology | integrated_manufacturer | chipmaker | industrial, automotive, consumer, communications | 2026-10-30 | [^mchp-semis] [^smh-universe] |
| NASDAQ:AVGO | Broadcom | fabless | chipmaker | data_center, communications, consumer | 2026-10-30 | [^smhx-model] [^smh-universe] |
| NASDAQ:QCOM | Qualcomm | fabless, ip_licensing | chipmaker, design_ip | communications, consumer, automotive | 2026-10-30 | [^qcom-semis] [^smh-universe] |
| NASDAQ:MRVL | Marvell Technology | fabless | chipmaker | data_center, communications | 2026-10-30 | [^mrvl-semis] [^smh-universe] |
| NASDAQ:MU | Micron Technology | integrated_manufacturer | chipmaker | data_center, consumer, automotive, industrial | 2026-10-30 | [^mu-semis] [^smh-universe] |
| NYSE:TSM | Taiwan Semiconductor Manufacturing ADR | foundry | chipmaker | data_center, consumer, automotive, industrial, communications | 2026-10-30 | [^tsm-semis] [^smh-universe] |
| NASDAQ:GFS | GlobalFoundries | foundry | chipmaker | data_center, consumer, automotive, industrial, communications | 2026-10-30 | [^gfs-semis] |
| NASDAQ:AMAT | Applied Materials | equipment | equipment | semiconductor_manufacturing | 2026-10-30 | [^amat-semis] [^smh-universe] |
| NASDAQ:LRCX | Lam Research | equipment | equipment | semiconductor_manufacturing | 2026-10-30 | [^lrcx-semis] [^smh-universe] |
| NASDAQ:KLAC | KLA | equipment | equipment | semiconductor_manufacturing | 2026-10-30 | [^klac-semis] [^smh-universe] |
| NASDAQ:ASML | ASML Holding | equipment | equipment | semiconductor_manufacturing | 2026-10-30 | [^asml-semis] [^smh-universe] |
| NASDAQ:SNPS | Synopsys | software_ip | design_ip | semiconductor_design | 2026-10-30 | [^snps-semis] [^smh-universe] |
| NASDAQ:CDNS | Cadence Design Systems | software_ip | design_ip | semiconductor_design | 2026-10-30 | [^cdns-semis] [^smh-universe] |
| NASDAQ:ARM | Arm Holdings ADS | ip_licensing, fabless | design_ip, chipmaker | data_center, consumer, automotive, industrial | 2026-10-30 | [^arm-semis] [^smh-universe] |

# Interpretation

The `chipmaker` filter is an explicit project convention, not a provider industry
code. For an exclusive attribution chart, choose a primary role separately;
these overlapping sets cannot be summed as disjoint groups. In particular, Arm
and Qualcomm have both chip and IP roles. Broadcom also has non-chip software
activities; the fabless label describes its semiconductor operation, not the
entire business. ADI uses hybrid manufacturing, and an integrated manufacturer
may outsource some production. Do not infer pure exposure from membership.

Provider symbols need current resolution before execution. Reviewed is the
classification review date, not historical validity. Use one listing per company.
See [Semiconductors](/themes/semiconductors.md) for scope and research contracts.

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
