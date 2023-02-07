import time
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options

options = Options()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(
            firefox_options=options,
            executable_path=r"C:/Program Files/Mozilla Firefox/geckodriver.exe"
        )
        # staging_server = os.environ.get('STAGING_SERVER')
        staging_server = 'ingarbi006.pythonanywhere.com/'
        if staging_server:
            self.live_server_url = 'https://' + staging_server

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
