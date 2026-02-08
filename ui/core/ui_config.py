import os


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://www.twitch.tv")

    BROWSER = os.getenv("BROWSER", "chrome")
    MOBILE_DEVICE = os.getenv("MOBILE_DEVICE", "Pixel 2")

    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "60"))
    SCROLL_PIXELS = int(os.getenv("SCROLL_PIXELS", "500"))

    SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "Screenshots")
