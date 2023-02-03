from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
import unittest
from django.test import LiveServerTestCase

options = Options()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(
            firefox_options=options,
            executable_path=r"C:/Program Files/Mozilla Firefox/geckodriver.exe"
        )

    def tearDown(self):
        self.browser.quit()

    def check_for_now_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text

        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(inputbox.get_attribute(
            'placeholder'), 'Enter a to-do item')

        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_now_in_list_table('1: Buy peacock feathers')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_now_in_list_table('1: Buy peacock feathers')
        self.check_for_now_in_list_table(
            '2: Use peacock feathers to make a fly')

        self.fail('Finish the test!!!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
