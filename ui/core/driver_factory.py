from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ui.core import Config


def create_driver():
    options = Options()

    if Config.MOBILE_DEVICE:
        options.add_experimental_option(
            "mobileEmulation",
            {"deviceName": Config.MOBILE_DEVICE}
        )

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    return driver
