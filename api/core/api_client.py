import time
import requests
from api.utils import assert_status_code
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
            json: dict | None = None
    ):
        url = f"{self.base_url}/{path.lstrip('/')}"
        last_exc = None

        for attempt in range(self.retries + 1):
            try:
                resp = requests.request(
                    method=method.upper(),
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=json,
                    timeout=self.timeout,
                )

                if resp.status_code in (
                        HttpStatus.TOO_MANY_REQUESTS,
                        HttpStatus.INTERNAL_SERVER_ERROR,
                        HttpStatus.BAD_GATEWAY,
                        HttpStatus.SERVICE_UNAVAILABLE,
                        HttpStatus.GATEWAY_TIMEOUT
                ) and attempt < self.retries:
                    time.sleep(1 + attempt)
                    continue

                return resp

            except requests.RequestException as exc:
                last_exc = exc
                if attempt < self.retries:
                    time.sleep(1 + attempt)
                    continue
                raise last_exc

    def get(self, path: str, params: dict | None = None, expected_status: int | None = None):
        resp = self.request("GET", path, params=params)
        if expected_status:
            assert_status_code(resp, expected_status)
        return resp

    def post(self, path: str, json: dict | None = None, params: dict | None = None, expected_status: int | None = None):
        resp = self.request("POST", path, params=params, json=json)
        if expected_status:
            assert_status_code(resp, expected_status)
        return resp
