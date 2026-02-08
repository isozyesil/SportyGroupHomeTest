from api.utils.logger import logger
import json

def assert_status_code(response, expected: int):
    if response.status_code != expected:
        logger.error(f"Status Code Assertion Failed: Expected {expected}, got {response.status_code}")
        try:
            logger.error(f"Response Body: {json.dumps(response.json(), indent=2)}")
        except:
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


def safe_text(response, limit: int = 500):
    try:
        text = response.text or ""
        return text[:limit]
    except Exception:
        return "<unreadable response body>"