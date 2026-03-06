"""Tests for DataForSEO API client."""

import json
from pathlib import Path
from typing import Any

import httpx
import pytest
import respx

from dfseo.client import (
    API_BASE_URL,
    AuthenticationError,
    DataForSeoClient,
    InsufficientBalanceError,
    RateLimitError,
    ValidationError,
)
from dfseo.config import Config
from dfseo.models import SerpResult


# Load fixtures
def load_fixture(name: str) -> dict[str, Any]:
    """Load a JSON fixture file."""
    fixture_path = Path(__file__).parent / "fixtures" / name
    with open(fixture_path) as f:
        return json.load(f)


@pytest.fixture
def mock_config(tmp_path: Path) -> Config:
    """Create a mock config with test credentials."""
    config_file = tmp_path / "config.toml"
    config = Config(config_path=config_file)
    config.set("auth", "login", "test@example.com")
    config.set("auth", "password", "test_password")
    config.save()
    return Config(config_path=config_file)


@pytest.fixture
def client(mock_config: Config) -> DataForSeoClient:
    """Create a test client with mock config."""
    return DataForSeoClient(config=mock_config)


class TestDataForSeoClient:
    """Test suite for DataForSeoClient."""

    def test_client_initialization(self, mock_config: Config) -> None:
        """Test client initializes correctly with credentials."""
        client = DataForSeoClient(config=mock_config)
        assert client.login == "test@example.com"
        assert client.password == "test_password"
        assert "Authorization" in client.headers
        assert client.headers["Authorization"].startswith("Basic ")

    def test_client_initialization_without_credentials(self, tmp_path: Path) -> None:
        """Test client raises AuthenticationError without credentials."""
        config_file = tmp_path / "config.toml"
        config = Config(config_path=config_file)

        with pytest.raises(AuthenticationError):
            DataForSeoClient(config=config)

    @respx.mock
    def test_get_user_data_success(self, client: DataForSeoClient) -> None:
        """Test successful user data retrieval."""
        fixture = load_fixture("user_data_response.json")
        route = respx.get(f"{API_BASE_URL}/appendix/user_data").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        user_data = client.get_user_data()

        assert route.called
        assert user_data.login == "user@example.com"
        assert user_data.balance == 42.50
        assert user_data.rate_limit == 2000

    @respx.mock
    def test_serp_google_success(self, client: DataForSeoClient) -> None:
        """Test successful Google SERP search."""
        fixture = load_fixture("google_serp_response.json")
        route = respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = client.serp_google(
            keyword="email hosting provider",
            location_name="Italy",
            language_name="Italian",
            device="desktop",
            depth=100,
        )

        assert route.called
        assert result.keyword == "email hosting provider"
        assert result.location == "Italy"
        assert result.language == "Italian"
        assert result.device == "desktop"
        assert result.cost == 0.002
        assert len(result.organic_results) > 0
        assert len(result.serp_features) > 0

    @respx.mock
    def test_serp_bing_success(self, client: DataForSeoClient) -> None:
        """Test successful Bing SERP search."""
        fixture = load_fixture("bing_serp_response.json")
        route = respx.post(f"{API_BASE_URL}/serp/bing/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = client.serp_bing(
            keyword="email hosting provider",
            location_name="United States",
            language_name="English",
            device="desktop",
            depth=50,
        )

        assert route.called
        assert result.keyword == "email hosting provider"
        assert len(result.organic_results) == 5

    @respx.mock
    def test_serp_youtube_success(self, client: DataForSeoClient) -> None:
        """Test successful YouTube SERP search."""
        fixture = load_fixture("youtube_serp_response.json")
        route = respx.post(f"{API_BASE_URL}/serp/youtube/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = client.serp_youtube(
            keyword="email marketing tutorial",
            location_name="United States",
            language_name="English",
            device="desktop",
            depth=20,
        )

        assert route.called
        assert result.keyword == "email marketing tutorial"
        # Fixture has organic results for YouTube
        assert len(result.organic_results) == 3

    @respx.mock
    def test_get_locations_success(self, client: DataForSeoClient) -> None:
        """Test successful locations retrieval."""
        fixture = load_fixture("locations_response.json")
        route = respx.get(f"{API_BASE_URL}/serp/google/locations").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        locations = client.get_locations()

        assert route.called
        assert len(locations) == 15
        assert locations[0].location_name == "United States"
        assert locations[0].location_code == 2840

    @respx.mock
    def test_get_languages_success(self, client: DataForSeoClient) -> None:
        """Test successful languages retrieval."""
        fixture = load_fixture("languages_response.json")
        route = respx.get(f"{API_BASE_URL}/serp/google/languages").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        languages = client.get_languages()

        assert route.called
        assert len(languages) == 15
        assert languages[0].language_name == "English"
        assert languages[0].language_code == "en"


class TestErrorHandling:
    """Test suite for API error handling."""

    @respx.mock
    def test_authentication_error_http(self, client: DataForSeoClient) -> None:
        """Test authentication error on HTTP 401."""
        respx.get(f"{API_BASE_URL}/appendix/user_data").mock(
            return_value=httpx.Response(401, text="Unauthorized")
        )

        with pytest.raises(AuthenticationError):
            client.get_user_data()

    @respx.mock
    def test_authentication_error_api(self, client: DataForSeoClient) -> None:
        """Test authentication error from API response."""
        fixture = load_fixture("auth_error_response.json")
        respx.get(f"{API_BASE_URL}/appendix/user_data").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        with pytest.raises(AuthenticationError):
            client.get_user_data()

    @respx.mock
    def test_rate_limit_error_http(self, client: DataForSeoClient) -> None:
        """Test rate limit error on HTTP 429."""
        respx.get(f"{API_BASE_URL}/appendix/user_data").mock(
            return_value=httpx.Response(429, text="Rate Limited")
        )

        with pytest.raises(RateLimitError):
            client.get_user_data()

    @respx.mock
    def test_rate_limit_error_api(self, client: DataForSeoClient) -> None:
        """Test rate limit error from API response at task level."""
        # API returns rate limit in task status_code
        fixture = {
            "status_code": 20000,
            "status_message": "Ok.",
            "tasks": [
                {
                    "id": "task123",
                    "status_code": 42900,
                    "status_message": "Rate limit exceeded. Please wait and try again.",
                    "result": []
                }
            ]
        }
        respx.get(f"{API_BASE_URL}/appendix/user_data").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        with pytest.raises(RateLimitError):
            client.get_user_data()

    @respx.mock
    def test_insufficient_balance_error(self, client: DataForSeoClient) -> None:
        """Test insufficient balance error."""
        fixture = load_fixture("insufficient_balance_response.json")
        respx.get(f"{API_BASE_URL}/appendix/user_data").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        with pytest.raises(InsufficientBalanceError):
            client.get_user_data()


class TestRetryLogic:
    """Test suite for retry logic."""

    @respx.mock
    def test_retry_on_rate_limit(self, client: DataForSeoClient) -> None:
        """Test retry logic on rate limit."""
        fixture = load_fixture("user_data_response.json")
        route = respx.get(f"{API_BASE_URL}/appendix/user_data")
        # First two calls return 429, third succeeds
        route.side_effect = [
            httpx.Response(429),
            httpx.Response(429),
            httpx.Response(200, json=fixture),
        ]

        user_data = client.get_user_data()

        assert route.call_count == 3
        assert user_data.login == "user@example.com"

    @respx.mock
    def test_max_retries_exceeded(self, client: DataForSeoClient) -> None:
        """Test error when max retries exceeded."""
        respx.get(f"{API_BASE_URL}/appendix/user_data").mock(
            return_value=httpx.Response(429)
        )

        with pytest.raises(RateLimitError):
            client.get_user_data()


class TestSerpResponseParsing:
    """Test suite for SERP response parsing."""

    @respx.mock
    def test_parse_organic_results(self, client: DataForSeoClient) -> None:
        """Test parsing of organic results."""
        fixture = load_fixture("google_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = client.serp_google(keyword="test")

        organic = result.organic_results
        assert len(organic) == 5  # 5 organic results in fixture

        first = organic[0]
        assert first.rank == 2
        assert first.rank_group == 1
        assert first.domain == "example.com"
        assert first.url == "https://www.example.com/email-hosting"
        assert first.title == "Best Email Hosting Provider 2026 - Compare Top Services"
        assert first.breadcrumb == "example.com › email › hosting"

    @respx.mock
    def test_parse_featured_snippet(self, client: DataForSeoClient) -> None:
        """Test parsing of featured snippet."""
        fixture = load_fixture("google_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = client.serp_google(keyword="test")

        assert result.featured_snippet is not None
        assert "email hosting service" in result.featured_snippet.text
        assert result.featured_snippet.source_domain == "en.wikipedia.org"
        assert "wikipedia.org" in result.featured_snippet.source_url

    @respx.mock
    def test_parse_people_also_ask(self, client: DataForSeoClient) -> None:
        """Test parsing of people also ask."""
        fixture = load_fixture("google_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = client.serp_google(keyword="test")

        assert len(result.people_also_ask) == 3
        assert result.people_also_ask[0].question == "What is the best email hosting for business?"
        assert "Google Workspace" in result.people_also_ask[0].expanded_text

    @respx.mock
    def test_parse_serp_features(self, client: DataForSeoClient) -> None:
        """Test parsing of SERP features list."""
        fixture = load_fixture("google_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = client.serp_google(keyword="test")

        assert "featured_snippet" in result.serp_features
        assert "people_also_ask" in result.serp_features
        assert "local_pack" in result.serp_features
        assert "videos" in result.serp_features
        assert "images" in result.serp_features

    @respx.mock
    def test_empty_results(self, client: DataForSeoClient) -> None:
        """Test handling of empty results."""
        empty_response = {
            "status_code": 20000,
            "status_message": "Ok.",
            "tasks": [
                {
                    "status_code": 20000,
                    "result": [
                        {
                            "items": []
                        }
                    ]
                }
            ],
            "cost": 0.001,
        }
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=empty_response)
        )

        result = client.serp_google(keyword="test")

        assert result.organic_results == []
        assert result.people_also_ask == []
        assert result.featured_snippet is None


class TestClientContextManager:
    """Test suite for client context manager."""

    def test_context_manager(self, mock_config: Config) -> None:
        """Test client works as context manager."""
        with DataForSeoClient(config=mock_config) as client:
            assert client.login == "test@example.com"

    @respx.mock
    def test_client_close(self, mock_config: Config) -> None:
        """Test client closes properly."""
        client = DataForSeoClient(config=mock_config)
        client.close()
        # After close, the httpx client should be closed
        assert client.client.is_closed


class TestParameters:
    """Test suite for API request parameters."""

    @respx.mock
    def test_serp_google_with_os(self, client: DataForSeoClient) -> None:
        """Test Google SERP with OS parameter."""
        fixture = load_fixture("google_serp_response.json")
        route = respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        client.serp_google(
            keyword="test",
            location_name="Italy",
            language_name="Italian",
            device="mobile",
            os="android",
            depth=50,
        )

        # Check request body
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body[0]["os"] == "android"
        assert body[0]["device"] == "mobile"
        assert body[0]["depth"] == 50

    @respx.mock
    def test_depth_limit(self, client: DataForSeoClient) -> None:
        """Test that depth is limited to 700."""
        fixture = load_fixture("google_serp_response.json")
        route = respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        client.serp_google(
            keyword="test",
            depth=1000,  # Should be capped at 700
        )

        request = route.calls[0].request
        body = json.loads(request.content)
        assert body[0]["depth"] == 700

    @respx.mock
    def test_locations_with_search(self, client: DataForSeoClient) -> None:
        """Test locations endpoint with search parameter."""
        fixture = load_fixture("locations_response.json")
        route = respx.get(f"{API_BASE_URL}/serp/google/locations").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        client.get_locations(search="italy")

        request = route.calls[0].request
        assert request.url.params["search"] == "italy"

    @respx.mock
    def test_languages_with_search(self, client: DataForSeoClient) -> None:
        """Test languages endpoint with search parameter."""
        fixture = load_fixture("languages_response.json")
        route = respx.get(f"{API_BASE_URL}/serp/google/languages").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        client.get_languages(search="ital")

        request = route.calls[0].request
        assert request.url.params["search"] == "ital"
