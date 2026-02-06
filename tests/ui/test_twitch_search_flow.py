from core.config import Config
from pages.home_page import HomePage
from pages.streamer_page import StreamerPage


def test_search_and_open_streamer(driver):
    home_page = HomePage(driver)
    streamer_page = StreamerPage(driver)
    home_page.open(Config.BASE_URL)  # Go to Twitch
    home_page.click_empty_overlay()  # Exit from Browser Suggestion or Downloading App
    home_page.click_search()  # Click on Browser Button
    home_page.search_for_game("Hunt")  # Search for Starcraft
    home_page.click_first_search_result_with_text("Hunt")  # Pick First Result that Matches with "Starcraft II"
    home_page.scroll_down()  # First Scroll Down
    home_page.scroll_down()
    home_page.scroll_down()
    streamer_page.click_random_streamer()
    streamer_page.verify_stream_is_live()
    streamer_page.capture_screenshot("test_search_and_open_streamer")