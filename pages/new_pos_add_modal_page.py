from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class NewAddPOSModalPage(BasePage):
    PAYMENT_PROVIDER_DROPDOWN = (By.CSS_SELECTOR, 'div[data-testid="formItem-bankId"]')
    POS_NAME_INPUT = (By.CSS_SELECTOR, '[data-testid="formItem-name"]')
    DROPDOWN_TRIGGER = (By.XPATH, "//div[contains(@class, 'select-container')]//span[contains(@class, 'select__arrow')]")
    SAVE_BUTTON = (By.XPATH, "//button[normalize-space(text())='Kaydet']")
    POS_STATUS_DROPDOWN = (By.CSS_SELECTOR, "div.select-container > span.select__arrow")
    TANIMLAMALAR = (By.XPATH, "//p[contains(text(), 'Tanımlamalar')]")


    def __init__(self, driver):
        """
        Initializes the Add New POS Modal and verifies that all required elements are present.
        """
        super().__init__(driver)
        self.verify_page_loaded()

    def verify_page_loaded(self):
        """
        Verifies that the modal container, PAYMENT_PROVIDER_DROPDOWN, SAVE_BUTTON, and save button are present.
        """
        required_elements = {
            "Ödeme Sistemi (Sanal POS) Dropdown": self.PAYMENT_PROVIDER_DROPDOWN,
            "Kaydet Button": self.SAVE_BUTTON
        }
        self.verify_elements(required_elements)

    def click_save_button(self):
        from pages.pos_setup_page import POSSetupPage
        """
        Clicks the 'Kaydet' button.
        """
        try:
            button = self.find_element_clickable(self.SAVE_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()
        except:
            button = self.find_element(self.SAVE_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            self.driver.execute_script("arguments[0].click();", button)

        try:
            self.find_element(self.TANIMLAMALAR)
            return POSSetupPage(self.driver)
        except self.TimeoutException:
            return self

    def click_provider_dropdown(self):
        """
        Clicks the 'Ödeme Sistemi(Sanal POS)' dropdown to open its options.
        """
        self.find_element(self.PAYMENT_PROVIDER_DROPDOWN).click()

    # def click_dropdowns_with_placeholder_text(self, option_text):
    #     """
    #     Clicks the Dropdowns with id 'select-label' if its text contains the provided parameter.
    #     """
    #     locator = (By.XPATH, f"//label[@id='select-label' and contains(text(),'{option_text}')]")
    #     self.find_element_clickable(locator).click()

    def click_dropdowns_with_placeholder_text(self, option_text):
        """
        Clicks the Dropdowns with id 'select-label' if its text contains the provided parameter.
        """
        locator = (By.XPATH, f"//label[@id='select-label' and contains(text(),'{option_text}')]")
        element = self.find_element_clickable(locator)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.driver.execute_script("arguments[0].click();", element)

    def enter_pos_name(self, pos_name):
        """
        Enters the provided POS name into the input field.
        pos_name: The POS name to enter.
        """
        input_field = self.find_element(self.POS_NAME_INPUT)
        input_field.clear()
        input_field.send_keys(pos_name)

    def select_option_from_dropdown(self, option_text):
        """
        Selects the dropdown option that matches the given text.
        :param option_text: The text of the option to select.
        """
        option_locator = (By.XPATH, f"//ul[@role='listbox']//li[.//p[normalize-space(text())='{option_text}']]")
        option_element = self.find_element(option_locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", option_element)
        option_element.click()

    def enter_provider_info(self, values: list):
        """
        Enters the provided values into the merchant information input fields.
        :param values: A list of strings to be entered into the corresponding input fields.
        """
        for index, value in enumerate(values):
            locator = (By.CSS_SELECTOR, f"[data-testid='formItem-posConnectionParameters.{index}.value']")
            input_field = self.find_element_clickable(locator)
            input_field.clear()
            input_field.send_keys(value)

    def enter_values_into_merchant_info(self, values):
        """
        Merchant bilgi input alanlarına verilen değerleri girer.
        :param values: Her input için girilecek string değerler listesi.
        """
        for index, value in enumerate(values):
            locator = (By.CSS_SELECTOR, f"[data-testid='formItem-posConnectionParameters.{index}.value']")
            input_field = self.find_element_clickable(locator)

            input_field.clear()

            try:
                input_field.send_keys(value)
            except Exception as e:
                self.driver.execute_script(
                    """
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    """,
                    input_field,
                    value
                )

    def select_installment_options(self, options, installment_type: str):
        """
        Selects the installment option(s) matching the provided value(s) in the specified installment type container.
        :param options: A single option value (int/str) or a list of values to select.
        :param installment_type: The installment type suffix to use in the data-testid (e.g. "Personal", "Nonpersonal", etc.).
        """
        if not isinstance(options, list):
            options = [options]
        for opt in options:
            locator = (By.XPATH, f"//div[@data-testid='formItem-posInstalment{installment_type}']//div[./span[normalize-space(text())='{opt}']]")
            self.find_element(locator).click()