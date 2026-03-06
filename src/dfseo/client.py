"""DataForSEO API client wrapper."""

from __future__ import annotations

import base64
import time
from typing import Any

import httpx

from dfseo.config import Config
from dfseo.models import ApiResponse, Language, Location, SerpResult, UserData

API_BASE_URL = "https://api.dataforseo.com/v3"
RATE_LIMIT_MAX = 2000  # requests per minute


class DataForSeoError(Exception):
    """Base exception for DataForSEO API errors."""

    def __init__(self, message: str, exit_code: int = 1) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class AuthenticationError(DataForSeoError):
    """Authentication failed."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, exit_code=2)


class RateLimitError(DataForSeoError):
    """Rate limit exceeded."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(message, exit_code=3)


class ValidationError(DataForSeoError):
    """Invalid parameters."""

    def __init__(self, message: str = "Invalid parameters") -> None:
        super().__init__(message, exit_code=4)


class InsufficientBalanceError(DataForSeoError):
    """Insufficient balance."""

    def __init__(self, message: str = "Insufficient balance") -> None:
        super().__init__(message, exit_code=5)


class DataForSeoClient:
    """HTTP client for DataForSEO API."""

    def __init__(
        self,
        login: str | None = None,
        password: str | None = None,
        config: Config | None = None,
        verbose: bool = False,
    ) -> None:
        """Initialize the client.

        Args:
            login: API login (or use env/config)
            password: API password (or use env/config)
            config: Config instance (creates new if None)
            verbose: Print request/response details to stderr
        """
        self.config = config or Config()
        self.verbose = verbose

        # Resolve credentials
        try:
            self.login, self.password = self.config.resolve_auth(login, password)
        except ValueError as e:
            raise AuthenticationError(str(e))

        # Create auth header
        credentials = base64.b64encode(
            f"{self.login}:{self.password}".encode()
        ).decode()
        self.headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json",
        }

        self.client = httpx.Client(
            base_url=API_BASE_URL,
            headers=self.headers,
            timeout=60.0,
        )

    def _log(self, message: str) -> None:
        """Log message to stderr if verbose mode."""
        import sys

        if self.verbose:
            print(f"[dfseo] {message}", file=sys.stderr)

    def _handle_error(self, response: httpx.Response | ApiResponse) -> None:
        """Handle API errors and raise appropriate exceptions."""
        if isinstance(response, httpx.Response):
            if response.status_code == 401:
                raise AuthenticationError("Invalid credentials")
            elif response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            response.raise_for_status()
        else:
            # Handle API-level errors
            if response.status_code == 40200:
                raise InsufficientBalanceError()
            elif response.status_code == 40001:
                raise ValidationError(response.status_message or "Invalid parameters")
            elif response.status_code == 40100:
                raise AuthenticationError(response.status_message)
            elif response.status_code == 42900:
                raise RateLimitError(response.status_message or "Rate limit exceeded")

    def _request(
        self,
        method: str,
        path: str,
        json_data: dict[str, Any] | list[dict[str, Any]] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP request with retry logic.

        Args:
            method: HTTP method
            path: API path
            json_data: JSON body
            params: Query parameters

        Returns:
            Response JSON

        Raises:
            DataForSeoError: On API errors
        """
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                self._log(f"{method} {path}")
                if json_data:
                    self._log(f"Request body: {json_data}")

                response = self.client.request(
                    method=method,
                    url=path,
                    json=json_data,
                    params=params,
                )

                self._log(f"Response status: {response.status_code}")

                # Handle HTTP errors
                if response.status_code == 429:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = 2 ** retry_count
                        self._log(f"Rate limited, waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    raise RateLimitError()

                self._handle_error(response)
                return response.json()

            except httpx.HTTPStatusError as e:
                self._handle_error(e.response)
                raise

        raise RateLimitError("Max retries exceeded")

    def get_user_data(self) -> UserData:
        """Get current user data including balance.

        Returns:
            UserData with login, balance, and rate limit info
        """
        data = self._request("GET", "/appendix/user_data")
        api_response = ApiResponse.model_validate(data)
        self._handle_error(api_response)

        # Check task-level errors
        if api_response.tasks:
            task = api_response.tasks[0]
            if task.status_code != 20000:
                self._handle_error(
                    ApiResponse(
                        status_code=task.status_code,
                        status_message=task.status_message,
                        tasks=[],
                    )
                )

            if task.result:
                result = task.result[0]
                return UserData(
                    login=result.get("login", ""),
                    balance=float(result.get("money", {}).get("balance", 0)),
                    rate_limit=RATE_LIMIT_MAX,
                )

        raise DataForSeoError("Invalid response from user_data endpoint")

    def serp_google(
        self,
        keyword: str,
        location_name: str = "United States",
        language_name: str = "English",
        device: str = "desktop",
        os: str | None = None,
        depth: int = 100,
    ) -> SerpResult:
        """Get Google SERP results.

        Args:
            keyword: Search keyword
            location_name: Location name (e.g., "United States", "Italy")
            language_name: Language name (e.g., "English", "Italian")
            device: Device type ("desktop" or "mobile")
            os: Operating system ("windows", "macos", "ios", "android")
            depth: Number of results (max 700)

        Returns:
            Parsed SERP result
        """
        payload = [{
            "keyword": keyword,
            "location_name": location_name,
            "language_name": language_name,
            "device": device,
            "depth": min(depth, 700),
        }]
        if os:
            payload[0]["os"] = os

        data = self._request("POST", "/serp/google/organic/live/advanced", json_data=payload)
        return self._parse_serp_response(
            data, keyword, location_name, language_name, device
        )

    def serp_bing(
        self,
        keyword: str,
        location_name: str = "United States",
        language_name: str = "English",
        device: str = "desktop",
        depth: int = 100,
    ) -> SerpResult:
        """Get Bing SERP results.

        Args:
            keyword: Search keyword
            location_name: Location name
            language_name: Language name
            device: Device type
            depth: Number of results

        Returns:
            Parsed SERP result
        """
        payload = [{
            "keyword": keyword,
            "location_name": location_name,
            "language_name": language_name,
            "device": device,
            "depth": min(depth, 700),
        }]

        data = self._request("POST", "/serp/bing/organic/live/advanced", json_data=payload)
        return self._parse_serp_response(
            data, keyword, location_name, language_name, device
        )

    def serp_youtube(
        self,
        keyword: str,
        location_name: str = "United States",
        language_name: str = "English",
        device: str = "desktop",
        depth: int = 100,
    ) -> SerpResult:
        """Get YouTube SERP results.

        Args:
            keyword: Search keyword
            location_name: Location name
            language_name: Language name
            device: Device type
            depth: Number of results

        Returns:
            Parsed SERP result
        """
        payload = [{
            "keyword": keyword,
            "location_name": location_name,
            "language_name": language_name,
            "device": device,
            "depth": min(depth, 700),
        }]

        data = self._request("POST", "/serp/youtube/organic/live/advanced", json_data=payload)
        return self._parse_serp_response(
            data, keyword, location_name, language_name, device
        )

    def get_locations(self, search: str | None = None) -> list[Location]:
        """Get available locations.

        Args:
            search: Optional search filter

        Returns:
            List of locations
        """
        params = {}
        if search:
            params["search"] = search

        data = self._request("GET", "/serp/google/locations", params=params)
        api_response = ApiResponse.model_validate(data)
        self._handle_error(api_response)

        locations = []
        if api_response.tasks and api_response.tasks[0].result:
            for item in api_response.tasks[0].result:
                locations.append(Location.model_validate(item))

        return locations

    def get_languages(self, search: str | None = None) -> list[Language]:
        """Get available languages.

        Args:
            search: Optional search filter

        Returns:
            List of languages
        """
        params = {}
        if search:
            params["search"] = search

        data = self._request("GET", "/serp/google/languages", params=params)
        api_response = ApiResponse.model_validate(data)
        self._handle_error(api_response)

        languages = []
        if api_response.tasks and api_response.tasks[0].result:
            for item in api_response.tasks[0].result:
                languages.append(Language.model_validate(item))

        return languages

    def _parse_serp_response(
        self,
        data: dict[str, Any],
        keyword: str,
        location: str,
        language: str,
        device: str,
    ) -> SerpResult:
        """Parse SERP API response into SerpResult model.

        Args:
            data: Raw API response
            keyword: Original keyword
            location: Location name
            language: Language name
            device: Device type

        Returns:
            Parsed SerpResult
        """
        from datetime import datetime, timezone

        from dfseo.models import FeaturedSnippet, OrganicResult, PeopleAlsoAskItem

        api_response = ApiResponse.model_validate(data)
        self._handle_error(api_response)

        result = SerpResult(
            keyword=keyword,
            location=location,
            language=language,
            device=device,
            results_count=0,
            timestamp=datetime.now(timezone.utc).isoformat(),
            cost=api_response.cost or 0.0,
        )

        if not api_response.tasks or not api_response.tasks[0].result:
            return result

        task_result = api_response.tasks[0].result[0]
        items = task_result.get("items", [])
        result.results_count = len(items)

        serp_features = set()

        for item in items:
            item_type = item.get("type", "")

            if item_type == "organic":
                organic = OrganicResult(
                    rank=item.get("rank_absolute", 0),
                    rank_group=item.get("rank_group", 0),
                    domain=item.get("domain", ""),
                    url=item.get("url", ""),
                    title=item.get("title", ""),
                    description=item.get("description", None),
                    breadcrumb=item.get("breadcrumb", None),
                )
                result.organic_results.append(organic)

            elif item_type == "featured_snippet":
                serp_features.add("featured_snippet")
                result.featured_snippet = FeaturedSnippet(
                    text=item.get("text", ""),
                    source_url=item.get("source", {}).get("url", ""),
                    source_domain=item.get("source", {}).get("domain", ""),
                )

            elif item_type == "people_also_ask":
                serp_features.add("people_also_ask")
                for paa_item in item.get("items", []):
                    result.people_also_ask.append(
                        PeopleAlsoAskItem(
                            question=paa_item.get("question", ""),
                            expanded_text=paa_item.get("answer", ""),
                        )
                    )

            elif item_type == "local_pack":
                serp_features.add("local_pack")
            elif item_type == "knowledge_graph":
                serp_features.add("knowledge_graph")
            elif item_type == "top_stories":
                serp_features.add("top_stories")
            elif item_type == "images":
                serp_features.add("images")
            elif item_type == "videos":
                serp_features.add("videos")
            elif item_type == "shopping":
                serp_features.add("shopping")

        result.serp_features = sorted(list(serp_features))
        return result

    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self) -> DataForSeoClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
