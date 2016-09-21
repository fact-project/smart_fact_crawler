import html
import requests
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


def smartfact2table(url):
    if url.startswith('http'):
        ret = requests.get(url, timeout=1)
        ret.raise_for_status()
        text = ret.text

    else:
        with open(url) as f:
            text = f.read()

    return parse_table(text)
