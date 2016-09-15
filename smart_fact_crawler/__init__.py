# -*- encoding:utf-8 -*-
from datetime import datetime
from datetime import timedelta

from .tools import str2float as s2f
from .tools import smartfact_time2datetime as sft2dt
from .table_crawler import TableCrawler

from collections import namedtuple

def to_namedtuple(name, dictionary):
    return namedtuple(name, dictionary.keys())(**dictionary)

smartfacturl = "http://fact-project.org/smartfact/data/"

def all():
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
    return to_namedtuple('SmartFact',
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
        'timestamp': (sft2dt(tc[0, 0]), None),
        'source_name': (tc[1, 1:], None),
        'right_ascension': (s2f(tc[2, 1]), 'h'),
        'declination': (s2f(tc[3, 1]), 'deg'),
        'zenith_distance': (s2f(tc[4, 1]), 'deg'),
        'azimuth': (s2f(tc[5, 1]), 'deg'),
        'control_deviation': (s2f(tc[6, 1]), 'arcsec'),
        'moon_distance': (tc[7, 1], 'h'),
    })


def pointing(url=smartfacturl + 'pointing.data'):
    tc = TableCrawler(url)
    return to_namedtuple('PointingPage', {
        'timestamp': (sft2dt(tc[0, 0]), None),
        'azimuth': (s2f(tc[1, 1]), 'deg'),
        'zenith_distance': (s2f(tc[2, 1]), 'deg'),
    })


def sqm(url=smartfacturl + 'sqm.data'):
    tc = TableCrawler(url)
    return to_namedtuple('SqmPage', {
        'timestamp': (sft2dt(tc[0, 0]), None),
        'magnitude': (s2f(tc[1, 1]), '???'),
        'sensor_frequency': (s2f(tc[2, 1]), 'Hz'),
        'sensor_period': (s2f(tc[4, 1]), 's'),
        'sensor_temperature': (s2f(tc[5, 1]), 'C'),
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
        'timestamp': (sft2dt(tc[0, 0]), None),
        'End_of_dark_time': (conv(tc[1, 1]), None),
        'End_of_astro_twilight': (conv(tc[2, 1]), None),
        'End_of_nautic_twilight': (conv(tc[3, 1]), None),
        'Start_of_day_time': (conv(tc[4, 1]), None),
        'End_of_day_time': (conv(tc[5, 1]), None),
        'Start_of_nautic_twilight': (conv(tc[6, 1]), None),
        'Start_of_astro_twilight': (conv(tc[7, 1]), None),
        'Start_of_dark_time': (conv(tc[8, 1]), None),
    })


def weather(url=smartfacturl + 'weather.data'):
    tc = TableCrawler(url)
    return to_namedtuple('WeatherPage', {
        'timestamp': (sft2dt(tc[0, 0]), None),
        'sun': (tc[1, 1], '%'),
        'moon': (tc[2, 1], '%'),
        'temperature': (s2f(tc[3, 1]), 'C'),
        'dew_point': (s2f(tc[4, 1]), 'C'),
        'humidity': (s2f(tc[5, 1]), '%'),
        'pressure': (s2f(tc[6, 1]), 'hPa'),
        'sind_speed': (s2f(tc[7, 1]), 'km/h'),
        'wind_gusts': (s2f(tc[8, 1]), 'km/h'),
        'wind_direction': (tc[9, 1], None),
        'dust_tng': (s2f(tc[10, 1]), 'ug/m3'),
    })


def sipm_currents(url=smartfacturl + 'current.data'):
    tc = TableCrawler(url)
    return to_namedtuple('CurrentPage', {
        'timestamp': (sft2dt(tc[0, 0]), None),
        'calibrated': (tc[1, 1], None),
        'min_per_sipm': (s2f(tc[2, 1]), 'uA'),
        'median_per_sipm': (s2f(tc[3, 1]), 'uA'),
        'mean_per_sipm': (s2f(tc[4, 1]), 'uA'),
        'max_per_sipm': (s2f(tc[5, 1]), 'uA'),
        'power': (s2f(tc[6, 1][:-1]), 'W'),
    })

def sipm_voltages(url=smartfacturl + 'voltage.data'):
    tc = TableCrawler(url)
    return to_namedtuple('VoltagePage', {
        'timestamp': (sft2dt(tc[0, 0]), None),
        'min': (s2f(tc[1, 1]), 'V'),
        'median': (s2f(tc[2, 1]), 'V'),
        'mean': (s2f(tc[3, 1]), 'V'),
        'max': (s2f(tc[4, 1]), 'V'),
    })

def status(url=smartfacturl + 'status.data'):
    tc = TableCrawler(url)
    return to_namedtuple('StatusPage', {
        'timestamp': (sft2dt(tc[0, 0]), None),
        'dim': (tc[1, 1], None),
        'dim_control': (tc[2, 1], None),
        'mcp': (tc[3, 1], None),
        'datalogger': (tc[4, 1], None),
        'drive_control': (tc[5, 1], None),
        'drive_pc_time_check': (tc[6, 1], None),
        'fad_control': (tc[7, 1], None),
        'ftm_control': (tc[8, 1], None),
        'bias_control': (tc[9, 1], None),
        'feedback': (tc[10, 1], None),
        'rate_control': (tc[11, 1], None),
        'fsc_control': (tc[12, 1], None),
        'pfmini_control': (tc[13, 1], None),
        'gps_control': (tc[14, 1], None),
        'sqm_control': (tc[15, 1], None),
        'agilent_control_24v': (tc[16, 1], None),
        'agilent_control_50v': (tc[17, 1], None),
        'agilent_control_80v': (tc[18, 1], None),
        'power_control': (tc[19, 1], None),
        'lid_control': (tc[20, 1], None),
        'ratescan': (tc[21, 1], None),
        'magic_weather': (tc[22, 1], None),
        'tng_weather': (tc[23, 1], None),
        'magic_lidar': (tc[24, 1], None),
        'temperature': (tc[25, 1], None),
        'chat_server': (tc[26, 1], None),
        'skype_client': (tc[27, 1], None),
        'free_space_newdaq': (s2f(tc[28, 1]), 'TB'),
        'free_space_daq': (s2f(tc[29, 1]), 'TB'),
        'smartfact_runtime': (tc[30, 1], None),
    })


def container_temperature(url=smartfacturl + 'temperature.data'):
    tc = TableCrawler(url)
    return to_namedtuple('ContainerTemperaturePage', {
        'timestamp': (sft2dt(tc[0, 0]), None),
        'daily_min': (tc[1, 1], 'C'),
        'current': (tc[2, 1], 'C'),
        'daily_max': (tc[3, 1], 'C'),
    })


def current_source(url=smartfacturl + 'source.data'):
    tc = TableCrawler(url)
    return to_namedtuple('SourcePage', {
        'timestamp': (sft2dt(tc[0, 0]), None),
        'name': (tc[1, 1:], None),
        'right_ascension': (s2f(tc[2, 1]), 'h'),
        'declination': (s2f(tc[3, 1]), 'deg'),
        'wobble_offset': (s2f(tc[4, 1]), 'deg'),
        'wobble_angle': (s2f(tc[5, 1]), 'deg'),
    })


def camera_climate(url=smartfacturl + 'fsc.data'):
    tc = TableCrawler(url)
    return to_namedtuple('CameraClimatePage', {
        'timestamp': (sft2dt(tc[0, 0]), None),
        'humidity_mean': (s2f(tc[1, 1]), '%'),
        'relative_temperature_max': (s2f(tc[2, 1]), 'C'),
        'relative_temperature_mean': (s2f(tc[3, 1]), 'C'),
        'relative_temperature_min': (s2f(tc[4, 1]), 'C'),
    })


def main_page(url=smartfacturl + 'fact.data'):
    tc = TableCrawler(url)
    return to_namedtuple('MainPage', {
        'timestamp_1': (sft2dt(tc[0, 0]), None),
        'timestamp_2': (sft2dt(tc[0, 1]), None),
        'system_status': (' '.join(tc[1, 1:]), None),
        'relative_camera_temperature': (s2f(tc[3, 1]), 'C'),
        'humidity': (s2f(tc[4, 1]), '%'),
        'wind_speed': (s2f(tc[4, 2]), 'km/h'),
    })


def trigger_rate(url=smartfacturl + 'trigger.data'):
    tc = TableCrawler(url)
    return to_namedtuple('TriggerPage', {
        'timestamp': (sft2dt(tc[0, 0]), None),
        'trigger_rate': (s2f(tc[1, 1]), '1/s'),
    })

def errorhist(url=smartfacturl + 'errorhist.data'):
    tc = TableCrawler(url)
    history = [h for h in tc[1, 1].split("<->")[1].split("<br/>") if len(h)]
    return to_namedtuple('ErrorHistPage', {
        'timestamp': (sft2dt(tc[0, 0]), None),
        'history': (history, None),
    })
