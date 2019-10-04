'''
downloads all files from both /data and /struct folder
downloads all .data, .bin and .page files.

you have to delete the files you do not want to use during testing yourself
'''

import requests
import schedule
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import logging
from time import sleep
from functools import partial
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


def get_file_urls(url):
    all_urls = []
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features='lxml')

    for link in soup.find_all('a'):
        full_url = url + link.get('href')
        if (
            full_url.endswith('.data') or
            full_url.endswith('.bin') or
            full_url.endswith('.page')
        ):
            print(full_url)
            all_urls.append(full_url)

    return all_urls


def download(url, outputfile):
    logging.info(f'{url} -> {outputfile}')
    try:
        ret = requests.get(url)
        ret.raise_for_status()

        with open(outputfile, 'w') as f:
            f.write(ret.text)
    except requests.exceptions.RequestException as e:
        logging.exception('Could not download {}'.format(url))


def make_output_dir(suffix=''):
    now = datetime.utcnow()

    output_directory = '{}_{:02d}_{:02d}_{:%H%M}{}'.format(
        now.year, now.month, now.day, now, suffix
    )
    os.makedirs(output_directory, exist_ok=True)

    return output_directory


def make_out_path(output_directory, filename):
    return os.path.join(output_directory, filename)


def download_all():
    logging.info('Start downloading all')
    for folder in ('data', 'struct'):

        url = f'http://fact-project.org/smartfact/{folder}/'
        output_directory = make_output_dir(suffix=f'/{folder}')
        out_path = partial(make_out_path, output_directory)

        files = get_file_urls(url)
        with ThreadPoolExecutor(max_workers=len(files)) as executor:
            for filename in files:
                executor.submit(
                    download,
                    filename,
                    out_path(os.path.split(filename)[-1])
                )


if __name__ == '__main__':
    download_all()
