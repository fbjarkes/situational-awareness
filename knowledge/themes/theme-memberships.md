---
type: Dataset
title: Theme memberships
description: Shared dated stock-to-theme relationships and references to existing constituent snapshots.
tags: [themes, tickers, membership]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-29T23:01:31Z"
sources:
  - id: ionq-issuer
    resource: https://investors.ionq.com/overview/
    title: IonQ issuer quantum computing platform description, consulted 2026-10-30
  - id: rigetti-issuer
    resource: https://investors.rigetti.com/ir-resources/investor-faqs
    title: Rigetti issuer cloud quantum systems and Nasdaq RGTI listing, consulted 2026-10-30
  - id: dwave-issuer
    resource: https://ir.dwavequantum.com/
    title: D-Wave issuer quantum systems and services description, consulted 2026-10-30
  - id: dwave-listing
    resource: https://ir.dwavequantum.com/resources/investor-faqs/
    title: D-Wave issuer current Nasdaq QBTS listing, consulted 2026-10-30
  - id: dwave-transfer
    resource: https://www.sec.gov/Archives/edgar/data/1907982/000190798226000129/qbts-20260630.htm
    title: D-Wave Q2 2026 Form 10-Q confirms Nasdaq trading began 2026-07-27, consulted 2026-10-30
  - id: qubt-issuer
    resource: https://quantumcomputinginc.com/investor-relations
    title: Quantum Computing Inc issuer photonic systems and Nasdaq QUBT listing, consulted 2026-10-30
  - id: ibm-quantum
    resource: https://www.ibm.com/quantum
    title: IBM issuer quantum systems and software platform, consulted 2026-10-30
  - id: microsoft-quantum
    resource: https://azure.microsoft.com/en-us/solutions/quantum-computing/
    title: Microsoft Azure Quantum platform and quantum research, consulted 2026-10-30
  - id: google-quantum
    resource: https://quantumai.google/
    title: Google Quantum AI hardware and software research, consulted 2026-10-30
  - id: lilly-metabolic
    resource: https://investor.lilly.com/news-releases/news-release-details/lilly-reports-second-quarter-2026-financial-results-raises-full
    title: Lilly issuer Q2 2026 results, NYSE LLY and metabolic medicines, consulted 2026-10-29
  - id: novo-metabolic
    resource: https://www.novonordisk.com/content/nncorp/global/en/news-and-media/news-and-ir-materials/news-details.html?id=916590
    title: Novo Nordisk issuer Q2 2026 update, obesity and diabetes portfolio, consulted 2026-10-29
  - id: novo-listing
    resource: https://www.novonordisk.com/about/corporate-governance.html
    title: Novo Nordisk issuer NYSE NVO ADR listing, consulted 2026-10-29
  - id: viking-metabolic
    resource: https://ir.vikingtherapeutics.com/2026-10-28-Viking-Therapeutics-Reports-Third-Quarter-2026-Financial-Results-and-Provides-Corporate-Update
    title: Viking issuer update dated 2026-10-28, Nasdaq VKTX and clinical metabolic programs, consulted 2026-10-29
  - id: structure-metabolic
    resource: https://ir.structuretx.com/news-releases/news-release-details/structure-therapeutics-reports-second-quarter-2026-financial
    title: Structure issuer results dated 2026-08-06, Nasdaq GPCR and clinical obesity programs, consulted 2026-10-29
  - id: dexcom-metabolic
    resource: https://investors.dexcom.com/news/news-details/2026/Dexcom-Reports-Third-Quarter-2026-Financial-Results/default.aspx
    title: Dexcom issuer results dated 2026-10-29, Nasdaq DXCM and glucose monitoring, consulted 2026-10-29
  - id: altimmune-metabolic
    resource: https://ir.altimmune.com/news-releases/news-release-details/altimmune-announces-second-quarter-2026-financial-results-and
    title: Altimmune issuer update dated 2026-08-12, Nasdaq ALT and clinical liver-disease programs, consulted 2026-10-29
  - id: joby-aircraft
    resource: https://www.jobyaviation.com/technology
    title: Joby aircraft specifications; piloted electric air taxi, consulted 2026-10-29
  - id: joby-autonomy
    resource: https://www.jobyaviation.com/news/joby-completes-first-ever-fully-autonomous-flight-across-the-united-states
    title: Joby autonomous-flight demonstration, 2026-09-18; NYSE JOBY, consulted 2026-10-29
  - id: archer-issuer
    resource: https://investors.archer.com/news/news-details/2026/Archer-Announces-Fourth-Quarter-and-Full-Year-2025-Results-US-and-UAE-Air-Taxi-Pilot-Programs-On-Track-for-2026/default.aspx
    title: Archer issuer release, 2026-03-02; NYSE ACHR and piloted air taxis, consulted 2026-10-29
  - id: eve-issuer
    resource: https://ir.eveairmobility.com/news-events/press-releases/detail/118/eve-holding-inc-reports-second-quarter-2026-results
    title: Eve issuer results, 2026-08-04; NYSE EVEX and eVTOL development, consulted 2026-10-29
  - id: vertical-listing
    resource: https://www.sec.gov/Archives/edgar/data/1867102/000110465926113318/tm2625635d1_ex99-1.htm
    title: Vertical issuer release, 2026-10-02; NYSE EVTL, piloted aircraft, and listing notice, consulted 2026-10-29
  - id: ehang-issuer
    resource: https://ehang.gcs-web.com/news-releases/news-release-details/ehang-reports-second-quarter-2026-unaudited-financial-results
    title: EHang issuer Q2 2026 results; pilotless eVTOL and Nasdaq EH, consulted 2026-10-29
  - id: grid-holdings
    resource: https://www.ftportfolios.com/Retail/Etf/EtfHoldings.aspx?Ticker=GRID
    title: First Trust GRID holdings as of 2026-10-28, consulted 2026-10-29
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
  - id: shld-holdings
    resource: https://www.globalxetfs.com/funds/shld/
    title: Global X SHLD mandate and holdings as of 2026-10-28, consulted 2026-10-29
  - id: avav-issuer
    resource: https://investor.avinc.com/news-events/press-releases
    title: AeroVironment issuer releases and Nasdaq listing, consulted 2026-10-29
  - id: ktos-issuer
    resource: https://ir.kratosdefense.com/investor-relations
    title: Kratos issuer business description and Nasdaq listing, consulted 2026-10-29
  - id: rcat-issuer
    resource: https://ir.redcatholdings.com/
    title: Red Cat issuer defense drone and robotics description, consulted 2026-10-29
  - id: mrcy-issuer
    resource: https://newsroom.mrcy.com/posts/pressreleases/mercury-awarded-contracts-for-us-space-and-st
    title: Mercury Systems issuer release dated 2026-01-15, consulted 2026-10-29
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
| NYSE:IONQ | quantum | | core universe | core | | | 2026-10-30 | IonQ; Quantum computing and related platform technologies | [^ionq-issuer] |
| NASDAQ:RGTI | quantum | | core universe | core | | | 2026-10-30 | Rigetti Computing; Quantum processors and cloud systems | [^rigetti-issuer] |
| NASDAQ:QBTS | quantum | | core universe | core | | | 2026-10-30 | D-Wave Quantum; Quantum systems and services; Nasdaq transfer effective July 2026 | [^dwave-issuer] [^dwave-listing] [^dwave-transfer] |
| NASDAQ:QUBT | quantum | | core universe | core | | | 2026-10-30 | Quantum Computing Inc.; Photonic quantum systems and related technologies | [^qubt-issuer] |
| NYSE:IBM | quantum | | extended candidate | diversified | | | 2026-10-30 | IBM; Quantum systems and Qiskit within broader technology business | [^ibm-quantum] |
| NASDAQ:MSFT | quantum | | extended candidate | diversified | | | 2026-10-30 | Microsoft; Azure Quantum and quantum research within broader technology business | [^microsoft-quantum] |
| NASDAQ:GOOGL | quantum | | extended candidate | diversified | | | 2026-10-30 | Alphabet Class A; Google Quantum AI; one Alphabet share class selected | [^google-quantum] |
| NYSE:LLY | longevity | longevity-obesity-treatments | core universe | diversified | | | 2026-10-29 | Eli Lilly; established metabolic medicines and obesity pipeline | [^lilly-metabolic] |
| NYSE:NVO | longevity | longevity-obesity-treatments | core universe | core | | | 2026-10-29 | Novo Nordisk ADR; obesity and diabetes medicines | [^novo-metabolic] [^novo-listing] |
| NASDAQ:VKTX | longevity | longevity-obesity-treatments | core universe | core | | | 2026-10-29 | Viking Therapeutics; clinical-stage metabolic and obesity programs | [^viking-metabolic] |
| NASDAQ:GPCR | longevity | longevity-obesity-treatments | core universe | core | | | 2026-10-29 | Structure Therapeutics ADS; clinical-stage oral obesity programs | [^structure-metabolic] |
| NASDAQ:DXCM | longevity | longevity-glucose-monitoring | core universe | core | | | 2026-10-29 | Dexcom; glucose monitoring and diabetes management | [^dexcom-metabolic] |
| NASDAQ:ALT | longevity | longevity-metabolic-liver-disease | extended candidate | core | | | 2026-10-29 | Altimmune; clinical-stage liver-disease programs; metabolic-health extension | [^altimmune-metabolic] |
| NYSE:JOBY | drones | drones-autonomous-aviation | extended candidate | diversified | | | 2026-10-29 | Joby Aviation; autonomous flight technology distinct from piloted air taxi | [^joby-autonomy] [^joby-aircraft] |
| NYSE:JOBY | mobility | mobility-air-taxis | core universe | core | | | 2026-10-29 | Joby Aviation; piloted electric air taxi | [^joby-aircraft] |
| NYSE:JOBY | mobility | mobility-autonomous-aviation | core universe | diversified | | | 2026-10-29 | Joby Aviation; separate autonomy technology; deduplicate within parent theme | [^joby-autonomy] |
| NYSE:ACHR | mobility | mobility-air-taxis | core universe | core | | | 2026-10-29 | Archer Aviation; piloted eVTOL air taxis | [^archer-issuer] |
| NYSE:EVEX | mobility | mobility-air-taxis | core universe | core | | | 2026-10-29 | Eve Holding; eVTOL and urban air mobility development | [^eve-issuer] |
| NYSE:EVTL | mobility | mobility-air-taxis | core universe | core | | | 2026-10-29 | Vertical Aerospace; piloted eVTOL; monitor disclosed NYSE noncompliance | [^vertical-listing] |
| NASDAQ:EH | mobility | mobility-air-taxis | core universe | core | | | 2026-10-29 | EHang ADS; pilotless passenger eVTOL | [^ehang-issuer] |
| NYSE:ETN | electrification | | core universe | diversified | | | 2026-10-29 | Eaton; selected GRID holding for project electrification universe | [^grid-holdings] |
| NYSE:PWR | electrification | | core universe | core | | | 2026-10-29 | Quanta Services; selected GRID holding for project electrification universe | [^grid-holdings] |
| NYSE:HUBB | electrification | | core universe | core | | | 2026-10-29 | Hubbell; selected GRID holding for project electrification universe | [^grid-holdings] |
| NYSE:NVT | electrification | | core universe | core | | | 2026-10-29 | nVent Electric; selected GRID holding for project electrification universe | [^grid-holdings] |
| NYSE:GEV | electrification | | core universe | diversified | | | 2026-10-29 | GE Vernova; selected GRID holding for project electrification universe | [^grid-holdings] |
| NASDAQ:MYRG | electrification | | core universe | core | | | 2026-10-29 | MYR Group; selected GRID holding for project electrification universe | [^grid-holdings] |
| NASDAQ:ITRI | electrification | | core universe | core | | | 2026-10-29 | Itron; selected GRID holding for project electrification universe | [^grid-holdings] |
| NASDAQ:AMSC | electrification | | core universe | core | | | 2026-10-29 | American Superconductor; selected GRID holding for project electrification universe | [^grid-holdings] |
| NYSE:WCC | electrification | | core universe | diversified | | | 2026-10-29 | WESCO International; selected GRID holding for project electrification universe | [^grid-holdings] |
| NASDAQ:FLNC | electrification | | core universe | core | | | 2026-10-29 | Fluence Energy; selected GRID holding for project electrification universe | [^grid-holdings] |
| NYSE:JCI | electrification | | extended candidate | diversified | | | 2026-10-29 | Johnson Controls International; selected GRID holding for project electrification universe | [^grid-holdings] |
| NASDAQ:TSLA | electrification | | extended candidate | diversified | | | 2026-10-29 | Tesla; selected GRID holding for project electrification universe | [^grid-holdings] |
| NASDAQ:AVAV | drones | | core universe | core | | | 2026-10-29 | AeroVironment; Uncrewed aerial systems | [^avav-issuer] |
| NASDAQ:KTOS | drones | | core universe | diversified | | | 2026-10-29 | Kratos Defense & Security Solutions; Unmanned systems within broader defense operations | [^ktos-issuer] |
| NASDAQ:RCAT | drones | | core universe | core | | | 2026-10-29 | Red Cat Holdings; Defense drone and robotic systems | [^rcat-issuer] |
| NASDAQ:ONDS | drones | | core universe | core | | | 2026-10-29 | Ondas; Autonomous drone and counter-UAS technologies | [^ondas-issuer] |
| AMEX:UMAC | drones | | core universe | core | | | 2026-10-29 | Unusual Machines; Drone products and components | [^umac-issuer] [^umac-listing] |
| NASDAQ:DPRO | drones | | core universe | core | | | 2026-10-29 | Draganfly; Drone solutions and technologies | [^dpro-release] |
| NASDAQ:AVAV | defense-tech | | core universe | core | | | 2026-10-29 | AeroVironment; Uncrewed systems and counter-drone technologies | [^avav-issuer] |
| NASDAQ:KTOS | defense-tech | | core universe | core | | | 2026-10-29 | Kratos Defense & Security Solutions; Unmanned systems and defense technologies | [^ktos-issuer] |
| NASDAQ:RCAT | defense-tech | | core universe | core | | | 2026-10-29 | Red Cat Holdings; Defense drone and robotic systems | [^rcat-issuer] |
| NASDAQ:MRCY | defense-tech | | core universe | core | | | 2026-10-29 | Mercury Systems; Mission-critical defense processing systems | [^mrcy-issuer] |
| NASDAQ:PLTR | defense-tech | | core universe | diversified | | | 2026-10-29 | Palantir Technologies; Selected defense software ecosystem exposure; SHLD holding | [^shld-holdings] |
| NYSE:LHX | defense-tech | | core universe | core | | | 2026-10-29 | L3Harris Technologies; Selected defense technology exposure; SHLD holding | [^shld-holdings] |
| NYSE:LMT | defense-tech | | extended candidate | core | | | 2026-10-29 | Lockheed Martin; Broader defense-prime extension; SHLD holding | [^shld-holdings] |
| NYSE:NOC | defense-tech | | extended candidate | core | | | 2026-10-29 | Northrop Grumman; Broader defense-prime extension; SHLD holding | [^shld-holdings] |
| NYSE:RTX | defense-tech | | extended candidate | diversified | | | 2026-10-29 | RTX; Broader aerospace/defense extension; SHLD holding | [^shld-holdings] |
| NYSE:GD | defense-tech | | extended candidate | core | | | 2026-10-29 | General Dynamics; Broader defense-prime extension; SHLD holding | [^shld-holdings] |
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

# Defense technology selection

The initial US-listed shortlist has six core candidates and four broader defense
extensions. Selection role is distinct from exposure: a broad prime can have
core defense exposure while remaining optional for a narrower technology peer
comparison. Palantir has both government and commercial activities; its inclusion
does not imply pure defense exposure. Classifications are provisional project
judgments, not verified revenue thresholds. Subthemes, provider symbol resolution,
and historical membership validity remain pending. Source review is not an
independent validation of predictive effects or a historical membership start.

# Electrification and grid selection

The selection has ten core candidates and two optional extensions, using the
GRID issuer snapshot dated 2026-10-28. Core/extended and exposure labels are
provisional project judgments. Selection role is separate from exposure: a core
candidate may be a diversified business. Subtheme and current provider symbol
checks remain pending; no historical membership start is inferred from review.
The source fund holds foreign listings that are excluded from this US-only subset.

# Longevity and metabolic health selection

The initial six-stock selection covers metabolic treatments, glucose monitoring,
and a metabolic liver-disease extension. It is not a list of demonstrated
lifespan-extension companies. Healthy-ageing and eldercare remain unpopulated.
Subtheme assignments are project judgments based on cited issuer descriptions;
revenue thresholds and predictive effects have not been independently validated.
Separate clinical developers, established medicines, and devices in peer studies.

# Quantum computing selection

Four initial core candidates and three diversified extensions are recorded from
issuer sources reviewed 2026-10-30. These are provisional exposure judgments,
not revenue thresholds or verified technical-performance claims. Distinguish
hardware architectures and broader technology companies in research. Company-level
subthemes remain pending. D-Wave is Nasdaq-listed following its July 2026 transfer;
Alphabet is represented once through GOOGL. Current provider symbol resolution
is required before execution; review dates do not establish historical membership.

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

[^shld-holdings]: Global X SHLD issuer mandate and holdings dated 2026-10-28, consulted 2026-10-29; supports PLTR, LHX, LMT, NOC, RTX, and GD inclusion, not the project's core/extended split.
[^avav-issuer]: AeroVironment issuer releases, including October 2026 uncrewed-system announcements; Nasdaq AVAV, consulted 2026-10-29.
[^ktos-issuer]: Kratos issuer investor relations; Nasdaq KTOS and unmanned systems, communications, and defense technologies, consulted 2026-10-29.
[^rcat-issuer]: Red Cat issuer investor relations; RCAT and defense drone/robotic systems, consulted 2026-10-29; provider symbol resolution remains pending.
[^mrcy-issuer]: Mercury Systems issuer release dated 2026-01-15; Nasdaq MRCY and defense/space processing systems, consulted 2026-10-29.

[^ondas-issuer]: Ondas issuer description; Nasdaq ONDS and autonomous drones/counter-UAS, consulted 2026-10-29.
[^umac-issuer]: Unusual Machines issuer page; drone-industry products, consulted 2026-10-29.
[^umac-listing]: SEC Form 8-K dated 2026-01-15 lists UMAC on NYSE American; current provider symbol resolution required before execution.
[^dpro-release]: Draganfly issuer release dated 2026-09-29, distributed through Nasdaq; Nasdaq DPRO and drone systems/technology, consulted 2026-10-29.

[^grid-holdings]: First Trust GRID issuer holdings dated 2026-10-28, consulted 2026-10-29; supports company/ticker inclusion, not the project's selection roles or revenue-concentration labels.

[^joby-aircraft]: Joby aircraft specifications; piloted electric air taxi; consulted 2026-10-29.
[^joby-autonomy]: Joby autonomous-flight demonstration, 2026-09-18; NYSE JOBY; consulted 2026-10-29.
[^archer-issuer]: Archer issuer release, 2026-03-02; NYSE ACHR and piloted air taxis; consulted 2026-10-29.
[^eve-issuer]: Eve issuer results, 2026-08-04; NYSE EVEX and eVTOL development; consulted 2026-10-29.
[^vertical-listing]: Vertical issuer release, 2026-10-02; NYSE EVTL, piloted aircraft, and listing notice; consulted 2026-10-29.
[^ehang-issuer]: EHang issuer Q2 2026 results; pilotless eVTOL and Nasdaq EH; consulted 2026-10-29.

[^lilly-metabolic]: Lilly issuer Q2 2026 results, NYSE LLY and metabolic medicines; consulted 2026-10-29.
[^novo-metabolic]: Novo Nordisk issuer Q2 2026 update, obesity and diabetes portfolio; consulted 2026-10-29.
[^novo-listing]: Novo Nordisk issuer NYSE NVO ADR listing; consulted 2026-10-29.
[^viking-metabolic]: Viking issuer update dated 2026-10-28, Nasdaq VKTX and clinical metabolic programs; consulted 2026-10-29.
[^structure-metabolic]: Structure issuer results dated 2026-08-06, Nasdaq GPCR and clinical obesity programs; consulted 2026-10-29.
[^dexcom-metabolic]: Dexcom issuer results dated 2026-10-29, Nasdaq DXCM and glucose monitoring; consulted 2026-10-29.
[^altimmune-metabolic]: Altimmune issuer update dated 2026-08-12, Nasdaq ALT and clinical liver-disease programs; consulted 2026-10-29.

[^ionq-issuer]: IonQ issuer quantum computing platform description; consulted 2026-10-30.
[^rigetti-issuer]: Rigetti issuer cloud quantum systems and Nasdaq RGTI listing; consulted 2026-10-30.
[^dwave-issuer]: D-Wave issuer quantum systems and services description; consulted 2026-10-30.
[^dwave-listing]: D-Wave issuer current Nasdaq QBTS listing; consulted 2026-10-30.
[^dwave-transfer]: D-Wave Q2 2026 Form 10-Q confirms Nasdaq trading began 2026-07-27; consulted 2026-10-30.
[^qubt-issuer]: Quantum Computing Inc issuer photonic systems and Nasdaq QUBT listing; consulted 2026-10-30.
[^ibm-quantum]: IBM issuer quantum systems and software platform; consulted 2026-10-30.
[^microsoft-quantum]: Microsoft Azure Quantum platform and quantum research; consulted 2026-10-30.
[^google-quantum]: Google Quantum AI hardware and software research; consulted 2026-10-30.
