import locale
import os
import sys
import tempfile
import webbrowser
from dataclasses import dataclass
from importlib import resources as pkg_resources
from os.path import expanduser, dirname, realpath, join, exists

import requests

from .. import instruments
from . import resources

_CHART_JS_URL = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.0.1/chart.umd.js'
_CACHE_DIR = expanduser(join(dirname(realpath(__file__)), 'cache'))
_CHART_JS_CACHE_FILE = expanduser(join(_CACHE_DIR, 'chart.js'))
_DEFAULT_LOCALE = locale.getlocale()[0].replace('_', '-')
try:
    locale.setlocale(locale.LC_ALL, '')
    _DEFAULT_CURRENCY = locale.localeconv().get('int_curr_symbol').strip()
except:
    _DEFAULT_CURRENCY = 'USD'


@dataclass
class _Chart:
    title: str
    allocations: dict[str, float]

    def __repr__(self):
        return '{ title: "' + self.title + '", allocations: ' + str(self.allocations) + ' }'


def generate(title: str,
             value_by_ticker: dict[str, float],
             currency: str = _DEFAULT_CURRENCY,
             user_locale: str = _DEFAULT_LOCALE):
    data_by_ticker = instruments.get_data(list(value_by_ticker.keys()))
    _generate_report(title, currency, user_locale, [
        _Chart(title, value_by_ticker),
        _Chart('Allocation by currency', _value_by_field('currencies', value_by_ticker, data_by_ticker)),
        _Chart('Allocation by country', _value_by_field('countries', value_by_ticker, data_by_ticker)),
        _Chart('Allocation by industry', _value_by_field('industries', value_by_ticker, data_by_ticker)),
        _Chart('Allocation by asset class', _value_by_field('classes', value_by_ticker, data_by_ticker))
    ])


def _value_by_field(field: str,
                    value_by_ticker: dict[str, float],
                    data_by_ticker: dict[str, dict]) -> dict[str, float]:
    result = {}
    for ticker, volume in value_by_ticker.items():
        data = data_by_ticker.get(ticker)
        if data is None:
            print('No data for ticker "' + ticker + '", allocation report will not reflect it', file=sys.stderr)
            continue
        share_by_value = data.get(field)
        if share_by_value is None:
            continue
        for value, share in share_by_value.items():
            if share == 0:
                continue
            result[value] = result.setdefault(value, 0) + volume * share
    return result


def _generate_report(title: str, currency: str, user_locale: str, charts: list[_Chart]):
    _ensure_chart_js_downloaded()
    report = pkg_resources.read_text(resources, 'report_template.html') \
        .replace('%PLACEHOLDER%', str(charts)) \
        .replace('%CHART_JS%', _CHART_JS_CACHE_FILE) \
        .replace('%CURRENCY%', currency) \
        .replace('%LOCALE%', user_locale) \
        .replace('%TITLE%', title)
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
        file.write(report)
        webbrowser.open('file://' + file.name)


def _ensure_chart_js_downloaded():
    if exists(_CHART_JS_CACHE_FILE):
        return
    os.makedirs(name=_CACHE_DIR, mode=0o755, exist_ok=True)
    with open(_CHART_JS_CACHE_FILE, 'w') as file:
        file.write(requests.get(_CHART_JS_URL).text)
