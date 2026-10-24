---
type: Research Result
title: Breadth downward-crossing event study
description: Exploratory SPY forward price returns after individual MMOH and MMOF threshold crossings.
status: draft
tags: [breadth, SPY, event-study]
generated:
  by: process:breadth-study
sources:
  - id: tradingview-data
    resource: https://www.tradingview.com/
    title: TradingView daily OHLCV downloads through the connected MCP tool
market_report:
  evidence_status: exploratory
  enabled: false
---
# Breadth threshold event study

Shared observation period: 2002-01-02 to 2026-10-23.

SPY forward price returns, in percent. Horizons count SPY trading sessions.

Crossing: previous available indicator close >= threshold and current close < threshold.
Each indicator is tested separately; this does not test both-below or either-below combinations.
Entry is the signal-session SPY close; no next-session execution or transaction costs are modeled.
Prices are split-adjusted, not dividend-adjusted. This is a descriptive event study, not an executable strategy backtest.

Each cell below is mean return / median return / positive-return frequency (N mature events).

## MMOH

| Threshold | 10 days | 20 days | 30 days | 50 days | 100 days | 200 days |
|---|---|---|---|---|---|---|
| Below 30 | -1.63% / -0.71% / 41% (N=70) | -1.84% / -0.95% / 41% (N=70) | -1.01% / -0.26% / 47% (N=70) | -0.87% / 2.80% / 60% (N=70) | -0.01% / -0.61% / 50% (N=70) | 3.60% / 8.12% / 63% (N=70) |
| Below 25 | 0.91% / 1.84% / 63% (N=52) | 0.62% / 2.58% / 65% (N=52) | 1.22% / 1.30% / 58% (N=52) | 2.26% / 5.14% / 69% (N=52) | 1.94% / 2.70% / 56% (N=52) | 3.93% / 10.27% / 65% (N=52) |
| Below 20 | -0.35% / 1.72% / 62% (N=32) | 0.97% / 2.59% / 62% (N=32) | 3.17% / 4.60% / 78% (N=32) | 4.68% / 6.46% / 84% (N=32) | 5.11% / 7.01% / 72% (N=32) | 10.21% / 11.24% / 78% (N=32) |
| Unconditional mean | 0.36% | 0.72% | 1.08% | 1.80% | 3.65% | 7.74% |

## MMOF

| Threshold | 10 days | 20 days | 30 days | 50 days | 100 days | 200 days |
|---|---|---|---|---|---|---|
| Below 30 | -0.92% / -0.28% / 44% (N=79) | -0.47% / 0.99% / 56% (N=79) | -0.28% / 0.89% / 57% (N=79) | 0.14% / 2.77% / 58% (N=79) | 0.19% / 0.53% / 51% (N=79) | 2.33% / 7.27% / 59% (N=79) |
| Below 25 | -0.40% / 0.63% / 55% (N=65) | -0.08% / 2.37% / 63% (N=65) | 1.00% / 2.66% / 68% (N=65) | 1.74% / 4.73% / 71% (N=65) | 1.67% / 4.43% / 60% (N=65) | 6.73% / 10.48% / 71% (N=65) |
| Below 20 | 1.04% / 1.76% / 72% (N=40) | 1.88% / 2.49% / 62% (N=40) | 3.30% / 4.14% / 75% (N=40) | 5.19% / 6.84% / 78% (N=40) | 4.41% / 4.83% / 72% (N=40) | 8.73% / 10.43% / 75% (N=40) |
| Unconditional mean | 0.36% | 0.72% | 1.08% | 1.80% | 3.65% | 7.74% |

## Limitations

- Recent signals without a complete forward horizon are excluded separately for each horizon; counts therefore differ.
- Crossings use adjacent available indicator observations; missing sessions are not reconstructed.
- Every recrossing counts. Return windows can overlap and events cluster within market declines; samples are not independent.
- The unconditional baseline uses all available common starting dates, with the same maturity requirement per horizon.
- The baseline is descriptive, without regime matching, significance testing, or multiple-testing correction.
- Worst/best returns in CSV are terminal horizon returns, not maximum interim drawdowns.
- Provider history may contain revisions or constituent changes. Input hashes identify the downloaded snapshot.
- Neither threshold rarity nor a robust buying rule is established by this simple study.

# Reproduction and snapshot provenance

Run `uv run breadth-study.py` from the repository root. Inputs are local
`data/research/AMEX-SPY.json`, `INDEX-MMOH.json`, and `INDEX-MMOF.json`;
raw downloads and generated CSVs are ignored by Git.
Data source: TradingView daily bars.[^tradingview-data]

```json
{
  "provider": "tradingview",
  "generated_at": "2026-10-24T22:32:52.715642+00:00",
  "inputs": {
    "AMEX-SPY": {
      "file": "AMEX-SPY.json",
      "sha256": "c40ba58bc69733e5bd08a2c9ca8127ade30e52ffa61c17d0a9fdd83db6d5aa97",
      "fetched_at": "2026-10-24T22:31:47.107Z"
    },
    "INDEX-MMOH": {
      "file": "INDEX-MMOH.json",
      "sha256": "8afdc782e882c1245acc20c12e49752a04ac4c8b4dfa51cc25c13ee1597e7d05",
      "fetched_at": "2026-10-24T22:31:51.421Z"
    },
    "INDEX-MMOF": {
      "file": "INDEX-MMOF.json",
      "sha256": "d6b2c7696d1a7b02edaf62aac0bc44fb76c79d84bbb73f270b37bb86f5287523",
      "fetched_at": "2026-10-24T22:32:02.096Z"
    }
  }
}
```

[^tradingview-data]: TradingView MCP get_ohlcv, daily split-adjusted bars through 2026-10-23.
