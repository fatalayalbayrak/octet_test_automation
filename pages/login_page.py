from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.sms_code_page import SMSCodePage
from utils.driver_factory import DriverFactory

class LoginPage(BasePage):
    DEFAULT_URL = "https://testotomasyon.octet.com.tr/giris"
    DEFAULT_USERNAME = "virkiyokku@gufum.com"
    DEFAULT_PASSWORD = "Otomasyon123"
    DEFAULT_SMS_CODE = "123456"
    EMAIL_INPUT = (By.CSS_SELECTOR, '[data-testid="formItem-email"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-testid="formItem-password"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[data-testid="form-submit"]')
    SMS_SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'ONAYLA VE GİRİŞ YAP')]")

    def __init__(self, driver=None, url=None):
        """
        Initializes the Login page and verifies required elements are present.
        """
        if driver is None:
            factory = DriverFactory()
            driver = factory.get_driver()
        self.url = url if url is not None else LoginPage.DEFAULT_URL
        super().__init__(driver)
        self.load()
        self.verify_page_loaded()

    def load(self):
        self.driver.get(self.url)

    def verify_page_loaded(self):
        """
        Verifies that the essential elements (email field, password field, and login button) are present on the page.
        """
        required_elements = {
            "Mail Field": LoginPage.EMAIL_INPUT,
            "Password Field": LoginPage.PASSWORD_INPUT,
            "Login Button": LoginPage.SUBMIT_BUTTON
        }
        self.verify_elements(required_elements)

    def enter_email(self, email: str):
        """
        Enters the provided email into the email input field.
        :param email: The email address to be entered.
        """
        email_input = self.find_element(self.EMAIL_INPUT)
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password: str):
        """
        Enters the provided password into the password input field.
        :param password: The password to be entered.
        """
        password_input = self.find_element(self.PASSWORD_INPUT)
        password_input.clear()
        password_input.send_keys(password)

    def click_submit_button(self):
        """
        Clicks the submit button identified by SUBMIT_BUTTON.
        """
        self.find_element(self.SUBMIT_BUTTON).click()

    def login(self, username=None, password=None):
        """
        Logs in with the provided or default credentials; if the SMS submit button appears, returns an SMSCodePage, otherwise returns self.
        :param username: Email to use for login (default: LoginPage.DEFAULT_USERNAME).
        :param password: Password to use for login (default: LoginPage.DEFAULT_PASSWORD).
        """
        user_mail = username if username is not None else LoginPage.DEFAULT_USERNAME
        password = password if password is not None else LoginPage.DEFAULT_PASSWORD

        self.enter_email(user_mail)
        self.enter_password(password)
        self.click_submit_button()
        try:
            self.find_element(self.SMS_SUBMIT_BUTTON)
            return SMSCodePage(self.driver)
        except self.TimeoutException:
            return self