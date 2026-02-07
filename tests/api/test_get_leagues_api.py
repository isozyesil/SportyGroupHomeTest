import pytest
from api.core.endpoints import Endpoints
from api.utils.assert_utils import assert_status_code, assert_has_keys


def test_get_leagues_status_code(api_client):
    resp = api_client.get(Endpoints.LEAGUES)
    assert_status_code(resp, 200)


def test_leagues_response_contains_expected_keys(api_client):
    resp = api_client.get(Endpoints.LEAGUES)
    assert_status_code(resp, 200)

    data = resp.json()
    assert_has_keys(data, ["response"])

    assert isinstance(data["response"], list)
    assert len(data["response"]) > 0

    first = data["response"][0]
    assert_has_keys(first, ["league", "country", "seasons"])


@pytest.mark.parametrize(
    "query_params, expected_min_length",
    [
        ({}, 1),
        ({"name": "Premier League"}, 1),
    ]
)
def test_leagues_filtering(api_client, query_params, expected_min_length):
    resp = api_client.get(Endpoints.LEAGUES, params=query_params)
    assert_status_code(resp, 200)

    data = resp.json()
    assert "response" in data
    assert len(data["response"]) >= expected_min_length
