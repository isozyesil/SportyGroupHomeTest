import pytest


@pytest.fixture
def driver():
    from ui import create_driver
    driver = create_driver()
    yield driver
    driver.quit()


@pytest.fixture
def pages(driver):
    from ui import Pages, Config
    driver.get(Config.BASE_URL)
    pages = Pages(driver)
    pages.home_page.click_empty_overlay()
    return pages
