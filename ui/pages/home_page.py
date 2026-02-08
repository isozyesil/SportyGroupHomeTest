from selenium.webdriver.common.by import By
from ui.pages.base_page import BasePage


class HomePage(BasePage):
    BROWSE_BUTTON = (By.XPATH, "//a[.//div[normalize-space()='Browse']]")
    SEARCH_TEXTBOX = (By.XPATH, "//input[@type='search' and @placeholder='Search']")
    SEARCH_RESULTS = (By.XPATH, "//ul//li//a[contains(@href,'/directory')]")
    STREAMER_CARD = (By.XPATH, "//a[contains(@href, '/')]")
    KEEP_USING_WEB = (By.XPATH, "//button[p[normalize-space()='Keep using web']]")
    EMPTY_OVERLAY = (By.XPATH, "//div[contains(@class,'ScTouchActionFilter')]")

    def click_empty_overlay(self):
        self.click(self.EMPTY_OVERLAY)

    def click_search(self):
        self.click(self.BROWSE_BUTTON)

    def search_for_game(self, game_name):
        self.type(self.SEARCH_TEXTBOX, game_name)

    def search_and_select_game(self, game_name):
        self.click_search()
        self.search_for_game(game_name)
        self.click_first_search_result_with_text(game_name)

    def click_first_search_result_with_text(self, expected_text):
        results = self.find_elements(self.SEARCH_RESULTS)
        for result in results:
            if expected_text.lower() in result.text.lower():
                result.click()
                return
        raise AssertionError(f"No search result contains text: {expected_text}")