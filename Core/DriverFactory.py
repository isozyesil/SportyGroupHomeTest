from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from Core.Config import Config


class DriverFactory:

    @staticmethod
    def create_driver():
        chrome_options = Options()

        mobile_emulation = {
            "deviceName": Config.MOBILE_DEVICE
        }
        chrome_options.add_experimental_option(
            "mobileEmulation", mobile_emulation
        )

        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-gpu")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

        return driver