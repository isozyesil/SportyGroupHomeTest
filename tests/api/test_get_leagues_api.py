import pytest
from api import Endpoints, HttpStatus, assert_has_keys


@pytest.mark.parametrize(
    "test_id, query_params, expected_min_results",
    [
        ("API-01_Status_Check", {}, 1),
        ("API-02_Schema_Validation", {}, 1),
        ("API-03_ID_Filter", {"id": 39}, 1),
        ("API-04_Name_Filter", {"name": "Premier League"}, 1),
        ("API-05_Country_Filter", {"country": "England"}, 1),
    ]
)
def test_get_leagues_parametrized(api_client, test_id, query_params, expected_min_results):
    resp = api_client.get(
        Endpoints.LEAGUES,
        params=query_params,
        expected_status=HttpStatus.OK
    )
    data = resp.json()

    assert_has_keys(data, ["response"])
    assert isinstance(data["response"], list)

    assert len(data["response"]) >= expected_min_results, f"Expected at least {expected_min_results} results"

    if len(data["response"]) > 0:
        first = data["response"][0]
        assert_has_keys(first, ["league", "country", "seasons"])


def test_api_failure_logging_mechanism(api_client):
    api_client.get("non-existent-endpoint")
