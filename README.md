# Daily market situational awareness

Python + uv proof of concept, starting with TradingView `INDEX:MMOH` and
`INDEX:MMOF`. Generates a standalone HTML report with an embedded SVG chart,
a JSON report containing the plotted observations and metadata, and a terminal
summary. No browser assets or external chart service are required.

## Report section template

Each datapoint has a heading, one simple chart or table, and a one- or
two-sentence interpretation. Breadth uses one shared MMOH/MMOF line chart;
latest values appear in its legend. Technical provenance stays in JSON.
Material data-quality warnings remain visible in the report.

Next planned section: SPDR sector analysis, using a sector table with RS-1,
RS-3, and RS-6 columns for 1-, 3-, and 6-month relative returns. Proposed
calculation: sector ETF return minus SPY return, expressed in percentage
points, with matched observation dates and a consistent adjustment policy.
Positive values indicate outperformance. The sector section is not yet
implemented.

## Knowledge library

The version-controlled [knowledge bundle](knowledge/index.md) follows the
[official OKF v0.2 specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md).
It contains indicator references, an explicitly unvalidated breadth hypothesis,
and the proposed sector RS methodology. Concept metadata uses YAML frontmatter;
explanations and evidence live in Markdown. The `market_report` extension is
project-specific and is not yet consumed by the report generator.

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

The default `--provider snapshot` uses the local real TradingView data:
180 daily observations per index, fetched through the chat's TradingView
connector on 24 October 2026, ending on 23 October. It is a fixed snapshot;
running the default command on subsequent days does not fetch new readings.
`--snapshot PATH` accepts another snapshot with the same schema. Fetched data
in `data/` is ignored by Git and must be fetched or supplied on a new checkout.

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

Live responses are cached by requested date and lookback in `.cache/`.
Use `--refresh` in scheduled jobs to ensure a fresh request each run. Failed
requests return a nonzero exit status; they never silently fall back to the
local snapshot. Tokens and endpoint URLs are excluded from report metadata.
The provider fetches a little extra history for five-session comparisons.
It rejects truncated responses instead of silently reporting partial history.

## Dates and interpretation

- `--date YYYY-MM-DD` means observations at or before that date. Default:
  today's date in New York; the latest available prior observation is shown.
- The current New York calendar date is always excluded because a daily bar
  may still be forming. Run on the following morning for the previous close.
  This conservative PoC does not use an exchange holiday/session calendar.
- Every card shows its actual observation date. Missing history, differing
  latest dates, and observations more than three calendar days old are flagged.
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

## Breadth event study

`uv run breadth-study.py` reproduces the threshold study using local TradingView
downloads in `data/research/`. It writes event-level CSV, summary CSV, methodology,
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
