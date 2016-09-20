# -*- encoding:utf-8 -*-
from datetime import datetime
from datetime import timedelta

from .tools import str2float as s2f
from .tools import smartfact_time2datetime as sft2dt
from .table_crawler import TableCrawler

from collections import namedtuple

smartfacturl = "http://fact-project.org/smartfact/data/"

Quantity = namedtuple('Quantity', ['value', 'unit'])


def to_namedtuple(name, dictionary):
    return namedtuple(name, dictionary.keys())(**dictionary)


def smartfact():
    functions = [
        status,
        drive,
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
        errorhist]
    return to_namedtuple(
        'SmartFact',
        {f.__name__: f() for f in functions}
    )


def drive():
    return {
        "tracking": tracking(),
        "pointing": pointing(),
    }


def tracking(url=smartfacturl + 'tracking.data'):
    tc = TableCrawler(url)
    return to_namedtuple('TrackingPage', {
        'timestamp': sft2dt(tc[0, 0]),
        'source_name': str.join(' ', tc[1, 1:]),
        'right_ascension': Quantity(s2f(tc[2, 1]), 'hourangle'),
        'declination': Quantity(s2f(tc[3, 1]), 'deg'),
        'zenith_distance': Quantity(s2f(tc[4, 1]), 'deg'),
        'azimuth': Quantity(s2f(tc[5, 1]), 'deg'),
        'control_deviation': Quantity(s2f(tc[6, 1]), 'arcsec'),
        'moon_distance': Quantity(s2f(tc[7, 1]), 'deg'),
    })


def pointing(url=smartfacturl + 'pointing.data'):
    tc = TableCrawler(url)
    return to_namedtuple('PointingPage', {
        'timestamp': sft2dt(tc[0, 0]),
        'azimuth': Quantity(s2f(tc[1, 1]), 'deg'),
        'zenith_distance': Quantity(s2f(tc[2, 1]), 'deg'),
    })


def sqm(url=smartfacturl + 'sqm.data'):
    tc = TableCrawler(url)
    return to_namedtuple('SqmPage', {
        'timestamp': sft2dt(tc[0, 0]),
        'magnitude': Quantity(s2f(tc[1, 1]), 'mag'),
        'sensor_frequency': Quantity(s2f(tc[2, 1]), 'Hz'),
        'sensor_period': Quantity(s2f(tc[4, 1]), 's'),
        'sensor_temperature': Quantity(s2f(tc[5, 1]), 'deg_C'),
    })


def sun(url=smartfacturl + 'sun.data'):

    def next_datetime_from_hhmm_string(hhmm):
        now = datetime.utcnow()
        hour = int(hhmm[0:2])
        minute = int(hhmm[3:5])

        new_date = now.replace(hour=hour, minute=minute, second=0)
        if not new_date > now:
            new_date += timedelta(days=1)
        return new_date

    conv = next_datetime_from_hhmm_string

    tc = TableCrawler(url)
    return to_namedtuple('SunPage', {
        'timestamp': sft2dt(tc[0, 0]),
        'end_of_dark_time': conv(tc[1, 1]),
        'end_of_astronomical_twilight': conv(tc[2, 1]),
        'end_of_nautical_twilight': conv(tc[3, 1]),
        'start_of_day_time': conv(tc[4, 1]),
        'end_of_day_time': conv(tc[5, 1]),
        'start_of_nautical_twilight': conv(tc[6, 1]),
        'start_of_astronomical_twilight': conv(tc[7, 1]),
        'start_of_dark_time': conv(tc[8, 1]),
    })


def weather(url=smartfacturl + 'weather.data'):
    tc = TableCrawler(url)
    return to_namedtuple('WeatherPage', {
        'timestamp': sft2dt(tc[0, 0]),
        'sun': tc[1, 1],
        'moon': tc[2, 1],
        'temperature': Quantity(s2f(tc[3, 1]), 'deg_C'),
        'dew_point': Quantity(s2f(tc[4, 1]), 'deg_C'),
        'humidity': Quantity(s2f(tc[5, 1]), '%'),
        'pressure': Quantity(s2f(tc[6, 1]), 'hPa'),
        'wind_speed': Quantity(s2f(tc[7, 1]), 'km/h'),
        'wind_gusts': Quantity(s2f(tc[8, 1]), 'km/h'),
        'wind_direction': tc[9, 1],
        'dust_tng': Quantity(s2f(tc[10, 1]), 'ug/m3'),
    })


def sipm_currents(url=smartfacturl + 'current.data'):
    tc = TableCrawler(url)
    return to_namedtuple('CurrentPage', {
        'timestamp': sft2dt(tc[0, 0]),
        'calibrated': tc[1, 1] == 'yes',
        'min_per_sipm': Quantity(s2f(tc[2, 1]), 'uA'),
        'median_per_sipm': Quantity(s2f(tc[3, 1]), 'uA'),
        'mean_per_sipm': Quantity(s2f(tc[4, 1]), 'uA'),
        'max_per_sipm': Quantity(s2f(tc[5, 1]), 'uA'),
        'power': Quantity(s2f(tc[6, 1][:-1]), 'W'),
    })


def sipm_voltages(url=smartfacturl + 'voltage.data'):
    tc = TableCrawler(url)
    return to_namedtuple('VoltagePage', {
        'timestamp': sft2dt(tc[0, 0]),
        'min': Quantity(s2f(tc[1, 1]), 'V'),
        'median': Quantity(s2f(tc[2, 1]), 'V'),
        'mean': Quantity(s2f(tc[3, 1]), 'V'),
        'max': Quantity(s2f(tc[4, 1]), 'V'),
    })


def status(url=smartfacturl + 'status.data'):
    tc = TableCrawler(url)

    value, unit = tc[28, 1].split(' ')[:2]
    storage_newdaq = Quantity(s2f(value), unit)

    value, unit = tc[29, 1].split(' ')[:2]
    storage_daq = Quantity(s2f(value), unit)

    return to_namedtuple('StatusPage', {
        'timestamp': sft2dt(tc[0, 0]),
        'dim': tc[1, 1],
        'dim_control': tc[2, 1],
        'mcp': tc[3, 1],
        'datalogger': tc[4, 1],
        'drive_control': tc[5, 1],
        'drive_pc_time_check': tc[6, 1],
        'fad_control': tc[7, 1],
        'ftm_control': tc[8, 1],
        'bias_control': tc[9, 1],
        'feedback': tc[10, 1],
        'rate_control': tc[11, 1],
        'fsc_control': tc[12, 1],
        'pfmini_control': tc[13, 1],
        'gps_control': tc[14, 1],
        'sqm_control': tc[15, 1],
        'agilent_control_24v': tc[16, 1],
        'agilent_control_50v': tc[17, 1],
        'agilent_control_80v': tc[18, 1],
        'power_control': tc[19, 1],
        'lid_control': tc[20, 1],
        'ratescan': tc[21, 1],
        'magic_weather': tc[22, 1],
        'tng_weather': tc[23, 1],
        'magic_lidar': tc[24, 1],
        'temperature': tc[25, 1],
        'chat_server': tc[26, 1],
        'skype_client': tc[27, 1],
        'free_space_newdaq': storage_newdaq,
        'free_space_daq': storage_daq,
        'smartfact_runtime': tc[30, 1],
    })


def container_temperature(url=smartfacturl + 'temperature.data'):
    tc = TableCrawler(url)
    return to_namedtuple('ContainerTemperaturePage', {
        'timestamp': sft2dt(tc[0, 0]),
        'daily_min': Quantity(tc[1, 1], 'deg_C'),
        'current': Quantity(tc[2, 1], 'deg_C'),
        'daily_max': Quantity(tc[3, 1], 'deg_C'),
    })


def current_source(url=smartfacturl + 'source.data'):
    tc = TableCrawler(url)
    return to_namedtuple('SourcePage', {
        'timestamp': sft2dt(tc[0, 0]),
        'name': str.join(' ', tc[1, 1:]),
        'right_ascension': Quantity(s2f(tc[2, 1]), 'h'),
        'declination': Quantity(s2f(tc[3, 1]), 'deg'),
        'wobble_offset': Quantity(s2f(tc[4, 1]), 'deg'),
        'wobble_angle': Quantity(s2f(tc[5, 1]), 'deg'),
    })


def camera_climate(url=smartfacturl + 'fsc.data'):
    tc = TableCrawler(url)
    return to_namedtuple('CameraClimatePage', {
        'timestamp': sft2dt(tc[0, 0]),
        'humidity_mean': Quantity(s2f(tc[1, 1]), '%'),
        'relative_temperature_max': Quantity(s2f(tc[2, 1]), 'deg_C'),
        'relative_temperature_mean': Quantity(s2f(tc[3, 1]), 'deg_C'),
        'relative_temperature_min': Quantity(s2f(tc[4, 1]), 'deg_C'),
    })


def main_page(url=smartfacturl + 'fact.data'):
    tc = TableCrawler(url)
    return to_namedtuple('MainPage', {
        'timestamp_1': sft2dt(tc[0, 0]),
        'timestamp_2': sft2dt(tc[0, 1]),
        'system_status': ' '.join(tc[1, 1:]),
        'relative_camera_temperature': Quantity(s2f(tc[3, 1]), 'deg_C'),
        'humidity': Quantity(s2f(tc[4, 1]), '%'),
        'wind_speed': Quantity(s2f(tc[4, 2]), 'km/h'),
    })


def trigger_rate(url=smartfacturl + 'trigger.data'):
    tc = TableCrawler(url)
    return to_namedtuple('TriggerPage', {
        'timestamp': sft2dt(tc[0, 0]),
        'trigger_rate': Quantity(s2f(tc[1, 1]), '1/s'),
    })


def errorhist(url=smartfacturl + 'errorhist.data'):
    tc = TableCrawler(url)
    history = [h for h in tc[1, 1].split("<->")[1].split("<br/>") if len(h)]
    return to_namedtuple('ErrorHistPage', {
        'timestamp': sft2dt(tc[0, 0]),
        'history': history,
    })
