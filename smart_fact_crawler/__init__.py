# -*- encoding:utf-8 -*-
from __future__ import print_function, absolute_import
from collections import defaultdict
import time
import random
from datetime import datetime
from datetime import timedelta
import requests
import inspect
import html


smartfacturl = "http://fact-project.org/smartfact/data/"


class TableCrawler(object):
    def __init__(self, url):
        self.url = url
        self.connection_error_counter = 0
        self._load_payload()

    def _load_payload(self):
        self._request_web_page()
        self._build_page_payload()

    def _request_web_page(self):
        while True:
            try:
                self.web_page = requests.get(self.url, timeout=15.)
                self.connection_error_counter = 0
                break
            except requests.exceptions.ConnectionError:
                self._acknowledge_error_and_wait_a_moment()

    def _build_page_payload(self):
        self.page_payload = [
            [html.unescape(elem) for elem in line.split('\t')]
            for line in self.web_page.text.splitlines()
        ]

    def _acknowledge_error_and_wait_a_moment(self):
        self.connection_error_counter += 1
        if self.connection_error_counter >= 10:
            raise
        else:
            # sleep between 1 and 2 seconds.
            time.sleep(1. + random.random())        

    def __getitem__(self, index):
        row, col = index
        while True:
            try:
                item = self.page_payload[row][col]
                self.connection_error_counter = 0
                break
            except IndexError:
                self._acknowledge_error_and_wait_a_moment()
        return item


def str2float(text):
    try:
        number = float(text)
    except:
        number = float("nan")

    return number


def smartfact_time2datetime(fact_time_stamp):
    return datetime.utcfromtimestamp(
        str2float(fact_time_stamp) / 1000.0
    )


class SmartFact(object):

    def __init__(self):
        self.status = status
        self.drive = drive
        self.sqm = sqm
        self.sun = sun
        self.weather = weather
        self.sipm_currents = sipm_currents
        self.sipm_voltages = sipm_voltages
        self.container_temperature = container_temperature
        self.current_source = current_source
        self.camera_climate = camera_climate
        self.main_page = main_page
        self.trigger_rate = trigger_rate

    def all(self):
        functions = inspect.getmembers(self, predicate=inspect.isfunction)

        full = dict()
        for function in functions:
            full[function[0]] = function[1]()

        return full


def drive():
    return {
        "tracking": tracking(),
        "pointing": pointing(),
    }


def tracking(url=smartfacturl + 'tracking.data'):
    tc = TableCrawler(url)
    return {
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
        'Source_Name': tc[1, 1:],
        'Right_Ascention_in_h': str2float(tc[2, 1]),
        'Declination_in_Deg': str2float(tc[3, 1]),
        'Zenith_Distance_in_Deg': str2float(tc[4, 1]),
        'Azimuth_in_Deg': str2float(tc[5, 1]),
        'Control_Deviation_in_ArcSec': str2float(tc[6, 1]),
        'Distance_to_Moon_in_Deg': tc[7, 1],
    }


def pointing(url=smartfacturl + 'pointing.data'):
    tc = TableCrawler(url)
    return {
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
        'Azimuth_in_Deg': str2float(tc[1, 1]),
        'Zenith_Distance_in_Deg': str2float(tc[2, 1]),
    }


def sqm(url=smartfacturl + 'sqm.data'):
    tc = TableCrawler(url)
    return {
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
        'Magnitude': str2float(tc[1, 1]),
        'Sensor_Frequency_in_Hz': str2float(tc[2, 1]),
        'Sensor_Period_in_s': str2float(tc[4, 1]),
        'Sensor_Temperature_in_C': str2float(tc[5, 1]),
    }


def sun(url=smartfacturl + 'sun.data'):

    def next_datetime_from_hhmm_string(hhmm):
        now = datetime.utcnow()
        hour = int(hhmm[0:2])
        minute = int(hhmm[3:5])

        new_date = datetime(
            now.year,
            now.month,
            now.day,
            hour,
            minute,
            0)
        if not new_date > now:
            new_date += timedelta(days=1)

        return new_date


    tc = TableCrawler(url)
    return {
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
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
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
        'Sun_in_Percent': tc[1, 1],
        'Moon_in_Percent': tc[2, 1],
        'Temperature_in_C': str2float(tc[3, 1]),
        'Dew_point_in_C': str2float(tc[4, 1]),
        'Humidity_in_Percent': str2float(tc[5, 1]),
        'Pressure_in_hPa': str2float(tc[6, 1]),
        'Wind_speed_in_km_per_h': str2float(tc[7, 1]),
        'Wind_gusts_in_km_per_h': str2float(tc[8, 1]),
        'Wind_direction': tc[9, 1],
        'Dust_TNG_in_ug_per_m3': str2float(tc[10, 1]),
    }


def sipm_currents(url=smartfacturl + 'current.data'):
    tc = TableCrawler(url)
    return {
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
        'Clibrated': tc[1, 1],
        'Min_current_per_GAPD_in_uA': str2float(tc[2, 1]),
        'Med_current_per_GAPD_in_uA': str2float(tc[3, 1]),
        'Avg_current_per_GAPD_in_uA': str2float(tc[4, 1]),
        'Max_current_per_GAPD_in_uA': str2float(tc[5, 1]),
        # The W is stucked to the float and needs to be removed
        'Power_camera_GAPD_in_W': str2float(tc[6, 1][:-1]),
    }

def sipm_voltages(url=smartfacturl + 'voltage.data'):
    tc = TableCrawler(url)
    return {
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
        'Min_voltage_in_V': str2float(tc[1, 1]),
        'Med_voltage_in_V': str2float(tc[2, 1]),
        'Avg_voltage_in_V': str2float(tc[3, 1]),
        'Max_voltage_in_V': str2float(tc[4, 1]),
    }

def status(url=smartfacturl + 'status.data'):
    tc = TableCrawler(url)
    return {
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
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
        'Free_space_newdaq_in_TB': str2float(tc[28, 1]),
        'Free_space_daq_in_TB': str2float(tc[29, 1]),
        'Smartfact_runtime': tc[30, 1],
    }


def container_temperature(url=smartfacturl + 'temperature.data'):
    tc = TableCrawler(url)
    return {
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
        '24h_min_temperature_in_C': tc[1, 1],
        'Current_temperature_in_C': tc[2, 1],
        '24h_max_temperature_in_C': tc[3, 1],
    }


def current_source(url=smartfacturl + 'source.data'):
    tc = TableCrawler(url)
    return {
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
        'Source_Name': tc[1, 1:],
        'Right_Ascention_in_h': str2float(tc[2, 1]),
        'Declination_in_Deg': str2float(tc[3, 1]),
        'Wobble_offset_in_Deg': str2float(tc[4, 1]),
        'Wobble_angle_in_Deg': str2float(tc[5, 1]),
    }


def camera_climate(url=smartfacturl + 'fsc.data'):
    tc = TableCrawler(url)
    return {
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
        'Avg_humidity_in_percent': str2float(tc[1, 1]),
        'Max_rel_temp_in_C': str2float(tc[2, 1]),
        'Avg_rel_temp_in_C': str2float(tc[3, 1]),
        'Min_rel_temp_in_C': str2float(tc[4, 1]),
    }


def main_page(url=smartfacturl + 'fact.data'):
    tc = TableCrawler(url)
    return {
        'Time_Stamp_1': smartfact_time2datetime(tc[0, 0]),
        'Time_Stamp_2': smartfact_time2datetime(tc[0, 1]),
        'System_Status': ' '.join(tc[1, 1:]),
        'Rel_camera_temp_in_C': str2float(tc[3, 1]),
        'Humidity_in_Percent': str2float(tc[4, 1]),
        'Wind_speed_in_km_per_h': str2float(tc[4, 2]),
    }


def trigger_rate(url=smartfacturl + 'trigger.data'):
    tc = TableCrawler(url)
    return {
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
        'Trigger_Rate_in_1_per_s': str2float(tc[1, 1]),
    }

def errorhist(url=smartfacturl + 'errorhist.data'):
    tc = TableCrawler(url)
    history = tc.page_payload[1].split("<->")[1].split("<br/>")
    return {
        'Time_Stamp': smartfact_time2datetime(tc[0, 0]),
        'history': history,
    }
