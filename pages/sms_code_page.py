from selenium.webdriver.common.by import By
from pages.home_page import HomePage

from pages.base_page import BasePage

class SMSCodePage(BasePage):
    SMS_CODE_CONTAINER = (By.CSS_SELECTOR, ".code-input.login-sms-code-input")
    SMS_SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'ONAYLA VE GİRİŞ YAP')]")
    ADD_BUTTON = (By.XPATH, "//button[contains(., 'Ekle')]")


    def __init__(self, driver):
        """
        Initializes the SMS page and verifies required elements are present.
        """
        super().__init__(driver)
        self.verify_page_loaded()

    def verify_page_loaded(self):
        """
        Verifies that the SMS code container and submit button are present.
        """
        required_elements = {
            "SMS Code Container": SMSCodePage.SMS_CODE_CONTAINER,
            "SMS Submit Button": SMSCodePage.SMS_SUBMIT_BUTTON
        }
        self.verify_elements(required_elements)

    def enter_sms_code(self, code: str = None):
        """
        Enters an SMS code into the input fields within the SMS code container.
        If no code is provided, the default '123456' is used.

        :param code: A string representing the SMS code. Defaults to '123456' if None.
        """
        if code is None:
            code = "123456"

        container = self.find_element(self.SMS_CODE_CONTAINER)
        inputs = container.find_elements(By.CSS_SELECTOR, "input[data-index]")
        if len(inputs) < 6:
            raise Exception("Expected 6 SMS code input fields, but found fewer.")

        for i, digit in enumerate(code):
            input_field = container.find_element(By.CSS_SELECTOR, f"input[data-index='{i}']")
            input_field.clear()
            input_field.send_keys(digit)

    def click_sms_submit_button(self):
        """
        Clicks the 'SMS_SUBMIT_BUTTON' button to confirm and log in.
        """
        button = self.find_element(self.SMS_SUBMIT_BUTTON)
        button.click()


    def sms_login(self, code: str = None):
        """
        Performs SMS login by entering the SMS code and clicking the submit button.
        """
        self.enter_sms_code(code)
        self.click_sms_submit_button()
        try:
            self.find_element(self.ADD_BUTTON)
            return HomePage(self.driver)
        except self.TimeoutException:
            return self