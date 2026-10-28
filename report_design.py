"""Presentation layer for the self-contained daily briefing."""
from datetime import date
from html import escape


CSS = """
:root{color-scheme:dark;--bg:#0b111b;--panel:#111b29;--line:#263346;--ink:#e8eef5;--muted:#a2b1c3;--accent:#67ddc4}
*{box-sizing:border-box}html{scroll-behavior:auto;scroll-padding-top:28px}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}
a{color:inherit}a:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:5px}a.skip{position:fixed;left:16px;top:-100px;background:var(--panel);padding:12px;z-index:9}a.skip:focus{top:12px}
.shell{max-width:1460px;margin:auto;display:grid;grid-template-columns:220px minmax(0,1fr);gap:52px;padding:0 40px}.sidebar{position:sticky;top:0;height:100vh;padding:38px 0;border-right:1px solid var(--line)}
.brand{font-size:12px;text-transform:uppercase;letter-spacing:.16em;font-weight:700}.edition{font-size:12px;color:var(--muted);margin:6px 0 40px}.nav-label{font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
nav a{display:flex;gap:10px;align-items:center;justify-content:space-between;margin-right:22px;padding:10px 12px;text-decoration:none;color:var(--muted);border-left:2px solid transparent;border-radius:0 5px 5px 0}nav a:hover{background:#162334;color:var(--ink)}nav a[aria-current]{color:var(--accent);background:#132a2c;border-left-color:var(--accent)}.nav-sub{font-size:12px;margin:2px 0 22px 26px;color:var(--muted)}.nav-tag{font-size:9px;text-transform:uppercase;letter-spacing:.08em}
main{min-width:0;padding:44px 0 30px}.eyebrow{font-size:10px;letter-spacing:.2em;font-weight:650;text-transform:uppercase;color:var(--accent);margin:0 0 10px}h1{font-size:clamp(25px,3vw,35px);line-height:1.2;font-weight:600;letter-spacing:-.035em;margin:0 0 16px}.report-header{padding-bottom:27px;border-bottom:1px solid var(--line)}.metadata{display:flex;gap:8px 22px;flex-wrap:wrap;color:var(--muted);font-size:12px}.metadata strong{color:var(--ink);font-weight:500}
.group{padding-top:34px;scroll-margin-top:24px}.group-heading{display:flex;align-items:baseline;gap:14px;margin-bottom:16px}.group-heading h2{margin:0;font-size:21px;font-weight:550;letter-spacing:-.02em}.group-number{font-size:11px;color:var(--muted);font-variant-numeric:tabular-nums}.group-description{font-size:12px;color:var(--muted);margin:0 0 16px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:24px 26px}.card-header{display:flex;align-items:flex-start;justify-content:space-between;gap:20px;flex-wrap:wrap}.card h3{font-size:16px;font-weight:550;line-height:1.35;margin:0 0 5px}.subheading{font-size:12px;color:var(--muted);margin:0}.period{font-size:11px;padding:3px 9px;border:1px solid var(--line);border-radius:5px;color:var(--muted);white-space:nowrap}.readings{display:flex;gap:16px 36px;flex-wrap:wrap;margin:20px 0 8px}.reading{min-width:145px}.reading-label{font-size:11px;font-weight:600;letter-spacing:.035em;display:flex;gap:8px;align-items:center}.swatch{display:inline-block;width:18px;border-top:2px solid currentColor}.reading-value{font-size:23px;letter-spacing:-.03em;line-height:1.5;font-variant-numeric:tabular-nums}.change{font-size:11px;color:var(--muted);margin-left:10px;letter-spacing:0}.asof{font-size:10px;color:var(--muted)}
.chart{width:100%;margin:8px 0 4px}.chart svg{display:block;width:100%;height:auto;overflow:visible}.chart svg text{fill:var(--muted);font-size:12px;font-family:inherit}.chart-caption{font-size:10px;color:var(--muted);display:flex;gap:12px;flex-wrap:wrap}.interpretation{margin:18px 0 0;line-height:1.75;font-size:14px;max-width:90ch}.details{border-top:1px solid var(--line);margin-top:22px;padding-top:12px;font-size:12px;color:var(--muted)}summary{cursor:pointer;width:fit-content;font-size:11px;letter-spacing:.025em}details[open] summary{margin-bottom:12px}.details p{margin:8px 0}.details ul{padding-left:18px}.details a{color:var(--accent)}.data-status{margin:14px 0 0;font-size:11px;color:var(--muted)}.data-status ul{margin:8px 0;padding-left:18px}.warning{border-left:3px solid #eabd70;background:#302719;padding:10px 14px;font-size:12px;border-radius:4px;margin:16px 0}.planned{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:15px 0;color:var(--muted);font-size:12px}.planned span{font-size:10px;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--line);padding:3px 7px;margin-right:10px;border-radius:4px}.theme-name{font-size:12px;color:var(--muted);font-weight:500;margin:0 0 14px}footer{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:10px}
@media(min-width:1300px){.shell{gap:64px}main{max-width:1050px}}
@media(max-width:850px){html{scroll-padding-top:100px}.shell{display:block;padding:0 20px}.sidebar{height:auto;position:sticky;top:0;padding:12px 0;background:var(--bg);border-right:0;border-bottom:1px solid var(--line);z-index:3}.brand{font-size:10px}.edition,.nav-label,.nav-sub{display:none}nav{display:flex;overflow-x:auto;gap:8px;margin-top:6px}nav a{flex-shrink:0;padding:6px 10px;margin:0;font-size:12px;border-left:0;border-bottom:2px solid transparent}nav a[aria-current]{border-bottom-color:var(--accent)}.nav-tag{display:none}main{padding:26px 0}.group{scroll-margin-top:100px}.card{padding:20px 16px}.interpretation{font-size:13px}.readings{gap:16px 24px}.reading-value{font-size:21px}.chart svg text{font-size:13px}.chart{margin-top:12px}.group-heading h2{font-size:20px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{:root{color-scheme:light;--bg:white;--panel:white;--line:#bbb;--ink:#111;--muted:#444;--accent:#135a4c}.sidebar,.skip,.data-status{display:none}.shell{display:block;padding:0}main{padding:0;max-width:none}.card{break-inside:avoid;border-color:#bbb}.chart svg text{fill:#444}h1{font-size:25px}.group{padding-top:24px}.interpretation{font-size:11px}}
"""

CSS += """
.chart-narrow{display:none}
@media(max-width:850px){.group{scroll-margin-top:0}}
@media(max-width:600px){.chart-wide{display:none}.chart-narrow{display:block}.chart .chart-narrow svg text{font-size:18px}}
"""

CSS += """
.research-todos{margin-top:20px;padding-top:16px;border-top:1px solid var(--line);font-size:12px}.research-todos h2{font-size:11px;color:var(--muted);font-weight:500;margin:0 0 8px}.research-todos ul{padding-left:18px;margin:0}.research-todos li{padding:3px 0}.research-todos strong{font-weight:550}.research-todos p{color:var(--muted);margin:0}
.status-strip{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;margin:24px 0 0}.status-item{border-left:1px solid var(--line);padding-left:16px}.status-item:first-child{border:0;padding-left:0}.status-item dt{font-size:10px;letter-spacing:.04em;color:var(--muted)}.status-item dd{font-size:22px;font-variant-numeric:tabular-nums;margin:3px 0 0;line-height:1.4}.status-item small{display:block;font-size:10px;color:var(--muted);margin-top:3px}.overview-label{margin-top:30px!important;font-size:15px!important;color:var(--ink)!important}.data-mode{padding:1px 8px;border:1px solid var(--line);border-radius:4px;font-size:10px}
@media(max-width:600px){.status-strip{grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.status-item:nth-child(3){border:0;padding-left:0}}
.report-page{display:none}.report-page.overview{display:block}
main:has(>.report-page:target)>.report-page{display:none}
main:has(>.report-page:target)>.report-page:target{display:block}
.welcome{padding:40px 0 30px;max-width:680px}.welcome h2{font-size:clamp(24px,3vw,34px);line-height:1.25;font-weight:500;letter-spacing:-.03em;margin:0 0 16px}.welcome p:last-child{color:var(--muted);font-size:15px;line-height:1.8;margin:0}.overview-label{font-size:12px;font-weight:500;color:var(--muted);margin:0 0 16px}.overview-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.overview-card{display:flex;flex-direction:column;padding:24px;background:var(--panel);border:1px solid var(--line);border-radius:10px;text-decoration:none;min-height:245px;transition:border-color .15s}.overview-card:hover{border-color:var(--accent)}.overview-card-top{display:flex;align-items:center;justify-content:space-between;gap:12px}.overview-card h3{font-size:18px;letter-spacing:-.02em;margin:0;font-weight:550}.overview-card p{font-size:13px;color:var(--muted);margin:16px 0}.overview-preview{font-size:12px;font-variant-numeric:tabular-nums}.open-section{font-size:12px;color:var(--accent);padding-top:24px;margin-top:auto;display:flex;justify-content:space-between}.back-overview{display:inline-block;color:var(--muted);font-size:12px;text-decoration:none;margin-bottom:20px}.back-overview:hover{color:var(--accent)}
@media(max-width:850px){.overview-grid{grid-template-columns:1fr}.overview-card{min-height:210px}.welcome{padding-top:28px}.welcome p:last-child{font-size:14px}}
@media print{main>.report-page{display:block!important}.back-overview,.overview-grid{display:none}.welcome{padding:16px 0}.overview-label{display:none}}
"""

CSS += """
.limitations{border-left:3px solid #7fa7e0;background:#162238;padding:12px 16px;border-radius:4px;margin:18px 0 0;font-size:12px}.limitations h2{font-size:12px;font-weight:600;margin:0 0 6px}.limitations ul{margin:0;padding-left:18px}.limitations li{padding:2px 0}.limitations p{margin:6px 0 0;color:var(--muted)}
.source-note{font-size:11px;color:var(--muted);margin:14px 0 0;padding:6px 10px;border:1px dashed var(--line);border-radius:5px;width:fit-content}.source-note strong{color:var(--ink);font-weight:550}
.unavailable{margin:20px 0 4px;padding:18px;border:1px dashed #7fa7e0;border-radius:8px;font-size:13px}.unavailable strong{display:block;margin-bottom:4px}
@media print{.limitations{border:1px solid #888;background:white}}
"""

PROVIDER_LABELS = {"tradingview": "TradingView", "alpaca": "Alpaca"}


def provider_name(provider):
    return PROVIDER_LABELS.get(provider, provider or "unknown")


def limitations_panel(report):
    """Visible summary of series a requested provider cannot supply."""
    items = report.get("provider_coverage", [])
    if not items:
        return ""
    rows = []
    for item in items:
        name = item["symbol"].split(":")[-1]
        what = item.get("label", name)
        if item["status"] == "substituted":
            outcome = f'shown from {item["source"]}'
        elif item["status"] == "partial":
            outcome = item["source"]
        else:
            outcome = "not shown"
        rows.append(f'<li><strong>{escape(what)}</strong> ({escape(item["section"])}): not available from '
                    f'{escape(provider_name(item["requested_provider"]))}; {escape(outcome)}. {escape(item["reason"])}</li>')
    return ('<section class="limitations" aria-labelledby="limitations-heading"><h2 id="limitations-heading">'
            f'Provider limitations · {len(items)}</h2><ul>' + "".join(rows) + '</ul>'
            '<p>Substituted series keep their original provider; they are labelled, not merged into another provider\'s data.</p></section>')


CSS += """
.metric-table{width:100%;border-collapse:collapse;margin:18px 0 4px;font-size:14px;font-variant-numeric:tabular-nums}.metric-table th,.metric-table td{padding:9px 4px;border-bottom:1px solid var(--line);text-align:left}.metric-table th{font-weight:500;color:var(--muted)}.metric-table td{text-align:right;font-size:16px}.metric-table tr:last-child>*{border-bottom:0}
"""


def spy_card(spy):
    """SPY trend metrics as one table; unavailable data is stated, not hidden."""
    title = '<div class="card-header"><div><h3 id="spy-title">SPY · S&amp;P 500 ETF</h3><p class="subheading">Trend and streak metrics</p></div>'
    if "metrics" not in spy:
        return (f'<article class="card" aria-labelledby="spy-title">{title}<span class="period">Unavailable</span></div>'
                f'<div class="unavailable" role="note"><strong>No SPY data</strong>{escape(spy["unavailable"])}</div></article>')
    m = spy["metrics"]
    def pct(value):
        return "n/a" if value is None else f"{value:+.2f}%"
    def streak(key):
        return f'{"≥" if m["lower_bound"][key] else ""}{m[key]}'
    side = ("Cons. days above 50-day SMA", streak("cons_days_above_sma50")) if m["cons_days_above_sma50"] else ("Cons. days below 50-day SMA", streak("cons_days_below_sma50"))
    rows = [("Close", f'{m["close"]:.2f}'), ("Distance from 200-day SMA", pct(m["distance_from_sma200_pct"])),
            ("Distance from 50-day SMA", pct(m["distance_from_sma50_pct"])), side,
            ("Cons. down days", streak("cons_down_days"))]
    table = '<table class="metric-table"><tbody>' + "".join(f'<tr><th scope="row">{escape(k)}</th><td>{escape(v)}</td></tr>' for k, v in rows) + '</tbody></table>'
    source = provider_name(spy["provider"]) + (f' · {spy["feed"]} feed' if spy.get("feed") else "") + f' · {spy["symbol"]}'
    info = (f'<details class="details"><summary>Details and methodology</summary><p>Simple moving averages include the current close. '
            'Distance is 100 × (close / SMA − 1). Streaks count consecutive sessions ending at the latest close; an unchanged close or a close equal to the SMA ends a streak. '
            f'"≥" marks a streak that reaches the start of the downloaded history ({escape(m["history_start"])}, {m["history_sessions"]} sessions).</p>'
            f'<p>Source: {escape(spy["source"])}. Data fetched: {escape(str(spy.get("fetched_at")))}. '
            'Studies of these metrics are open Research TODOs in knowledge/index/spy.md.</p></details>')
    return (f'<article class="card" aria-labelledby="spy-title">{title}<span class="period">{escape(spy["as_of"])}</span></div>{table}'
            f'<div class="chart-caption"><span>{escape(source)}</span><span>{escape("Adjustment: " + spy["adjustment"] if spy.get("adjustment") else "Adjustment not recorded by provider")}</span></div>'
            f'<p class="interpretation">{escape(spy["interpretation"])}</p>{info}</article>')


def vix_card(vix):
    title = '<div class="card-header"><div><h3 id="vix-title">VIX · S&amp;P 500 implied volatility</h3><p class="subheading">30-day expected volatility · spot index</p></div>'
    if not vix or "metrics" not in vix:
        reason = vix.get("unavailable", "VIX was not loaded for this report.") if vix else "VIX was not loaded for this report."
        return f'<article class="card" style="margin-top:20px" aria-labelledby="vix-title">{title}<span class="period">Unavailable</span></div><p class="unavailable">{escape(reason)}</p></article>'
    metrics = vix["metrics"]
    table = (f'<table class="metric-table"><tbody><tr><th scope="row">Latest VIX</th><td>{metrics["close"]:.2f}</td></tr>'
             f'<tr><th scope="row">Day low · up to {vix["period"]} sessions</th><td>{metrics["day_low"]}</td></tr></tbody></table>')
    note = 'The search reached the available history or configured period; the low span may be longer.' if vix["day_low_lower_bound"] else 'Higher or equal to the preceding close returns 0; the current observation is included when counting a new low.'
    info = (f'<details class="details"><summary>Details and methodology</summary><p>Day low is the longest trailing span in which the latest observation is strictly lower than every preceding observation, capped at {vix["period"]} sessions. A strict low across 365 closes returns 365; a tie ends the span.</p>'
            f'<p>{note} {vix["history_sessions"]} closes available since {escape(vix["history_start"])}; effective lookback {vix["effective_lookback"]}.</p>'
            f'<p>CBOE:VIX · TradingView · Fetched {escape(vix["fetched_at"])}. Knowledge: index/vix.md.</p></details>')
    return (f'<article class="card" style="margin-top:20px" aria-labelledby="vix-title">{title}<span class="period">{escape(vix["as_of"])}</span></div>{table}'
            f'<p class="interpretation">{escape(vix["interpretation"])}</p>{info}</article>')


NAV_SCRIPT = """
const links = [...document.querySelectorAll('nav a')];
const pages = [...document.querySelectorAll('.report-page')];
function navigate(focus = false) {
  const id = pages.some(page => '#' + page.id === location.hash) ? location.hash.slice(1) : 'overview';
  for (const link of links) { if (link.hash === '#' + id) link.setAttribute('aria-current', 'page'); else link.removeAttribute('aria-current'); }
  if (focus) { window.scrollTo(0, 0); document.querySelector('#' + id + ' h2')?.focus({preventScroll:true}); }
}
addEventListener('hashchange', () => navigate(true)); navigate();
"""


def reading(label, series, color, *, dashed=False):
    change = series.get("daily_change")
    delta = "" if change is None else f'<span class="change">{change:+.2f} pp / session</span>'
    style = "border-top-style:dashed" if dashed else ""
    return (f'<div class="reading"><div class="reading-label" style="color:{color}">'
            f'<span class="swatch" style="{style}" aria-hidden="true"></span>{escape(label)}</div>'
            f'<div class="reading-value">{series["latest"]["close"]:.2f}%{delta}</div>'
            f'<div class="asof">({escape(series["as_of"])})</div></div>')


def details(report, *, gdx=False):
    if gdx:
        definition = report["definition"]
        universe = report["universe"]
        coverage = report["coverage"]
        text = (f'<p>Equal-weight percentage above the {definition["window"]}-observation simple moving average, including the current close. '
                f'Above: {coverage["above"]}; below: {coverage["below"]}; equal: {coverage["equal"]}.</p>'
                f'<p>Fixed holdings as of {escape(str(universe.get("as_of") or "unspecified"))}. Historical results use this same universe; they do not reconstruct historical fund membership.</p>'
                f'<p>Missing prices are not carried forward. Minimum eligible coverage: {100 * definition["min_coverage"]:g}%. '
                'Exchange-local session dates are aligned before calculation. No predictive threshold has been validated.</p>'
                f'<p>Constituent prices: {escape(provider_name(report.get("input_provider")))}.'
                + (f' {len(report["provider_unavailable"])} constituents are not available from this provider and count as missing.' if report.get("provider_unavailable") else '')
                + '</p><p>Knowledge: sectors/gdx.md · references/gdx-breadth.md.</p>')
    else:
        text = ('<p>MMOH: percentage above the 100-day average. MMOF: percentage above the 150-day average. '
                'The provider stock universe and average type remain undocumented in the consulted sources.</p>'
                '<p>The historical study describes downward crossings, not all low readings; findings are exploratory and include overlapping events.</p>'
                '<p>Sources: <a href="https://www.tradingview.com/symbols/INDEX-MMOH/">TradingView MMOH</a> · '
                '<a href="https://www.tradingview.com/symbols/INDEX-MMOF/">TradingView MMOF</a>.</p>')
    text += (f'<p>Data fetched: {escape(str(report.get("data_fetched_at", "Unavailable")))}. '
             f'Chart window: {report["lookback_months"]} months. Changes are percentage points.</p>')
    return f'<details class="details"><summary>Details and methodology</summary>{text}</details>'


def render_report(report, chart, interpretation):
    def responsive_chart(section):
        return f'<div class="chart-wide">{chart(section)}</div><div class="chart-narrow">{chart(section, compact=True)}</div>'
    requested = date.fromisoformat(report["requested_date"])
    gdx = report.get("gdx_breadth")
    vix = report.get("vix")
    all_series = list(report["series"].values())
    if vix and "metrics" in vix:
        all_series.append(vix)
    if gdx:
        all_series += list(gdx["series"].values())
    dates = sorted({s["latest"]["date"] for s in all_series})
    freshness = ("Latest observation " + date.fromisoformat(dates[-1]).strftime("%d %b %Y")) if dates else "No observations available"
    if len(dates) > 1:
        freshness += " · mixed observation dates"
    if any(s.get("latest_status") == "intraday" for s in all_series):
        freshness += " · includes provisional intraday values"
    warnings = "".join(f'<div class="warning"><strong>Data warning:</strong> {escape(w)}</div>' for w in report["warnings"])
    notes = list(report.get("notes", [])) + (list(gdx.get("notes", [])) if gdx else [])
    status = ('<details class="data-status"><summary>Data availability</summary><ul>' +
              "".join(f'<li>{escape(note)}</li>' for note in dict.fromkeys(notes)) + '</ul></details>') if notes else ""
    source_symbols = set(report["series"])
    spy = report.get("spy") or {"symbol": "SPY", "unavailable": "SPY was not loaded for this report."}
    if "metrics" in spy:
        source_symbols.add(spy["symbol"])
    if vix and "metrics" in vix:
        source_symbols.add(vix["symbol"])
    if gdx:
        source_symbols.update(set(gdx["universe"]["symbols"]) - set(gdx["universe"].get("missing_symbols", [])))
    run = report.get("run_status", {})
    downloads = str(run["downloaded_symbols"]) if "downloaded_symbols" in run else "—"
    coverage_text = f'{gdx["coverage"]["eligible"]}/{gdx["coverage"]["universe_size"]}' if gdx else "—"
    source_detail = f'{len(report["series"])} breadth indices' + (' · SPY' if "metrics" in spy else '') + (' · VIX' if vix and "metrics" in vix else '') + (f' · {len(set(gdx["universe"]["symbols"]) - set(gdx["universe"].get("missing_symbols", [])))} GDX constituents' if gdx else '')
    stats = [("Source symbols", str(len(source_symbols)), source_detail),
             ("Downloaded this run", downloads, ""),
             ("GDX coverage", coverage_text, "Eligible / constituent universe" if gdx else "Not included"),
             ("Data warnings", str(len(set(report["warnings"]))), "")]
    status_strip = '<dl class="status-strip" aria-label="Report data status">' + ''.join(f'<div class="status-item"><dt>{label}</dt><dd>{escape(value)}</dd>' + (f'<small>{escape(note)}</small>' if note else '') + '</div>' for label, value, note in stats) + '</dl>'
    data_mode = f'<span class="data-mode">{escape(run["data_mode"])}</span>' if run.get("data_mode") else ""
    if run.get("download_batch"):
        data_mode += f'<span>Download batch {date.fromisoformat(run["download_batch"]).strftime("%d %b %Y")}</span>'
    todos = report.get("research_todos", [])
    todo_list = '<ul>' + ''.join(f'<li><strong>{escape(task["title"])}:</strong> {escape(task["description"])}</li>' for task in todos) + '</ul>' if todos else '<p>No open research TODOs.</p>'
    research_status = f'<section class="research-todos" aria-labelledby="research-todos-heading"><h2 id="research-todos-heading">Open research TODOs · {len(todos)}</h2>{todo_list}</section>'
    readings = "".join(reading(s.split(":")[-1], value, color, dashed=i == 1)
                       for i, ((s, value), color) in enumerate(zip(report["series"].items(), ("#67ddc4", "#ffc078"))))
    substituted = [c for c in report.get("provider_coverage", []) if c["section"] == "Market breadth" and c["status"] == "substituted"]
    source_note = ""
    if substituted:
        source_note = (f'<p class="source-note"><strong>Source: {escape(provider_name(substituted[0]["provider_used"]))}</strong> · '
                       f'{escape(substituted[0]["source"])} · not available from {escape(provider_name(substituted[0]["requested_provider"]))}</p>')
    breadth = (f'<article class="card" aria-labelledby="breadth-title"><div class="card-header"><div><h3 id="breadth-title">Stocks above their moving averages</h3>'
               f'<p class="subheading">MMOH · 100-day average &nbsp; / &nbsp; MMOF · 150-day average</p></div><span class="period">{report["lookback_months"]}-month view</span></div>'
               f'{source_note}<div class="readings">{readings}</div><div class="chart">{responsive_chart(report)}</div>'
               '<div class="chart-caption"><span>Share of stocks (%) · 0–100 scale</span><span>TradingView</span></div>'
               f'<p class="interpretation">{escape(interpretation(report))}</p>{details(report)}</article>') if report["series"] else (
               '<article class="card" aria-labelledby="breadth-title"><div class="card-header"><div><h3 id="breadth-title">Stocks above their moving averages</h3>'
               '<p class="subheading">MMOH · 100-day average &nbsp; / &nbsp; MMOF · 150-day average</p></div><span class="period">Unavailable</span></div>'
               f'<div class="unavailable" role="note"><strong>No breadth data for this provider</strong>{escape(report.get("breadth_unavailable", "No observations are available."))}</div></article>')
    themes = '<p class="planned"><span>Planned</span>Theme coverage will appear here as observations are added.</p>'
    if gdx:
        value = next(iter(gdx["series"].values()))
        coverage = gdx["coverage"]
        themes = (f'<p class="theme-name">Gold miners / GDX</p><article class="card" aria-labelledby="gdx-title"><div class="card-header"><div><h3 id="gdx-title">GDX breadth</h3>'
                  f'<p class="subheading">Constituents above their {gdx["definition"]["window"]}-day SMA</p></div><span class="period">{gdx["lookback_months"]}-month view</span></div>'
                  f'<div class="readings">{reading("Above SMA", value, "#67ddc4")}</div><div class="chart">{responsive_chart(gdx)}</div>'
                  f'<div class="chart-caption"><span>Coverage {coverage["eligible"]}/{coverage["universe_size"]}</span><span>Equal-weight · fixed current constituents</span><span>Share of stocks (%)</span></div>'
                  f'<p class="interpretation">{escape(gdx["interpretation"])}</p>{details(gdx, gdx=True)}</article>')
    groups = [("market-breadth", "Market Breadth", breadth),
              ("sp500", "S&P 500", spy_card(spy) + vix_card(vix) + '<p class="planned"><span>Planned</span>Sector relative strength</p>'),
              ("themes", "Themes", themes)]
    cards = []
    for key, title, _ in groups:
        if key == "market-breadth":
            description = "Participation across the market, using MMOH and MMOF."
            preview = " · ".join(f'{symbol.split(":")[-1]} {value["latest"]["close"]:.2f}%' for symbol, value in report["series"].items()) or "Unavailable from the selected provider"
            badge = "Available" if report["series"] else "Unavailable"
            if substituted:
                badge = "TradingView data"
        elif key == "themes":
            description = "Explore focused market themes, starting with gold miners."
            preview = f'GDX breadth {next(iter(gdx["series"].values()))["latest"]["close"]:.2f}% · {gdx["coverage"]["eligible"]}/{gdx["coverage"]["universe_size"]} coverage' if gdx else "Theme coverage coming next"
            badge = "Available" if gdx else "Planned"
        else:
            description = "SPY trend and streak metrics, plus VIX implied volatility."
            if "metrics" in spy:
                m = spy["metrics"]
                d200 = "" if m["distance_from_sma200_pct"] is None else f' · {m["distance_from_sma200_pct"]:+.1f}% vs 200-day'
                preview = f'SPY {m["close"]:.2f}{d200} · {m["cons_down_days"]} down days'
                badge = "Available"
            else:
                preview, badge = "SPY data unavailable", "Unavailable"
        cards.append(f'<a class="overview-card" href="#{key}"><div class="overview-card-top"><h3>{escape(title)}</h3><span class="period">{badge}</span></div><p>{escape(description)}</p><div class="overview-preview">{escape(preview)}</div><span class="open-section">Explore section <span aria-hidden="true">→</span></span></a>')
    overview = ('<section class="report-page overview" id="overview" aria-labelledby="overview-heading">'
                '<h2 class="overview-label" id="overview-heading" tabindex="-1">Sections</h2><div class="overview-grid">' + ''.join(cards) + '</div></section>')
    navigation = '<a href="#overview" aria-current="page"><span>Overview</span></a>'
    navigation += "".join(f'<a href="#{key}"><span>{escape(title)}</span>' + ('<span class="nav-tag">Unavailable</span>' if key == 'sp500' and "metrics" not in spy else '') + '</a>' for key, title, _ in groups)
    body = overview + "".join(f'<section class="group report-page" id="{key}" aria-labelledby="{key}-heading"><a class="back-overview" href="#overview">← All sections</a><div class="group-heading"><span class="group-number">0{i+1}</span><h2 id="{key}-heading" tabindex="-1">{escape(title)}</h2></div>{content}</section>' for i, (key, title, content) in enumerate(groups))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Market report · {report['requested_date']}</title><style>{CSS}</style></head>
<body><a class="skip" href="#main">Skip to report</a><div class="shell"><aside class="sidebar"><div class="brand">Situational awareness</div><div class="edition">Daily market briefing</div><div class="nav-label">In this report</div><nav aria-label="Report sections">{navigation}</nav></aside>
<main id="main"><header class="report-header"><p class="eyebrow">Daily market briefing</p><h1>Daily situational awareness</h1><div class="metadata"><strong>{requested.strftime('%A, %d %B %Y')}</strong><span>{escape(freshness)}</span>{data_mode}</div>{limitations_panel(report)}{status_strip}{research_status}{status}</header>{warnings}{body}<footer>Generated {escape(report['generated_at'])} · Observations and interpretation archived with this edition.</footer></main></div><script>{NAV_SCRIPT}</script></body></html>'''
