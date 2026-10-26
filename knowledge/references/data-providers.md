---
type: Reference
title: Market data providers and symbol availability
description: Which report series TradingView and Alpaca can supply, how unavailable series are handled, and provider-specific data treatment.
tags: [data, providers, alpaca, tradingview, methodology]
status: draft
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-10-26T12:00:00Z"
market_report:
  providers: [tradingview, alpaca]
  default_provider: snapshot
  substitution_policy: label_and_keep_original_provider
  implementation_status: report_and_custom_breadth
sources:
  - id: alpaca-asset-lookup
    resource: Alpaca MCP get_asset and get_stock_bars, consulted 2026-10-26
    title: Alpaca asset lookups for MMOH, MMOF, and NEM; SPY daily bars
  - id: alpaca-bars-api
    resource: https://docs.alpaca.markets/reference/stockbars
    title: Alpaca Market Data historical stock bars endpoint
  - id: gdx-holdings
    resource: /sectors/gdx.md
    title: GDX holdings snapshot dated 2026-10-22
---
# Providers

| Provider | Symbols | Coverage | Credentials |
|---|---|---|---|
| TradingView | Exchange-qualified, e.g. `NYSE:NEM`, `INDEX:MMOH` | Global listings and TradingView-calculated indices | `TRADINGVIEW_MCP_TOKEN` |
| Alpaca | Plain US tickers, e.g. `NEM` | US-listed stocks and ETFs | `APCA_API_KEY_ID`, `APCA_API_SECRET_KEY` |

Because the symbol formats differ, both providers' files can share a
download-date folder without colliding. Reads choose a provider explicitly;
a batch never combines providers, feeds, or adjustment settings.

# Confirmed availability

- `INDEX:MMOH` and `INDEX:MMOF` are TradingView-only. Alpaca asset lookups for
  `MMOH` and `MMOF` returned "asset not found" on 2026-10-26.[^alpaca-asset-lookup]
- `NEM` resolved to the NYSE-listed Newmont asset, and SPY daily bars were
  returned, timestamped at 04:00 UTC (New York midnight).[^alpaca-asset-lookup]

# GDX constituents

Of the 59 GDX security rows, 27 carry a non-US market suffix
(AU, CN, LN, HK, IJ, MM) and have no Alpaca listing. The remaining 32 have
plain labels and are treated as US listings; each has not been individually
verified on Alpaca.[^gdx-holdings] An Alpaca GDX breadth series therefore covers
at most 32/59 (54%) of the fixed universe, below the report's 0.8 minimum
coverage, so its percentages are suppressed unless that cutoff is lowered.
Even then, it is a US-listed subset that is not comparable with the
TradingView full-universe series. Do not combine the two into one history.

# Report behavior

- SPY is available from both providers. Stored runs and `--provider tradingview`
  use `AMEX:SPY`; `--provider alpaca` downloads `SPY` from Alpaca (about three
  years of daily history) and labels the feed on the card.
- `--provider alpaca` reads TradingView-only breadth series from the latest
  complete stored TradingView batch (or `--download-date`) and labels each one
  in a visible "Provider limitations" panel and on the section. JSON records
  the substitution in `provider_coverage`.
- With no stored TradingView batch, the breadth section renders as
  unavailable instead of failing the report.
- A GDX snapshot built from Alpaca lists the constituents it could not supply
  in `universe.provider_unavailable`. The report shows how many were missing.
- Failed downloads still fail the run; they never fall back to another provider.

Per-series availability for MMOH/MMOF is recorded in each concept's
`market_report.data_providers` field, which the report reads.

# Data treatment

Alpaca bars are requested with `adjustment=split` by default so SMAs are
not distorted by splits. The repository has not recorded TradingView's
adjustment policy for MCP downloads, so Alpaca and TradingView closes are
not assumed to be equivalent.
The free `iex` feed reports IEX trades only, so its close and volume can
differ from the consolidated close. Use `--alpaca-feed sip` for research
that compares with TradingView or official closes.[^alpaca-bars-api]
Feed and adjustment are stored with every file and in derived snapshots.

# TODOs

- [ ] Verify each plain-label GDX constituent on Alpaca before relying on Alpaca GDX breadth.
  - Record any plain label that Alpaca does not resolve, or resolves to a different issuer.
- [ ] Compare Alpaca `sip` and `iex` closes with TradingView for a sample of shared symbols.
  - Report the date range, symbols, and largest close differences.

[^alpaca-asset-lookup]: Lookups through the connected Alpaca MCP tool in chat, 2026-10-26.
[^alpaca-bars-api]: Alpaca's documented `feed` and `adjustment` parameters for historical stock bars.
[^gdx-holdings]: Issuer ticker labels in the GDX holdings snapshot dated 2026-10-22; classification by label suffix.
