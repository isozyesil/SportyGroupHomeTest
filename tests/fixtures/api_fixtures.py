import pytest
from api import ApiConfig, ApiClient


@pytest.fixture(scope="session")
def api_client():
    return ApiClient(
        base_url=ApiConfig.BASE_URL,
        headers=ApiConfig.headers(),
        timeout=ApiConfig.TIMEOUT,
        retries=ApiConfig.RETRIES,
    )
