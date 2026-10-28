# Knowledge update log

## 2026-10-28

- Added the themes registry and shared ticker-universe manifest, linking the existing dated GDX holdings without duplicating them; recorded within-theme RS-high research and a proposed reusable utility.
- Added an open SPY research plan for forward returns when at least 50% of S&P 500 constituents make new 20-day highs, with proposed event definitions, horizons, baseline, overlap, drawdowns, and membership biases.

## 2026-10-26

- Added the sourced VIX concept, reusable closing-low span utility, and VIX metrics in the S&P 500 report section.

- Added the SPY report card (distance from 200/50-day SMA, consecutive days above/below the 50-day SMA, consecutive down days) and price_stats.py helpers; recorded metric definitions and three SPY Research TODOs.
- Added the index folder with a SPY concept and a separate SPY holdings list: 503 listed securities as of 2026-10-22, retrieved 2026-10-26 from the issuer's daily holdings file.
- Added Alpaca as an alternative daily-bar provider and the data-providers reference covering symbol availability, substitution labelling, feed, and adjustment treatment.
- Recorded per-provider availability for MMOH and MMOF: TradingView-only; Alpaca lookups returned not found.
- Documented that Alpaca GDX breadth covers at most 32 of 59 constituents (US listings) and is not comparable with the TradingView full-universe series.

## 2026-10-25

- Added OKF/TODO authoring conventions to AGENTS.md and a GDX constituent breadth event-study research checklist.
- Standardized raw bar storage under data/research/day/<download-date>/<symbol>.json and updated breadth/report utilities to read dated per-symbol files.
- Added the GDX 50-day breadth report section and downloaded all 59 constituent histories; normalized exchange session dates and retained coverage and fixed-universe labels.
- Renamed the custom breadth methodology reference to gdx-breadth.md and updated its links.
- Added the reusable custom SMA breadth helper, snapshot contract, availability policy, and fixed-current-GDX-universe limitations.
- Added the complete displayed GDX holdings table, dated 2026-10-22, with list update date 2026-10-25, weights, cash rows, and issuer provenance.
- Added a US GDX concept under sectors with issuer-sourced definition, dated exposure context, proposed comparison questions, and explicit evidence gaps.
- Added index-specific crossing-study findings to MMOH and MMOF, with sample sizes, below-20 outcomes, threshold comparisons, and evidence limitations.
- Added a reproducible individual-index breadth crossing study at 30/25/20, with SPY forward returns over 10/20/30/50/100/200 sessions; retained the combined rule as disabled.
- Updated MMOH/MMOF from TradingView symbol labels: 100-day and 150-day averages respectively; added sources, percentage units, interpretation, and unresolved methodology details.
- Created the OKF v0.2 knowledge bundle from the official specification.
- Added MMOH/MMOF references with definitions explicitly awaiting verification.
- Recorded the below-20 hypothesis as unvalidated and disabled for report selection.
- Documented the proposed sector RS calculation and report section template.
