import pytest
from api.utils.logger import logger


@pytest.fixture
def driver(request):
    from ui import create_driver
    test_name = request.node.name
    logger.info(f"STARTING TEST: {test_name}")
    
    driver = create_driver()
    yield driver
    
    # Check if test failed
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        logger.error(f"TEST FAILED: {test_name}")
        from ui.utils import take_screenshot
        take_screenshot(driver, f"FAILURE_{test_name}")
    
    logger.info(f"ENDING TEST: {test_name}")
    driver.quit()


@pytest.fixture
def pages(driver):
    from ui import Pages, Config
    logger.info(f"Navigating to {Config.BASE_URL}")
    driver.get(Config.BASE_URL)
    pages = Pages(driver)
    logger.info("Dismissing initial overlay if present")
    pages.home_page.click_empty_overlay()
    return pages
