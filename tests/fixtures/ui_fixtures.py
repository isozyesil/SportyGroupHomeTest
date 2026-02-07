import pytest


@pytest.fixture
def driver():
    # Lazy import so API runs do not import Selenium
    from ui.core.driver_factory import create_driver
    driver = create_driver()
    yield driver
    driver.quit()
