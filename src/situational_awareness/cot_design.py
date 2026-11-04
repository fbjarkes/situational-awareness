"""Inline SVG candles and weekly trader net-position bars."""
from datetime import date
from html import escape

from situational_awareness.cot import GROUPS


def cot_chart(market):
    start, end = (date.fromisoformat(market[k]).toordinal() for k in ('start', 'end'))
    x = lambda day: 72 + 900 * (date.fromisoformat(day).toordinal() - start) / max(1, end - start)
    svg = [f'<svg viewBox="0 0 1000 510" role="img" aria-label="{escape(market["title"])} daily futures prices and weekly COT net positions">']
    svg.append('<text x="72" y="18">Daily futures price · index points</text>')
    prices = market['prices']
    if prices:
        low, high = min(p['l'] for p in prices), max(p['h'] for p in prices)
        padding = max((high - low) * .05, 1)
        low, high = low - padding, high + padding
        y = lambda v: 225 - 185 * (v - low) / (high - low)
        for i in range(4):
            value = low + i * (high - low) / 3
            svg.append(f'<line x1="72" x2="972" y1="{y(value):.1f}" y2="{y(value):.1f}" stroke="#2d3b4b"/><text x="62" y="{y(value)+4:.1f}" text-anchor="end">{value:,.0f}</text>')
        width = min(5, 900 / max(1, len(prices)) * .7)
        for p in prices:
            color = '#67ddc4' if p['c'] >= p['o'] else '#ff7676'
            at = x(p['date'])
            svg.append(f'<g><title>{p["date"]}: O {p["o"]:,.2f}, H {p["h"]:,.2f}, L {p["l"]:,.2f}, C {p["c"]:,.2f}</title><line x1="{at:.1f}" x2="{at:.1f}" y1="{y(p["h"]):.1f}" y2="{y(p["l"]):.1f}" stroke="{color}"/><rect x="{at-width/2:.1f}" y="{min(y(p["o"]),y(p["c"])):.1f}" width="{width:.1f}" height="{max(1,abs(y(p["c"])-y(p["o"]))):.1f}" fill="{color}"/></g>')
    else:
        svg.append('<text x="72" y="120">Daily futures prices unavailable in bar store</text>')
    svg.append('<text x="72" y="268">Weekly net positions · contracts (long − short)</text>')
    maximum = max(1, max(abs(p['groups'][g]['net']) for p in market['points'] for g in GROUPS)) * 1.08
    baseline, halfheight = 370, 78
    for value in (-maximum, 0, maximum):
        yvalue = baseline - value / maximum * halfheight
        svg.append(f'<line x1="72" x2="972" y1="{yvalue:.1f}" y2="{yvalue:.1f}" stroke="{ "#afbdce" if value==0 else "#2d3b4b"}"/><text x="62" y="{yvalue+4:.1f}" text-anchor="end">{value/1000:,.0f}K</text>')
    cluster = min(15, 900 * 7 / max(1, end-start) * .85)
    width = cluster / len(GROUPS)
    for i, (key, (label, _, color)) in enumerate(GROUPS.items()):
        svg.append(f'<g class="cot-series" data-cot-group="{key}">')
        for point in market['points']:
            value = point['groups'][key]['net']
            yvalue = baseline - value / maximum * halfheight
            svg.append(f'<rect x="{x(point["date"])+(i-2.5)*width:.1f}" y="{min(baseline,yvalue):.1f}" width="{max(.5,width-.25):.1f}" height="{max(.5,abs(yvalue-baseline)):.1f}" fill="{color}"><title>{point["date"]} · {label}: {value:+,} contracts</title></rect>')
        svg.append('</g>')
    for i in range(5):
        day = date.fromordinal(round(start + (end-start)*i/4)).isoformat()
        svg.append(f'<text x="{x(day):.1f}" y="478" text-anchor="{ "start" if i==0 else "end" if i==4 else "middle"}">{day}</text>')
    svg.append('</svg>')
    return ''.join(svg)


def cot_cards(section):
    if not section or not section.get('markets'):
        return '<p class="unavailable">COT history is unavailable. Download the CFTC history with uv run cot --refresh.</p>'
    cards = []
    for market in section['markets']:
        latest = market['points'][-1]
        legend = ''.join(f'<span style="color:{color}">{escape(label)} {latest["groups"][key]["net"]:+,}</span>' for key, (label, _, color) in GROUPS.items())
        price_date = market['prices'][-1]['date'] if market['prices'] else 'unavailable'
        if market.get('price_intraday'):
            price_date += ' (provisional intraday)'
        cards.append(f'<article class="card" style="margin-bottom:24px"><div class="card-header"><div><h3>{escape(market["title"])} futures positioning</h3><p class="subheading">{section["months"]}-month view · CFTC consolidated · futures only</p></div><span class="period">Positions {market["as_of"]}</span></div>'
                     f'<div class="chart-caption" style="gap:12px;margin:14px 0">{legend}</div><div class="chart" style="min-width:600px">{cot_chart(market)}</div>'
                     f'<div class="chart-caption"><span>Weekly COT through {market["as_of"]} · daily price through {price_date}</span></div><p class="interpretation">{escape(market["interpretation"])}</p>'
                     '<details class="details"><summary>Sources and interpretation</summary><p>Positive bars are net long; negative bars are net short. The five colors identify trader groups, not buy/sell signals. Hover on bars and candles for values. Positions are weekly Tuesday observations, normally published Friday; historical bars are placed at observation dates and are not a point-in-time trading signal.</p>'
                     '<p>Positioning: CFTC Traders in Financial Futures, consolidated contracts (S&P 500 code 13874+, Nasdaq-100 code 20974+). Prices: TradingView ES1!/NQ1! continuous E-mini contracts. Consolidated positioning covers a broader contract universe; continuous prices may reflect contract rolls. CME sessions opening at or after 17:00 Chicago time are labelled with the following session date. Price and positioning have separate scales and observation dates.</p>'
                     '<p>Source archives, download timestamps, hashes, gross positions, open interest and small source reconciliation residuals are retained in report JSON. A short history alone does not establish a statistically extreme position.</p></details></article>')
    return '<div style="overflow-x:auto">' + ''.join(cards) + '</div>'
