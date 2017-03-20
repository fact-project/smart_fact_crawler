import html
import requests
import urllib
from datetime import datetime
import re

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


def extract_run_id_from_system_status(system_status):
    '''
    system_status: string like 'data(47) [1169/279s]' or 'Idle [pedestal]'
    returns: integer `run_id`
        or None if no number between braces `()` found in system_status.

    throws TypeError in case `system_status` is not string like
    enough to be used inside re.match()
    '''
    run_id_in_system_status_pattern = r'.*\((\d+)\).*'
    match_run_id = re.match(run_id_in_system_status_pattern, system_status)
    if match_run_id is None:
        run_id = None
    else:
        run_id = int(match_run_id.groups()[0])
    return run_id
