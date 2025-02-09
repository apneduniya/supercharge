import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException, Timeout, ConnectionError
from urllib3.util.retry import Retry
import time

from core.helpers.api import ApiError, ApiRouter


class BaseAPIService:
    def __init__(self, service_name, base_url, headers=None, max_requests_per_minute=60):
        self.service_name = service_name
        self.base_url = base_url
        self.headers = headers or {}
        self.max_requests_per_minute = max_requests_per_minute
        self.request_count = 0
        self.last_request_time = 0

        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.setup_retries()

    def setup_retries(self) -> None:
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def check_rate_limit(self) -> None:
        now = time.time()
        time_window = 60  # 1 minute window

        if now - self.last_request_time > time_window:
            self.request_count = 0
            self.last_request_time = now

        if self.request_count >= self.max_requests_per_minute:
            wait_time = self.last_request_time + time_window - now
            raise ApiError("RATE_LIMIT_EXCEEDED", "Rate limit exceeded", {"retry_after": wait_time})

        self.request_count += 1
        self.last_request_time = now

    def handle_http_error(self, error) -> ApiError:
        if isinstance(error, Timeout):
            return ApiError("TIMEOUT", "Request timed out")
        if isinstance(error, ConnectionError):
            return ApiError("CONNECTION_ERROR", "Connection error")
        if error.response:
            status = error.response.status_code
            if status == 429:
                return ApiError("RATE_LIMIT_EXCEEDED", "Rate limit exceeded", {"retry_after": error.response.headers.get("Retry-After", "60")})
            if status == 401:
                return ApiError("UNAUTHORIZED", "Unauthorized")
            if status == 403:
                return ApiError("FORBIDDEN", "Forbidden")
            if status == 404:
                return ApiError("NOT_FOUND", "Resource not found")
            if status >= 500:
                return ApiError("SERVER_ERROR", "Internal server error")
        return ApiError("UNKNOWN_ERROR", "An unexpected error occurred")

    def get(self, url: ApiRouter) -> dict:
        self.check_rate_limit()
        try:
            response = self.session.get(f"{self.base_url}{url.value}")
            response.raise_for_status()
            return response.json()
        except RequestException as error:
            raise self.handle_http_error(error)

    def post(self, url: ApiRouter, data: dict | None = None) -> dict:
        self.check_rate_limit()
        try:
            response = self.session.post(f"{self.base_url}{url.value}", json=data)
            response.raise_for_status()
            return response.json()
        except RequestException as error:
            raise self.handle_http_error(error)

    def set_auth_token(self, token) -> None:
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            print(f"Auth token set: {token[:10]}...")

    def clear_auth_token(self) -> None:
        self.session.headers.pop("Authorization", None)
        print("Auth token cleared")





