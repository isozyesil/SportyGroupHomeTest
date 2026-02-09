import time
import requests
import json
from api.utils import assert_status_code
from api.utils.logger import logger
from api.core.http_status import HttpStatus

_MAX_LOG_BODY_CHARS = 2000

def _truncate_for_log(text: str) -> str:
    if text is None:
        return ""
    if len(text) > _MAX_LOG_BODY_CHARS:
        return text[:_MAX_LOG_BODY_CHARS] + f"... [truncated {len(text) - _MAX_LOG_BODY_CHARS} chars]"
    return text


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
                
                # Always log body/text at INFO (truncated) for observability
                try:
                    body = resp.json()
                    pretty = json.dumps(body, indent=2)
                    logger.info(f"RESPONSE BODY: {_truncate_for_log(pretty)}")
                except Exception:
                    logger.info(f"RESPONSE TEXT: {_truncate_for_log(resp.text or '')}")

                # Framework-level failure logging: escalate 4xx/5xx to ERROR with context
                if resp.status_code >= 400:
                    ctx = {
                        "method": method.upper(),
                        "url": url,
                        "params": params or {},
                        "status": resp.status_code,
                    }
                    try:
                        body = resp.json()
                        pretty = json.dumps(body, indent=2)
                        body_str = _truncate_for_log(pretty)
                    except Exception:
                        body_str = _truncate_for_log(resp.text or "")
                    logger.error(f"API ERROR: {ctx} | BODY: {body_str}")

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
        resp = self.request("POST", path, params=params, json_data=json_data)
        if expected_status:
            assert_status_code(resp, expected_status)
        return resp
