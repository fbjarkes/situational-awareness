# Knowledge update log

## 2026-10-30

- Added descriptive theme relative-strength rankings versus SPY over 5/10 sessions and 1/3/6/12 months, using archived same-batch price ratios; research signals remain unvalidated.

- Added the report theme-return table using deduplicated core universes and daily-rebalanced equal-weight price returns over 1W/1M/3M/6M/12M; documented strict coverage, one-batch provenance, US-only gold miners, and ticker-identity cutoffs. Corrected Centrus Energy to TradingView symbol NYSE:LEU.
- Added separate AI neocloud and hyperscaler/platform categories; populated NBIS, CRWV, and IREN with issuer evidence, direct-supplier roles, and dated IREN mining-to-cloud transition context, keeping other AI segments unpopulated.

- Added the Semiconductors parent theme, seven product subthemes, and 18 US-listed candidates; introduced separate security profiles for business models, ecosystem roles, and end markets, with explicit chipmaker/ecosystem RS scopes, overlapping tags, and insufficient-peer handling.

- Populated Space and Satellites with VSAT, SPCX, RKLB, ASTS, IRDM, PL, RDW, and LUNR; recorded issuer sources, dated reviews, subthemes, SPCX ticker-reuse history, and the pending Rocket Lab/Iridium transaction.

- Added Nasdaq PURR (Hyperliquid Strategies) as a Crypto treasury company with HYPE/staking exposure, distinct from ETF exposures; recorded fiscal 2026 filing evidence and legacy-business history limitations.

- Added BITO and ETHE as separately tracked Crypto fund exposures; distinguished Bitcoin futures/swaps from spot/staked Ether, excluded funds from company breadth/peer groups, and documented historical structure and total-return treatment.

- Added Crypto and Blockchain with COIN, CRCL, GEMI, MARA, RIOT, CLSK, and MSTR core candidates plus HOOD as an extension; recorded issuer sources, dated reviews, distinct business segments, BKCH proxy, and Digital Finance overlap.

- Populated Healthcare Technology and Innovation with TEM, GH, NTRA, RXRX, and SDGR as core candidates plus HIMS, ISRG, and DXCM extensions; recorded issuer evidence, peer subthemes, review dates, and Robotics/Metabolic Health overlaps.

- Populated Clean Energy using the existing renewables concept/ID and added a separate Batteries theme, with US-listed universes (8 and 7 names), dated issuer evidence, separate proxies, and explicit generation/storage/mobility boundaries.

- Added IONQ, RGTI, QBTS, and QUBT as initial quantum core candidates, with IBM, MSFT, and GOOGL as diversified extensions; recorded issuer sources, review dates, D-Wave Nasdaq transfer, Alphabet share-class deduplication, and technical-evidence limitations.

## 2026-10-29

- Added LLY, NVO, VKTX, GPCR, and DXCM as metabolic-health core candidates and ALT as a liver-disease extension, with issuer sources, dated reviews, new monitoring/liver subthemes, and explicit longevity evidence gaps.

- Added JOBY as an extended Drones autonomous-aviation member and populated Future Mobility with JOBY, ACHR, EVEX, EVTL, and EH; separated piloted eVTOL from autonomy, recorded issuer evidence and listing caveats, and documented JOBY deduplication.

- Added ten US-listed Electrification and Grid core candidates and two broader extensions from GRID holdings dated 2026-10-28, with review dates, provisional classifications, and GRID as a proposed proxy.

- Added the Drones theme with six US-listed candidates (AVAV, KTOS, RCAT, ONDS, UMAC, DPRO), issuer sources, dated reviews, provisional classifications, and explicit Defense Technology overlap.

- Added six US-listed Defense Technology core candidates and four broader defense extensions, with issuer/SHLD sources, review dates, provisional classifications, and SHLD as a proposed proxy.

- Restricted theme universes to US exchange listings; replaced foreign-only robotics listings with TER, ROK, and SYM, and required a US-only filter on legacy GDX holdings.

- Added eight core robotics/automation candidates and two ecosystem extensions, with BOTZ and separately dated BOTZ UCITS evidence, provisional labels, local listings, and BOTZ as a proposed proxy.
- Populated nuclear energy with 10 core stocks and two optional generation extensions from NLR holdings dated 2026-10-28; recorded source/review dates, provisional classifications, pending subthemes, and NLR as a proposed proxy.
- Populated cybersecurity memberships with 12 core stocks and three optional extended candidates, sourced to CIBR holdings dated 2026-10-28; recorded review dates, provisional exposure labels, pending subthemes, and BUG as a proposed ETF proxy.

## 2026-10-28

- Expanded themes into 16 proposed concepts with subthemes, a machine-readable registry, shared memberships, and methodology; retained active GDX holdings by reference and deprecated the old ticker manifest.

- Recorded user-suggested 5- and 10-session theme RS calculation periods, distinguishing rolling relative returns from RS-level new-high lookbacks.
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
