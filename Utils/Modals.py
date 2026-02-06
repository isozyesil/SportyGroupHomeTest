from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



CONTENT_GATE = (By.XPATH,"//div[@data-a-target='content-classification-gate-overlay']")
START_WATCHING_BUTTON = (By.XPATH,"//button[@data-a-target='content-classification-gate-overlay-start-watching-button']")
GENERIC_CLOSE_BUTTON = ( By.XPATH,"//button[@aria-label='Close']")


def dismiss_modal_if_present(driver, timeout=5):
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(EC.presence_of_element_located(CONTENT_GATE))

        wait.until(
            EC.element_to_be_clickable(START_WATCHING_BUTTON)
        ).click()

        return

    except TimeoutException:
        pass


    try:
        wait.until(
            EC.element_to_be_clickable(GENERIC_CLOSE_BUTTON)
        ).click()

    except TimeoutException:
        pass
