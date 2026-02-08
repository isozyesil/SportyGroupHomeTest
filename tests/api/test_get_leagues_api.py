import pytest
from api import Endpoints, HttpStatus, assert_has_keys


@pytest.mark.parametrize(
    "query_params, expected_min_results",
    [
        ({}, 1),
        ({"name": "Premier League"}, 1),
    ]
)
def test_get_leagues_parametrized(api_client, query_params, expected_min_results):
    """
    Unified API test for Leagues endpoint.
    Covers:
    - API-01: Status Code Validation (via expected_status)
    - API-02: Schema/Keys Validation
    - API-03: Basic Fetch (no params)
    - API-04: Filtered Fetch (with params)
    """
    # 1. Status Code & Execution
    resp = api_client.get(
        Endpoints.LEAGUES,
        params=query_params,
        expected_status=HttpStatus.OK
    )
    data = resp.json()

    # 2. Schema Validation (Root response key)
    assert_has_keys(data, ["response"])
    assert isinstance(data["response"], list)

    # 3. Content & Item Schema Validation
    assert len(data["response"]) >= expected_min_results, f"Expected at least {expected_min_results} results"

    if len(data["response"]) > 0:
        first = data["response"][0]
        assert_has_keys(first, ["league", "country", "seasons"])
