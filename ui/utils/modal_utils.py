from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from ui.utils.wait_utils import wait_until
from selenium.webdriver.support import expected_conditions as EC
from ui.core.ui_config import Config


CONTENT_GATE = (By.XPATH, "//div[@data-a-target='content-classification-gate-overlay']")
START_WATCHING_BUTTON = (By.XPATH, "//button[@data-a-target='content-classification-gate-overlay-start-watching-button']")
GENERIC_CLOSE_BUTTON = (By.XPATH, "//button[@aria-label='Close']")

COOKIE_ACCEPT_BUTTON = (
    By.XPATH,
    "//button[normalize-space()='Accept' or .//*[normalize-space()='Accept']]"
)
COOKIE_IFRAME_LOCATOR = (
    By.XPATH,
    "//iframe[starts-with(@id,'sp_message_iframe') or contains(@name,'sp_message_iframe') or contains(@title,'privacy') or contains(@title,'consent') or contains(@title,'message')]"
)


def _try_click(driver, locator, timeout):
    try:
        wait_until(driver, EC.element_to_be_clickable(locator), timeout).click()
        return True
    except TimeoutException:
        return False


def _accept_cookies_if_present(driver, timeout):
    if _try_click(driver, COOKIE_ACCEPT_BUTTON, timeout):
        return True

    try:
        iframes = driver.find_elements(*COOKIE_IFRAME_LOCATOR)
    except Exception:
        iframes = []

    for frame in iframes:
        try:
            driver.switch_to.frame(frame)
            if _try_click(driver, COOKIE_ACCEPT_BUTTON, timeout):
                driver.switch_to.default_content()
                return True
        except Exception:
            pass
        finally:
            try:
                driver.switch_to.default_content()
            except Exception:
                pass
    return False


def dismiss_modal_if_present(driver, timeout=None):
    timeout = timeout or 2

    try:
        if _accept_cookies_if_present(driver, timeout):
            return
    except Exception:
        pass

    try:
        wait_until(driver, EC.presence_of_element_located(CONTENT_GATE), timeout)
        wait_until(
            driver,
            EC.element_to_be_clickable(START_WATCHING_BUTTON),
            timeout
        ).click()
        return
    except TimeoutException:
        pass

    try:
        wait_until(
            driver,
            EC.element_to_be_clickable(GENERIC_CLOSE_BUTTON),
            timeout
        ).click()
    except TimeoutException:
        pass
