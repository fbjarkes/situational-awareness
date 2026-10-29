---
type: Reference
title: Crypto and blockchain
description: US-listed companies providing crypto markets, stablecoin infrastructure, mining, and digital-asset treasury exposure.
tags: [themes, crypto, blockchain, digital-finance]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-29T23:20:57Z"
sources:
  - id: coinbase-crypto
    resource: https://investor.coinbase.com/news/news-details/2026/Coinbase-Q3-2026-Earnings-Show-All-time-high-Coinbase-One-Subscribers-and-Prediction-Markets-Surpassing-200-Million-in-Annualized-Revenue/default.aspx
    title: Coinbase issuer Q3 2026 results, crypto trading/services and Nasdaq COIN, consulted 2026-10-30
  - id: circle-crypto
    resource: https://investor.circle.com/overview/default.aspx
    title: Circle issuer stablecoins, public-blockchain services, and NYSE CRCL listing, consulted 2026-10-30
  - id: gemini-crypto
    resource: https://investors.gemini.com/news-releases/news-release-details/gemini-reports-second-quarter-2026-results
    title: Gemini issuer Q2 2026 results, crypto platform and Nasdaq GEMI, consulted 2026-10-30
  - id: mara-crypto
    resource: https://ir.mara.com/news-events/press-releases/detail/1427/mara-announces-second-quarter-2026-results
    title: MARA issuer Q2 2026 results, digital infrastructure and Nasdaq MARA, consulted 2026-10-30
  - id: riot-crypto
    resource: https://www.riotplatforms.com/
    title: Riot issuer Bitcoin mining, data centers, and Nasdaq RIOT, consulted 2026-10-30
  - id: cleanspark-crypto
    resource: https://investors.cleanspark.com/
    title: CleanSpark issuer Bitcoin/compute infrastructure and Nasdaq CLSK, consulted 2026-10-30
  - id: strategy-crypto
    resource: https://www.sec.gov/Archives/edgar/data/1050446/000119312526352145/d169243dfwp.htm
    title: Strategy issuer August 2026 investor briefing, Bitcoin treasury/software and Nasdaq MSTR, consulted 2026-10-30
  - id: robinhood-crypto
    resource: https://investors.robinhood.com/
    title: Robinhood issuer diversified brokerage/crypto platform and Nasdaq HOOD, consulted 2026-10-30
  - id: bkch-proxy
    resource: https://www.globalxetfs.com/funds/bkch/
    title: Global X BKCH blockchain mandate and holdings dated 2026-10-28, consulted 2026-10-30

theme:
  id: crypto-blockchain
  classification: structural_theme
  tracking_status: proposed
  memberships: /themes/theme-memberships.md
  subthemes:
    - id: crypto-markets
      title: Exchanges and financial platforms
    - id: crypto-stablecoins
      title: Stablecoins and blockchain payments
    - id: crypto-mining
      title: Mining and digital infrastructure
    - id: crypto-treasury
      title: Digital-asset treasury exposure
market_report:
  section: themes
  implementation_status: universe_recorded
  evidence_status: exploratory
  enabled: false
---
# Scope

Equity exposure to crypto markets, stablecoin/payment infrastructure, blockchain
services, mining-related infrastructure, and corporate digital-asset treasuries.
Only US exchange-listed stocks are eligible, including foreign issuers and ADRs;
exclude foreign-only and OTC listings. Tokens, spot-crypto ETFs, leveraged funds,
preferred shares, and warrants are outside this initial common-equity universe.

This is a narrower theme than [Digital finance](/themes/digital-finance.md), which
also covers ordinary payments and financial platforms without material crypto
exposure. Assign overlapping memberships explicitly; do not automatically copy
all digital-finance or semiconductor companies into this basket.

# Initial universe

The authoritative [shared membership table](/themes/theme-memberships.md) contains:

| Ticker | Company | Proposed segment | Role |
|---|---|---|---|
| COIN | Coinbase Global | Crypto trading and services. [^coinbase-crypto] | Core |
| CRCL | Circle Internet Group | Stablecoin/blockchain-payment infrastructure. [^circle-crypto] | Core |
| GEMI | Gemini Space Station | Crypto and financial markets platform. [^gemini-crypto] | Core |
| MARA | MARA Holdings | Digital-asset compute and infrastructure. [^mara-crypto] | Core |
| RIOT | Riot Platforms | Bitcoin mining and digital infrastructure. [^riot-crypto] | Core |
| CLSK | CleanSpark | Bitcoin/compute infrastructure with data-center diversification. [^cleanspark-crypto] | Core |
| MSTR | Strategy | Bitcoin treasury alongside other businesses. [^strategy-crypto] | Core |
| HOOD | Robinhood Markets | Broader financial platform including crypto. [^robinhood-crypto] | Extended |

Core-universe role is distinct from exposure concentration. Exposure labels and
subthemes are provisional project judgments, not verified revenue thresholds.
GEMI also offers non-crypto products; mining/compute companies can diversify into
AI/HPC data centers. Reassess business mix before treating them as pure miners.
The shortlist is not exhaustive. Current provider symbols and corporate actions
must be checked before execution; review dates do not establish historical
membership. Do not count Strategy preferred instruments as extra company members.

# Comparison and research

Compare exchanges, stablecoin businesses, miners, and treasury companies
separately as well as within the parent basket. Equity returns can differ from
token returns because of costs, financing, dilution, leverage, or operating mix.
Corporate treasury exposure is not ownership of the underlying token, and shares
of Circle are not USDC. Stablecoin-company exposure is not a price-stability claim.

BKCH is a proposed ETF comparison proxy with a global blockchain mandate and a
different constituent mix; it is not a peer-group stock.[^bkch-proxy] Record any
Bitcoin or other token comparison separately with aligned valuation times and
weekend/session treatment. No token prices are downloaded by this update.
Use [shared methodology](/themes/methodology.md) and the authoritative
[RS research checklist](/themes/themes.md#research-todos). No report output or
trading rule is enabled.

[^coinbase-crypto]: Coinbase issuer Q3 2026 results, crypto trading/services and Nasdaq COIN; consulted 2026-10-30.
[^circle-crypto]: Circle issuer stablecoins, public-blockchain services, and NYSE CRCL listing; consulted 2026-10-30.
[^gemini-crypto]: Gemini issuer Q2 2026 results, crypto platform and Nasdaq GEMI; consulted 2026-10-30.
[^mara-crypto]: MARA issuer Q2 2026 results, digital infrastructure and Nasdaq MARA; consulted 2026-10-30.
[^riot-crypto]: Riot issuer Bitcoin mining, data centers, and Nasdaq RIOT; consulted 2026-10-30.
[^cleanspark-crypto]: CleanSpark issuer Bitcoin/compute infrastructure and Nasdaq CLSK; consulted 2026-10-30.
[^strategy-crypto]: Strategy issuer August 2026 investor briefing, Bitcoin treasury/software and Nasdaq MSTR; consulted 2026-10-30.
[^robinhood-crypto]: Robinhood issuer diversified brokerage/crypto platform and Nasdaq HOOD; consulted 2026-10-30.
[^bkch-proxy]: Global X BKCH blockchain mandate and holdings dated 2026-10-28; consulted 2026-10-30.
