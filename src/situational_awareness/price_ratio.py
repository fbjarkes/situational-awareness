"""Aligned daily price-ratio studies over archived single-provider bars."""
from datetime import date, datetime, timezone
from html import escape
import math
from zoneinfo import ZoneInfo

from situational_awareness.bar_store import ROOT as BAR_ROOT, load_bars
from situational_awareness.theme_returns import months_before

RSPD_RSPS = ('AMEX:RSPD', 'AMEX:RSPS')


def ratio_points(numerator, denominator):
    """Preserve gaps: a ratio requires two finite, positive same-day closes."""
    points = []
    for day in sorted(set(numerator) | set(denominator)):
        a, b = numerator.get(day), denominator.get(day)
        valid = all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v > 0 for v in (a, b))
        points.append({'date': day.isoformat(), 'value': a / b if valid else None})
    return points


def build_rspd_rsps(as_of, *, months=6, data_root=BAR_ROOT, provider='tradingview'):
    symbols = RSPD_RSPS if provider == 'tradingview' else ('RSPD', 'RSPS')
    result = {'title': 'RSPD / RSPS', 'symbols': list(symbols), 'provider': provider,
              'months': months, 'points': [], 'used_symbols': []}
    try:
        payload = load_bars(symbols, data_root, provider=provider)
        closes = {}
        for symbol in symbols:
            prices = {}
            zone = ZoneInfo(payload.get('session_timezones', {}).get(symbol, 'America/New_York'))
            for bar in payload['series'][symbol]:
                day = datetime.fromtimestamp(bar['t'], timezone.utc).astimezone(zone).date()
                if day <= as_of:
                    prices[day] = bar.get('c')
            closes[symbol] = prices
        history = ratio_points(closes[symbols[0]], closes[symbols[1]])
        valid = [p for p in history if p['value'] is not None]
        if not valid:
            raise ValueError('No paired positive closes on or before the report date')
        latest = valid[-1]
        previous = next((p for p in reversed(valid) if p['date'] <= months_before(date.fromisoformat(latest['date']), 1).isoformat()), None)
        change = 100 * (latest['value'] / previous['value'] - 1) if previous else None
        fetched = datetime.fromisoformat(payload['fetched_at'].replace('Z', '+00:00')).astimezone(ZoneInfo('America/New_York'))
        result.update(as_of=latest['date'], latest=latest['value'], change_1m_pct=change,
                      change_start=previous['date'] if previous else None,
                      intraday=latest['date'] == fetched.date().isoformat() and (fetched.hour, fetched.minute) < (16, 0),
                      points=[p for p in history if p['date'] >= months_before(as_of, months).isoformat()],
                      download_date=payload['download_date'], input_bar_files=payload['bar_files'],
                      fetched_at=payload['fetched_at'], used_symbols=list(symbols),
                      latest_pair_missing=bool(history and history[-1]['value'] is None))
        if not any(p['value'] is not None for p in result['points']):
            raise ValueError('No paired history in the requested chart window')
        if change is None:
            result['interpretation'] = f'The RSPD/RSPS price ratio is {latest["value"]:.3f}, with insufficient paired history for a one-month comparison. '
        else:
            direction = 'outperformed' if change > 0 else 'underperformed' if change < 0 else 'matched'
            result['interpretation'] = f'The RSPD/RSPS ratio is {latest["value"]:.3f}, changing {change:+.1f}% over the past month; equal-weight consumer discretionary has {direction} consumer staples on a price basis. '
        result['interpretation'] += 'This describes cyclical-versus-defensive sector leadership, rather than the number of stocks participating in a move.'
    except ValueError as error:
        result['unavailable'] = str(error)
    return result


def ratio_card(section):
    if not section:
        return ''
    title = '<h3 id="rspd-rsps-title">Consumer discretionary / staples</h3>'
    if section.get('unavailable'):
        return f'<article class="card" style="margin-top:24px">{title}<p class="unavailable">RSPD / RSPS: {escape(section["unavailable"])}</p></article>'
    points = section['points']
    values = [p['value'] for p in points if p['value'] is not None]
    low, high = min(values), max(values)
    padding = max((high-low)*.1, abs(high)*.005)
    low, high = low-padding, high+padding
    start, end = (date.fromisoformat(points[i]['date']).toordinal() for i in (0, -1))
    x = lambda day: 65 + 900 * (date.fromisoformat(day).toordinal()-start) / max(1, end-start)
    y = lambda value: 265 - 220 * (value-low)/(high-low)
    svg = ['<svg viewBox="0 0 1000 315" role="img" aria-label="RSPD divided by RSPS daily closing-price ratio">']
    for i in range(5):
        value = low + (high-low)*i/4
        svg.append(f'<line x1="65" x2="965" y1="{y(value):.1f}" y2="{y(value):.1f}" stroke="#2d3b4b"/><text x="55" y="{y(value)+4:.1f}" text-anchor="end">{value:.3f}</text>')
    segment = []
    for p in points + [{'value': None}]:
        if p['value'] is None:
            if segment:
                svg.append('<polyline points="' + ' '.join(segment) + '" fill="none" stroke="#67ddc4" stroke-width="2"/>')
                segment = []
        else:
            segment.append(f'{x(p["date"]):.1f},{y(p["value"]):.1f}')
    for day, anchor in ((points[0]['date'], 'start'), (points[-1]['date'], 'end')):
        svg.append(f'<text x="{x(day):.1f}" y="295" text-anchor="{anchor}">{day}</text>')
    svg.append('</svg>')
    provisional = ' · provisional intraday' if section.get('intraday') else ''
    gap_note = ' Latest input sessions are unmatched; the displayed reading is the last paired close.' if section.get('latest_pair_missing') else ''
    return (f'<article class="card" style="margin-top:24px" aria-labelledby="rspd-rsps-title"><div class="card-header"><div>{title}<p class="subheading">RSPD / RSPS · daily closing-price ratio</p></div><span class="period">{section["months"]}-month view</span></div>'
            f'<div class="readings"><span>Ratio <strong>{section["latest"]:.3f}</strong> · {section["as_of"]}{provisional}</span></div><div class="chart">' + ''.join(svg) + '</div>'
            f'<p class="interpretation">{escape(section["interpretation"])}</p><details class="details"><summary>Ratio calculation and sources</summary>'
            f'<p>RSPD close divided by RSPS close for the same US session. RSPD is the Invesco S&P 500 Equal Weight Consumer Discretionary ETF; RSPS is its Consumer Staples counterpart. Rising means discretionary outperforms staples; both ETFs may still be rising or falling. This is an unrebased price ratio; dividends are excluded and the level 1 has no special signal meaning.</p><p>Provider: {escape(section["provider"])} · paired download batch {section["download_date"]}. No dates or providers are mixed within this ratio; missing/invalid closes produce chart gaps.{gap_note} Raw input hashes and observation dates are in report JSON.</p></details></article>')
