---
type: Reference
title: Quantum computing
description: Companies developing quantum computation and its enabling technologies.
tags: [themes, quantum]
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
  - id: provider-framework
    resource: https://www.msci.com/our-solutions/indexes/thematic-investing/themes-and-sub-themes
    title: Provider thematic classification framework
  - id: project-taxonomy
    resource: /themes/themes.md
    title: Project theme registry and proposed taxonomy
theme:
  id: quantum
  classification: structural_theme
  tracking_status: proposed
  memberships: /themes/theme-memberships.md
  subthemes:
    - id: quantum-quantum-hardware
      title: Quantum hardware
    - id: quantum-enabling-components
      title: Enabling components
    - id: quantum-quantum-software
      title: Quantum software
    - id: quantum-quantum-safe-security
      title: Quantum-safe security
---
# Scope

Companies developing quantum computation and its enabling technologies. This is a proposed project universe, not an industry classification
or a claim of current market leadership.

# Classification and subthemes

Provider frameworks support the broad thematic approach.[^provider-framework]
The names, boundaries, and subdivisions below are the project's first-draft
synthesis, not a provider's official membership rules.[^project-taxonomy]

- Quantum hardware
- Enabling components
- Quantum software
- Quantum-safe security

# Membership criteria

Require documented products, services, revenue, or investment exposure relevant
to the scope. Marketing references alone do not establish membership. Record
exposure as core, diversified, or indirect, supported by a source and rationale.
Membership can overlap other themes and subthemes.

The [shared membership table](/themes/theme-memberships.md) records four initial
core candidates and three diversified extensions:

| US ticker | Company | Basis for inclusion | Role |
|---|---|---|---|
| IONQ | IonQ | Quantum computing and associated platform technologies. [^ionq-issuer] | Core |
| RGTI | Rigetti Computing | Quantum processors and cloud-accessible systems. [^rigetti-issuer] | Core |
| QBTS | D-Wave Quantum | Quantum systems, software, and services. [^dwave-issuer] | Core |
| QUBT | Quantum Computing Inc. | Photonic quantum systems and related technologies. [^qubt-issuer] | Core |
| IBM | IBM | Quantum hardware, cloud access, and Qiskit software. [^ibm-quantum] | Extended |
| MSFT | Microsoft | Azure Quantum and quantum research. [^microsoft-quantum] | Extended |
| GOOGL | Alphabet Class A | Google Quantum AI hardware and software research. [^google-quantum] | Extended |

Only US exchange-listed stocks are eligible. Use GOOGL as the selected Alphabet
share class; do not also count GOOG as a second company. Core versus extended
and exposure labels are provisional project choices, not verified revenue
thresholds. The shared table is authoritative for symbols, dates, and roles.
D-Wave transferred from NYSE to Nasdaq, with Nasdaq trading beginning
2026-07-27; use `NASDAQ:QBTS`, not a stale NYSE mapping.[^dwave-listing][^dwave-transfer]
Review dates do not establish historical membership. Current provider symbols
and corporate actions must be checked before research.

# Research distinctions

This is an initial shortlist, not an exhaustive list. Distinguish dedicated
quantum businesses from diversified groups whose quantum activities may be a
small part of the business. Hardware architectures, annealing, gate-model systems,
photonic technologies, software, and quantum-safe security are not interchangeable
peer groups. Company-specific subthemes remain pending review. Issuer technology
claims establish proposed exposure, not independent proof of quantum advantage,
commercial scalability, profitability, or future equity returns.
No dedicated ETF proxy is selected and no report signal is enabled.

# Interpretation and research

Use [shared methodology](/themes/methodology.md) for weighting, calendars,
coverage, and RS. Compare a stock with its narrow peers and its parent theme
separately; this concept enables no trading rule.

The authoritative [within-theme RS research checklist](/themes/themes.md#research-todos)
is maintained once in the registry.

[^provider-framework]: Provider framework consulted during project taxonomy research on 2026-10-28; supports broad categories, not every proposed subdivision.
[^project-taxonomy]: User-approved first-draft organization, 2026-10-28; membership and predictive effects remain unvalidated.

[^ionq-issuer]: IonQ issuer quantum computing platform description; consulted 2026-10-30.
[^rigetti-issuer]: Rigetti issuer cloud quantum systems and Nasdaq RGTI listing; consulted 2026-10-30.
[^dwave-issuer]: D-Wave issuer quantum systems and services description; consulted 2026-10-30.
[^dwave-listing]: D-Wave issuer current Nasdaq QBTS listing; consulted 2026-10-30.
[^dwave-transfer]: D-Wave Q2 2026 Form 10-Q confirms Nasdaq trading began 2026-07-27; consulted 2026-10-30.
[^qubt-issuer]: Quantum Computing Inc issuer photonic systems and Nasdaq QUBT listing; consulted 2026-10-30.
[^ibm-quantum]: IBM issuer quantum systems and software platform; consulted 2026-10-30.
[^microsoft-quantum]: Microsoft Azure Quantum platform and quantum research; consulted 2026-10-30.
[^google-quantum]: Google Quantum AI hardware and software research; consulted 2026-10-30.
