import time
from datetime import datetime, timedelta

from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class POSDetailPage(BasePage):
    ADD_BUTTON = (By.XPATH, "//button[contains(., 'Ekle')]")
    DIFFERENT_COMMISSION_TOGGLE = (By.CSS_SELECTOR, "label[data-testid='formItem-defineDifferentValuesForCommercialCards']")
    COMMISSION_NAME_INPUT = (By.CSS_SELECTOR, "input[data-testid='formItem-name']")
    START_DATE_INPUT = (By.CSS_SELECTOR, "[data-testid='formItem-startDate'] input")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space(text())='Kaydet']")
    CLOSE_ICON = (By.CSS_SELECTOR, "span.drawer-xmark")

    def __init__(self,driver):
        """
        Initializes the POS Detail page and verifies required elements are present.
        """
        super().__init__(driver)
        #self.verify_page_loaded()

    def click_tab(self, tab_text: str):
        """
        Clicks the tab button matching the given text within the tab's container.
        :param tab_text: The visible text of the tab to click.
        """
        locator = (By.XPATH, f"//div[contains(@class, 'tabs-form-detail')]//button[normalize-space(text())='{tab_text}']")
        self.find_element(locator).click()

    def click_save_button(self):
        """
        Clicks the 'Kaydet' button.
        """
        button = self.find_elements(self.SAVE_BUTTON)
        second_button = button[1]
        self.driver.execute_script("arguments[0].scrollIntoView(true);", second_button)
        try:
            second_button.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", second_button)

    def is_commissions_tab_opened(self):
        """
        Returns True if the modal is present and visible on the page, else False.
        """
        self.is_element_present(self.ADD_BUTTON)

    def click_add_button(self):
        """
        Clicks the Ekle button.
        """
        time.sleep(2)
        try:
            button = self.find_elements(self.ADD_BUTTON)
            second_button = button[1]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", second_button)
            second_button.click()
        except:
            button = self.find_elements(self.ADD_BUTTON)
            second_button = button[1]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", second_button)
            self.driver.execute_script("arguments[0].click();", second_button)

    def click_close_icon(self):
        """
        Clicks the close icon.
        """
        self.find_element(self.CLOSE_ICON).click()

    def is_commission_details_form_opened(self):
        """
        Returns True if the Commission Details form is present and visible on the page, else False.
        """
        self.is_element_present(self.DIFFERENT_COMMISSION_TOGGLE)

    def click_commission_toggle(self):
        """
        Clicks the toggle for defining different commission conditions for commercial cards.
        """
        self.find_element(self.DIFFERENT_COMMISSION_TOGGLE).click()

    def enter_commission_name(self, name: str):
        """
        Enters the provided commission name into the input field.
        :param name: The commission name to be entered.
        """
        input_field = self.find_elements(self.COMMISSION_NAME_INPUT)
        second_input = input_field[1]
        second_input.clear()
        second_input.send_keys(name)

    def enter_start_date(self, hours_offset: int = 24):
        """
        Enters a date into the start date input field in the format dd/mm/yyyy-HH:MM, where the date is calculated as the current time plus the specified number of hours (default is 24 hours).
        :param hours_offset: The number of hours to add to the current time. Defaults to 24.
        """
        future_date = datetime.now() + timedelta(hours=hours_offset)
        formatted_date = future_date.strftime("%d/%m/%Y-%H:%M")
        input_field = self.find_element(self.START_DATE_INPUT)
        input_field.clear()
        input_field.send_keys(formatted_date)
        input_field.send_keys(self.ENTER_KEY)

    def enter_computed_values_for_specific_indexes(self, pivot_index: int, base_value: float, increment: float, other_value: float, other_increment: float):
        """
        Enters computed values into enabled mask input fields with even indexes within the specified pivot container.
        If pivot_index is 2 and the enabled element's index is even, the first even input gets base_value,
        and each subsequent even input receives the previous value increased by increment.
        Otherwise, for elements not meeting these conditions, a custom value is entered.
        :param pivot_index: The 1-based index of the pivot container (must be 1, 2, or 3).
        :param base_value: The starting computed value for even enabled input when pivot_index is 2.
        :param increment: The amount to add to the computed value for each subsequent even enabled input when pivot_index is 2.
        :param other_value: The starting other computed value for enabled input when pivot_index diff then 2.
        :param other_increment: The amount to add to the other computed value for each subsequent enabled input when pivot_index diff then 2.
        """

        locator = (By.XPATH, f"(//div[contains(@class, 'table-pivot-is-wrapper')])[{pivot_index}]"
                             "//div[contains(@class, 'mask-input') and contains(@class, 'mask-input-is-hasValue')]//input")
        elements = self.find_elements(locator)
        enabled_elements = [el for el in elements if el.is_enabled()]

        computed_value = base_value
        other_computed_value = other_value
        for idx, element in enumerate(enabled_elements):
            if pivot_index == 2 and idx % 2 == 0:
                element.clear()
                element.send_keys(str(computed_value))
                computed_value += increment
            else:
                element.clear()
                element.send_keys(other_computed_value)
                other_computed_value += other_increment