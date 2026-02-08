from ui import Config
import pytest


@pytest.mark.parametrize("game_name", ["Starcraft II"])
def test_search_and_open_streamer(pages, game_name):
    pages.home_page.search_and_select_game(game_name)
    pages.home_page.scroll_down(times=2)

    pages.streamer_page.click_random_streamer()
    pages.streamer_page.verify_stream_is_live()
    pages.streamer_page.capture_screenshot(f"test_search_and_open_streamer_{game_name}")
