import os


class ApiConfig:
    BASE_URL = os.getenv("API_BASE_URL", "https://v3.football.api-sports.io")
    API_KEY = os.getenv("API_KEY", "022308117e1535e2d0b5c6082ea7272a")
    TIMEOUT = int(os.getenv("API_TIMEOUT", "20"))
    RETRIES = int(os.getenv("API_RETRIES", "2"))

    @staticmethod
    def headers():
        if not ApiConfig.API_KEY:
            raise RuntimeError(
                "API_KEY is not set. Set it as an environment variable: export API_KEY='...'"
            )
        return {"x-apisports-key": ApiConfig.API_KEY}
