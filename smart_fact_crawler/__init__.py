# -*- encoding:utf-8 -*-
import os.path
from datetime import datetime
from datetime import timedelta

from .tools import str2float as s2f
from .tools import smartfact_time2datetime as sft2dt
from .tools import smartfact2table
from .tools import extract_run_id_from_system_status

from collections import namedtuple


smartfacturl = "http://fact-project.org/smartfact/data/"

Quantity = namedtuple('Quantity', ['value', 'unit'])


def to_namedtuple(name, dictionary):
    return namedtuple(name, dictionary.keys())(**dictionary)


def smartfact(timeout=None):
    functions = [
        status,
        drive_tracking,
        drive_pointing,
        sqm,
        sun,
        weather,
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
        {f.__name__: f(timeout=timeout) for f in functions}
    )


def drive_tracking(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'tracking.data')
    table = smartfact2table(url, timeout=timeout)
    return to_namedtuple('TrackingPage', {
        'timestamp': sft2dt(table[0][0]),
        'source_name': table[1][1],
        'right_ascension': Quantity(s2f(table[2][1]), 'hourangle'),
        'declination': Quantity(s2f(table[3][1]), 'deg'),
        'zenith_distance': Quantity(s2f(table[4][1]), 'deg'),
        'azimuth': Quantity(s2f(table[5][1]), 'deg'),
        'control_deviation': Quantity(s2f(table[6][1]), 'arcsec'),
        'moon_distance': Quantity(s2f(table[7][1]), 'deg'),
    })


def drive_pointing(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'pointing.data')
    table = smartfact2table(url, timeout=timeout)
    return to_namedtuple('PointingPage', {
        'timestamp': sft2dt(table[0][0]),
        'azimuth': Quantity(s2f(table[1][1]), 'deg'),
        'zenith_distance': Quantity(s2f(table[2][1]), 'deg'),
    })


def sqm(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'sqm.data')
    table = smartfact2table(url, timeout=timeout)
    return to_namedtuple('SqmPage', {
        'timestamp': sft2dt(table[0][0]),
        'magnitude': Quantity(s2f(table[1][1]), 'mag'),
        'sensor_frequency': Quantity(s2f(table[2][1]), 'Hz'),
        'sensor_period': Quantity(s2f(table[4][1]), 's'),
        'sensor_temperature': Quantity(s2f(table[5][1]), 'deg_C'),
    })


def sun(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'sun.data')

    def next_datetime_from_hhmm_string(hhmm):
        now = datetime.utcnow()
        hour = int(hhmm[0:2])
        minute = int(hhmm[3:5])

        new_date = now.replace(hour=hour, minute=minute, second=0)
        if not new_date > now:
            new_date += timedelta(days=1)
        return new_date

    conv = next_datetime_from_hhmm_string

    table = smartfact2table(url, timeout=timeout)
    return to_namedtuple('SunPage', {
        'timestamp': sft2dt(table[0][0]),
        'end_of_dark_time': conv(table[1][1]),
        'end_of_astronomical_twilight': conv(table[2][1]),
        'end_of_nautical_twilight': conv(table[3][1]),
        'start_of_day_time': conv(table[4][1]),
        'end_of_day_time': conv(table[5][1]),
        'start_of_nautical_twilight': conv(table[6][1]),
        'start_of_astronomical_twilight': conv(table[7][1]),
        'start_of_dark_time': conv(table[8][1]),
    })


def weather(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'weather.data')
    table = smartfact2table(url, timeout=timeout)
    return to_namedtuple('WeatherPage', {
        'timestamp': sft2dt(table[0][0]),
        'sun': table[1][1],
        'moon': table[2][1],
        'temperature': Quantity(s2f(table[3][1]), 'deg_C'),
        'dew_point': Quantity(s2f(table[4][1]), 'deg_C'),
        'humidity': Quantity(s2f(table[5][1]), '%'),
        'pressure': Quantity(s2f(table[6][1]), 'hPa'),
        'wind_speed': Quantity(s2f(table[7][1]), 'km/h'),
        'wind_gusts': Quantity(s2f(table[8][1]), 'km/h'),
        'wind_direction': table[9][1],
        'dust_tng': Quantity(s2f(table[10][1]), 'ug/m3'),
    })


def sipm_currents(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'current.data')
    table = smartfact2table(url, timeout=timeout)
    return to_namedtuple('CurrentPage', {
        'timestamp': sft2dt(table[0][0]),
        'calibrated': table[1][1] == 'yes',
        'min_per_sipm': Quantity(s2f(table[2][1]), 'uA'),
        'median_per_sipm': Quantity(s2f(table[3][1]), 'uA'),
        'mean_per_sipm': Quantity(s2f(table[4][1]), 'uA'),
        'max_per_sipm': Quantity(s2f(table[5][1]), 'uA'),
        'power': Quantity(s2f(table[6][1][:-1]), 'W'),
    })


def sipm_voltages(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'voltage.data')
    table = smartfact2table(url, timeout=timeout)
    return to_namedtuple('VoltagePage', {
        'timestamp': sft2dt(table[0][0]),
        'min': Quantity(s2f(table[1][1]), 'V'),
        'median': Quantity(s2f(table[2][1]), 'V'),
        'mean': Quantity(s2f(table[3][1]), 'V'),
        'max': Quantity(s2f(table[4][1]), 'V'),
    })


def status(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'status.data')
    table = smartfact2table(url, timeout=timeout)

    value, unit = table[28][1].split(' ')[:2]
    storage_newdaq = Quantity(s2f(value), unit)

    value, unit = table[29][1].split(' ')[:2]
    storage_daq = Quantity(s2f(value), unit)

    return to_namedtuple('StatusPage', {
        'timestamp': sft2dt(table[0][0]),
        'dim': table[1][1],
        'dim_control': table[2][1],
        'mcp': table[3][1],
        'datalogger': table[4][1],
        'drive_control': table[5][1],
        'drive_pc_time_check': table[6][1],
        'fad_control': table[7][1],
        'ftm_control': table[8][1],
        'bias_control': table[9][1],
        'feedback': table[10][1],
        'rate_control': table[11][1],
        'fsc_control': table[12][1],
        'pfmini_control': table[13][1],
        'gps_control': table[14][1],
        'sqm_control': table[15][1],
        'agilent_control_24v': table[16][1],
        'agilent_control_50v': table[17][1],
        'agilent_control_80v': table[18][1],
        'power_control': table[19][1],
        'lid_control': table[20][1],
        'ratescan': table[21][1],
        'magic_weather': table[22][1],
        'tng_weather': table[23][1],
        'magic_lidar': table[24][1],
        'temperature': table[25][1],
        'chat_server': table[26][1],
        'skype_client': table[27][1],
        'free_space_newdaq': storage_newdaq,
        'free_space_daq': storage_daq,
        'smartfact_runtime': table[30][1],
    })


def container_temperature(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'temperature.data')
    table = smartfact2table(url, timeout=timeout)
    return to_namedtuple('ContainerTemperaturePage', {
        'timestamp': sft2dt(table[0][0]),
        'daily_min': Quantity(table[1][1], 'deg_C'),
        'current': Quantity(table[2][1], 'deg_C'),
        'daily_max': Quantity(table[3][1], 'deg_C'),
    })


def current_source(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'source.data')
    table = smartfact2table(url, timeout=timeout)
    return to_namedtuple('SourcePage', {
        'timestamp': sft2dt(table[0][0]),
        'name': table[1][1],
        'right_ascension': Quantity(s2f(table[2][1]), 'h'),
        'declination': Quantity(s2f(table[3][1]), 'deg'),
        'wobble_offset': Quantity(s2f(table[4][1]), 'deg'),
        'wobble_angle': Quantity(s2f(table[5][1]), 'deg'),
    })


def camera_climate(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'fsc.data')
    table = smartfact2table(url, timeout=timeout)
    return to_namedtuple('CameraClimatePage', {
        'timestamp': sft2dt(table[0][0]),
        'humidity_mean': Quantity(s2f(table[1][1]), '%'),
        'relative_temperature_max': Quantity(s2f(table[2][1]), 'deg_C'),
        'relative_temperature_mean': Quantity(s2f(table[3][1]), 'deg_C'),
        'relative_temperature_min': Quantity(s2f(table[4][1]), 'deg_C'),
    })


def main_page(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'fact.data')
    table = smartfact2table(url, timeout=timeout)

    try:
        humidity = Quantity(s2f(table[4][1]), '%')
        wind_speed = Quantity(s2f(table[4][2]), 'km/h')
    except IndexError:
        humidity = Quantity(float('nan'), '%')
        wind_speed = Quantity(float('nan'), 'km/h')

    system_status = table[1][1]
    return to_namedtuple('MainPage', {
        'timestamp_1': sft2dt(table[0][0]),
        'timestamp_2': sft2dt(table[0][1]),
        'system_status': system_status,
        'run_id': extract_run_id_from_system_status(system_status),
        'relative_camera_temperature': Quantity(s2f(table[3][1]), 'deg_C'),
        'humidity': humidity,
        'wind_speed': wind_speed,
    })


def trigger_rate(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'trigger.data')
    table = smartfact2table(url, timeout=timeout)
    return to_namedtuple('TriggerPage', {
        'timestamp': sft2dt(table[0][0]),
        'trigger_rate': Quantity(s2f(table[1][1]), '1/s'),
    })


def errorhist(url=None, timeout=None):
    if url is None:
        url = os.path.join(smartfacturl, 'errorhist.data')
    table = smartfact2table(url, timeout=timeout)
    history = [h for h in table[1][1].split("<->")[1].split("<br/>") if h]
    return to_namedtuple('ErrorHistPage', {
        'timestamp': sft2dt(table[0][0]),
        'history': history,
    })
