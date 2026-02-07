import pytest
from api.core.api_config import ApiConfig
from api.core.api_client import ApiClient


@pytest.fixture(scope="session")
def api_client():
    return ApiClient(
        base_url=ApiConfig.BASE_URL,
        headers=ApiConfig.headers(),
        timeout=ApiConfig.TIMEOUT,
        retries=ApiConfig.RETRIES,
    )
