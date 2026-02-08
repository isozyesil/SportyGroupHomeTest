from ui.core.ui_config import Config


def scroll_down(driver, pixels=None, times=1):
    pixels = pixels or Config.SCROLL_PIXELS
    for _ in range(times):
        driver.execute_script(f"window.scrollBy(0, {pixels});")