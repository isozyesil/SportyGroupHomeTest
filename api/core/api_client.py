import time
import requests
import json
from api.utils import assert_status_code
from api.utils.logger import logger
from api.core.http_status import HttpStatus


class ApiClient:

    def __init__(self, base_url: str, headers: dict, timeout: int = 20, retries: int = 0):
        self.base_url = base_url.rstrip("/")
        self.headers = headers
        self.timeout = timeout
        self.retries = retries

    def request(
            self,
            method: str,
            path: str,
            params: dict | None = None,
            json_data: dict | None = None
    ):
        url = f"{self.base_url}/{path.lstrip('/')}"
        last_exc = None

        logger.info(f"API REQUEST: {method.upper()} {url}")
        if params:
            logger.info(f"PARAMS: {params}")
        if json_data:
            logger.info(f"BODY: {json.dumps(json_data, indent=2)}")

        for attempt in range(self.retries + 1):
            try:
                start_time = time.time()
                resp = requests.request(
                    method=method.upper(),
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=json_data,
                    timeout=self.timeout,
                )
                duration = time.time() - start_time

                logger.info(f"API RESPONSE: {resp.status_code} ({duration:.2f}s)")
                
                # Log response body if it fails, or if the API returns a quota error inside a 200 OK
                should_log_body = resp.status_code >= 400
                if resp.status_code == 200:
                    try:
                        body = resp.json()
                        # Sports API often returns errors inside 200 OK
                        if body.get("errors"):
                            should_log_body = True
                    except:
                        pass

                if should_log_body:
                    try:
                        logger.error(f"RESPONSE BODY: {json.dumps(resp.json(), indent=2)}")
                    except:
                        logger.error(f"RESPONSE TEXT: {resp.text}")

                if resp.status_code in (
                        HttpStatus.TOO_MANY_REQUESTS,
                        HttpStatus.INTERNAL_SERVER_ERROR,
                        HttpStatus.BAD_GATEWAY,
                        HttpStatus.SERVICE_UNAVAILABLE,
                        HttpStatus.GATEWAY_TIMEOUT
                ) and attempt < self.retries:
                    logger.warning(f"Retry attempt {attempt + 1} due to status {resp.status_code}")
                    time.sleep(1 + attempt)
                    continue

                return resp

            except requests.RequestException as exc:
                last_exc = exc
                logger.error(f"REQUEST FAILED: {str(exc)}")
                if attempt < self.retries:
                    time.sleep(1 + attempt)
                    continue
                raise last_exc

    def get(self, path: str, params: dict | None = None, expected_status: int | None = None):
        resp = self.request("GET", path, params=params)
        if expected_status:
            assert_status_code(resp, expected_status)
        return resp

    def post(self, path: str, json_data: dict | None = None, params: dict | None = None, expected_status: int | None = None):
        resp = self.request("POST", path, params=params, json=json_data)
        if expected_status:
            assert_status_code(resp, expected_status)
        return resp
