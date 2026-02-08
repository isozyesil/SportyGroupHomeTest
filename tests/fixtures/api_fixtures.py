import pytest
from api import ApiConfig, ApiClient
from api.utils.logger import logger


@pytest.fixture(scope="function")
def api_client(request):
    test_name = request.node.name
    logger.info(f"STARTING API TEST: {test_name}")
    
    client = ApiClient(
        base_url=ApiConfig.BASE_URL,
        headers=ApiConfig.headers(),
        timeout=ApiConfig.TIMEOUT,
        retries=ApiConfig.RETRIES,
    )
    yield client
    
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        logger.error(f"API TEST FAILED: {test_name}")
    
    logger.info(f"ENDING API TEST: {test_name}")
