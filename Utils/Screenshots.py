import os
from datetime import datetime


def take_screenshot(driver, test_name):
    os.makedirs("Screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"Screenshots/{test_name}_{timestamp}.png"
    driver.save_screenshot(file_path)