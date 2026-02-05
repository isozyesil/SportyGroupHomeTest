from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage
from Utils.Modals import dismiss_modal_if_present
from Utils.Screenshots import take_screenshot


class StreamerPage(BasePage):

    VIDEO_PLAYER = (By.TAG_NAME, "video")

    def wait_until_loaded(self):
        dismiss_modal_if_present(self.driver)
        self.wait_for_visibility(self.VIDEO_PLAYER)

    def capture_screenshot(self, test_name):
        take_screenshot(self.driver, test_name)