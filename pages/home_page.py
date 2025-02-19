from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
from pages.pos_detail_page import POSDetailPage
from pages.pos_setup_page import POSSetupPage
from pages.transaction_page import TransactionPage


class HomePage(BasePage):
    TANIMLAMALAR = (By.XPATH, "//p[contains(text(), 'Tanımlamalar')]")
    ISLEMLER = (By.XPATH, "//p[contains(text(), 'İşlemler')]")
    POS_TANIMLA = (By.XPATH, "//a[.//p[contains(text(), 'POS Tanımla')]]")
    ADD_BUTTON = (By.XPATH, "//button[contains(., 'Ekle')]")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-input")
    DETAIL_BUTTON = (By.CSS_SELECTOR, "button[data-testid='tableRowAction-detail']")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space(text())='Kaydet']")

    def __init__(self, driver):
        """
        Initializes the Home page and verifies required elements are present.
        """
        super().__init__(driver)
        self.verify_page_loaded()

    def verify_page_loaded(self):
        """
        Verifies that the Tanımlamalar button are present.
        """
        required_elements = {
            "Tanımlamalar Button": self.TANIMLAMALAR,
        }
        self.verify_elements(required_elements)


    def hover_and_click_pos_define(self):
        """
        Hovers over the 'Tanımlamalar' element and clicks the 'POS Tanımla' link.
        """
        definitions_element = self.find_element(self.TANIMLAMALAR)
        ActionChains(self.driver).move_to_element(definitions_element).perform()
        pos_define_element = self.find_element(self.POS_TANIMLA)
        pos_define_element.click()
        try:
            self.find_element(self.ADD_BUTTON)
            return POSSetupPage(self.driver)
        except self.TimeoutException:
            return self

    def hover_and_click_test_transactions(self):
        """
        Hovers over the 'İşlemler' element and clicks the 'Test İşlemleri' link.
        """
        definitions_element = self.find_elements(self.ISLEMLER)
        corrected_element = definitions_element[0]
        ActionChains(self.driver).move_to_element(corrected_element).perform()
        pos_define_element = self.find_element(self.POS_TANIMLA)
        pos_define_element.click()
        try:
            self.find_element(self.ADD_BUTTON)
            return TransactionPage (self.driver)
        except self.TimeoutException:
            return self

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