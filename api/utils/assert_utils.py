def assert_status_code(response, expected: int):
    assert response.status_code == expected, (
        f"Expected status {expected}, got {response.status_code}. "
        f"Body: {safe_text(response)}"
    )


def assert_has_keys(obj: dict, keys: list[str]):
    missing = [k for k in keys if k not in obj]
    assert not missing, f"Missing keys: {missing}. Actual keys: {list(obj.keys())}"


def safe_text(response, limit: int = 500):
    try:
        text = response.text or ""
        return text[:limit]
    except Exception:
        return "<unreadable response body>"