import random
from selenium.webdriver.common.by import By
from ui.pages.base_page import BasePage
from ui.utils import take_screenshot
from selenium.webdriver.common.action_chains import ActionChains


class StreamerPage(BasePage):
    VIDEO_PLAYER = (By.TAG_NAME, "video")
    VIDEO_STREAM_OVERLAY = (By.XPATH, "//div[@data-a-target='player-overlay-click-handler']")
    ALL_STREAMER_CARDS = (By.XPATH, "//button[contains(@aria-label, 'Live with')]")
    SHOW_PLAYER_CONTROLS = (By.XPATH,
                            "//div[@data-a-target='tw-core-button-label-text' and contains(text(),'Show player controls')]")

    def wait_until_loaded(self):
        self.wait_for_page_ready()
        self.find(self.VIDEO_PLAYER)

    def capture_screenshot(self, test_name):
        take_screenshot(self.driver, test_name)

    def click_random_streamer(self):
        streamers = self.find_elements(self.ALL_STREAMER_CARDS)
        assert streamers, "No streamer cards found"
        target = random.choice(streamers)
        self.js_click(target)

    def verify_stream_is_live(self):
        self._click_video_stream()
        self.wait_until_loaded()
        return True

    def _click_video_stream(self):
        self.wait_for_page_ready()
        video = self.find(self.VIDEO_STREAM_OVERLAY)
        ActionChains(self.driver).move_to_element(video).perform()
        self.js_click(video)