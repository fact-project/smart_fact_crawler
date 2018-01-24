import html
import requests
import urllib
from datetime import datetime


def str2float(text):
    try:
        number = float(text)
    except (ValueError, TypeError):
        number = float("nan")

    return number


def smartfact_time2datetime(fact_timestamp):
    if fact_timestamp is None:
        return None

    return datetime.utcfromtimestamp(
        str2float(fact_timestamp) / 1000.0
    )


def parse_table(text):
    return [line.split('\t') for line in text.splitlines()]


def smartfact2table(url, timeout=None):
    parsed_url = urllib.parse.urlparse(url)

    if parsed_url.scheme in ('http', 'https'):
        ret = requests.get(url, timeout=timeout)
        ret.raise_for_status()
        text = ret.text

    elif parsed_url.scheme in ('', 'file'):
        with open(parsed_url.path) as f:
            text = f.read()

    else:
        raise ValueError('Could not parse url: {}'.format(url))
    text = html.unescape(text)
    return parse_table(text), text


def get_entry(table, row, col, fallback=False, default=None):
    '''
    Get an element from a two dimensinoal list like the return value
    of smartfact2table, if fallback is True, default is returned for
    a non-existing element
    '''

    try:
        return table[row][col]
    except IndexError:
        if fallback is True:
            return default
        else:
            raise
