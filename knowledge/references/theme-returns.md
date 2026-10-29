---
type: Metric
title: Theme return table
description: Report methodology for core-constituent equal-weight theme price returns over one week and one, three, six, and twelve months.
tags: [themes, returns, report, methodology]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-29T23:54:52Z"
sources:
  - id: theme-members
    resource: /themes/theme-memberships.md
    title: Current theme memberships and separately tracked funds
  - id: shared-method
    resource: /themes/methodology.md
    title: Equal-weight peer-index and membership conventions
  - id: space-history
    resource: /themes/space-economy.md
    title: SpaceX issuer/ticker history boundary
  - id: crypto-history
    resource: /themes/crypto-blockchain.md
    title: PURR issuer/business transition and crypto fund separation
market_report:
  section: themes
  implementation_status: metrics_available
  evidence_status: descriptive
  enabled: false
  report_metrics: [1W, 1M, 3M, 6M, 12M]
---
# Universe

Read registry themes and core-universe stock rows from the shared membership
table; deduplicate by security within each theme and exclude optional extensions
and fund exposures.[^theme-members] Empty themes remain visible as unavailable.
Gold miners uses its dated holdings and explicit local symbol map filtered to
US exchange listings. That US-only return basket differs from the existing
full international GDX breadth chart. A missing map makes the return universe
unavailable, not an invitation to assume issuer labels are provider symbols.

# Calculation

Construct an equal-weight index rebalanced each reference session:
`index_t = index_previous * mean(close_i_t / close_i_previous)`.
Period return is `100 * (index_end / index_start - 1)`.[^shared-method]
This is not the arithmetic average of buy-and-hold constituent period returns.
Use USD split-adjusted price bars from a single provider, excluding dividends.
No trading costs or execution slippage are included.

1W is five SPY trading-session intervals. Month horizons use calendar-month
anniversaries of the common observation date and the last reference session
on or before each anniversary. Use SPY only as the US session calendar, not
as the return benchmark. Every constituent must have every required session;
do not forward-fill or shrink the basket. An unavailable cell is not zero.
Coverage counts stocks with an endpoint close and does not certify the full
horizon. Same-day bars are provisional when the reference was fetched before
the US regular close.

# Identity and reproducibility

Do not use legacy SPCX history before SpaceX's 2026-06-12 listing.[^space-history]
Exclude PURR history before its 2025-12-03 trading start as the new treasury
issuer.[^crypto-history] Apply such identity boundaries even if providers return
longer ticker histories. New listings can prevent a full-basket 6M/12M return.

Pin one download date and provider for the entire table. Record current symbol
lists, observation/start dates, source paths and hashes, fetch times, price
adjustment, knowledge hashes, and missing-data reasons in report JSON.
Current fixed universes create survivorship and selection bias; this table
describes current baskets and is not historical point-in-time theme performance.
Themes overlap, so their returns are correlated. Descriptive rankings do not
validate the separate RS research plan or a trading signal.

[^theme-members]: Authoritative project stock-to-theme relationships; fund exposures are maintained separately.
[^shared-method]: Project daily-rebalanced equal-weight index convention; implemented for descriptive price returns.
[^space-history]: Sourced SPCX issuer identity and prior ticker reuse warning.
[^crypto-history]: Sourced Hyperliquid Strategies trading start and legacy Sonnet transition.
