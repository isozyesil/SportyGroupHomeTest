import pytest
from Core.DriverFactory import DriverFactory


@pytest.fixture(scope="session")
def driver():
    driver = DriverFactory.create_driver()
    yield driver
    driver.quit()
