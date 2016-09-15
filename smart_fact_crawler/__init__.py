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

def all(self):
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
    return {f.__name__: f() for f in functions}


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
    return {
        'timestamp': sft2dt(tc[0, 0]),
        'Azimuth_in_Deg': s2f(tc[1, 1]),
        'Zenith_Distance_in_Deg': s2f(tc[2, 1]),
    }


def sqm(url=smartfacturl + 'sqm.data'):
    tc = TableCrawler(url)
    return {
        'timestamp': sft2dt(tc[0, 0]),
        'Magnitude': s2f(tc[1, 1]),
        'Sensor_Frequency_in_Hz': s2f(tc[2, 1]),
        'Sensor_Period_in_s': s2f(tc[4, 1]),
        'Sensor_Temperature_in_C': s2f(tc[5, 1]),
    }


def sun(url=smartfacturl + 'sun.data'):

    def next_datetime_from_hhmm_string(hhmm):
        now = datetime.utcnow()
        hour = int(hhmm[0:2])
        minute = int(hhmm[3:5])

        new_date = now.replace(hour=hour, minute=minute, second=0)
        if not new_date > now:
            new_date += timedelta(days=1)
        return new_date


    tc = TableCrawler(url)
    return {
        'timestamp': sft2dt(tc[0, 0]),
        'End_of_dark_time':         next_datetime_from_hhmm_string(tc[1, 1]),
        'End_of_astro_twilight':    next_datetime_from_hhmm_string(tc[2, 1]),
        'End_of_nautic_twilight':   next_datetime_from_hhmm_string(tc[3, 1]),
        'Start_of_day_time':        next_datetime_from_hhmm_string(tc[4, 1]),
        'End_of_day_time':          next_datetime_from_hhmm_string(tc[5, 1]),
        'Start_of_nautic_twilight': next_datetime_from_hhmm_string(tc[6, 1]),
        'Start_of_astro_twilight':  next_datetime_from_hhmm_string(tc[7, 1]),
        'Start_of_dark_time':       next_datetime_from_hhmm_string(tc[8, 1]),
    }


def weather(url=smartfacturl + 'weather.data'):
    tc = TableCrawler(url)
    return {
        'timestamp': sft2dt(tc[0, 0]),
        'Sun_in_Percent': tc[1, 1],
        'Moon_in_Percent': tc[2, 1],
        'Temperature_in_C': s2f(tc[3, 1]),
        'Dew_point_in_C': s2f(tc[4, 1]),
        'Humidity_in_Percent': s2f(tc[5, 1]),
        'Pressure_in_hPa': s2f(tc[6, 1]),
        'Wind_speed_in_km_per_h': s2f(tc[7, 1]),
        'Wind_gusts_in_km_per_h': s2f(tc[8, 1]),
        'Wind_direction': tc[9, 1],
        'Dust_TNG_in_ug_per_m3': s2f(tc[10, 1]),
    }


def sipm_currents(url=smartfacturl + 'current.data'):
    tc = TableCrawler(url)
    return {
        'timestamp': sft2dt(tc[0, 0]),
        'Clibrated': tc[1, 1],
        'Min_current_per_GAPD_in_uA': s2f(tc[2, 1]),
        'Med_current_per_GAPD_in_uA': s2f(tc[3, 1]),
        'Avg_current_per_GAPD_in_uA': s2f(tc[4, 1]),
        'Max_current_per_GAPD_in_uA': s2f(tc[5, 1]),
        # The W is stucked to the float and needs to be removed
        'Power_camera_GAPD_in_W': s2f(tc[6, 1][:-1]),
    }

def sipm_voltages(url=smartfacturl + 'voltage.data'):
    tc = TableCrawler(url)
    return {
        'timestamp': sft2dt(tc[0, 0]),
        'Min_voltage_in_V': s2f(tc[1, 1]),
        'Med_voltage_in_V': s2f(tc[2, 1]),
        'Avg_voltage_in_V': s2f(tc[3, 1]),
        'Max_voltage_in_V': s2f(tc[4, 1]),
    }

def status(url=smartfacturl + 'status.data'):
    tc = TableCrawler(url)
    return {
        'timestamp': sft2dt(tc[0, 0]),
        'DIM': tc[1, 1],
        'Dim_Control': tc[2, 1],
        'MCP': tc[3, 1],
        'Datalogger': tc[4, 1],
        'Drive_control': tc[5, 1],
        'Drive_PC_time_check': tc[6, 1],
        'FAD_control': tc[7, 1],
        'FTM_control': tc[8, 1],
        'Bias_control': tc[9, 1],
        'Feedback': tc[10, 1],
        'Rate_control': tc[11, 1],
        'FSC_control': tc[12, 1],
        'PFmini_control': tc[13, 1],
        'GPS_control': tc[14, 1],
        'SQM_control': tc[15, 1],
        'Agilent_control_24V': tc[16, 1],
        'Agilent_control_50V': tc[17, 1],
        'Agilent_control_80V': tc[18, 1],
        'Power_control': tc[19, 1],
        'Lid_control': tc[20, 1],
        'Ratescan': tc[21, 1],
        'Magic_Weather': tc[22, 1],
        'TNG_Weather': tc[23, 1],
        'Magic_Lidar': tc[24, 1],
        'Temperature': tc[25, 1],
        'Chat_server': tc[26, 1],
        'Skype_client': tc[27, 1],
        'Free_space_newdaq_in_TB': s2f(tc[28, 1]),
        'Free_space_daq_in_TB': s2f(tc[29, 1]),
        'Smartfact_runtime': tc[30, 1],
    }


def container_temperature(url=smartfacturl + 'temperature.data'):
    tc = TableCrawler(url)
    return {
        'timestamp': sft2dt(tc[0, 0]),
        '24h_min_temperature_in_C': tc[1, 1],
        'Current_temperature_in_C': tc[2, 1],
        '24h_max_temperature_in_C': tc[3, 1],
    }


def current_source(url=smartfacturl + 'source.data'):
    tc = TableCrawler(url)
    return {
        'timestamp': sft2dt(tc[0, 0]),
        'Source_Name': tc[1, 1:],
        'Right_Ascention_in_h': s2f(tc[2, 1]),
        'Declination_in_Deg': s2f(tc[3, 1]),
        'Wobble_offset_in_Deg': s2f(tc[4, 1]),
        'Wobble_angle_in_Deg': s2f(tc[5, 1]),
    }


def camera_climate(url=smartfacturl + 'fsc.data'):
    tc = TableCrawler(url)
    return {
        'timestamp': sft2dt(tc[0, 0]),
        'Avg_humidity_in_percent': s2f(tc[1, 1]),
        'Max_rel_temp_in_C': s2f(tc[2, 1]),
        'Avg_rel_temp_in_C': s2f(tc[3, 1]),
        'Min_rel_temp_in_C': s2f(tc[4, 1]),
    }


def main_page(url=smartfacturl + 'fact.data'):
    tc = TableCrawler(url)
    return {
        'Time_Stamp_1': sft2dt(tc[0, 0]),
        'Time_Stamp_2': sft2dt(tc[0, 1]),
        'System_Status': ' '.join(tc[1, 1:]),
        'Rel_camera_temp_in_C': s2f(tc[3, 1]),
        'Humidity_in_Percent': s2f(tc[4, 1]),
        'Wind_speed_in_km_per_h': s2f(tc[4, 2]),
    }


def trigger_rate(url=smartfacturl + 'trigger.data'):
    tc = TableCrawler(url)
    return {
        'timestamp': sft2dt(tc[0, 0]),
        'Trigger_Rate_in_1_per_s': s2f(tc[1, 1]),
    }

def errorhist(url=smartfacturl + 'errorhist.data'):
    tc = TableCrawler(url)
    history = [h for h in tc[1, 1].split("<->")[1].split("<br/>") if len(h)]
    return {
        'timestamp': sft2dt(tc[0, 0]),
        'history': history,
    }
