---
type: Dataset
title: Theme memberships
description: Shared dated stock-to-theme relationships and references to existing constituent snapshots.
tags: [themes, tickers, membership]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-29T22:33:06Z"
sources:
  - id: teradyne-ir
    resource: https://investors.teradyne.com/
    title: Teradyne US listing and robotics business, consulted 2026-10-29
  - id: rockwell-ir
    resource: https://www.rockwellautomation.com/en-us/company/investor-relations.html
    title: Rockwell US listing and industrial automation business, consulted 2026-10-29
  - id: symbotic-ir
    resource: https://ir.symbotic.com/news-releases/news-release-details/symbotic-announces-acquisition-arms-innovations-advancing-new
    title: Symbotic US listing and warehouse automation, consulted 2026-10-29
  - id: botz-holdings
    resource: https://www.globalxetfs.com/funds/botz/
    title: Global X BOTZ holdings as of 2026-10-28, consulted 2026-10-29
  - id: botz-ucits-holdings
    resource: https://globalxetfs.eu/funds/botz?download_full_holdings=true
    title: Global X BOTZ UCITS holdings as of 2026-10-20, consulted 2026-10-29
  - id: nlr-holdings
    resource: https://www.vaneck.com/us/en/investments/uranium-nuclear-energy-etf-nlr/overview
    title: VanEck NLR holdings as of 2026-10-28, consulted 2026-10-29
  - id: cibr-holdings
    resource: https://www.ftportfolios.com/Retail/Etf/EtfHoldings.aspx?Ticker=CIBR
    title: First Trust CIBR holdings as of 2026-10-28, consulted 2026-10-29
  - id: user-selection
    resource: User request in this project chat, 2026-10-29
    title: Add the proposed twelve core cybersecurity companies and three extended candidates
  - id: gdx-holdings
    resource: /sectors/gdx.md
    title: GDX dated holdings snapshot
---
# Memberships

One row represents one security-to-subtheme relationship. Multiple relationships
per stock are allowed. Parent-theme assignments can leave Subtheme ID blank
pending a sourced subtheme review. The cybersecurity selection below was recorded
on 2026-10-29 from the user's approved shortlist.[^user-selection]

| Symbol | Theme ID | Subtheme ID | Role | Exposure | Valid from | Valid to | Reviewed | Rationale | Source |
|---|---|---|---|---|---|---|---|---|---|
| NASDAQ:TER | robotics | | core universe | diversified | | | 2026-10-29 | Teradyne; collaborative and mobile robotics alongside automated test equipment | [^teradyne-ir] |
| NYSE:ROK | robotics | | core universe | core | | | 2026-10-29 | Rockwell Automation; industrial automation | [^rockwell-ir] |
| NASDAQ:SYM | robotics | | core universe | core | | | 2026-10-29 | Symbotic; warehouse robotics and automation | [^symbotic-ir] |
| NASDAQ:ISRG | robotics | | core universe | core | | | 2026-10-29 | Intuitive Surgical; selected robotics universe constituent | [^botz-holdings] |
| NASDAQ:CGNX | robotics | | core universe | core | | | 2026-10-29 | Cognex; selected automation universe constituent | [^botz-holdings] |
| NASDAQ:NVDA | robotics | | extended candidate | diversified | | | 2026-10-29 | NVIDIA; optional broader ecosystem extension | [^botz-holdings] |
| NASDAQ:TSLA | robotics | | extended candidate | diversified | | | 2026-10-29 | Tesla; optional broader ecosystem extension | [^botz-holdings] |
| NYSE:CCJ | nuclear | | core universe | core | | | 2026-10-29 | Cameco; selected nuclear universe constituent | [^nlr-holdings] |
| NYSE:BWXT | nuclear | | core universe | core | | | 2026-10-29 | BWX Technologies; selected nuclear universe constituent | [^nlr-holdings] |
| AMEX:LEU | nuclear | | core universe | core | | | 2026-10-29 | Centrus Energy; selected nuclear universe constituent | [^nlr-holdings] |
| AMEX:UEC | nuclear | | core universe | core | | | 2026-10-29 | Uranium Energy; selected nuclear universe constituent | [^nlr-holdings] |
| NYSE:NXE | nuclear | | core universe | core | | | 2026-10-29 | NexGen Energy; selected nuclear universe constituent | [^nlr-holdings] |
| AMEX:DNN | nuclear | | core universe | core | | | 2026-10-29 | Denison Mines; selected nuclear universe constituent | [^nlr-holdings] |
| AMEX:UUUU | nuclear | | core universe | core | | | 2026-10-29 | Energy Fuels; selected nuclear universe constituent | [^nlr-holdings] |
| NYSE:OKLO | nuclear | | core universe | core | | | 2026-10-29 | Oklo; selected nuclear universe constituent | [^nlr-holdings] |
| NYSE:SMR | nuclear | | core universe | core | | | 2026-10-29 | NuScale Power; selected nuclear universe constituent | [^nlr-holdings] |
| NASDAQ:NNE | nuclear | | core universe | core | | | 2026-10-29 | NANO Nuclear Energy; selected nuclear universe constituent | [^nlr-holdings] |
| NASDAQ:CEG | nuclear | | extended candidate | diversified | | | 2026-10-29 | Constellation Energy; optional generation extension | [^nlr-holdings] |
| NYSE:PEG | nuclear | | extended candidate | diversified | | | 2026-10-29 | Public Service Enterprise Group; optional generation extension | [^nlr-holdings] |
| NASDAQ:PANW | cybersecurity | | core universe | core | | | 2026-10-29 | Palo Alto Networks; selected for initial cybersecurity universe | [^cibr-holdings] [^user-selection] |
| NASDAQ:CRWD | cybersecurity | | core universe | core | | | 2026-10-29 | CrowdStrike; selected for initial cybersecurity universe | [^cibr-holdings] [^user-selection] |
| NASDAQ:FTNT | cybersecurity | | core universe | core | | | 2026-10-29 | Fortinet; selected for initial cybersecurity universe | [^cibr-holdings] [^user-selection] |
| NASDAQ:ZS | cybersecurity | | core universe | core | | | 2026-10-29 | Zscaler; selected for initial cybersecurity universe | [^cibr-holdings] [^user-selection] |
| NASDAQ:CHKP | cybersecurity | | core universe | core | | | 2026-10-29 | Check Point Software; selected for initial cybersecurity universe | [^cibr-holdings] [^user-selection] |
| NASDAQ:OKTA | cybersecurity | | core universe | core | | | 2026-10-29 | Okta; selected for initial cybersecurity universe | [^cibr-holdings] [^user-selection] |
| NYSE:S | cybersecurity | | core universe | core | | | 2026-10-29 | SentinelOne; selected for initial cybersecurity universe | [^cibr-holdings] [^user-selection] |
| NASDAQ:QLYS | cybersecurity | | core universe | core | | | 2026-10-29 | Qualys; selected for initial cybersecurity universe | [^cibr-holdings] [^user-selection] |
| NASDAQ:TENB | cybersecurity | | core universe | core | | | 2026-10-29 | Tenable; selected for initial cybersecurity universe | [^cibr-holdings] [^user-selection] |
| NASDAQ:VRNS | cybersecurity | | core universe | core | | | 2026-10-29 | Varonis Systems; selected for initial cybersecurity universe | [^cibr-holdings] [^user-selection] |
| NYSE:RBRK | cybersecurity | | core universe | core | | | 2026-10-29 | Rubrik; selected for initial cybersecurity universe | [^cibr-holdings] [^user-selection] |
| NASDAQ:NTSK | cybersecurity | | core universe | core | | | 2026-10-29 | Netskope; selected for initial cybersecurity universe | [^cibr-holdings] [^user-selection] |
| NYSE:NET | cybersecurity | | extended candidate | diversified | | | 2026-10-29 | Cloudflare; optional extension of the initial universe | [^cibr-holdings] [^user-selection] |
| NASDAQ:FFIV | cybersecurity | | extended candidate | diversified | | | 2026-10-29 | F5; optional extension of the initial universe | [^cibr-holdings] [^user-selection] |
| NASDAQ:AKAM | cybersecurity | | extended candidate | diversified | | | 2026-10-29 | Akamai Technologies; optional extension of the initial universe | [^cibr-holdings] [^user-selection] |

Use provider-qualified symbols. Unknown validity dates are left blank, not inferred
from a review date. Follow [methodology](/themes/methodology.md) when adding rows.

The 15 companies appear in CIBR's 2026-10-28 holdings.[^cibr-holdings]
Core versus extended and exposure labels are the project's provisional selection,
not issuer classifications or verified revenue thresholds. Use the 12 core rows
for the initial universe; including the three extended candidates requires an
explicit universe choice. Reviewed records the source/selection review date,
not an independent validation of company exposure or a historical membership date.
Subtheme assignments and provider symbol resolution remain pending before execution.

# Existing universe references

The US-only robotics shortlist contains five core candidates (ISRG, CGNX,
TER, ROK, SYM) and two extended candidates (NVDA, TSLA). Teradyne, Rockwell,
and Symbotic are supported by issuer sources rather than an inferred ETF
membership. Foreign-only listings have been removed; subthemes and provider
symbol resolution remain pending. Exposure labels are provisional.


| Theme ID | Membership as of | Authoritative ticker list | Securities | Selection |
|---|---|---|---:|---|
| gold-miners | 2026-10-22 | [GDX holdings](/sectors/gdx.md) | US-only count pending | Filter for eligible US exchange listings; full source has 59 securities |

GDX membership remains in its existing authoritative holdings table.[^gdx-holdings]
Issuer labels require provider resolution; GDX itself is a proxy, not an additional
constituent. This dated snapshot is not historical point-in-time membership.
The manifest review does not constitute a new holdings download.

[^gdx-holdings]: Existing GDX holdings snapshot as of 2026-10-22; linked without duplicating the ticker list.
[^cibr-holdings]: First Trust CIBR issuer holdings dated 2026-10-28, consulted 2026-10-29; supports company/ticker inclusion, not the project's exposure labels.
[^user-selection]: User approved adding the proposed 12 core companies and three extended candidates on 2026-10-29.
[^nlr-holdings]: VanEck NLR issuer holdings dated 2026-10-28, consulted 2026-10-29; project shortlist recorded 2026-10-29 without a historical membership claim.
[^botz-holdings]: Global X BOTZ issuer holdings dated 2026-10-28, consulted 2026-10-29; project subset, not a fund replication.
[^botz-ucits-holdings]: Global X BOTZ UCITS issuer holdings dated 2026-10-20, consulted 2026-10-29; supports OMRON inclusion and is distinct from the US fund snapshot.

[^teradyne-ir]: Teradyne issuer investor relations; Nasdaq TER and collaborative/mobile robotics business, consulted 2026-10-29.
[^rockwell-ir]: Rockwell Automation issuer investor relations; NYSE ROK and industrial automation, consulted 2026-10-29.
[^symbotic-ir]: Symbotic issuer release dated 2026-07-02; Nasdaq SYM and warehouse robotics, consulted 2026-10-29.
