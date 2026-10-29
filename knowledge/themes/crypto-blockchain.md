---
type: Reference
title: Crypto and blockchain
description: US-listed crypto and blockchain companies plus separately tracked crypto-linked ETF/ETP exposures.
tags: [themes, crypto, blockchain, digital-finance]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-29T23:24:03Z"
sources:
  - id: purr-treasury
    resource: https://www.sec.gov/Archives/edgar/data/2078856/000119312526370281/purr-20260630.htm
    title: Hyperliquid Strategies fiscal 2026 Form 10-K, Nasdaq PURR and HYPE treasury/staking business, consulted 2026-10-30
  - id: bito-issuer
    resource: https://www.proshares.com/our-etfs/strategic/bito
    title: ProShares BITO strategy and fund details, consulted 2026-10-30
  - id: ethe-issuer
    resource: https://etfs.grayscale.com/ethe
    title: Grayscale Ethereum Staking ETF strategy and NYSE Arca listing, consulted 2026-10-30
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
fund_exposures:
  - ticker: BITO
    symbol: AMEX:BITO
    instrument_type: futures_etf
    underlying: bitcoin
    role: crypto_asset_exposure
    stock_peer_group: false
  - ticker: ETHE
    symbol: AMEX:ETHE
    instrument_type: spot_staking_etp
    underlying: ether
    role: crypto_asset_exposure
    stock_peer_group: false
market_report:
  section: themes
  implementation_status: universe_recorded
  evidence_status: exploratory
  enabled: false
---
# Scope

Equity exposure to crypto markets, stablecoin/payment infrastructure, blockchain
services, mining-related infrastructure, and corporate digital-asset treasuries.
Company memberships use US exchange-listed stocks, including foreign issuers
and ADRs. Separately track user-requested US-listed crypto ETF/ETP exposures
below; they are not company constituents. Exclude foreign-only/OTC listings,
tokens, leveraged funds, preferred shares, and warrants from these universes.

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
| PURR | Hyperliquid Strategies | HYPE treasury, staking, and validator activities. [^purr-treasury] | Core |
| HOOD | Robinhood Markets | Broader financial platform including crypto. [^robinhood-crypto] | Extended |

Core-universe role is distinct from exposure concentration. Exposure labels and
subthemes are provisional project judgments, not verified revenue thresholds.
GEMI also offers non-crypto products; mining/compute companies can diversify into
AI/HPC data centers. Reassess business mix before treating them as pure miners.
The shortlist is not exhaustive. Current provider symbols and corporate actions
must be checked before execution; review dates do not establish historical
membership. Do not count Strategy preferred instruments as extra company members.

PURR is common stock in Hyperliquid Strategies, not a fund or the HYPE token.
Its proposed `crypto-treasury` membership is supported by its HYPE accumulation
and staking strategy.[^purr-treasury] Compare it with treasury companies separately
from exchanges and miners; token concentration, financing, dilution, and staking
operations can cause its equity returns to diverge from HYPE returns. Do not
splice legacy Sonnet biotech price history into a crypto-treasury study without
disclosing the business transition. Review date is not a membership start date.

# Crypto asset ETF/ETP exposures

The separate [fund table](/themes/theme-memberships.md#crypto-fund-exposures)
records BITO and ETHE, reviewed 2026-10-30:

| Ticker | Product | Underlying exposure | Structure |
|---|---|---|---|
| BITO | ProShares Bitcoin ETF | Bitcoin-linked | Futures and swaps; no direct bitcoin holdings. [^bito-issuer] |
| ETHE | Grayscale Ethereum Staking ETF | Ether | Spot Ether holdings with staking. [^ethe-issuer] |

Both are crypto-linked products, but BITO is not a spot-bitcoin fund. ETHE is
an ETP branded as an ETF; its structure differs from BITO's registered fund.
Do not combine fund rows with company rows for equal-weight stock breadth or
stock-versus-peer RS. Compare their returns as explicitly selected asset-exposure
series instead. BKCH remains a blockchain-equity proxy, distinct from these funds.
Provider-qualified symbols require resolution before execution.

For research, record expenses, distributions, futures roll/basis effects, staking,
and NAV premium/discount treatment. Use a consistent total-return policy;
unadjusted closing prices can misrepresent performance around distributions.
ETHE's earlier OTC period and 2024 ETP transition require separate historical
regime treatment.[^ethe-issuer] Review dates do not establish historical membership.

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

[^bito-issuer]: ProShares BITO issuer page, consulted 2026-10-30; futures/swaps exposure without direct bitcoin holdings and monthly distributions where applicable.
[^ethe-issuer]: Grayscale ETHE issuer page, consulted 2026-10-30; Ether holdings, staking, NYSE Arca listing, and historical OTC-to-ETP transition.

[^purr-treasury]: Hyperliquid Strategies fiscal-year 2026 Form 10-K; Nasdaq PURR common stock, HYPE accumulation, staking, and validator activities; consulted 2026-10-30.
