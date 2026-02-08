from ui.pages.home_page import HomePage
from ui.pages.streamer_page import StreamerPage


class Pages:
    def __init__(self, driver):
        self.home_page = HomePage(driver)
        self.streamer_page = StreamerPage(driver)
