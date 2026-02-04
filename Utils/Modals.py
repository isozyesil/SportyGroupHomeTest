from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def dismiss_modal_if_present(driver, timeout=5):
    try:
        wait = WebDriverWait(driver, timeout)
        close_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='Close']")
            )
        )
        close_button.click()
    except TimeoutException:
        pass
