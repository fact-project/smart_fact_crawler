# -*- encoding:utf-8 -*-
import os.path
from datetime import datetime
from datetime import timedelta

from .tools import str2float as s2f
from .tools import smartfact_time2datetime as sft2dt
from .tools import smartfact2table
from .tools import get_entry

import re

from collections import namedtuple
from functools import partial


smartfacturl = "http://fact-project.org/smartfact/data/"

Quantity = namedtuple('Quantity', ['value', 'unit'])


run_re = re.compile(
    r'([0-9]{2}:[0-9]{2}:[0-9]{2}) '  # match the time part
    r'<#[a-z]+>'                      # html color
    r'([a-zA-Z\-]+) '                 # run type
    r'\[([a-zA-Z0-9+.\-() ]+)\] '           # source name
    r'\(Run (\d+)\)'                  # run number
    r'</#>'
)
Run = namedtuple('Run', ['start', 'type', 'source', 'id'])


def to_namedtuple(name, dictionary):
    return namedtuple(name, dictionary.keys())(**dictionary)


def smartfact(timeout=None, fallback=False):
    functions = [
        status,
        drive_tracking,
        drive_pointing,
        sun,
        weather,
        tng_weather,
        sipm_currents,
        sipm_voltages,
        container_temperature,
        current_source,
        camera_climate,
        main_page,
        trigger_rate,
        errorhist,
    ]
    return to_namedtuple(
        'SmartFact',
        {f.__name__: f(timeout=timeout, fallback=fallback) for f in functions}
    )


def drive_tracking(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'tracking.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    return to_namedtuple('TrackingPage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'source_name': get(table, 1, 1),
        'right_ascension': Quantity(s2f(get(table, 2, 1)), 'hourangle'),
        'declination': Quantity(s2f(get(table, 3, 1)), 'deg'),
        'zenith_distance': Quantity(s2f(get(table, 4, 1)), 'deg'),
        'azimuth': Quantity(s2f(get(table, 5, 1)), 'deg'),
        'control_deviation': Quantity(s2f(get(table, 6, 1)), 'arcsec'),
        'moon_distance': Quantity(s2f(get(table, 7, 1)), 'deg'),
    })


def drive_pointing(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'pointing.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    return to_namedtuple('PointingPage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'azimuth': Quantity(s2f(get(table, 1, 1)), 'deg'),
        'zenith_distance': Quantity(s2f(get(table, 2, 1)), 'deg'),
    })


def sun(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'sun.data')

    def next_datetime_from_hhmm_string(hhmm):
        if hhmm is None:
            return None

        now = datetime.utcnow()
        hour = int(hhmm[0:2])
        minute = int(hhmm[3:5])

        new_date = now.replace(hour=hour, minute=minute, second=0)
        if not new_date > now:
            new_date += timedelta(days=1)

        return new_date

    conv = next_datetime_from_hhmm_string

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    return to_namedtuple('SunPage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'end_of_dark_time': conv(get(table, 1, 1)),
        'end_of_astronomical_twilight': conv(get(table, 2, 1)),
        'end_of_nautical_twilight': conv(get(table, 3, 1)),
        'start_of_day_time': conv(get(table, 4, 1)),
        'end_of_day_time': conv(get(table, 5, 1)),
        'start_of_nautical_twilight': conv(get(table, 6, 1)),
        'start_of_astronomical_twilight': conv(get(table, 7, 1)),
        'start_of_dark_time': conv(get(table, 8, 1)),
    })


def weather(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'weather.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    return to_namedtuple('WeatherPage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'sun': get(table, 1, 1),
        'moon': get(table, 2, 1),
        'temperature': Quantity(s2f(get(table, 3, 1)), 'deg_C'),
        'dew_point': Quantity(s2f(get(table, 3, 1)), 'deg_C'),
        'humidity': Quantity(s2f(get(table, 5, 1)), '%'),
        'pressure': Quantity(s2f(get(table, 6, 1)), 'hPa'),
        'wind_speed': Quantity(s2f(get(table, 7, 1)), 'km/h'),
        'wind_gusts': Quantity(s2f(get(table, 8, 1)), 'km/h'),
        'wind_direction': get(table, 9, 1),
        'dust_tng': Quantity(s2f(get(table, 10, 1)), 'ug/m3'),
        'dust_gtc': Quantity(s2f(get(table, 11, 1)), 'ug/m3'),
    })


def tng_weather(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'tngdata.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    return to_namedtuple('TNGWeather', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'temperature': Quantity(s2f(get(table, 1, 1)), 'deg_C'),
        'delta_temperature_24h': Quantity(s2f(get(table, 2, 1)), 'deg_C'),
        'dew_point': Quantity(s2f(get(table, 3, 1)), 'deg_C'),
        'humidity': Quantity(s2f(get(table, 4, 1)), '%'),
        'pressure': Quantity(s2f(get(table, 5, 1)), 'hPa'),
        'wind_speed': Quantity(s2f(get(table, 6, 1)), 'km/h'),
        'wind_direction': Quantity(s2f(get(table, 7, 1)), 'deg'),
        'dust_total': Quantity(s2f(get(table, 8, 1)), 'ug/m3'),
        'solarimeter': Quantity(s2f(get(table, 9, 1)), 'W/m2'),
    })


def sipm_currents(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'current.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)
    calibrated = get(table, 1, 1)

    power_str = get(table, 6, 1, default='')
    # we expect something like 5W [4mW]
    match = re.match(r'(\d+)([a-zA-Z]+)\s*\[(\d+)([a-zA-Z]+)\]', power_str)
    if match is not None:
        cam_value, cam_unit, gapd_value, gapd_unit = match.groups()
        power_camera = Quantity(s2f(cam_value), cam_unit)
        power_gapd = Quantity(s2f(gapd_value), gapd_unit)
    else:
        power_camera = Quantity(float('nan'), 'W')
        power_gapd = Quantity(float('nan'), 'W')

    return to_namedtuple('CurrentPage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'calibrated':  calibrated == 'yes' if calibrated is not None else None,
        'min_per_sipm': Quantity(s2f(get(table, 2, 1)), 'uA'),
        'median_per_sipm': Quantity(s2f(get(table, 3, 1)), 'uA'),
        'mean_per_sipm': Quantity(s2f(get(table, 4, 1)), 'uA'),
        'max_per_sipm': Quantity(s2f(get(table, 5, 1)), 'uA'),
        'power_camera': power_camera,
        'power_gapd': power_gapd,
    })


def sipm_voltages(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'voltage.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    return to_namedtuple('VoltagePage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'min': Quantity(s2f(get(table, 1, 1)), 'V'),
        'median': Quantity(s2f(get(table, 2, 1)), 'V'),
        'mean': Quantity(s2f(get(table, 3, 1)), 'V'),
        'max': Quantity(s2f(get(table, 4, 1)), 'V'),
    })


def status(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'status.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    value, unit = get(table, 31, 1, default='nan nan').split(' ')[:2]
    storage_newdaq = Quantity(s2f(value), unit)

    value, unit = get(table, 32, 1, default='nan nan').split(' ')[:2]
    storage_daq = Quantity(s2f(value), unit)

    return to_namedtuple('StatusPage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'dim': get(table, 1, 1),
        'dim_control': get(table, 2, 1),
        'mcp': get(table, 3, 1),
        'datalogger': get(table, 4, 1),
        'drive_control': get(table, 5, 1),
        'drive_pc_time_check': get(table, 6, 1),
        'fad_control': get(table, 7, 1),
        'ftm_control': get(table, 8, 1),
        'bias_control': get(table, 9, 1),
        'feedback': get(table, 10, 1),
        'rate_control': get(table, 11, 1),
        'fsc_control': get(table, 12, 1),
        'pfmini_control': get(table, 13, 1),
        'bias_temp': get(table, 14, 1),
        'gps_control': get(table, 15, 1),
        'sqm_control': get(table, 16, 1),
        'agilent_control_24v': get(table, 17, 1),
        'agilent_control_50v': get(table, 18, 1),
        'agilent_control_80v': get(table, 19, 1),
        'power_control': get(table, 20, 1),
        'lid_control': get(table, 21, 1),
        'ratescan': get(table, 22, 1),
        'magic_weather': get(table, 23, 1),
        'tng_weather': get(table, 24, 1),
        'gtc_dust': get(table, 25, 1),
        'magic_lidar': get(table, 26, 1),
        'temperature': get(table, 27, 1),
        'rain_sensor': get(table, 28, 1),
        'chat_server': get(table, 29, 1),
        'skype_client': get(table, 30, 1),
        'free_space_newdaq': storage_newdaq,
        'free_space_daq': storage_daq,
        'smartfact_runtime': get(table, 33, 1),
    })


def container_temperature(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'temperature.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    return to_namedtuple('ContainerTemperaturePage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'daily_min': Quantity(get(table, 1, 1), 'deg_C'),
        'current': Quantity(get(table, 2, 1), 'deg_C'),
        'daily_max': Quantity(get(table, 3, 1), 'deg_C'),
    })


def current_source(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'source.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    return to_namedtuple('SourcePage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'name': get(table, 1, 1),
        'right_ascension': Quantity(s2f(get(table, 2, 1)), 'h'),
        'declination': Quantity(s2f(get(table, 3, 1)), 'deg'),
        'wobble_offset': Quantity(s2f(get(table, 4, 1)), 'deg'),
        'wobble_angle': Quantity(s2f(get(table, 5, 1)), 'deg'),
    })


def camera_climate(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'fsc.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    return to_namedtuple('CameraClimatePage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'humidity_mean': Quantity(s2f(get(table, 1, 1)), '%'),
        'relative_temperature_max': Quantity(s2f(get(table, 2, 1)), 'deg_C'),
        'relative_temperature_mean': Quantity(s2f(get(table, 3, 1)), 'deg_C'),
        'relative_temperature_min': Quantity(s2f(get(table, 4, 1)), 'deg_C'),
    })


def main_page(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'fact.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    humidity = get(table, 4, 1, default='')

    if humidity.lower().strip() != 'rain':
        humidity = s2f(humidity)

    system_status = get(table, 1, 1)
    return to_namedtuple('MainPage', {
        'timestamp_1': sft2dt(get(table, 0, 0)),
        'timestamp_2': sft2dt(get(table, 0, 1)),
        'system_status': system_status,
        'relative_camera_temperature': Quantity(s2f(get(table, 3, 1)), 'deg_C'),
        'humidity': humidity,
        'wind_speed': Quantity(s2f(get(table, 4, 2)), 'km/h'),
    })


def trigger_rate(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'trigger.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    return to_namedtuple('TriggerPage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'trigger_rate': Quantity(s2f(get(table, 1, 1)), '1/s'),
    })


def errorhist(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'errorhist.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    history = [
        h
        for h in get(table, 1, 1, default='').split("<->")[1].split("<br/>")
        if h
    ]
    return to_namedtuple('ErrorHistPage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'history': history,
    })


def build_run(tup):
    start, run_type, source, run_id = tup
    run_id = int(run_id)

    now = datetime.utcnow()
    start = datetime.strptime(start, '%H:%M:%S').replace(
        year=now.year, month=now.month, day=now.day
    )

    if start > now:
        start -= timedelta(hours=24)

    return Run(start, run_type, source, run_id)


def observations(url=None, timeout=None, fallback=False):
    if url is None:
        url = os.path.join(smartfacturl, 'observations.data')

    table = smartfact2table(url, timeout=timeout)
    get = partial(get_entry, fallback=fallback)

    run_list = get(table, 1, 1)
    if run_list is not None:
        runs = list(map(build_run, run_re.findall(table[1][1])))
        runs.sort(key=lambda r: r.id)
    else:
        runs = None

    return to_namedtuple('ErrorHistPage', {
        'timestamp': sft2dt(get(table, 0, 0)),
        'runs': runs,
    })
