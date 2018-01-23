import requests
import schedule
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import logging
from time import sleep
from functools import partial

logging.basicConfig(level=logging.INFO)


url = 'http://fact-project.org/smartfact/data/{}.data'
files = [
    'agilent24.data',
    'agilent50.data',
    'biastemp.data',
    'boardrates.data',
    'cam-biascontrol-current.bin',
    'cam-biascontrol-voltage.bin',
    'cam-fadcontrol-eventdata.bin',
    'cam-feedback-overvoltage.bin',
    'cam-fsccontrol-temperature.bin',
    'cam-ftmcontrol-boardrates.bin',
    'cam-ftmcontrol-patchrates.bin',
    'cam-ftmcontrol-thresholds-board.bin',
    'cam-ftmcontrol-thresholds-patch.bin',
    'camtemp.data',
    'current.data',
    'current-prediction.data',
    'dew.data',
    'error.data',
    'errorhist.data',
    'fact.data',
    'fad.data',
    'feedback.data',
    'fsc.data',
    'ftm.data',
    'ftu.data',
    'gps.data',
    'gusts.data',
    'hist-biascontrol-current.bin',
    'hist-control-deviation.bin',
    'hist-current-prediction.bin',
    'hist-fsccontrol-temperature.bin',
    'hist-ftmcontrol-triggerrate.bin',
    'hist-magicweather-dew.bin',
    'hist-magicweather-gusts.bin',
    'hist-magicweather-hum.bin',
    'hist-magicweather-press.bin',
    'hist-magicweather-temp.bin',
    'hist-magicweather-wind.bin',
    'hist-pfmini-hum.bin',
    'hist-pfmini-temp.bin',
    'hist-ratecontrol-threshold.bin',
    'hist-temperaturecontrol.bin',
    'hist-tng-dust.bin',
    'hist-visibility.bin',
    'hum.data',
    'moon.data',
    'observations.data',
    'patchrates.data',
    'pfmini.data',
    'pointing.data',
    'press.data',
    'scriptlog.data',
    'source.data',
    'source-list.data',
    'sqm.data',
    'status.data',
    'sun.data',
    'temp.data',
    'temperature.data',
    'thresholds-board.data',
    'thresholds.data',
    'thresholds-patch.data',
    'tngdust.data',
    'tracking.data',
    'trigger.data',
    'visibility.data',
    'voltage.data',
    'weather.data',
    'wind.data',
]


def download(url, outputfile):
    try:
        ret = requests.get(url)
        ret.raise_for_status()

        with open(outputfile, 'w') as f:
            f.write(ret.text)
    except requests.ConnectionError:
        logging.error('Could not download {}'.format(url))


def make_output_dir():
    now = datetime.utcnow()

    output_directory = '{}/{:02d}/{:02d}/{:%H%M}'.format(
        now.year, now.month, now.day, now
    )
    os.makedirs(output_directory, exist_ok=True)

    return output_directory


def make_out_path(output_directory, filename):
    os.path.join(
        output_directory, '{}.data'.format(filename)
    )


def download_all():
    logging.info('Start downloading all')
    output_directory = make_output_dir()
    out_path = partial(make_out_path, output_directory)

    with ThreadPoolExecutor(max_workers=len(files)) as executor:
        for filename in files:
            executor.submit(
                download,
                url.format(filename),
                out_path(filename)
            )


def download_all_without_executor():
    logging.info('Start download_all_without_executor')
    output_directory = make_output_dir()
    out_path = partial(make_out_path, output_directory)

    for filename in files:
        download(
            url.format(filename),
            out_path(filename)
        )

if __name__ == '__main__':
    while True:
        download_all_without_executor()
        sleep(5 * 60)

