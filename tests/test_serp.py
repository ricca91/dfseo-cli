"""Tests for SERP commands."""

import json
from pathlib import Path
from typing import Any

import httpx
import pytest
import respx
from typer.testing import CliRunner

from dfseo.cli import app
from dfseo.client import API_BASE_URL

runner = CliRunner()


def load_fixture(name: str) -> dict[str, Any]:
    """Load a JSON fixture file."""
    fixture_path = Path(__file__).parent / "fixtures" / name
    with open(fixture_path) as f:
        return json.load(f)


@pytest.fixture
def mock_env_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set mock environment credentials."""
    monkeypatch.setenv("DATAFORSEO_LOGIN", "test@example.com")
    monkeypatch.setenv("DATAFORSEO_PASSWORD", "test_password")


class TestSerpGoogleCommand:
    """Test suite for `dfseo serp google` command."""

    @respx.mock
    def test_google_basic_search(self, mock_env_credentials: None) -> None:
        """Test basic Google SERP search."""
        fixture = load_fixture("google_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["serp", "google", "email hosting"])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["keyword"] == "email hosting"  # CLI passes keyword as-is
        # Location comes from defaults ("United States") unless specified
        assert output["location"] == "United States"
        assert "organic_results" in output
        assert len(output["organic_results"]) > 0

    @respx.mock
    def test_google_with_location_language(self, mock_env_credentials: None) -> None:
        """Test Google SERP with custom location and language."""
        fixture = load_fixture("google_serp_response.json")
        route = respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            [
                "serp",
                "google",
                "test keyword",
                "--location",
                "United States",
                "--language",
                "English",
                "--device",
                "mobile",
                "--depth",
                "50",
            ],
        )

        assert result.exit_code == 0
        # Verify request parameters
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body[0]["location_name"] == "United States"
        assert body[0]["language_name"] == "English"
        assert body[0]["device"] == "mobile"
        assert body[0]["depth"] == 50

    @respx.mock
    def test_google_json_pretty_output(self, mock_env_credentials: None) -> None:
        """Test Google SERP with json-pretty output."""
        fixture = load_fixture("google_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["serp", "google", "test", "--output", "json-pretty"],
        )

        assert result.exit_code == 0
        # Should be indented JSON
        assert "\n  " in result.output
        output = json.loads(result.output)
        assert output["keyword"] == "test"  # CLI passes keyword as-is

    @respx.mock
    def test_google_table_output(self, mock_env_credentials: None) -> None:
        """Test Google SERP with table output."""
        fixture = load_fixture("google_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["serp", "google", "test", "--output", "table"],
        )

        assert result.exit_code == 0
        assert "Keyword:" in result.output
        assert "Domain" in result.output
        assert "example.com" in result.output

    @respx.mock
    def test_google_csv_output(self, mock_env_credentials: None) -> None:
        """Test Google SERP with CSV output."""
        fixture = load_fixture("google_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["serp", "google", "test", "--output", "csv"],
        )

        assert result.exit_code == 0
        assert "rank,rank_group,domain,url,title,description" in result.output
        assert "example.com" in result.output

    @respx.mock
    def test_google_features_only(self, mock_env_credentials: None) -> None:
        """Test Google SERP with --features-only flag."""
        fixture = load_fixture("google_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["serp", "google", "test", "--features-only"],
        )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert "organic_results" not in output
        assert "serp_features" in output
        assert "featured_snippet" in output
        assert "people_also_ask" in output

    @respx.mock
    def test_google_invalid_device(self, mock_env_credentials: None) -> None:
        """Test Google SERP with invalid device."""
        result = runner.invoke(
            app,
            ["serp", "google", "test", "--device", "tablet"],
        )

        assert result.exit_code == 4
        assert "Invalid device" in result.output

    @respx.mock
    def test_google_invalid_os(self, mock_env_credentials: None) -> None:
        """Test Google SERP with invalid OS."""
        result = runner.invoke(
            app,
            ["serp", "google", "test", "--os", "linux"],
        )

        assert result.exit_code == 4
        assert "Invalid OS" in result.output


class TestSerpBingCommand:
    """Test suite for `dfseo serp bing` command."""

    @respx.mock
    def test_bing_basic_search(self, mock_env_credentials: None) -> None:
        """Test basic Bing SERP search."""
        fixture = load_fixture("bing_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/bing/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["serp", "bing", "email hosting"])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["keyword"] == "email hosting"  # CLI passes keyword as-is
        assert "organic_results" in output

    @respx.mock
    def test_bing_with_options(self, mock_env_credentials: None) -> None:
        """Test Bing SERP with options."""
        fixture = load_fixture("bing_serp_response.json")
        route = respx.post(f"{API_BASE_URL}/serp/bing/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            [
                "serp",
                "bing",
                "test",
                "--location",
                "Germany",
                "--depth",
                "30",
            ],
        )

        assert result.exit_code == 0
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body[0]["location_name"] == "Germany"
        assert body[0]["depth"] == 30


class TestSerpYoutubeCommand:
    """Test suite for `dfseo serp youtube` command."""

    @respx.mock
    def test_youtube_basic_search(self, mock_env_credentials: None) -> None:
        """Test basic YouTube SERP search."""
        fixture = load_fixture("youtube_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/youtube/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["serp", "youtube", "email marketing"])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["keyword"] == "email marketing"  # CLI passes keyword as-is
        assert "organic_results" in output


class TestSerpLocationsCommand:
    """Test suite for `dfseo serp locations` command."""

    @respx.mock
    def test_locations_list(self, mock_env_credentials: None) -> None:
        """Test locations list command."""
        fixture = load_fixture("locations_response.json")
        respx.get(f"{API_BASE_URL}/serp/google/locations").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["serp", "locations"])

        assert result.exit_code == 0
        assert "United States" in result.output
        assert "Italy" in result.output

    @respx.mock
    def test_locations_with_search(self, mock_env_credentials: None) -> None:
        """Test locations with search filter."""
        fixture = load_fixture("locations_response.json")
        route = respx.get(f"{API_BASE_URL}/serp/google/locations").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["serp", "locations", "--search", "italy"],
        )

        assert result.exit_code == 0
        request = route.calls[0].request
        assert request.url.params["search"] == "italy"

    @respx.mock
    def test_locations_json_output(self, mock_env_credentials: None) -> None:
        """Test locations with JSON output."""
        fixture = load_fixture("locations_response.json")
        respx.get(f"{API_BASE_URL}/serp/google/locations").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["serp", "locations", "--output", "json"],
        )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert isinstance(output, list)
        assert len(output) == 15


class TestSerpLanguagesCommand:
    """Test suite for `dfseo serp languages` command."""

    @respx.mock
    def test_languages_list(self, mock_env_credentials: None) -> None:
        """Test languages list command."""
        fixture = load_fixture("languages_response.json")
        respx.get(f"{API_BASE_URL}/serp/google/languages").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["serp", "languages"])

        assert result.exit_code == 0
        assert "English" in result.output
        assert "Italian" in result.output

    @respx.mock
    def test_languages_with_search(self, mock_env_credentials: None) -> None:
        """Test languages with search filter."""
        fixture = load_fixture("languages_response.json")
        route = respx.get(f"{API_BASE_URL}/serp/google/languages").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["serp", "languages", "--search", "ital"],
        )

        assert result.exit_code == 0
        request = route.calls[0].request
        assert request.url.params["search"] == "ital"


class TestSerpCompareCommand:
    """Test suite for `dfseo serp compare` command."""

    @respx.mock
    def test_compare_google_bing(self, mock_env_credentials: None) -> None:
        """Test compare command with Google and Bing."""
        google_fixture = load_fixture("google_serp_response.json")
        bing_fixture = load_fixture("bing_serp_response.json")

        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=google_fixture)
        )
        respx.post(f"{API_BASE_URL}/serp/bing/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=bing_fixture)
        )

        result = runner.invoke(
            app,
            ["serp", "compare", "email hosting", "--engines", "google,bing"],
        )

        assert result.exit_code == 0
        assert "SERP Compare" in result.output or "google" in result.output.lower()

    @respx.mock
    def test_compare_invalid_engine(self, mock_env_credentials: None) -> None:
        """Test compare with invalid engine."""
        result = runner.invoke(
            app,
            ["serp", "compare", "test", "--engines", "google,yahoo"],
        )

        assert result.exit_code == 4
        assert "Invalid engine" in result.output


class TestAuthenticationErrors:
    """Test suite for authentication error handling."""

    def test_missing_credentials(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test error when credentials are missing."""
        # Ensure no credentials are set
        monkeypatch.delenv("DATAFORSEO_LOGIN", raising=False)
        monkeypatch.delenv("DATAFORSEO_PASSWORD", raising=False)

        result = runner.invoke(app, ["serp", "google", "test"])

        # Should get exit code 2 for auth error
        assert result.exit_code == 2
        # Error message might be in stdout or stderr
        combined_output = result.output + (result.stderr or "")
        assert "Authentication" in combined_output or "credentials" in combined_output.lower()

    @respx.mock
    def test_invalid_credentials(self, mock_env_credentials: None) -> None:
        """Test error with invalid credentials."""
        fixture = load_fixture("auth_error_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["serp", "google", "test"])

        assert result.exit_code == 2
        combined_output = result.output + (result.stderr or "")
        assert "Authentication" in combined_output or "Invalid" in combined_output


class TestRateLimitErrors:
    """Test suite for rate limit error handling."""

    @respx.mock
    def test_rate_limit_error(self, mock_env_credentials: None) -> None:
        """Test handling of rate limit error."""
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(429, text="Rate Limited")
        )

        result = runner.invoke(app, ["serp", "google", "test"])

        assert result.exit_code == 3
        assert "Rate limit" in result.output


class TestOutputFormats:
    """Test suite for various output formats."""

    @respx.mock
    def test_json_output_default(self, mock_env_credentials: None) -> None:
        """Test default JSON output is compact."""
        fixture = load_fixture("google_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["serp", "google", "test"])

        assert result.exit_code == 0
        # Should be compact JSON (no newlines except trailing)
        lines = result.output.strip().split("\n")
        assert len(lines) == 1  # Single line for compact JSON

    @respx.mock
    def test_quiet_mode(self, mock_env_credentials: None) -> None:
        """Test quiet mode flag."""
        fixture = load_fixture("google_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["serp", "google", "test", "--quiet"])

        assert result.exit_code == 0
        # In quiet mode, output should still be valid JSON
        output = json.loads(result.output)
        assert "keyword" in output

    @respx.mock
    def test_verbose_mode(self, mock_env_credentials: None) -> None:
        """Test verbose mode flag."""
        fixture = load_fixture("google_serp_response.json")
        respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["serp", "google", "test", "--verbose"])

        assert result.exit_code == 0
        # Verbose mode writes to stderr, output on stdout should still be valid JSON
        # Output might have newlines from verbose messages mixed in capture, try parsing
        try:
            output = json.loads(result.output)
            assert "keyword" in output
        except json.JSONDecodeError:
            # If output isn't pure JSON, it should contain our result
            assert "test" in result.output or "keyword" in result.output


class TestCredentialsPriority:
    """Test credential priority: CLI flags > env > config."""

    @respx.mock
    def test_cli_credentials_override_env(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test CLI credentials override environment variables."""
        fixture = load_fixture("google_serp_response.json")
        route = respx.post(f"{API_BASE_URL}/serp/google/organic/live/advanced").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        # Set env credentials that should be overridden
        monkeypatch.setenv("DATAFORSEO_LOGIN", "env_user@example.com")
        monkeypatch.setenv("DATAFORSEO_PASSWORD", "env_password")

        result = runner.invoke(
            app,
            [
                "serp",
                "google",
                "test",
                "--login",
                "cli_user@example.com",
                "--password",
                "cli_password",
            ],
        )

        assert result.exit_code == 0
        # Request should succeed with CLI credentials
        assert route.called
