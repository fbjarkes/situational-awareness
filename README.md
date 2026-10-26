# Daily market situational awareness

Python + uv proof of concept, starting with TradingView `INDEX:MMOH` and
`INDEX:MMOF`. Generates a standalone HTML report with an embedded SVG chart,
a JSON report containing the plotted observations and metadata, and a terminal
summary. No browser assets or external chart service are required.

## Report section template

The HTML briefing opens on an overview with cards for Market Breadth,
S&P 500, and Themes. Select a card or menu item to open just that section;
All sections returns to the overview. URLs support direct section links,
and browser Back/Forward preserves navigation. GDX lives under Gold miners.
Unimplemented coverage is labeled Planned. On mobile the navigator becomes
a compact top menu and charts use a narrower layout with readable axis labels.

The header shows source-symbol counts, symbols downloaded during this run,
GDX coverage, data-warning counts, and the selected download batch. Stored-data
runs show zero downloads; historical symbol coverage is not counted as a new download.
It also lists open research TODOs from the knowledge bundle as one-sentence
bullets. Completed checkboxes, ordinary TODO sections, and code examples are
excluded; source paths and line numbers are archived in the report JSON.

Each breadth chart uses a fixed 0–100% scale. Observation dates and changes
sit beside the readings; routine availability notes and methodology are
expandable, while data-quality warnings remain visible. The report is a
self-contained HTML file and includes print and reduced-motion styles.

Each datapoint has a heading, one simple chart or table, and a one- or
two-sentence interpretation. Breadth uses one shared MMOH/MMOF line chart;
latest values appear in its legend. Technical provenance stays in JSON.
Material data-quality warnings remain visible in the report.

The S&P 500 section shows an SPY card with distance from the 200- and 50-day
SMAs, consecutive days above or below the 50-day SMA, and consecutive down
days. It reads `AMEX:SPY` from the bar store (or downloads it with a live
provider); without stored SPY history the card says it is unavailable.
Helpers live in `price_stats.py`. Readings are descriptive; the related
studies are Research TODOs in `knowledge/index/spy.md`.

Next planned section: SPDR sector analysis, using a sector table with RS-1,
RS-3, and RS-6 columns for 1-, 3-, and 6-month relative returns. Proposed
calculation: sector ETF return minus SPY return, expressed in percentage
points, with matched observation dates and a consistent adjustment policy.
Positive values indicate outperformance. The sector section is not yet
implemented.

GDX breadth is included when `data/gdx-breadth-sma50.json` exists. It uses
the current holdings snapshot, with a six-month chart of the percentage above
the 50-day SMA, latest coverage, and a two-sentence participation summary.
Override its snapshot with `--gdx-breadth PATH`. Both sections use the report's
date cutoff and lookback. Constituent prices are not refreshed by the daily
report; regenerate the custom snapshot when refreshing.

## Knowledge library

The version-controlled [knowledge bundle](knowledge/index.md) follows the
[official OKF v0.2 specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md).
It contains indicator references, an explicitly unvalidated breadth hypothesis,
and the proposed sector RS methodology. Concept metadata uses YAML frontmatter;
explanations and evidence live in Markdown. The `market_report` extension is
project-specific. The report reads breadth definitions and crossing thresholds
for interpretation and records the knowledge content and hashes in JSON.

## Run

From this directory:

```powershell
uv run market-report.py --date 2026-10-23
uv run market-report.py daily --lookback 3 --format html,json
uv run market-report.py --help
```

uv creates and maintains `.venv` using `pyproject.toml` and `uv.lock`.
Outputs go to `reports/market-report-YYYY-MM-DD.html` and `.json`.
Use `--output PATH` to change the destination. Rerunning a date replaces that
date's outputs. `--lookback` is an integer number of calendar months (default 6).

The default `--provider snapshot` reads MMOH/MMOF from the latest complete
batch in the per-symbol bar store. It does not fetch new readings.
Use `--download-date 2026-10-25` to pin the batch, or `--snapshot PATH` for a
legacy combined snapshot. Raw data is ignored by Git and must be fetched or
supplied on a new checkout.

## Downloaded bar storage

All new raw downloads use `data/research/day/<download-date>/<symbol>.json`.
Download dates use Stockholm time, independently of the sessions covered.
For example: `data/research/day/2026-10-25/NYSE%3ANEM.json`. The symbol is
percent-encoded so exchange qualifiers and special characters remain safe
on Windows without filename collisions.

Each file contains one symbol's daily history with provider, fetch timestamp,
timeframe, and retrieval ranges. Same-day downloads merge by timestamp,
retaining longer history and the newer retrieved values. `bar_store.py`
provides `save_bars` and `load_bars` for every utility to reuse.
Default reads select the latest batch containing every requested symbol;
they never silently combine different download dates. An explicit incomplete
`--download-date` fails. `--data-root PATH` selects another store root.
The current implementation supports the `day` timeframe.

Existing combined downloads were copied into the dated store while retaining
their original fetch timestamps. Legacy originals are kept locally for recovery.
Derived breadth snapshots and symbol maps remain outside the raw bar store.

## Live TradingView provider

```powershell
$env:TRADINGVIEW_MCP_TOKEN = '<your independently provisioned bearer token>'
uv run market-report.py --provider tradingview --refresh
```

The default Streamable HTTP endpoint is `https://mcp.tradingview.com/mcp`, as
configured locally. Override it with `--mcp-url` or `TRADINGVIEW_MCP_URL`.
The endpoint must expose a single tool whose name ends with `get_ohlcv` and
which accepts TradingView's OHLCV arguments.

**Authentication is required:** an unauthenticated initialization request to
this endpoint returned HTTP 401 during verification. The chat connection's
credentials are not exported or reused by this script. The PoC accepts a
bearer token through `TRADINGVIEW_MCP_TOKEN`; obtaining/renewing a standalone
token or implementing an OAuth flow remains an integration step. Consequently,
the live provider has not been verified end to end against authenticated
TradingView. Snapshot generation is fully runnable and tested.

Live responses are archived in the bar store; `.cache/` holds only batch
pointers keyed by requested date and lookback, not another copy of bar data.
Use `--refresh` in scheduled jobs to ensure a fresh request each run. Failed
requests return a nonzero exit status; they never silently fall back to the
local snapshot. Tokens and endpoint URLs are excluded from report metadata.
The provider fetches a little extra history for five-session comparisons.
It rejects truncated responses instead of silently reporting partial history.

## Alpaca provider

Alpaca is an alternative source for US-listed stocks and ETFs. Set
`APCA_API_KEY_ID` and `APCA_API_SECRET_KEY` (optionally `APCA_DATA_URL`).
Downloads use the bar store with plain tickers (`NEM`, not `NYSE:NEM`)
and record the feed and price adjustment.

```powershell
uv run market-report.py --provider alpaca
uv run custom-breadth.py --holdings-md knowledge/sectors/gdx.md --symbol-map data/gdx-symbol-map.json --alpaca --alpaca-feed sip --ma 50 --output data/gdx-breadth-sma50-alpaca.json
```

With `--provider alpaca`, the report downloads SPY from Alpaca for the S&P 500
card (`--alpaca-feed iex|sip`, default `iex`); credentials are then required.

**Limitations.** MMOH and MMOF are TradingView-only indices. With
`--provider alpaca` the report reads them from the latest stored TradingView
batch and shows a "Provider limitations" panel plus a source label on the
section; with no stored batch the section is shown as unavailable. Alpaca has
no foreign listings, so GDX breadth from Alpaca covers at most 32 of 59
constituents; the missing ones are listed in the snapshot and the report.
The free `iex` feed's close is IEX-only; use `--alpaca-feed sip` for research.
Use `--provider alpaca` with stored reads of `custom-breadth.py` to select
Alpaca files. See the [data providers reference](knowledge/references/data-providers.md).

## Dates and interpretation

- `--date YYYY-MM-DD` means observations at or before that date. Default:
  today's date in Stockholm; the latest available prior observation is shown.
- Today's bar is included when the provider has one, so a run during the last
  hour of trading reports current values. A bar dated on the fetch day and
  fetched before 16:00 ET is labelled `intraday HH:MM ET`; changes then compare
  it with the previous close. Use `--close-only` to report previous closes only.
  No exchange holiday/session calendar is used.
- Indicators may come from different dates, e.g. yesterday's MMOF close next to
  today's intraday reading for another series. That is allowed: every value
  shows its own `as of` label, and the report adds a note saying which reading
  is from when. Missing history and observations more than three calendar days
  old are flagged as warnings.
- Live runs for today always fetch fresh data; the cache only serves past dates.
  Whether TradingView updates a given breadth index during the session is not
  yet verified. If it only updates after the close, today's run shows the
  previous close and labels it as such.
- Daily and five-session changes are absolute index-point differences from
  the preceding available observations, not percentage changes.
- Historical reports filter today's available data by observation date;
  they cannot recreate old provider revisions or past publication timestamps.
- The chart uses a shared, automatically fitted scale. Definitions, units,
  interpretation thresholds, and a neutral 50 line are deliberately pending
  verification; the narrative currently describes direction only.

## Scheduling

Once standalone authentication works, the CLI is suitable for a scheduler.
No scheduled task is installed by this PoC.

Windows Task Scheduler example (daily at 07:00 Stockholm local time):

- Program: full path returned by `Get-Command uv`.
- Arguments: `run --project "C:\projects\situational-awareness" "C:\projects\situational-awareness\market-report.py" --provider tradingview --refresh`
- Start in: `C:\projects\situational-awareness` (replace with your checkout path).
- Configure authentication in the scheduler account's environment. Do not put
  the token in command arguments. Capture failures with your scheduler's logs.

Equivalent cron example on a machine whose scheduler timezone is Stockholm
(replace the paths; provision the token in the execution environment):

```cron
0 7 * * * cd /path/to/situational-awareness && /path/to/uv run market-report.py --provider tradingview --refresh >> market-report.log 2>&1
```

## Custom constituent breadth

The reusable `calculate_breadth` function in `breadth.py` accepts a list of
symbols and `{symbol: {"YYYY-MM-DD": close}}` histories. It calculates daily
equal-weight participation above/below/equal to an N-observation simple moving
average (including the current close). Date filters preserve prior warmup data.

```python
from breadth import calculate_breadth

snapshot = calculate_breadth(
    symbols, prices, window=50,
    start="2020-01-01", end="2026-10-23",
    name="CUSTOM:GDX-SMA50", universe_as_of="2026-10-22",
)
```

CLI using archived daily bar files:

```powershell
uv run custom-breadth.py --symbols NYSE:NEM NYSE:AEM --ma 50 --download-date 2026-10-25 --output data/custom-breadth.json
```

The two-stock example only demonstrates syntax; a GDX constituent index should
instead select the full holdings list and supply its exchange-qualified map:

```powershell
uv run custom-breadth.py --holdings-md knowledge/sectors/gdx.md --symbol-map data/gdx-symbol-map.json --ma 50 --min-coverage 0.8 --universe-as-of 2026-10-22 --name CUSTOM:GDX-SMA50 --download-date 2026-10-25 --output data/gdx-breadth-sma50.json
```

The symbol map is a JSON object mapping every issuer ticker label to exactly
one provider symbol, e.g. `{"NEM": "NYSE:NEM", ...}`. All 59 security rows are
selected; cash is excluded. Missing mappings fail. GDX symbol mappings,
downloaded histories, and calculated snapshots stay local under ignored `data/`.

To fetch all available history, replace `--download-date` and its value with
`--mcp-url https://mcp.tradingview.com/mcp`. Every completed symbol is archived
automatically; no separate save option is needed. It uses
`TRADINGVIEW_MCP_TOKEN` and pages history backwards. `--end` limits the last included date; use the latest
completed session to avoid forming bars. `--start` limits output dates, not
downloaded warmup. Without dates, all available supplied/downloaded history is used.

The output has the existing snapshot shape (`provider`, `series`, and bars
with `t`/`c`), with `c` equal to percentage above the SMA. Extra per-day fields
give above/below/equal counts, unavailable count, and coverage. Other OHLCV
fields are null. Missing prices are not forward-filled; the denominator is
eligible securities on each date. `--min-coverage 1` requires full-universe
coverage; the default allows any nonzero coverage. Before enough history
exists, percentages are null. Coverage is important for comparisons across time.

`--input PATH` remains available for a legacy combined snapshot.
This is a fixed-current-universe history, not historical GDX membership.
The report includes the GDX custom snapshot alongside MMOH/MMOF.
See the [methodology](knowledge/references/gdx-breadth.md).

## Breadth event study

`uv run breadth-study.py` reproduces the threshold study using local TradingView
downloads from the latest complete `data/research/day/<date>/` batch.
Use `--download-date` to pin a batch and `--data PATH` to change the store root.
It writes event-level CSV, summary CSV, methodology,
and snapshot hashes to `reports/breadth-study/`. Inputs and generated outputs are
ignored by Git; a research summary is preserved in the
[knowledge library](knowledge/references/breadth-crossing-study.md).
The script analyzes existing downloads; it does not refresh them.

## Verification

```powershell
uv run python -m unittest -v
```

Tests cover historical cutoffs, current-day exclusion, session changes,
missing/stale observations, month-end arithmetic, and actual CLI artifacts.

The provider functions, report calculation, and HTML renderer are separate
so further market sections and providers can be introduced independently.
