"""Tests for site audit commands."""

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


class TestSiteCrawlCommand:
    """Test suite for `dfseo site crawl` command."""

    @respx.mock
    def test_crawl_basic(self, mock_env_credentials: None) -> None:
        """Test basic site crawl."""
        respx.post(f"{API_BASE_URL}/on_page/task_post").mock(
            return_value=httpx.Response(
                200,
                json={
                    "tasks": [{
                        "id": "task-12345",
                        "status_code": 20100,
                    }],
                    "cost": 0.05,
                }
            )
        )

        result = runner.invoke(app, ["site", "crawl", "example.com"])

        assert result.exit_code == 0
        assert "task-12345" in result.output
        assert "example.com" in result.output

    @respx.mock
    def test_crawl_with_options(self, mock_env_credentials: None) -> None:
        """Test crawl with options."""
        route = respx.post(f"{API_BASE_URL}/on_page/task_post").mock(
            return_value=httpx.Response(
                200,
                json={
                    "tasks": [{"id": "task-67890", "status_code": 20100}],
                    "cost": 0.1,
                }
            )
        )

        result = runner.invoke(app, [
            "site", "crawl", "example.com",
            "--max-pages", "50",
            "--enable-javascript",
            "--load-resources",
        ])

        assert result.exit_code == 0
        request = route.calls[0].request
        body = json.loads(request.content)
        assert body[0]["max_crawl_pages"] == 50
        assert body[0]["enable_javascript"] is True
        assert body[0]["load_resources"] is True


class TestSiteSummaryCommand:
    """Test suite for `dfseo site summary` command."""

    @respx.mock
    def test_summary_basic(self, mock_env_credentials: None) -> None:
        """Test getting summary for a task."""
        respx.get(f"{API_BASE_URL}/on_page/summary/task-12345").mock(
            return_value=httpx.Response(
                200,
                json={
                    "tasks": [{
                        "result": [{
                            "domain": {"name": "example.com"},
                            "crawl_progress": "finished",
                            "crawl_status": {
                                "pages_crawled": 45,
                                "pages_in_queue": 0,
                            },
                            "onpage_score": 78,
                        }]
                    }],
                    "cost": 0.02,
                }
            )
        )

        result = runner.invoke(app, ["site", "summary", "task-12345"])

        assert result.exit_code == 0
        assert "example.com" in result.output or "45" in result.output

    @respx.mock
    def test_summary_json_output(self, mock_env_credentials: None) -> None:
        """Test summary with JSON output."""
        respx.get(f"{API_BASE_URL}/on_page/summary/task-12345").mock(
            return_value=httpx.Response(
                200,
                json={
                    "tasks": [{
                        "result": [{
                            "domain": {"name": "example.com"},
                            "crawl_progress": "finished",
                            "crawl_status": {"pages_crawled": 45},
                        }]
                    }],
                    "cost": 0.02,
                }
            )
        )

        result = runner.invoke(app, ["site", "summary", "task-12345", "-o", "json"])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["target"] == "example.com"


class TestSiteAuditCommand:
    """Test suite for `dfseo site audit` command."""

    @respx.mock
    def test_audit_instant_page(self, mock_env_credentials: None) -> None:
        """Test audit with instant pages (single URL)."""
        respx.post(f"{API_BASE_URL}/on_page/instant_pages").mock(
            return_value=httpx.Response(
                200,
                json={
                    "tasks": [{
                        "result": [{
                            "items": [{
                                "url": "https://example.com/page",
                                "status_code": 200,
                                "onpage_score": 85,
                                "meta": {
                                    "title": "Test Page",
                                    "title_length": 10,
                                    "description": "Test description",
                                    "content": {"plain_text_word_count": 500},
                                },
                                "links": {"internal": [], "external": []},
                                "images": [],
                            }]
                        }]
                    }],
                    "cost": 0.01,
                }
            )
        )

        result = runner.invoke(app, [
            "site", "audit", "https://example.com/page",
            "--max-pages", "1",
        ])

        assert result.exit_code == 0
        assert "Test Page" in result.output or "85" in result.output


class TestSitePagesCommand:
    """Test suite for `dfseo site pages` command."""

    @respx.mock
    def test_pages_basic(self, mock_env_credentials: None) -> None:
        """Test getting pages for a task."""
        respx.post(f"{API_BASE_URL}/on_page/pages").mock(
            return_value=httpx.Response(
                200,
                json={
                    "tasks": [{
                        "result": [{
                            "total_count": 45,
                            "items": [
                                {
                                    "url": "https://example.com/",
                                    "status_code": 200,
                                    "onpage_score": 80,
                                    "meta": {"title": "Home", "content": {"plain_text_word_count": 300}},
                                    "links": {"internal": [], "external": []},
                                    "images": [],
                                }
                            ]
                        }]
                    }],
                    "cost": 0.02,
                }
            )
        )

        result = runner.invoke(app, ["site", "pages", "task-12345"])

        assert result.exit_code == 0
        assert "Home" in result.output or "45" in result.output


class TestTaskIdValidation:
    """Test task ID validation."""

    def test_invalid_task_id(self, mock_env_credentials: None) -> None:
        """Test error with invalid task ID format."""
        result = runner.invoke(app, ["site", "summary", "invalid-task-id!"])
        assert result.exit_code == 4
        assert "Invalid task_id" in result.output


class TestSiteLinksCommand:
    """Test suite for `dfseo site links` command."""

    @respx.mock
    def test_links_broken(self, mock_env_credentials: None) -> None:
        """Test getting broken links."""
        respx.post(f"{API_BASE_URL}/on_page/links").mock(
            return_value=httpx.Response(
                200,
                json={
                    "tasks": [{
                        "result": [{
                            "total_count": 5,
                            "items": [
                                {
                                    "url": "https://example.com/broken",
                                    "status_code": 404,
                                    "type": "external",
                                }
                            ]
                        }]
                    }],
                    "cost": 0.02,
                }
            )
        )

        result = runner.invoke(app, ["site", "links", "task-12345", "--type", "broken"])

        assert result.exit_code == 0
        assert "404" in result.output or "broken" in result.output.lower()
