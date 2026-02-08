from ui.core.ui_config import Config
import os
from datetime import datetime


def take_screenshot(driver, test_name):
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"{Config.SCREENSHOT_DIR}/{test_name}_{timestamp}.png"
    driver.save_screenshot(file_path)