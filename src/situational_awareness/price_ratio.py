"""Aligned daily price-ratio studies over archived single-provider bars."""
from datetime import date, datetime, timezone
from html import escape
import math
import hashlib
from zoneinfo import ZoneInfo

from situational_awareness.bar_store import ROOT as BAR_ROOT, load_bars
from situational_awareness.theme_returns import months_before
from situational_awareness.providers import alpaca_symbol

RSPD_RSPS = ('AMEX:RSPD', 'AMEX:RSPS')
RATIO_STUDIES = (
    dict(numerator=RSPD_RSPS[0], denominator=RSPD_RSPS[1], title='Consumer discretionary / staples',
         numerator_label='equal-weight consumer discretionary', denominator_label='equal-weight consumer staples',
         context='This describes cyclical-versus-defensive sector leadership.'),
    dict(numerator='AMEX:SPY', denominator='AMEX:XLP', title='S&P 500 / consumer staples',
         numerator_label='S&P 500', denominator_label='consumer staples',
         context='This compares the broad large-cap market with its consumer staples sector.'),
    dict(numerator='AMEX:SPY', denominator='AMEX:IWM', title='S&P 500 / small caps',
         numerator_label='S&P 500', denominator_label='Russell 2000 small caps',
         context='A rising ratio favors large caps; a falling ratio favors small caps.'),
)
RATIO_SYMBOLS = tuple(sorted({s for study in RATIO_STUDIES for s in (study['numerator'], study['denominator'])}))


def ratio_points(numerator, denominator):
    """Preserve gaps: a ratio requires two finite, positive same-day closes."""
    points = []
    for day in sorted(set(numerator) | set(denominator)):
        a, b = numerator.get(day), denominator.get(day)
        valid = all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v > 0 for v in (a, b))
        points.append({'date': day.isoformat(), 'value': a / b if valid else None})
    return points


def build_price_ratio(numerator, denominator, as_of, *, months=6, data_root=BAR_ROOT,
                      provider='tradingview', download_date=None, title=None,
                      numerator_label=None, denominator_label=None, context=None):
    """Build any exchange-qualified US stock/ETF ratio using one paired batch."""
    if provider not in ('tradingview', 'alpaca'):
        raise ValueError('Unsupported ratio provider')
    if not all(isinstance(s, str) and ':' in s for s in (numerator, denominator)):
        raise ValueError('Provide exchange-qualified symbols for both ratio legs')
    symbols = (numerator, denominator) if provider == 'tradingview' else (alpaca_symbol(numerator), alpaca_symbol(denominator))
    label = f"{numerator.split(':')[-1]} / {denominator.split(':')[-1]}"
    numerator_label = numerator_label or numerator.split(':')[-1]
    denominator_label = denominator_label or denominator.split(':')[-1]
    result = {'title': title or label, 'ratio_label': label,
              'chart_id': 'ratio-' + hashlib.sha256(f'{numerator}/{denominator}'.encode()).hexdigest()[:12],
              'numerator': numerator, 'denominator': denominator,
              'numerator_label': numerator_label, 'denominator_label': denominator_label,
              'symbols': list(symbols), 'provider': provider,
              'months': months, 'points': [], 'used_symbols': []}
    try:
        if any(s is None for s in symbols):
            raise ValueError('Provider cannot supply both ratio legs')
        payload = load_bars(symbols, data_root, provider=provider, download_date=download_date)
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
            result['interpretation'] = f'The {label} price ratio is {latest["value"]:.3f}, with insufficient paired history for a one-month comparison. '
        else:
            direction = 'outperformed' if change > 0 else 'underperformed' if change < 0 else 'matched'
            result['interpretation'] = f'The {label} ratio is {latest["value"]:.3f}, changing {change:+.1f}% over the past month; {numerator_label} has {direction} {denominator_label} on a price basis. '
        result['interpretation'] += context or 'This describes relative price performance, not a count of participating stocks.'
    except ValueError as error:
        result['unavailable'] = str(error)
    return result


def ratio_card(section):
    if not section:
        return ''
    heading_id = section['chart_id']
    title = f'<h3 id="{heading_id}">{escape(section["title"])}</h3>'
    label = escape(section['ratio_label'])
    if section.get('unavailable'):
        return f'<article class="card" style="margin-top:24px">{title}<p class="unavailable">{label}: {escape(section["unavailable"])}</p></article>'
    points = section['points']
    values = [p['value'] for p in points if p['value'] is not None]
    low, high = min(values), max(values)
    padding = max((high-low)*.1, abs(high)*.005)
    low, high = low-padding, high+padding
    start, end = (date.fromisoformat(points[i]['date']).toordinal() for i in (0, -1))
    x = lambda day: 65 + 900 * (date.fromisoformat(day).toordinal()-start) / max(1, end-start)
    y = lambda value: 265 - 220 * (value-low)/(high-low)
    svg = [f'<svg viewBox="0 0 1000 315" role="img" aria-label="{label} daily closing-price ratio">']
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
    return (f'<article class="card" style="margin-top:24px" aria-labelledby="{heading_id}"><div class="card-header"><div>{title}<p class="subheading">{label} · daily closing-price ratio</p></div><span class="period">{section["months"]}-month view</span></div>'
            f'<div class="readings"><span>Ratio <strong>{section["latest"]:.3f}</strong> · {section["as_of"]}{provisional}</span></div><div class="chart">' + ''.join(svg) + '</div>'
            f'<p class="interpretation">{escape(section["interpretation"])}</p><details class="details"><summary>Ratio calculation and sources</summary>'
            f'<p>{escape(section["numerator_label"])} close divided by {escape(section["denominator_label"])} close for the same US session. Rising means the numerator outperforms the denominator; both ETFs may still be rising or falling. This is an unrebased price ratio; dividends are excluded and the level 1 has no special signal meaning.</p><p>Provider: {escape(section["provider"])} · paired download batch {section["download_date"]}. No dates or providers are mixed within this ratio; missing/invalid closes produce chart gaps.{gap_note} Raw input hashes and observation dates are in report JSON.</p></details></article>')


def build_breadth_ratios(as_of, **kwargs):
    """All configured studies share the same builder and renderer."""
    return [build_price_ratio(as_of=as_of, **study, **kwargs) for study in RATIO_STUDIES]


def build_rspd_rsps(as_of, **kwargs):
    """Compatibility helper delegating to the general ratio implementation."""
    return build_price_ratio(as_of=as_of, **RATIO_STUDIES[0], **kwargs)
