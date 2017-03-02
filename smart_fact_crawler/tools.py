import html
import requests
import urllib
from datetime import datetime


def str2float(text):
    try:
        number = float(text)
    except:
        number = float("nan")

    return number


def smartfact_time2datetime(fact_timestamp):
    return datetime.utcfromtimestamp(
        str2float(fact_timestamp) / 1000.0
    )


def parse_table(text):
    return [
        line.split('\t')
        for line in html.unescape(text).splitlines()
    ]


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

    return parse_table(text)
