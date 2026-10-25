"""Presentation layer for the self-contained daily briefing."""
from datetime import date
from html import escape


CSS = """
:root{color-scheme:dark;--bg:#0b111b;--panel:#111b29;--line:#263346;--ink:#e8eef5;--muted:#a2b1c3;--accent:#67ddc4}
*{box-sizing:border-box}html{scroll-behavior:auto;scroll-padding-top:28px}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}
a{color:inherit}a:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:5px}a.skip{position:fixed;left:16px;top:-100px;background:var(--panel);padding:12px;z-index:9}a.skip:focus{top:12px}
.shell{max-width:1460px;margin:auto;display:grid;grid-template-columns:220px minmax(0,1fr);gap:52px;padding:0 40px}.sidebar{position:sticky;top:0;height:100vh;padding:38px 0;border-right:1px solid var(--line)}
.brand{font-size:12px;text-transform:uppercase;letter-spacing:.16em;font-weight:700}.edition{font-size:12px;color:var(--muted);margin:6px 0 40px}.nav-label{font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
nav a{display:flex;gap:10px;align-items:center;justify-content:space-between;margin-right:22px;padding:10px 12px;text-decoration:none;color:var(--muted);border-left:2px solid transparent;border-radius:0 5px 5px 0}nav a:hover{background:#162334;color:var(--ink)}nav a[aria-current=true]{color:var(--accent);background:#132a2c;border-left-color:var(--accent)}.nav-sub{font-size:12px;margin:2px 0 22px 26px;color:var(--muted)}.nav-tag{font-size:9px;text-transform:uppercase;letter-spacing:.08em}
main{min-width:0;padding:44px 0 30px}.eyebrow{font-size:10px;letter-spacing:.2em;font-weight:650;text-transform:uppercase;color:var(--accent);margin:0 0 10px}h1{font-size:clamp(25px,3vw,35px);line-height:1.2;font-weight:600;letter-spacing:-.035em;margin:0 0 16px}.report-header{padding-bottom:27px;border-bottom:1px solid var(--line)}.metadata{display:flex;gap:8px 22px;flex-wrap:wrap;color:var(--muted);font-size:12px}.metadata strong{color:var(--ink);font-weight:500}
.group{padding-top:34px;scroll-margin-top:24px}.group-heading{display:flex;align-items:baseline;gap:14px;margin-bottom:16px}.group-heading h2{margin:0;font-size:21px;font-weight:550;letter-spacing:-.02em}.group-number{font-size:11px;color:var(--muted);font-variant-numeric:tabular-nums}.group-description{font-size:12px;color:var(--muted);margin:0 0 16px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:24px 26px}.card-header{display:flex;align-items:flex-start;justify-content:space-between;gap:20px;flex-wrap:wrap}.card h3{font-size:16px;font-weight:550;line-height:1.35;margin:0 0 5px}.subheading{font-size:12px;color:var(--muted);margin:0}.period{font-size:11px;padding:3px 9px;border:1px solid var(--line);border-radius:5px;color:var(--muted);white-space:nowrap}.readings{display:flex;gap:16px 36px;flex-wrap:wrap;margin:20px 0 8px}.reading{min-width:145px}.reading-label{font-size:11px;font-weight:600;letter-spacing:.035em;display:flex;gap:8px;align-items:center}.swatch{display:inline-block;width:18px;border-top:2px solid currentColor}.reading-value{font-size:23px;letter-spacing:-.03em;line-height:1.5;font-variant-numeric:tabular-nums}.change{font-size:11px;color:var(--muted);margin-left:10px;letter-spacing:0}.asof{font-size:10px;color:var(--muted)}
.chart{width:100%;margin:8px 0 4px}.chart svg{display:block;width:100%;height:auto;overflow:visible}.chart svg text{fill:var(--muted);font-size:12px;font-family:inherit}.chart-caption{font-size:10px;color:var(--muted);display:flex;gap:12px;flex-wrap:wrap}.interpretation{margin:18px 0 0;line-height:1.75;font-size:14px;max-width:90ch}.details{border-top:1px solid var(--line);margin-top:22px;padding-top:12px;font-size:12px;color:var(--muted)}summary{cursor:pointer;width:fit-content;font-size:11px;letter-spacing:.025em}details[open] summary{margin-bottom:12px}.details p{margin:8px 0}.details ul{padding-left:18px}.details a{color:var(--accent)}.data-status{margin:14px 0 0;font-size:11px;color:var(--muted)}.data-status ul{margin:8px 0;padding-left:18px}.warning{border-left:3px solid #eabd70;background:#302719;padding:10px 14px;font-size:12px;border-radius:4px;margin:16px 0}.planned{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:15px 0;color:var(--muted);font-size:12px}.planned span{font-size:10px;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--line);padding:3px 7px;margin-right:10px;border-radius:4px}.theme-name{font-size:12px;color:var(--muted);font-weight:500;margin:0 0 14px}footer{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:10px}
@media(min-width:1300px){.shell{gap:64px}main{max-width:1050px}}
@media(max-width:850px){html{scroll-padding-top:100px}.shell{display:block;padding:0 20px}.sidebar{height:auto;position:sticky;top:0;padding:12px 0;background:var(--bg);border-right:0;border-bottom:1px solid var(--line);z-index:3}.brand{font-size:10px}.edition,.nav-label,.nav-sub{display:none}nav{display:flex;overflow-x:auto;gap:8px;margin-top:6px}nav a{flex-shrink:0;padding:6px 10px;margin:0;font-size:12px;border-left:0;border-bottom:2px solid transparent}nav a[aria-current=true]{border-bottom-color:var(--accent)}.nav-tag{display:none}main{padding:26px 0}.group{scroll-margin-top:100px}.card{padding:20px 16px}.interpretation{font-size:13px}.readings{gap:16px 24px}.reading-value{font-size:21px}.chart svg text{font-size:13px}.chart{margin-top:12px}.group-heading h2{font-size:20px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{:root{color-scheme:light;--bg:white;--panel:white;--line:#bbb;--ink:#111;--muted:#444;--accent:#135a4c}.sidebar,.skip,.data-status{display:none}.shell{display:block;padding:0}main{padding:0;max-width:none}.card{break-inside:avoid;border-color:#bbb}.chart svg text{fill:#444}h1{font-size:25px}.group{padding-top:24px}.interpretation{font-size:11px}}
"""

CSS += """
.chart-narrow{display:none}
@media(max-width:850px){.group{scroll-margin-top:0}}
@media(max-width:600px){.chart-wide{display:none}.chart-narrow{display:block}.chart .chart-narrow svg text{font-size:18px}}
"""

NAV_SCRIPT = """
const links = [...document.querySelectorAll('nav a')];
const groups = [...document.querySelectorAll('main > section.group')];
function mark(id) { for (const link of links) { if (link.hash === '#' + id) link.setAttribute('aria-current', 'true'); else link.removeAttribute('aria-current'); } }
let queued = false;
function update() { const cutoff = innerWidth <= 850 ? 140 : 100; let current = groups[0]; for (const group of groups) { if (group.getBoundingClientRect().top <= cutoff) current = group; } if (current) mark(current.id); queued = false; }
addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(update); } }, {passive:true});
addEventListener('resize', update); update();
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
                '<p>Knowledge: sectors/gdx.md · references/gdx-breadth.md.</p>')
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
    all_series = list(report["series"].values())
    if gdx:
        all_series += list(gdx["series"].values())
    dates = sorted({s["latest"]["date"] for s in all_series})
    freshness = ("Latest observation " + date.fromisoformat(dates[-1]).strftime("%d %b %Y"))
    if len(dates) > 1:
        freshness += " · mixed observation dates"
    if any(s.get("latest_status") == "intraday" for s in all_series):
        freshness += " · includes provisional intraday values"
    warnings = "".join(f'<div class="warning"><strong>Data warning:</strong> {escape(w)}</div>' for w in report["warnings"])
    notes = list(report.get("notes", [])) + (list(gdx.get("notes", [])) if gdx else [])
    status = ('<details class="data-status"><summary>Data availability</summary><ul>' +
              "".join(f'<li>{escape(note)}</li>' for note in dict.fromkeys(notes)) + '</ul></details>') if notes else ""
    readings = "".join(reading(s.split(":")[-1], value, color, dashed=i == 1)
                       for i, ((s, value), color) in enumerate(zip(report["series"].items(), ("#67ddc4", "#ffc078"))))
    breadth = (f'<article class="card" aria-labelledby="breadth-title"><div class="card-header"><div><h3 id="breadth-title">Stocks above their moving averages</h3>'
               f'<p class="subheading">MMOH · 100-day average &nbsp; / &nbsp; MMOF · 150-day average</p></div><span class="period">{report["lookback_months"]}-month view</span></div>'
               f'<div class="readings">{readings}</div><div class="chart">{responsive_chart(report)}</div>'
               '<div class="chart-caption"><span>Share of stocks (%) · 0–100 scale</span><span>TradingView</span></div>'
               f'<p class="interpretation">{escape(interpretation(report))}</p>{details(report)}</article>')
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
              ("sp500", "S&P 500", '<div class="planned"><span>Planned</span>Price and trend · Sector relative strength</div>'),
              ("themes", "Themes", themes)]
    navigation = "".join(f'<a href="#{key}"' + (' aria-current="true"' if i == 0 else '') + f'><span>{escape(title)}</span>' + ('<span class="nav-tag">Planned</span>' if key == 'sp500' else '') + '</a>' + ('<div class="nav-sub">Gold miners</div>' if key == 'themes' and gdx else '') for i, (key, title, _) in enumerate(groups))
    body = "".join(f'<section class="group" id="{key}" aria-labelledby="{key}-heading"><div class="group-heading"><span class="group-number">0{i+1}</span><h2 id="{key}-heading">{escape(title)}</h2></div>{content}</section>' for i, (key, title, content) in enumerate(groups))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Market report · {report['requested_date']}</title><style>{CSS}</style></head>
<body><a class="skip" href="#main">Skip to report</a><div class="shell"><aside class="sidebar"><div class="brand">Situational awareness</div><div class="edition">Daily market briefing</div><div class="nav-label">In this report</div><nav aria-label="Report sections">{navigation}</nav></aside>
<main id="main"><header class="report-header"><p class="eyebrow">Daily market briefing</p><h1>Daily situational awareness</h1><div class="metadata"><strong>{requested.strftime('%A, %d %B %Y')}</strong><span>{escape(freshness)}</span></div>{status}</header>{warnings}{body}<footer>Generated {escape(report['generated_at'])} · Observations and interpretation archived with this edition.</footer></main></div><script>{NAV_SCRIPT}</script></body></html>'''
