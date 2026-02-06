from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.Modals import dismiss_modal_if_present


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def wait_for_visibility(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_elements(self, locator):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )

    def scroll_down(self):
        self.driver.execute_script("window.scrollBy(0, 500);")

    def wait_for_page_ready(self):
        WebDriverWait(self.driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        dismiss_modal_if_present(self.driver)
