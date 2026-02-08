from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from ui.utils.wait_utils import wait_until
from selenium.webdriver.support import expected_conditions as EC
from ui.core.ui_config import Config


CONTENT_GATE = (By.XPATH, "//div[@data-a-target='content-classification-gate-overlay']")
START_WATCHING_BUTTON = (By.XPATH, "//button[@data-a-target='content-classification-gate-overlay-start-watching-button']")
GENERIC_CLOSE_BUTTON = (By.XPATH, "//button[@aria-label='Close']")


def dismiss_modal_if_present(driver, timeout=None):
    timeout = timeout or 2
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
