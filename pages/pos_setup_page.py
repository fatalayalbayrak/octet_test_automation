import time

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.new_pos_add_modal_page import NewAddPOSModalPage
from pages.pos_detail_page import POSDetailPage


class POSSetupPage(BasePage):
    ADD_BUTTON = (By.XPATH, "//button[contains(., 'Ekle')]")
    PAYMENT_PROVIDER_DROPDOWN = (By.CSS_SELECTOR, 'div[data-testid="formItem-bankId"]')
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-input")
    DETAIL_BUTTON = (By.CSS_SELECTOR, "button[data-testid='tableRowAction-detail']")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space(text())='Kaydet']")

    def __init__(self, driver):
        """
        Initializes the POS setup page and verifies required elements are present.
        """
        super().__init__(driver)
        self.verify_page_loaded()

    def verify_page_loaded(self):
        required_elements = {
            "Ekle Button": self.ADD_BUTTON,
        }
        self.verify_elements(required_elements)

    def click_add_button(self):
        """
        Clicks the add button labeled 'Ekle'.
        """
        self.find_element(self.ADD_BUTTON).click()
        try:
            self.find_element(self.PAYMENT_PROVIDER_DROPDOWN)
            return NewAddPOSModalPage(self.driver)
        except self.TimeoutException:
            return self

    def search_pos_from_list(self, text: str):
        """
        Enters the given text into the search input field and presses Enter.
        :param text: The text to be entered.
        """
        search_field = self.find_element(self.SEARCH_INPUT)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", search_field)
        search_field.clear()
        search_field.send_keys(text)
        search_field.send_keys(self.ENTER_KEY)
        time.sleep(2)

    def click_pos_detail_button(self):
        """
        Clicks the POS detail button.
        """
        self.find_element(self.DETAIL_BUTTON).click()
        try:
            self.find_element(self.SAVE_BUTTON)
            return POSDetailPage(self.driver)
        except self.TimeoutException:
            return self