from selenium.webdriver.common.by import By
from pages.base_page import BasePage



class TransactionPage(BasePage):
    ADD_BUTTON = (By.XPATH, "//button[contains(., 'Ekle')]")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-input")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space(text())='Kaydet']")
    S3DBUTTON = (By.XPATH, "//button[@type='button' and normalize-space(text())='Satış (3D)']")
    AMOUNT_INPUT = (By.CSS_SELECTOR, "input[data-testid='formItem-amount']")
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "input[data-testid='formItem-cardNumber']")
    CARD_HOLDER_NAME_INPUT = (By.CSS_SELECTOR, "input[data-testid='formItem-cardHolderName']")
    CARD_EXPIRE_INPUT = (By.CSS_SELECTOR, "input[data-testid='formItem-cardExpire']")
    CARD_CVV2_INPUT = (By.CSS_SELECTOR, "input[data-testid='formItem-cardCvv2']")
    REFERENCE_NUMBER_INPUT = (By.CSS_SELECTOR, "input[data-testid='formItem-referenceNumber']")

    def __init__(self, driver):
        """
        Initializes the Transaction page and verifies required elements are present.
        """
        super().__init__(driver)
        self.verify_page_loaded()

    def verify_page_loaded(self):
        """
        Verifies that the Ekle button are present.
        """
        required_elements = {
            "Ekle Button": self.ADD_BUTTON,
        }
        self.verify_elements(required_elements)

    def click_add_button(self):
        """
        Clicks the Ekle button.
        """
        self.find_element(self.ADD_BUTTON).click()

    def is_s3d_button_displayed(self):
        """
        Returns True if the 3D Secure button is present and visible on the page, else False.
        """
        self.is_element_present(self.S3DBUTTON)

    def is_add_button_displayed(self):
        """
        Returns True if the 'Ekle' button is displayed, otherwise False.
        """
        self.is_element_present(self.ADD_BUTTON)

    def click_dropdowns_with_placeholder_text(self, option_text):
        """
        Clicks the Dropdowns with id 'select-label' if its text contains the provided parameter.
        """
        locator = (By.XPATH, f"//label[@id='select-label' and contains(text(),'{option_text}')]")
        self.find_element(locator).click()

    def enter_amount(self, amount: str):
        """
        Enters the provided amount into the 'formItem-amount' input field.
        :param amount: The amount value to be entered.
        """
        input_field = self.find_element(self.AMOUNT_INPUT)
        input_field.clear()
        input_field.send_keys(amount)

    def select_option_from_dropdown(self, option_text):
        """
        Selects the dropdown option that matches the given text.
        :param option_text: The text of the option to select.
        """
        option_locator = (By.XPATH, f"//ul[@role='listbox']//li[.//p[normalize-space(text())='{option_text}']]")
        option_element = self.find_element(option_locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", option_element)
        option_element.click()


    def enter_card_number(self, card_number: str):
        """
        Enters the provided card number into the 'formItem-cardNumber' input field.
        :param card_number: The card number to be entered.
        """
        input_field = self.find_element(self.CARD_NUMBER_INPUT)
        input_field.clear()
        input_field.send_keys(card_number)

    def enter_card_holder_name(self, name: str):
        """
        Enters the provided cardholder name into the 'formItem-cardHolderName' input field.
        :param name: The cardholder name to be entered.
        """
        input_field = self.find_element(self.CARD_HOLDER_NAME_INPUT)
        input_field.clear()
        input_field.send_keys(name)

    def enter_card_expire(self, expire_date: str):
        """
        Enters the provided card expiration date into the 'formItem-cardExpire' input field.
        :param expire_date: The card expiration date to be entered.
        """
        input_field = self.find_element(self.CARD_EXPIRE_INPUT)
        input_field.clear()
        input_field.send_keys(expire_date)

    def enter_card_cvv2(self, cvv: str):
        """
        Enters the provided card CVV2 into the 'formItem-cardCvv2' input field.
        :param cvv: The CVV2 value to be entered.
        """
        input_field = self.find_element(self.CARD_CVV2_INPUT)
        input_field.clear()
        input_field.send_keys(cvv)

    def enter_reference_number(self, reference: str):
        """
        Enters the provided reference number into the 'formItem-referenceNumber' input field.
        :param reference: The reference number to be entered.
        """
        input_field = self.find_element(self.REFERENCE_NUMBER_INPUT)
        input_field.clear()
        input_field.send_keys(reference)

    def click_s3d_button(self):
        """
        Clicks the 'Satış (3D)' button.
        """
        self.find_element(self.S3DBUTTON).click()