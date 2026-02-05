from Core.Config import Config
from Pages.HomePage import HomePage
from Pages.StreamerPage import StreamerPage


def test_search_and_open_streamer(driver):
    home_page = HomePage(driver)
    streamer_page = StreamerPage(driver)

    home_page.open(Config.BASE_URL)
    home_page.click_empty_overlay()
    home_page.click_search()
    home_page.search_for_game("StarCraft II")
    home_page.scroll_and_select_streamer()


    streamer_page.wait_until_loaded()
    streamer_page.capture_screenshot("test_search_and_open_streamer")