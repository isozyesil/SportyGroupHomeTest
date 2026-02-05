from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage
from Utils.Scrolling import scroll_down


class HomePage(BasePage):

    SEARCH_BUTTON = (By.XPATH, "//a[@aria-label='Search']")
    SEARCH_INPUT = (By.XPATH, "//input[@type='search']")
    STREAMER_CARD = (By.XPATH, "//a[contains(@href, '/')]")
    KEEP_USING_WEB = (By.XPATH, "//button[p[normalize-space()='Keep using web']]")
    EMPTY_OVERLAY = (By.XPATH, "//div[contains(@class,'ScTouchActionFilter')]")

    def open(self, url):
        self.driver.get(url)

    def click_keep_using_web(self):
        self.driver.find_element(*self.KEEP_USING_WEB).click()

    def click_empty_overlay(self):
        self.driver.find_element(*self.EMPTY_OVERLAY).click()

    def click_search(self):
        self.wait_for_clickable(self.SEARCH_BUTTON).click()

    def search_for_game(self, game_name):
        search_input = self.wait_for_visibility(self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(game_name)

    def scroll_and_select_streamer(self):
        scroll_down(self.driver, times=2)
        self.wait_for_clickable(self.STREAMER_CARD).click()