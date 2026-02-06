import requests
import pytest

BASE_URL = "https://v3.football.api-sports.io"
API_KEY = "022308117e1535e2d0b5c6082ea7272a"

HEADERS = {
    "x-apisports-key": API_KEY
}

def test_get_leagues_status_code():

    response = requests.get(f"{BASE_URL}/leagues", headers=HEADERS)
    assert response.status_code == 200


def test_leagues_response_contains_expected_keys():

    response = requests.get(f"{BASE_URL}/leagues", headers=HEADERS)
    data = response.json()


    assert "response" in data
    assert isinstance(data["response"], list)
    assert len(data["response"]) > 0


    first_league = data["response"][0]
    assert "league" in first_league
    assert "country" in first_league
    assert "seasons" in first_league


@pytest.mark.parametrize(
    "query_params, expected_min_length",
    [
        ({}, 1),                         # no params
        ({"name": "Premier League"}, 1), # search by name
        ({"country": "England"}, 1),     # filter by country
    ]
)
def test_leagues_with_query_params(query_params, expected_min_length):

    response = requests.get(
        f"{BASE_URL}/leagues",
        headers=HEADERS,
        params=query_params
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["response"], list)
    assert len(data["response"]) >= expected_min_length
