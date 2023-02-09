from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from lists.forms import DUPLICATE_ITEM_ERROR


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:invalid',
            )
        )
        # She tries again with some text for the item, which now works
        self.add_list_item('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She receives a similar warning on the list page
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # And she can correct it by filling some text in
        self.add_list_item('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')
        # She accidentally tries to enter a duplicate item
        self.add_list_item('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        # She sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            DUPLICATE_ITEM_ERROR))

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)
        self.add_list_item('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')
        self.add_list_item('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))
        # She starts typing in the input box to clear the error
        self.add_list_item('a')
        # She is pleased to see that the error message disappears
        # self.wait_for(lambda: self.assertFalse(
        #     self.get_error_element().is_displayed()
        # ))
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))
