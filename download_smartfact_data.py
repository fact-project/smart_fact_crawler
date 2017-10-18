import requests
import schedule
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import logging
from time import sleep

logging.basicConfig(level=logging.INFO)


url = 'http://fact-project.org/smartfact/data/{}.data'
files = [
    'tracking',
    'pointing',
    'sqm',
    'sun',
    'weather',
    'current',
    'voltage',
    'status',
    'temperature',
    'source',
    'fsc',
    'fact',
    'trigger',
    'errorhist',
    'observations',
]


def download(url, outputfile):
    try:
        ret = requests.get(url)
        ret.raise_for_status()

        with open(outputfile, 'w') as f:
            f.write(ret.text)
    except requests.ConnectionError:
        logging.error('Could not download {}'.format(url))


def download_all():
    logging.info('Start downloading all')
    now = datetime.utcnow()

    output_directory = '{}/{:02d}/{:02d}'.format(now.year, now.month, now.day)
    os.makedirs(output_directory, exist_ok=True)

    with ThreadPoolExecutor(max_workers=7) as executor:
        for filename in files:
            executor.submit(
                download,
                url.format(filename),
                os.path.join(
                    output_directory, '{}_{:%H%M}.data'.format(filename, now)
                )
            )


if __name__ == '__main__':
    download_all()

    schedule.every(5).minutes.do(download_all)
    while True:
        schedule.run_pending()
        sleep(10)
