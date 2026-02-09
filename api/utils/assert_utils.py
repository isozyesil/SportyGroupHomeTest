from api.utils.logger import logger
import json
from typing import Any, Iterable, Optional, Type, Union


def assert_status_code(response, expected: int):
    if response.status_code != expected:
        logger.error(f"Status Code Assertion Failed: Expected {expected}, got {response.status_code}")
        try:
            logger.error(f"Response Body: {json.dumps(response.json(), indent=2)}")
        except Exception:
            logger.error(f"Response Text: {response.text}")

    assert response.status_code == expected, (
        f"Expected status {expected}, got {response.status_code}. "
        f"Body: {safe_text(response)}"
    )


def assert_has_keys(obj: dict, keys: list[str]):
    missing = [k for k in keys if k not in obj]
    if missing:
        logger.error(f"Key Assertion Failed: Missing {missing}. Actual keys: {list(obj.keys())}")
        logger.error(f"Object Content: {json.dumps(obj, indent=2)}")

    assert not missing, f"Missing keys: {missing}. Actual keys: {list(obj.keys())}"


def assert_is_type(value: Any, expected_type: Union[Type, tuple[Type, ...]], field_path: str = "value"):
    assert isinstance(value, expected_type), (
        f"Type mismatch for {field_path}: expected {expected_type}, got {type(value)} with value {value!r}"
    )


def assert_optional_type(value: Any, expected_type: Union[Type, tuple[Type, ...]], field_path: str = "value"):
    if value is None:
        return
    assert_is_type(value, expected_type, field_path)


def assert_list(value: Any, min_len: int = 0, field_path: str = "value"):
    assert isinstance(value, list), f"{field_path} must be a list, got {type(value)}"
    assert len(value) >= min_len, f"{field_path} expected min length {min_len}, got {len(value)}"


def assert_list_of_dicts(items: Any, min_len: int = 0, field_path: str = "items"):
    assert_list(items, min_len=min_len, field_path=field_path)
    for i, it in enumerate(items):
        assert isinstance(it, dict), f"{field_path}[{i}] must be dict, got {type(it)}"


def safe_text(response, limit: int = 500):
    try:
        text = response.text or ""
        return text[:limit]
    except Exception:
        return "<unreadable response body>"