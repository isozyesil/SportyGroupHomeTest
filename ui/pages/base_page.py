from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
from ui.utils.modal_utils import dismiss_modal_if_present
from ui.utils.wait_utils import wait_until, wait_until_not
from ui.utils.scrolling_utils import scroll_down as scroll_down_util
from ui.core.ui_config import Config


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.timeout = Config.EXPLICIT_WAIT

    def find(self, locator, timeout=None):
        return self.wait_for_visibility(locator, timeout)

    def find_elements(self, locator, timeout=None):
        return self.wait_for_elements(locator, timeout)

    def click(self, locator, timeout=None):
        try:
            self.wait_for_clickable(locator, timeout).click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            dismiss_modal_if_present(self.driver)
            self.wait_for_clickable(locator, timeout).click()

    def type(self, locator, text, timeout=None):
        try:
            element = self.find(locator, timeout)
            element.clear()
            element.send_keys(text)
        except (ElementClickInterceptedException, ElementNotInteractableException):
            dismiss_modal_if_present(self.driver)
            element = self.find(locator, timeout)
            element.clear()
            element.send_keys(text)

    def wait_for_visibility(self, locator, timeout=None):
        return wait_until(
            self.driver,
            EC.visibility_of_element_located(locator),
            timeout=timeout or self.timeout
        )

    def wait_for_invisibility(self, locator, timeout=None):
        return wait_until_not(
            self.driver,
            EC.visibility_of_element_located(locator),
            timeout=timeout or self.timeout
        )

    def wait_for_clickable(self, locator, timeout=None):
        return wait_until(
            self.driver,
            EC.element_to_be_clickable(locator),
            timeout=timeout or self.timeout
        )

    def wait_for_elements(self, locator, timeout=None):
        return wait_until(
            self.driver,
            EC.presence_of_all_elements_located(locator),
            timeout=timeout or self.timeout
        )

    def scroll_down(self, times=1):
        scroll_down_util(self.driver, times=times)

    def wait_for_page_ready(self, timeout=None):
        wait_until(
            self.driver,
            lambda d: d.execute_script("return document.readyState") == "complete",
            timeout=timeout or Config.PAGE_LOAD_TIMEOUT
        )
        dismiss_modal_if_present(self.driver)

    def js_click(self, element_or_locator):
        element = element_or_locator
        if isinstance(element_or_locator, tuple):
            element = self.find(element_or_locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)