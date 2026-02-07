from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from ui.pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class HomePage(BasePage):
    BROWSE_BUTTON = (By.XPATH, "//a[.//div[normalize-space()='Browse']]")
    SEARCH_TEXTBOX = (By.XPATH, "//input[@type='search' and @placeholder='Search']")
    SEARCH_RESULTS = (By.XPATH, "//ul//li//a[contains(@href,'/directory')]")
    STREAMER_CARD = (By.XPATH, "//a[contains(@href, '/')]")
    KEEP_USING_WEB = (By.XPATH, "//button[p[normalize-space()='Keep using web']]")
    EMPTY_OVERLAY = (By.XPATH, "//div[contains(@class,'ScTouchActionFilter')]")

    def open(self, url):
        self.driver.get(url)

    def click_empty_overlay(self):
        self.driver.find_element(*self.EMPTY_OVERLAY).click()

    def click_search(self):
        self.wait_for_visibility(self.BROWSE_BUTTON)
        self.wait_for_clickable(self.BROWSE_BUTTON).click()

    def search_for_game(self, game_name):
        self._click_search_box()
        search_input = self.wait_for_visibility(self.SEARCH_TEXTBOX)
        search_input.clear()
        search_input.send_keys(game_name)

    def _click_search_box(self):
        search_input = self.wait_for_visibility(self.SEARCH_TEXTBOX)
        search_input.click()

    def click_first_search_result_with_text(self, expected_text):
        results = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.SEARCH_RESULTS))
        for result in results:
            if expected_text.lower() in result.text.lower():
                result.click()
                return
        raise AssertionError(f"No search result contains text: {expected_text}")
