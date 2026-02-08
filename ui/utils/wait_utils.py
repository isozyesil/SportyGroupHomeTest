from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from ui.core.ui_config import Config


def wait_until(driver, condition, timeout=None, message=""):
    return WebDriverWait(driver, timeout or Config.EXPLICIT_WAIT).until(condition, message)


def wait_until_not(driver, condition, timeout=None, message=""):
    return WebDriverWait(driver, timeout or Config.EXPLICIT_WAIT).until_not(condition, message)


def is_visible(driver, locator, timeout=None):
    try:
        wait_until(driver, EC.visibility_of_element_located(locator), timeout or Config.IMPLICIT_WAIT)
        return True
    except TimeoutException:
        return False


def is_clickable(driver, locator, timeout=None):
    try:
        wait_until(driver, EC.element_to_be_clickable(locator), timeout or Config.IMPLICIT_WAIT)
        return True
    except TimeoutException:
        return False
