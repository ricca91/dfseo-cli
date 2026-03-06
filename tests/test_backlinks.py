"""Tests for backlinks commands."""

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


class TestBacklinksSummaryCommand:
    """Test suite for `dfseo backlinks summary` command."""

    @respx.mock
    def test_summary_basic(self, mock_env_credentials: None) -> None:
        """Test basic backlinks summary."""
        respx.post(f"{API_BASE_URL}/backlinks/summary/live").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status_code": 20000,
                    "tasks": [{
                        "status_code": 20000,
                        "result": [{
                            "rank": 245,
                            "backlinks": 1420,
                            "referring_domains": 312,
                            "referring_ips": 265,
                            "spam_score": 5,
                            "broken_backlinks": 12,
                            "link_summary": {
                                "dofollow": 980,
                                "nofollow": 440,
                            },
                            "top_pages": [
                                {"url": "https://example.com/", "backlinks": 450},
                            ],
                            "top_anchors": [
                                {"anchor": "example", "backlinks": 230},
                            ],
                        }]
                    }],
                    "cost": 0.02,
                }
            )
        )

        result = runner.invoke(app, ["backlinks", "summary", "example.com"])

        assert result.exit_code == 0
        assert "example.com" in result.output or "245" in result.output

    @respx.mock
    def test_summary_json_output(self, mock_env_credentials: None) -> None:
        """Test summary with JSON output."""
        respx.post(f"{API_BASE_URL}/backlinks/summary/live").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status_code": 20000,
                    "tasks": [{
                        "status_code": 20000,
                        "result": [{
                            "rank": 100,
                            "backlinks": 500,
                            "referring_domains": 100,
                            "link_summary": {"dofollow": 300, "nofollow": 200},
                        }]
                    }],
                    "cost": 0.02,
                }
            )
        )

        result = runner.invoke(app, ["backlinks", "summary", "example.com", "-o", "json"])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["target"] == "example.com"
        assert output["rank"] == 100


class TestBacklinksListCommand:
    """Test suite for `dfseo backlinks list` command."""

    @respx.mock
    def test_list_basic(self, mock_env_credentials: None) -> None:
        """Test basic backlinks list."""
        respx.post(f"{API_BASE_URL}/backlinks/backlinks/live").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status_code": 20000,
                    "tasks": [{
                        "status_code": 20000,
                        "result": [{
                            "total_count": 1000,
                            "items": [
                                {
                                    "domain_from": "techblog.com",
                                    "url_from": "https://techblog.com/article",
                                    "domain_to": "example.com",
                                    "url_to": "https://example.com/page",
                                    "rank": 185,
                                    "anchor": "great service",
                                    "dofollow": True,
                                }
                            ]
                        }]
                    }],
                    "cost": 0.03,
                }
            )
        )

        result = runner.invoke(app, ["backlinks", "list", "example.com"])

        assert result.exit_code == 0
        assert "techblog.com" in result.output or "185" in result.output

    @respx.mock
    def test_list_with_filters(self, mock_env_credentials: None) -> None:
        """Test list with filters."""
        route = respx.post(f"{API_BASE_URL}/backlinks/backlinks/live").mock(
            return_value=httpx.Response(200, json={
                "status_code": 20000,
                "tasks": [{"status_code": 20000, "result": [{"total_count": 50, "items": []}]}],
                "cost": 0.01,
            })
        )

        result = runner.invoke(app, [
            "backlinks", "list", "example.com",
            "--dofollow-only",
            "--min-rank", "100",
            "--sort", "rank",
            "--limit", "50",
        ])

        assert result.exit_code == 0
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body[0]["filters"] == [["dofollow", "=", True], "and", ["rank", ">=", 100]]


class TestBacklinksAnchorsCommand:
    """Test suite for `dfseo backlinks anchors` command."""

    @respx.mock
    def test_anchors_basic(self, mock_env_credentials: None) -> None:
        """Test anchors analysis."""
        respx.post(f"{API_BASE_URL}/backlinks/anchors/live").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status_code": 20000,
                    "tasks": [{
                        "status_code": 20000,
                        "result": [{
                            "total_count": 50,
                            "items": [
                                {"anchor": "example brand", "backlinks": 230, "referring_domains": 45},
                                {"anchor": "click here", "backlinks": 120, "referring_domains": 30},
                            ]
                        }]
                    }],
                    "cost": 0.02,
                }
            )
        )

        result = runner.invoke(app, ["backlinks", "anchors", "example.com"])

        assert result.exit_code == 0
        assert "example brand" in result.output or "230" in result.output


class TestBacklinksReferringDomainsCommand:
    """Test suite for `dfseo backlinks referring-domains` command."""

    @respx.mock
    def test_referring_domains(self, mock_env_credentials: None) -> None:
        """Test referring domains list."""
        respx.post(f"{API_BASE_URL}/backlinks/referring_domains/live").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status_code": 20000,
                    "tasks": [{
                        "status_code": 20000,
                        "result": [{
                            "total_count": 300,
                            "items": [
                                {"domain": "techblog.com", "rank": 310, "backlinks": 15, "dofollow": True},
                                {"domain": "news.com", "rank": 500, "backlinks": 8, "dofollow": True},
                            ]
                        }]
                    }],
                    "cost": 0.02,
                }
            )
        )

        result = runner.invoke(app, ["backlinks", "referring-domains", "example.com"])

        assert result.exit_code == 0
        assert "techblog.com" in result.output or "310" in result.output


class TestBacklinksBulkCommand:
    """Test suite for `dfseo backlinks bulk` commands."""

    @respx.mock
    def test_bulk_ranks(self, mock_env_credentials: None) -> None:
        """Test bulk ranks command."""
        respx.post(f"{API_BASE_URL}/backlinks/bulk_ranks/live").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status_code": 20000,
                    "tasks": [{
                        "status_code": 20000,
                        "result": [{
                            "items": [
                                {"target": "site1.com", "rank": 100, "backlinks": 500},
                                {"target": "site2.com", "rank": 200, "backlinks": 1000},
                            ]
                        }]
                    }],
                    "cost": 0.05,
                }
            )
        )

        result = runner.invoke(app, ["backlinks", "bulk", "ranks", "site1.com", "site2.com"])

        assert result.exit_code == 0
        assert "site1.com" in result.output or "100" in result.output
