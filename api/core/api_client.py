import time
import requests


class ApiClient:
    """
    Lightweight requests wrapper:
    - base_url + default headers
    - timeout
    - simple retry for transient failures (5xx / 429 / network)
    """

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

                # Retry on rate limit / server errors
                if resp.status_code in (429, 500, 502, 503, 504) and attempt < self.retries:
                    time.sleep(1 + attempt)
                    continue

                return resp

            except requests.RequestException as exc:
                last_exc = exc
                if attempt < self.retries:
                    time.sleep(1 + attempt)
                    continue
                raise last_exc

    def get(self, path: str, params: dict | None = None):
        return self.request("GET", path, params=params)

    def post(self, path: str, json: dict | None = None, params: dict | None = None):
        return self.request("POST", path, params=params, json=json)
