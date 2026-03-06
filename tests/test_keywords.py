"""Tests for Keywords commands."""

import json
from pathlib import Path
from typing import Any

import httpx
import pytest
import respx
import typer
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


class TestKeywordsVolumeCommand:
    """Test suite for `dfseo keywords volume` command."""

    @respx.mock
    def test_volume_basic(self, mock_env_credentials: None) -> None:
        """Test basic keyword volume command."""
        fixture = load_fixture("keyword_volume_response.json")
        respx.post(f"{API_BASE_URL}/dataforseo_labs/google/keyword_overview/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["keywords", "volume", "email hosting", "smtp provider"])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["keywords_count"] == 2
        assert output["location"] == "United States"  # Default
        assert "results" in output
        assert len(output["results"]) == 2

    @respx.mock
    def test_volume_with_location_language(self, mock_env_credentials: None) -> None:
        """Test keyword volume with custom location and language."""
        fixture = load_fixture("keyword_volume_response.json")
        route = respx.post(f"{API_BASE_URL}/dataforseo_labs/google/keyword_overview/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            [
                "keywords",
                "volume",
                "email hosting",
                "--location",
                "Italy",
                "--language",
                "Italian",
            ],
        )

        assert result.exit_code == 0
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body[0]["location_name"] == "Italy"
        assert body[0]["language_name"] == "Italian"

    @respx.mock
    def test_volume_with_serp_info(self, mock_env_credentials: None) -> None:
        """Test keyword volume with include-serp-info flag."""
        fixture = load_fixture("keyword_volume_response.json")
        route = respx.post(f"{API_BASE_URL}/dataforseo_labs/google/keyword_overview/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["keywords", "volume", "email hosting", "--include-serp-info"],
        )

        assert result.exit_code == 0
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body[0]["include_serp_info"] is True

    @respx.mock
    def test_volume_table_output(self, mock_env_credentials: None) -> None:
        """Test keyword volume with table output."""
        fixture = load_fixture("keyword_volume_response.json")
        respx.post(f"{API_BASE_URL}/dataforseo_labs/google/keyword_overview/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["keywords", "volume", "email hosting", "--output", "table"],
        )

        assert result.exit_code == 0
        assert "Location:" in result.output
        assert "email hosting" in result.output
        assert "Volume" in result.output

    @respx.mock
    def test_volume_csv_output(self, mock_env_credentials: None) -> None:
        """Test keyword volume with CSV output."""
        fixture = load_fixture("keyword_volume_response.json")
        respx.post(f"{API_BASE_URL}/dataforseo_labs/google/keyword_overview/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["keywords", "volume", "email hosting", "--output", "csv"],
        )

        assert result.exit_code == 0
        assert "keyword,search_volume,cpc" in result.output

    @respx.mock
    def test_volume_from_file(self, mock_env_credentials: None, tmp_path: Path) -> None:
        """Test keyword volume with --from-file option."""
        fixture = load_fixture("keyword_volume_response.json")
        route = respx.post(f"{API_BASE_URL}/dataforseo_labs/google/keyword_overview/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        # Create a test file
        keyword_file = tmp_path / "keywords.txt"
        keyword_file.write_text("email hosting\nsmtp provider\n# comment\n\nwebmail\n")

        result = runner.invoke(
            app,
            ["keywords", "volume", "--from-file", str(keyword_file)],
        )

        assert result.exit_code == 0
        request = route.calls[0].request
        body = json.loads(request.content)
        # Should have 3 keywords (comment and empty line skipped)
        assert len(body[0]["keywords"]) == 3

    def test_volume_too_many_keywords(self, mock_env_credentials: None) -> None:
        """Test error when too many keywords provided."""
        keywords = [f"keyword{i}" for i in range(701)]
        result = runner.invoke(app, ["keywords", "volume"] + keywords)

        assert result.exit_code == 4
        assert "Maximum 700 keywords" in result.output or "Maximum 700 keywords" in result.stderr


class TestKeywordsSuggestionsCommand:
    """Test suite for `dfseo keywords suggestions` command."""

    @respx.mock
    def test_suggestions_basic(self, mock_env_credentials: None) -> None:
        """Test basic keyword suggestions command."""
        fixture = load_fixture("keyword_suggestions_response.json")
        respx.post(f"{API_BASE_URL}/dataforseo_labs/google/keyword_suggestions/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["keywords", "suggestions", "email hosting"])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["seed_keyword"] == "email hosting"
        assert "results" in output
        assert len(output["results"]) > 0

    @respx.mock
    def test_suggestions_with_filters(self, mock_env_credentials: None) -> None:
        """Test keyword suggestions with volume and difficulty filters."""
        fixture = load_fixture("keyword_suggestions_response.json")
        route = respx.post(f"{API_BASE_URL}/dataforseo_labs/google/keyword_suggestions/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            [
                "keywords",
                "suggestions",
                "email hosting",
                "--min-volume",
                "100",
                "--max-difficulty",
                "40",
                "--limit",
                "50",
            ],
        )

        assert result.exit_code == 0
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body[0]["limit"] == 50
        assert "filters" in body[0]

    @respx.mock
    def test_suggestions_with_sort(self, mock_env_credentials: None) -> None:
        """Test keyword suggestions with sort options."""
        fixture = load_fixture("keyword_suggestions_response.json")
        route = respx.post(f"{API_BASE_URL}/dataforseo_labs/google/keyword_suggestions/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            [
                "keywords",
                "suggestions",
                "email hosting",
                "--sort",
                "volume",
                "--order",
                "desc",
            ],
        )

        assert result.exit_code == 0
        request = route.calls[0].request
        body = json.loads(request.content)
        assert "keyword_info.search_volume,desc" in body[0]["order_by"]

    @respx.mock
    def test_suggestions_invalid_sort(self, mock_env_credentials: None) -> None:
        """Test error with invalid sort field."""
        result = runner.invoke(
            app,
            ["keywords", "suggestions", "test", "--sort", "invalid"],
        )

        assert result.exit_code == 4
        assert "Invalid sort" in result.output


class TestKeywordsIdeasCommand:
    """Test suite for `dfseo keywords ideas` command."""

    @respx.mock
    def test_ideas_basic(self, mock_env_credentials: None) -> None:
        """Test basic keyword ideas command."""
        fixture = load_fixture("keyword_suggestions_response.json")
        respx.post(f"{API_BASE_URL}/dataforseo_labs/google/keyword_ideas/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["keywords", "ideas", "email hosting", "smtp service"])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert "results" in output

    @respx.mock
    def test_ideas_too_many_seeds(self, mock_env_credentials: None) -> None:
        """Test error when too many seed keywords provided."""
        seeds = [f"keyword{i}" for i in range(21)]
        result = runner.invoke(app, ["keywords", "ideas"] + seeds)

        assert result.exit_code == 4
        assert "Maximum 20" in result.output


class TestKeywordsDifficultyCommand:
    """Test suite for `dfseo keywords difficulty` command."""

    @respx.mock
    def test_difficulty_basic(self, mock_env_credentials: None) -> None:
        """Test basic keyword difficulty command."""
        fixture = load_fixture("keyword_difficulty_response.json")
        respx.post(f"{API_BASE_URL}/dataforseo_labs/google/bulk_keyword_difficulty/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["keywords", "difficulty", "email hosting", "smtp provider", "webmail"],
        )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["keywords_count"] == 3
        assert len(output["results"]) == 3
        assert output["results"][0]["keyword_difficulty"] == 67

    @respx.mock
    def test_difficulty_table_output(self, mock_env_credentials: None) -> None:
        """Test keyword difficulty with table output."""
        fixture = load_fixture("keyword_difficulty_response.json")
        respx.post(f"{API_BASE_URL}/dataforseo_labs/google/bulk_keyword_difficulty/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["keywords", "difficulty", "email hosting", "--output", "table"],
        )

        assert result.exit_code == 0
        assert "KD" in result.output
        assert "Hard" in result.output or "Medium" in result.output

    @respx.mock
    def test_difficulty_from_file(self, mock_env_credentials: None, tmp_path: Path) -> None:
        """Test keyword difficulty with --from-file option."""
        fixture = load_fixture("keyword_difficulty_response.json")
        route = respx.post(f"{API_BASE_URL}/dataforseo_labs/google/bulk_keyword_difficulty/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        keyword_file = tmp_path / "keywords.txt"
        keyword_file.write_text("email hosting\nsmtp provider\nwebmail\n")

        result = runner.invoke(
            app,
            ["keywords", "difficulty", "--from-file", str(keyword_file)],
        )

        assert result.exit_code == 0
        request = route.calls[0].request
        body = json.loads(request.content)
        assert len(body[0]["keywords"]) == 3


class TestKeywordsSearchIntentCommand:
    """Test suite for `dfseo keywords search-intent` command."""

    @respx.mock
    def test_search_intent_basic(self, mock_env_credentials: None) -> None:
        """Test basic search intent command."""
        fixture = load_fixture("search_intent_response.json")
        respx.post(f"{API_BASE_URL}/dataforseo_labs/google/search_intent/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            [
                "keywords",
                "search-intent",
                "buy email hosting",
                "what is DKIM",
            ],
        )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["keywords_count"] == 2
        assert len(output["results"]) == 3
        # Check first result
        assert output["results"][0]["main_intent"] == "transactional"

    @respx.mock
    def test_search_intent_table_output(self, mock_env_credentials: None) -> None:
        """Test search intent with table output."""
        fixture = load_fixture("search_intent_response.json")
        respx.post(f"{API_BASE_URL}/dataforseo_labs/google/search_intent/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["keywords", "search-intent", "test", "--output", "table"],
        )

        assert result.exit_code == 0
        assert "Main Intent" in result.output
        assert "Probability" in result.output


class TestKeywordsForSiteCommand:
    """Test suite for `dfseo keywords for-site` command."""

    @respx.mock
    def test_for_site_basic(self, mock_env_credentials: None) -> None:
        """Test basic for-site command."""
        fixture = load_fixture("keywords_for_site_response.json")
        respx.post(f"{API_BASE_URL}/dataforseo_labs/google/keywords_for_site/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(app, ["keywords", "for-site", "qboxmail.it"])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["target"] == "qboxmail.it"
        assert "results" in output

    @respx.mock
    def test_for_site_with_filters(self, mock_env_credentials: None) -> None:
        """Test for-site with volume filter."""
        fixture = load_fixture("keywords_for_site_response.json")
        route = respx.post(f"{API_BASE_URL}/dataforseo_labs/google/keywords_for_site/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            [
                "keywords",
                "for-site",
                "example.com",
                "--min-volume",
                "50",
                "--limit",
                "100",
            ],
        )

        assert result.exit_code == 0
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body[0]["limit"] == 100


class TestKeywordsAdsVolumeCommand:
    """Test suite for `dfseo keywords ads-volume` command."""

    @respx.mock
    def test_ads_volume_basic(self, mock_env_credentials: None) -> None:
        """Test basic Google Ads volume command."""
        fixture = load_fixture("google_ads_volume_response.json")
        respx.post(f"{API_BASE_URL}/keywords_data/google_ads/search_volume/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["keywords", "ads-volume", "email hosting", "smtp provider"],
        )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["keywords_count"] == 2
        assert "results" in output

    @respx.mock
    def test_ads_volume_with_date_range(self, mock_env_credentials: None) -> None:
        """Test Google Ads volume with date range."""
        fixture = load_fixture("google_ads_volume_response.json")
        route = respx.post(f"{API_BASE_URL}/keywords_data/google_ads/search_volume/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            [
                "keywords",
                "ads-volume",
                "email hosting",
                "--date-from",
                "2025-01",
                "--date-to",
                "2026-03",
            ],
        )

        assert result.exit_code == 0
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body[0]["date_from"] == "2025-01"
        assert body[0]["date_to"] == "2026-03"

    def test_ads_volume_too_many_keywords(self, mock_env_credentials: None) -> None:
        """Test error when too many keywords for Google Ads."""
        keywords = [f"keyword{i}" for i in range(21)]
        result = runner.invoke(app, ["keywords", "ads-volume"] + keywords)

        assert result.exit_code == 4
        assert "Maximum 20" in result.output


class TestKeywordsAdsSuggestionsCommand:
    """Test suite for `dfseo keywords ads-suggestions` command."""

    @respx.mock
    def test_ads_suggestions_basic(self, mock_env_credentials: None) -> None:
        """Test basic Google Ads suggestions command."""
        fixture = load_fixture("google_ads_suggestions_response.json")
        respx.post(f"{API_BASE_URL}/keywords_data/google_ads/keywords_for_keywords/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["keywords", "ads-suggestions", "email hosting"],
        )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert "results" in output
        assert len(output["results"]) == 2

    @respx.mock
    def test_ads_suggestions_with_limit(self, mock_env_credentials: None) -> None:
        """Test Google Ads suggestions with limit."""
        fixture = load_fixture("google_ads_suggestions_response.json")
        route = respx.post(f"{API_BASE_URL}/keywords_data/google_ads/keywords_for_keywords/live").mock(
            return_value=httpx.Response(200, json=fixture)
        )

        result = runner.invoke(
            app,
            ["keywords", "ads-suggestions", "email hosting", "--limit", "50"],
        )

        assert result.exit_code == 0
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body[0]["limit"] == 50


class TestLoadKeywordsUtility:
    """Test suite for load_keywords utility function."""

    def test_load_from_arguments(self) -> None:
        """Test loading keywords from CLI arguments."""
        from dfseo.commands.keywords import load_keywords

        result = load_keywords(["kw1", "kw2", "kw3"], None)
        assert result == ["kw1", "kw2", "kw3"]

    def test_load_from_file(self, tmp_path: Path) -> None:
        """Test loading keywords from file."""
        from dfseo.commands.keywords import load_keywords

        keyword_file = tmp_path / "keywords.txt"
        keyword_file.write_text("kw1\nkw2\nkw3\n")

        result = load_keywords([], str(keyword_file))
        assert result == ["kw1", "kw2", "kw3"]

    def test_load_from_file_with_comments(self, tmp_path: Path) -> None:
        """Test that comments and empty lines are skipped."""
        from dfseo.commands.keywords import load_keywords

        keyword_file = tmp_path / "keywords.txt"
        keyword_file.write_text("# This is a comment\nkw1\n\nkw2\n  \n# Another comment\nkw3\n")

        result = load_keywords([], str(keyword_file))
        assert result == ["kw1", "kw2", "kw3"]

    def test_load_from_file_not_found(self, tmp_path: Path) -> None:
        """Test error when file not found."""
        from dfseo.commands.keywords import load_keywords

        with pytest.raises(typer.Exit) as exc_info:
            load_keywords([], str(tmp_path / "nonexistent.txt"))
        assert exc_info.value.exit_code == 4


class TestBuildFiltersUtility:
    """Test suite for build_filters utility function."""

    def test_build_filters_min_volume(self) -> None:
        """Test building filter with min volume."""
        from dfseo.commands.keywords import build_filters

        result = build_filters(min_volume=100)
        assert result == ["keyword_info.search_volume", ">=", 100]

    def test_build_filters_multiple(self) -> None:
        """Test building filter with multiple conditions."""
        from dfseo.commands.keywords import build_filters

        result = build_filters(min_volume=100, max_difficulty=40)
        assert result == [
            ["keyword_info.search_volume", ">=", 100],
            "and",
            ["keyword_properties.keyword_difficulty", "<=", 40],
        ]

    def test_build_filters_none(self) -> None:
        """Test building filter with no conditions."""
        from dfseo.commands.keywords import build_filters

        result = build_filters()
        assert result is None


class TestBuildOrderByUtility:
    """Test suite for build_order_by utility function."""

    def test_order_by_volume_desc(self) -> None:
        """Test order by volume desc."""
        from dfseo.commands.keywords import build_order_by

        result = build_order_by("volume", "desc")
        assert result == ["keyword_info.search_volume,desc"]

    def test_order_by_difficulty_asc(self) -> None:
        """Test order by difficulty asc."""
        from dfseo.commands.keywords import build_order_by

        result = build_order_by("difficulty", "asc")
        assert result == ["keyword_properties.keyword_difficulty,asc"]

    def test_order_by_relevance(self) -> None:
        """Test order by relevance."""
        from dfseo.commands.keywords import build_order_by

        result = build_order_by("relevance", "desc")
        assert result == ["relevance,desc"]


class TestDifficultyLevelUtility:
    """Test suite for difficulty level utility functions."""

    def test_get_difficulty_level_easy(self) -> None:
        """Test easy difficulty level."""
        from dfseo.commands.keywords import _get_difficulty_level

        level, color = _get_difficulty_level(25)
        assert level == "Easy"
        assert color == "green"

    def test_get_difficulty_level_medium(self) -> None:
        """Test medium difficulty level."""
        from dfseo.commands.keywords import _get_difficulty_level

        level, color = _get_difficulty_level(40)
        assert level == "Medium"
        assert color == "yellow"

    def test_get_difficulty_level_hard(self) -> None:
        """Test hard difficulty level."""
        from dfseo.commands.keywords import _get_difficulty_level

        level, color = _get_difficulty_level(60)
        assert level == "Hard"
        assert color == "orange"

    def test_get_difficulty_level_very_hard(self) -> None:
        """Test very hard difficulty level."""
        from dfseo.commands.keywords import _get_difficulty_level

        level, color = _get_difficulty_level(85)
        assert level == "Very Hard"
        assert color == "red"

    def test_format_difficulty_bar(self) -> None:
        """Test difficulty bar formatting."""
        from dfseo.commands.keywords import _format_difficulty_bar

        bar = _format_difficulty_bar(50, width=10)
        assert "█" in bar
        assert "░" in bar
        assert len(bar) == 10
