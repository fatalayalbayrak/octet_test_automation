from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from utils.logger import logger
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementNotInteractableException,
    WebDriverException
)

class BasePage:
    driver: WebDriver = None
    ENTER_KEY = Keys.ENTER
    TimeoutException = TimeoutException
    NoSuchElementException = NoSuchElementException
    StaleElementReferenceException = StaleElementReferenceException
    ElementNotInteractableException = ElementNotInteractableException
    WebDriverException = WebDriverException

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logger

    def find_element(self, locator):
        """
        Waits until the element located by 'locator' is visible and returns it.
        :return: The visible WebElement.
        """
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_element_clickable(self, locator):
        """
        Waits until the element located by 'locator' is clickable and returns it.
        :return: The clickable WebElement.
        """
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_elements(self, locator):
        """
        Returns a list of all elements matching the given locator.
        :param locator: A tuple containing the Selenium By strategy and locator value.
        :return: List of WebElement objects.
        """
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def is_element_present(self, locator) -> bool:
        """Returns True if the element is present and visible, else False."""
        try:
            self.find_element(locator)
            return True
        except (TimeoutException, NoSuchElementException,
                StaleElementReferenceException, ElementNotInteractableException,
                WebDriverException):
            return False

    def verify_elements(self, required_elements: dict):
        """
        Verifies that all required elements are present.
        :param required_elements: A dictionary with keys as element descriptions and values as locators.
        :raises AssertionError: If one or more elements are not found.
        """
        missing_elements = [
            name for name, locator in required_elements.items()
            if not self.is_element_present(locator)
        ]
        if missing_elements:
            raise AssertionError(
                f"{self.__class__.__name__} missing elements: {', '.join(missing_elements)}"
            )
