import html
import requests
import random
import time

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
                self._load_payload()
        return item
