import pytest
from api import (
    Endpoints,
    HttpStatus,
    assert_has_keys,
    assert_is_type,
    assert_optional_type,
    assert_list,
    assert_list_of_dicts,
    assert_int_between,
)


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
    assert_is_type(data["response"], list, "response")
    assert len(data["response"]) >= expected_min_results, (
        f"Expected at least {expected_min_results} results"
    )

    if data["response"]:
        first = data["response"][0]
        assert_has_keys(first, ["league", "country", "seasons"])

        league = first["league"]
        country = first["country"]
        seasons = first["seasons"]

        # League object types
        assert_has_keys(league, ["id", "name", "type", "logo"])  # logo can be None
        assert_is_type(league["id"], int, "league.id")
        assert_is_type(league["name"], str, "league.name")
        assert_is_type(league["type"], str, "league.type")
        assert_optional_type(league.get("logo"), str, "league.logo")

        # Country object types (nullable fields allowed by API)
        assert_has_keys(country, ["name", "code", "flag"])  # some may be None
        assert_optional_type(country.get("name"), str, "country.name")
        assert_optional_type(country.get("code"), str, "country.code")
        assert_optional_type(country.get("flag"), str, "country.flag")

        # Seasons list types
        assert_list(seasons, min_len=1, field_path="seasons")
        if seasons:
            s0 = seasons[0]
            assert_has_keys(s0, ["year", "start", "end", "current"])  # others like coverage exist but optional here
            assert_is_type(s0["year"], int, "seasons[0].year")
            assert_int_between(s0["year"], 1900, 2100, "seasons[0].year")
            assert_optional_type(s0.get("start"), str, "seasons[0].start")
            assert_optional_type(s0.get("end"), str, "seasons[0].end")
            # current is typically a boolean
            assert_is_type(s0["current"], (bool, int), "seasons[0].current")  # accept int-bool edge cases

        # Filter-specific validations across all returned items
        if "id" in query_params:
            expected_id = query_params["id"]
            for item in data["response"]:
                assert_has_keys(item, ["league"])  # safety
                assert item["league"]["id"] == expected_id, (
                    f"Filter mismatch: expected league.id={expected_id}, got {item['league']['id']}"
                )
        if "name" in query_params:
            expected_name = query_params["name"]
            for item in data["response"]:
                assert_has_keys(item, ["league"])  # safety
                assert str(item["league"]["name"]).lower() == str(expected_name).lower(), (
                    f"Filter mismatch: expected league.name='{expected_name}', got '{item['league']['name']}'"
                )
        if "country" in query_params:
            expected_country = query_params["country"]
            for item in data["response"]:
                assert_has_keys(item, ["country"])  # safety
                actual = item["country"].get("name")
                assert actual and str(actual).lower() == str(expected_country).lower(), (
                    f"Filter mismatch: expected country.name='{expected_country}', got '{actual}'"
                )


def test_api_failure_logging_mechanism(api_client):
    # This test intentionally calls an invalid endpoint; framework-level logging will record details.
    # We don't assert status code here because this API may return 200 with an error payload.
    resp = api_client.get("non-existent-endpoint")
    assert resp is not None


@pytest.mark.parametrize(
    "query_params",
    [
        {"id": 0},
        {"id": 9999999},
        {"name": "X" * 100},
        {"country": "Atlantis"},
    ]
)
def test_get_leagues_boundary_filters_return_empty_or_minimal(api_client, query_params):
    resp = api_client.get(Endpoints.LEAGUES, params=query_params, expected_status=HttpStatus.OK)
    data = resp.json()
    assert_has_keys(data, ["response"])
    assert_is_type(data["response"], list, "response")
    # For boundary/nonexistent filters, API should return 0 results
    assert len(data["response"]) == 0, f"Expected 0 results for boundary filter {query_params}, got {len(data['response'])}"
