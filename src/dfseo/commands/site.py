"""Site audit commands for dfseo CLI - On-Page API.

This module implements the On-Page API commands for technical SEO audits.
Unlike SERP and Keywords APIs, On-Page uses async tasks requiring polling.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from typing import Any

import typer

from dfseo.client import AuthenticationError, DataForSeoClient, DataForSeoError
from dfseo.config import Config
from dfseo.output import filter_fields, format_output, print_error
from dfseo.polling import poll_lighthouse_task, poll_onpage_task
from dfseo.pricing import format_dry_run_output
from dfseo.validation import validate_target

app = typer.Typer(help="Site Audit (On-Page API) commands")

VALID_OUTPUTS = ["json", "json-pretty", "table", "csv"]
VALID_PAGE_SORTS = ["onpage_score", "status_code", "size", "load_time"]
VALID_LINK_TYPES = ["broken", "internal", "external", "redirect"]
VALID_DUPLICATE_TYPES = ["title", "description", "content"]
VALID_RESOURCE_TYPES = ["image", "script", "stylesheet", "broken"]
VALID_LIGHTHOUSE_CATEGORIES = ["performance", "accessibility", "seo", "best-practices", "pwa"]
VALID_NONINDEX_REASONS = ["noindex", "canonical", "robots_txt", "redirect"]

# Cost estimation constants (approximate values from DataForSEO pricing)
BASE_COST_PER_PAGE = 0.001  # Base cost per page crawled
JS_COST_MULTIPLIER = 2.0  # JavaScript rendering doubles cost
RESOURCES_COST_MULTIPLIER = 1.5  # Loading resources adds 50% cost
BROWSER_RENDERING_MULTIPLIER = 3.0  # Full browser rendering triples cost

# Suspicious characters that might indicate injection attempts
SUSPICIOUS_CHARS = re.compile(r'[<>\"\'\x00-\x1f\x7f]')

def _validate_target(target: str) -> bool:
    """Validate target domain/URL for suspicious characters."""
    if not target or len(target) > 2048:
        return False
    if SUSPICIOUS_CHARS.search(target):
        return False
    return True

def _validate_domain_format(target: str) -> bool:
    """Basic domain/URL format validation."""
    # Allow domains (example.com) and URLs (https://example.com)
    if target.startswith(('http://', 'https://')):
        # URL format check
        return bool(re.match(r'^https?://[^/\s]+', target))
    else:
        # Domain format check (simple)
        return bool(re.match(r'^[a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,}', target))


def _get_client(
    login: str | None,
    password: str | None,
    verbose: bool,
) -> DataForSeoClient:
    """Get configured client with error handling."""
    config = Config()
    return DataForSeoClient(
        login=login,
        password=password,
        config=config,
        verbose=verbose,
    )


def _get_defaults() -> dict[str, Any]:
    """Get default configuration values."""
    config = Config()
    return {
        "output": config.get_default("output") or "json",
    }


def _validate_task_id(task_id: str) -> bool:
    """Validate task ID format.

    Task IDs are UUIDs in format: 07281559-0695-0216-0000-c269be8b7592
    """
    if not task_id:
        return False
    # UUID pattern
    pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    return bool(re.match(pattern, task_id, re.IGNORECASE))


def _is_full_url(target: str) -> bool:
    """Check if target is a full URL (starts with http/https)."""
    return target.startswith("http://") or target.startswith("https://")


def _calculate_estimated_cost(
    max_pages: int,
    enable_javascript: bool,
    load_resources: bool,
    enable_browser_rendering: bool,
) -> float:
    """Calculate estimated cost for crawling.

    Args:
        max_pages: Maximum pages to crawl
        enable_javascript: JS execution flag
        load_resources: Resource loading flag
        enable_browser_rendering: Full browser rendering flag

    Returns:
        Estimated cost in USD
    """
    base_cost = max_pages * BASE_COST_PER_PAGE

    multiplier = 1.0
    if enable_browser_rendering:
        multiplier = max(multiplier, BROWSER_RENDERING_MULTIPLIER)
    if enable_javascript:
        multiplier = max(multiplier, JS_COST_MULTIPLIER)
    if load_resources:
        multiplier = max(multiplier, RESOURCES_COST_MULTIPLIER)

    return base_cost * multiplier


def _print_cost_warning(
    max_pages: int,
    enable_javascript: bool,
    load_resources: bool,
    enable_browser_rendering: bool,
) -> None:
    """Print estimated cost warning to stderr.

    Args:
        max_pages: Maximum pages to crawl
        enable_javascript: JS execution flag
        load_resources: Resource loading flag
        enable_browser_rendering: Full browser rendering flag
    """
    cost = _calculate_estimated_cost(
        max_pages, enable_javascript, load_resources, enable_browser_rendering
    )

    warnings = []
    if max_pages >= 1000:
        warnings.append(f"Large crawl: {max_pages} pages")
    if enable_javascript:
        warnings.append("JavaScript execution enabled (+cost)")
    if load_resources:
        warnings.append("Resource loading enabled (+cost)")
    if enable_browser_rendering:
        warnings.append("Browser rendering enabled (+cost)")

    if warnings:
        print(f"Estimated cost: ${cost:.3f}", file=sys.stderr)
        for warning in warnings:
            print(f"  ⚠ {warning}", file=sys.stderr)


def _build_filters(
    errors_only: bool | None = None,
    status_code: int | None = None,
    resource_type: str | None = None,
    min_size: int | None = None,
    external_only: bool | None = None,
) -> list[Any] | None:
    """Build DataForSEO filter array.

    Args:
        errors_only: Filter for pages with errors
        status_code: Filter by HTTP status code
        resource_type: Filter by resource type (html, image, etc.)
        min_size: Minimum size in bytes
        external_only: Filter for external resources only

    Returns:
        Filter array or None if no filters
    """
    filters = []

    if errors_only:
        filters.append(["checks.broken_links", "=", True])

    if status_code is not None:
        filters.append(["status_code", "=", status_code])

    if resource_type:
        filters.append(["resource_type", "=", resource_type])

    if min_size is not None:
        filters.append(["size", ">=", min_size])

    if external_only:
        filters.append(["is_external", "=", True])

    if not filters:
        return None

    if len(filters) == 1:
        return filters[0]

    # Combine with "and"
    result = []
    for i, f in enumerate(filters):
        if i > 0:
            result.append("and")
        result.append(f)
    return result


def _build_order_by(sort: str, order: str) -> list[str]:
    """Build order_by array.

    Args:
        sort: Sort field
        order: Sort order (asc/desc)

    Returns:
        Order by array
    """
    field_map = {
        "onpage_score": "onpage_score",
        "status_code": "status_code",
        "size": "size",
        "load_time": "time_to_interactive",
    }

    field = field_map.get(sort, sort)
    return [f"{field},{order}"]


def _parse_summary_response(data: dict[str, Any], task_id: str) -> dict[str, Any]:
    """Parse summary API response into standardized format."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "task_id": task_id,
        "crawl_progress": "unknown",
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]

        # Basic crawl info
        result["target"] = task_result.get("domain", {}).get("name", "")
        result["crawl_progress"] = task_result.get("crawl_progress", "unknown")

        # Crawl status
        crawl_status = task_result.get("crawl_status", {})
        result["crawl_status"] = {
            "max_crawl_pages": crawl_status.get("max_crawl_pages", 0),
            "pages_crawled": crawl_status.get("pages_crawled", 0),
            "pages_in_queue": crawl_status.get("pages_in_queue", 0),
        }

        # Domain info
        domain = task_result.get("domain", {})
        result["domain_info"] = {
            "name": domain.get("name", ""),
            "ip": domain.get("ip", ""),
            "server": domain.get("server", ""),
            "cms": domain.get("cms", None),
            "crawl_start": task_result.get("crawl_start_time", ""),
            "crawl_end": task_result.get("crawl_end_time", ""),
        }

        # On-page score
        result["onpage_score"] = task_result.get("onpage_score", 0)

        # Pages summary
        page_metrics = task_result.get("page_metrics", {})
        result["pages_summary"] = {
            "total": page_metrics.get("total", 0),
            "with_errors": page_metrics.get("errors", 0),
            "with_warnings": page_metrics.get("warnings", 0),
            "with_notices": page_metrics.get("notices", 0),
        }

        # Errors breakdown
        result["errors"] = _extract_errors(task_result)

        # Links summary
        links = task_result.get("links", {})
        result["links_summary"] = {
            "internal": links.get("internal", 0),
            "external": links.get("external", 0),
            "broken": links.get("broken", 0),
        }

    return result


def _extract_errors(task_result: dict[str, Any]) -> dict[str, Any]:
    """Extract error information from task result."""
    errors = {"critical": {}, "warnings": {}}

    # These are common check fields in the On-Page API
    checks_mapping = {
        # Critical errors
        "broken_links": "broken_links",
        "duplicate_title": "duplicate_title_tag",
        "no_title": "no_title",
        "redirect_loop": "redirect_loop",
        "is_http": "is_http",
        # Warnings
        "title_too_long": "title_too_long",
        "no_description": "no_description",
        "low_content": "low_content_rate",
        "missing_alt_tags": "images_without_alt",
    }

    # Try to extract from page_metrics
    page_metrics = task_result.get("page_metrics", {})

    # Count by issues - this is simplified
    # In real data, we'd need to aggregate from pages data
    errors["critical"] = {
        "broken_links": page_metrics.get("broken_links", 0),
        "duplicate_title": 0,  # Would need to query duplicate_tags endpoint
        "no_title": 0,  # Would need to aggregate from pages
        "redirect_loop": 0,
        "is_http": 0,
    }

    errors["warnings"] = {
        "title_too_long": 0,
        "no_description": 0,
        "low_content": 0,
        "missing_alt_tags": 0,
    }

    return errors


def _format_summary_table(data: dict[str, Any]) -> str:
    """Format summary as human-readable table."""
    output_lines = []

    target = data.get("target", "")
    pages_crawled = data.get("crawl_status", {}).get("pages_crawled", 0)
    max_pages = data.get("crawl_status", {}).get("max_crawl_pages", 0)
    score = data.get("onpage_score", 0)

    output_lines.append(f"  Target: {target} | Pages crawled: {pages_crawled}/{max_pages} | OnPage Score: {score}/100")
    output_lines.append("")

    # Critical errors
    critical = data.get("errors", {}).get("critical", {})
    critical_items = [(k.replace("_", " ").title(), v) for k, v in critical.items() if v > 0]

    if critical_items:
        output_lines.append("  ✗ CRITICAL ERRORS")
        for name, count in critical_items:
            output_lines.append(f"    {name:.<25} {count}")
        output_lines.append("")

    # Warnings
    warnings = data.get("errors", {}).get("warnings", {})
    warning_items = [(k.replace("_", " ").title(), v) for k, v in warnings.items() if v > 0]

    if warning_items:
        output_lines.append("  ⚠ WARNINGS")
        for name, count in warning_items:
            output_lines.append(f"    {name:.<25} {count}")
        output_lines.append("")

    # Links summary
    links = data.get("links_summary", {})
    output_lines.append(f"  Links: {links.get('internal', 0)} internal | {links.get('external', 0)} external | {links.get('broken', 0)} broken")
    output_lines.append("")

    cost = data.get("cost", 0)
    output_lines.append(f"  Cost: ${cost:.3f}")

    return "\n".join(output_lines)



@app.command("crawl")
def site_crawl(
    target: str = typer.Argument(..., help="Target domain or URL to crawl"),
    max_pages: int = typer.Option(100, "--max-pages", "-n", help="Maximum pages to crawl"),
    enable_javascript: bool = typer.Option(False, "--enable-javascript", "--js", help="Execute JavaScript (costs extra)"),
    load_resources: bool = typer.Option(False, "--load-resources", help="Load images, CSS, JS (costs extra)"),
    enable_browser_rendering: bool = typer.Option(False, "--enable-browser-rendering", help="Full browser rendering (costs extra)"),
    start_url: str | None = typer.Option(None, "--start-url", help="Starting URL (default: homepage)"),
    respect_sitemap: bool = typer.Option(True, "--respect-sitemap/--ignore-sitemap", help="Follow sitemap.xml"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Start a site crawl and return task_id (non-blocking)."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    # Validate target input
    try:
        target = validate_target(target)
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(code=4)

    # Handle dry-run mode
    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/on_page/task_post",
            request_body=[{"target": target, "max_crawl_pages": max_pages}],
            params={"max_crawl_pages": max_pages, "enable_javascript": enable_javascript, "load_resources": load_resources, "enable_browser_rendering": enable_browser_rendering},
        )
        print(format_output(result, output_format))
        return

    # Print cost warning for expensive options
    _print_cost_warning(max_pages, enable_javascript, load_resources, enable_browser_rendering)

    try:
        client = _get_client(login, password, verbose)

        payload = [{
            "target": target,
            "max_crawl_pages": max_pages,
            "load_resources": load_resources,
            "enable_javascript": enable_javascript,
            "enable_browser_rendering": enable_browser_rendering,
            "respect_sitemap": respect_sitemap,
        }]

        if start_url:
            payload[0]["start_url"] = start_url

        data = client._request("POST", "/on_page/task_post", json_data=payload)

        # Extract task_id
        task_id = None
        if data.get("tasks") and len(data["tasks"]) > 0:
            task_id = data["tasks"][0].get("id")

        if not task_id:
            print_error("Failed to get task_id from API response")
            raise typer.Exit(code=1)

        client.close()

        result = {
            "task_id": task_id,
            "target": target,
            "max_crawl_pages": max_pages,
            "status": "crawling",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        fields_list = fields.split(",") if fields else None
        if fields_list:
            result = filter_fields(result, fields_list)

        if output_format == "table":
            print(f"  Crawl started: {target}")
            print(f"  Task ID: {task_id}")
            print(f"  Max pages: {max_pages}")
        else:
            print(format_output(result, output_format))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


@app.command("summary")
def site_summary(
    task_id: str = typer.Argument(..., help="Task ID from crawl command"),
    wait: bool = typer.Option(False, "--wait", "-w", help="Wait for completion if still crawling"),
    timeout: int = typer.Option(300, "--timeout", help="Timeout in seconds for waiting"),
    poll_interval: int = typer.Option(10, "--poll-interval", help="Seconds between progress checks"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get crawl summary for a task."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    # Validate task_id
    if not _validate_task_id(task_id):
        print_error(f"Invalid task_id format: {task_id}")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        # If waiting, poll until complete
        if wait:
            try:
                summary = poll_onpage_task(
                    client=client,
                    task_id=task_id,
                    interval=poll_interval,
                    timeout=timeout,
                    verbose=verbose,
                )
                data = {"tasks": [{"result": [summary]}]}
            except TimeoutError:
                print_error(f"Timeout waiting for task {task_id}")
                raise typer.Exit(code=1)
        else:
            # Just get current status
            data = client._request("GET", f"/on_page/summary/{task_id}")

        client.close()

        result = _parse_summary_response(data, task_id)

        if output_format == "table":
            print(_format_summary_table(result))
        else:
            print(format_output(result, output_format))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


@app.command("audit")
def site_audit(
    target: str = typer.Argument(..., help="Target domain or URL to audit"),
    max_pages: int = typer.Option(100, "--max-pages", "-n", help="Maximum pages to crawl"),
    enable_javascript: bool = typer.Option(False, "--enable-javascript", "--js", help="Execute JavaScript (costs extra)"),
    load_resources: bool = typer.Option(False, "--load-resources", help="Load images, CSS, JS (costs extra)"),
    enable_browser_rendering: bool = typer.Option(False, "--enable-browser-rendering", help="Full browser rendering (costs extra)"),
    start_url: str | None = typer.Option(None, "--start-url", help="Starting URL"),
    respect_sitemap: bool = typer.Option(True, "--respect-sitemap/--ignore-sitemap", help="Follow sitemap.xml"),
    wait: bool = typer.Option(True, "--wait/--no-wait", "-w/", help="Wait for completion"),
    timeout: int = typer.Option(300, "--timeout", help="Timeout in seconds"),
    poll_interval: int = typer.Option(10, "--poll-interval", help="Seconds between progress checks"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="Show estimated cost without executing"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """All-in-one audit: crawl + wait + summary. Uses Instant Pages for single URLs."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    # Validate target input
    try:
        target = validate_target(target)
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(code=4)

    # Handle dry-run mode
    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/on_page/task_post",
            request_body=[{"target": target, "max_crawl_pages": max_pages}],
            params={"max_crawl_pages": max_pages, "enable_javascript": enable_javascript, "load_resources": load_resources, "enable_browser_rendering": enable_browser_rendering},
        )
        print(format_output(result, output_format))
        return

    # Check for single page instant mode
    if max_pages == 1 and _is_full_url(target):
        # Use Instant Pages API (Live)
        try:
            client = _get_client(login, password, verbose)

            payload = [{
                "url": target,
                "enable_javascript": enable_javascript,
                "load_resources": load_resources,
                "enable_browser_rendering": enable_browser_rendering,
            }]

            data = client._request("POST", "/on_page/instant_pages", json_data=payload)
            client.close()

            result = _parse_instant_pages_response(data, target)

            fields_list = fields.split(",") if fields else None
            if fields_list:
                result = filter_fields(result, fields_list)

            if output_format == "table":
                print(_format_instant_pages_table(result))
            else:
                print(format_output(result, output_format))

            return

        except AuthenticationError as e:
            print_error(f"Authentication error: {e}")
            raise typer.Exit(code=2)
        except DataForSeoError as e:
            print_error(f"Error: {e}")
            raise typer.Exit(code=e.exit_code)
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            raise typer.Exit(code=1)

    # Print cost warning
    _print_cost_warning(max_pages, enable_javascript, load_resources, enable_browser_rendering)

    try:
        client = _get_client(login, password, verbose)

        # Start crawl
        payload = [{
            "target": target,
            "max_crawl_pages": max_pages,
            "load_resources": load_resources,
            "enable_javascript": enable_javascript,
            "enable_browser_rendering": enable_browser_rendering,
            "respect_sitemap": respect_sitemap,
        }]

        if start_url:
            payload[0]["start_url"] = start_url

        data = client._request("POST", "/on_page/task_post", json_data=payload)

        task_id = None
        if data.get("tasks") and len(data["tasks"]) > 0:
            task_id = data["tasks"][0].get("id")

        if not task_id:
            print_error("Failed to get task_id from API response")
            raise typer.Exit(code=1)

        # If not waiting, return task_id like crawl command
        if not wait:
            client.close()
            result = {
                "task_id": task_id,
                "target": target,
                "max_crawl_pages": max_pages,
                "status": "crawling",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            print(format_output(result, output_format))
            return

        # Wait for completion
        try:
            summary = poll_onpage_task(
                client=client,
                task_id=task_id,
                interval=poll_interval,
                timeout=timeout,
                verbose=verbose,
            )
            data = {"tasks": [{"result": [summary]}]}
        except TimeoutError:
            print_error(f"Timeout waiting for task {task_id}")
            raise typer.Exit(code=1)
        finally:
            client.close()

        result = _parse_summary_response(data, task_id)

        fields_list = fields.split(",") if fields else None
        if fields_list:
            result = filter_fields(result, fields_list)

        if output_format == "table":
            print(_format_summary_table(result))
        else:
            print(format_output(result, output_format))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)



def _parse_instant_pages_response(data: dict[str, Any], url: str) -> dict[str, Any]:
    """Parse Instant Pages API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "url": url,
        "type": "instant_page",
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        items = task_result.get("items", [])

        if items:
            page = items[0]
            result["status_code"] = page.get("status_code", 0)
            result["onpage_score"] = page.get("onpage_score", 0)
            result["title"] = page.get("meta", {}).get("title", "")
            result["title_length"] = page.get("meta", {}).get("title_length", 0)
            result["description"] = page.get("meta", {}).get("description", "")
            result["description_length"] = page.get("meta", {}).get("description_length", 0)
            result["h1"] = page.get("meta", {}).get("h1", [])
            result["word_count"] = page.get("meta", {}).get("content", {}).get("plain_text_word_count", 0)
            result["internal_links"] = len(page.get("links", {}).get("internal", []))
            result["external_links"] = len(page.get("links", {}).get("external", []))
            result["images_without_alt"] = len([img for img in page.get("images", []) if not img.get("alt")])
            result["load_time"] = page.get("time_to_interactive", 0)
            result["checks"] = page.get("checks", {})

    return result


def _format_instant_pages_table(data: dict[str, Any]) -> str:
    """Format instant page result as table."""
    output_lines = []

    output_lines.append(f"  URL: {data.get('url', '')}")
    output_lines.append(f"  Status: {data.get('status_code', 'N/A')}")
    output_lines.append(f"  OnPage Score: {data.get('onpage_score', 0)}/100")
    output_lines.append("")

    output_lines.append(f"  Title: {data.get('title', 'N/A')[:60]}")
    output_lines.append(f"  Description: {data.get('description', 'N/A')[:80]}...")
    output_lines.append("")

    output_lines.append(f"  Word count: {data.get('word_count', 0)}")
    output_lines.append(f"  Links: {data.get('internal_links', 0)} internal | {data.get('external_links', 0)} external")
    output_lines.append(f"  Images without alt: {data.get('images_without_alt', 0)}")
    output_lines.append("")

    cost = data.get("cost", 0)
    output_lines.append(f"  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


@app.command("pages")
def site_pages(
    task_id: str = typer.Argument(..., help="Task ID from crawl command"),
    errors_only: bool = typer.Option(False, "--errors-only", help="Only pages with errors"),
    status_code: int | None = typer.Option(None, "--status-code", help="Filter by HTTP status code"),
    resource_type: str = typer.Option(None, "--type", help="Filter by type: html, image, script, stylesheet"),
    sort: str = typer.Option(None, "--sort", help="Sort by: onpage_score, status_code, size, load_time"),
    order: str = typer.Option("desc", "--order", help="Sort order: asc, desc"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    offset: int = typer.Option(0, "--offset", help="Offset for pagination"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table/csv)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """List crawled pages with metrics and checks."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if sort and sort not in VALID_PAGE_SORTS:
        print_error(f"Invalid sort field: {sort}")
        raise typer.Exit(code=4)

    if not _validate_task_id(task_id):
        print_error(f"Invalid task_id format: {task_id}")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        # Build payload
        payload = [{
            "id": task_id,
            "limit": limit,
            "offset": offset,
        }]

        # Add filters
        filters = _build_filters(
            errors_only=errors_only,
            status_code=status_code,
            resource_type=resource_type,
        )
        if filters:
            payload[0]["filters"] = filters

        # Add ordering
        if sort:
            payload[0]["order_by"] = _build_order_by(sort, order)

        data = client._request("POST", "/on_page/pages", json_data=payload)
        client.close()

        result = _parse_pages_response(data, task_id)

        if output_format == "table":
            print(_format_pages_table(result))
        elif output_format == "csv":
            print(_format_pages_csv(result))
        else:
            print(format_output(result, output_format))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_pages_response(data: dict[str, Any], task_id: str) -> dict[str, Any]:
    """Parse pages API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "task_id": task_id,
        "pages": [],
        "total_count": 0,
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        result["total_count"] = task_result.get("total_count", 0)

        for item in task_result.get("items", []):
            page = {
                "url": item.get("url", ""),
                "status_code": item.get("status_code", 0),
                "onpage_score": item.get("onpage_score", 0),
                "title": item.get("meta", {}).get("title", ""),
                "title_length": item.get("meta", {}).get("title_length", 0),
                "description": item.get("meta", {}).get("description", ""),
                "description_length": item.get("meta", {}).get("description_length", 0),
                "h1": item.get("meta", {}).get("h1", []),
                "word_count": item.get("meta", {}).get("content", {}).get("plain_text_word_count", 0),
                "internal_links": len(item.get("links", {}).get("internal", [])),
                "external_links": len(item.get("links", {}).get("external", [])),
                "images_without_alt": len([img for img in item.get("images", []) if not img.get("alt")]),
                "load_time": item.get("time_to_interactive", 0),
                "checks": item.get("checks", {}),
            }
            result["pages"].append(page)

    return result


def _format_pages_table(data: dict[str, Any]) -> str:
    """Format pages as table."""
    output_lines = []

    pages = data.get("pages", [])
    total = data.get("total_count", 0)

    output_lines.append(f"  Pages: {len(pages)} of {total} total")
    output_lines.append("")

    for page in pages[:20]:  # Limit to 20 for display
        status = page.get("status_code", 0)
        score = page.get("onpage_score", 0)
        title = page.get("title", "")[:40] or "No title"
        url = page.get("url", "")[:50]

        output_lines.append(f"  [{status}] {score:.0f} | {title}")
        output_lines.append(f"    {url}")

    if len(pages) > 20:
        output_lines.append(f"\n  ... and {len(pages) - 20} more pages")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_pages_csv(data: dict[str, Any]) -> str:
    """Format pages as CSV."""
    import csv
    import io

    output = io.StringIO()
    pages = data.get("pages", [])

    if pages:
        fieldnames = [
            "url", "status_code", "onpage_score", "title", "title_length",
            "description", "description_length", "word_count",
            "internal_links", "external_links", "images_without_alt", "load_time",
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for page in pages:
            writer.writerow(page)

    return output.getvalue()



@app.command("links")
def site_links(
    task_id: str = typer.Argument(..., help="Task ID from crawl command"),
    link_type: str | None = typer.Option(None, "--type", help="Filter by type: broken, internal, external, redirect"),
    page_from: str | None = typer.Option(None, "--page-from", help="Filter links from specific page"),
    page_to: str | None = typer.Option(None, "--page-to", help="Filter links to specific page"),
    dofollow_only: bool = typer.Option(False, "--dofollow-only", help="Only dofollow links"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table/csv)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """List links found during crawl."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if link_type and link_type not in VALID_LINK_TYPES:
        print_error(f"Invalid link type: {link_type}")
        raise typer.Exit(code=4)

    if not _validate_task_id(task_id):
        print_error(f"Invalid task_id format: {task_id}")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        # Build filters
        filters = None
        filter_parts = []

        # Translate --type broken to status_code filter
        if link_type == "broken":
            filter_parts.append(["status_code", ">=", 400])
        elif link_type == "internal":
            filter_parts.append(["is_external", "=", False])
        elif link_type == "external":
            filter_parts.append(["is_external", "=", True])
        elif link_type == "redirect":
            filter_parts.append(["status_code", ">=", 300])
            filter_parts.append(["status_code", "<", 400])

        if dofollow_only:
            filter_parts.append(["dofollow", "=", True])

        # Combine filters
        if len(filter_parts) == 1:
            filters = filter_parts[0]
        elif len(filter_parts) > 1:
            filters = []
            for i, f in enumerate(filter_parts):
                if i > 0:
                    filters.append("and")
                filters.append(f)

        payload = [{
            "id": task_id,
            "limit": limit,
        }]

        if filters:
            payload[0]["filters"] = filters

        data = client._request("POST", "/on_page/links", json_data=payload)
        client.close()

        result = _parse_links_response(data, task_id, link_type)

        if output_format == "table":
            print(_format_links_table(result))
        elif output_format == "csv":
            print(_format_links_csv(result))
        else:
            print(format_output(result, output_format))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_links_response(
    data: dict[str, Any],
    task_id: str,
    link_type: str | None,
) -> dict[str, Any]:
    """Parse links API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "task_id": task_id,
        "link_type_filter": link_type,
        "links": [],
        "total_count": 0,
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        result["total_count"] = task_result.get("total_count", 0)

        for item in task_result.get("items", []):
            link = {
                "url_from": item.get("url_from", ""),
                "url_to": item.get("url_to", ""),
                "status_code": item.get("status_code", 0),
                "is_external": item.get("is_external", False),
                "dofollow": item.get("dofollow", True),
                "link_type": item.get("link_type", ""),
                "text": item.get("text", ""),
            }
            result["links"].append(link)

    return result


def _format_links_table(data: dict[str, Any]) -> str:
    """Format links as table."""
    output_lines = []

    links = data.get("links", [])
    total = data.get("total_count", 0)
    link_type = data.get("link_type_filter", "all")

    output_lines.append(f"  Links ({link_type}): {len(links)} of {total} total")
    output_lines.append("")

    for link in links[:20]:
        status = link.get("status_code", 0)
        ext = "EXT" if link.get("is_external") else "INT"
        follow = "DF" if link.get("dofollow") else "NF"
        url_to = link.get("url_to", "")[:50]

        output_lines.append(f"  [{status}] {ext}/{follow} -> {url_to}")

    if len(links) > 20:
        output_lines.append(f"\n  ... and {len(links) - 20} more links")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_links_csv(data: dict[str, Any]) -> str:
    """Format links as CSV."""
    import csv
    import io

    output = io.StringIO()
    links = data.get("links", [])

    if links:
        fieldnames = ["url_from", "url_to", "status_code", "is_external", "dofollow", "link_type", "text"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for link in links:
            writer.writerow(link)

    return output.getvalue()


@app.command("duplicates")
def site_duplicates(
    task_id: str = typer.Argument(..., help="Task ID from crawl command"),
    dup_type: str = typer.Option("title", "--type", "-t", help="Type: title, description, content"),
    page: str | None = typer.Option(None, "--page", help="For content: URL of page to compare"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table/csv)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Find duplicate titles, descriptions, or content."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if dup_type not in VALID_DUPLICATE_TYPES:
        print_error(f"Invalid duplicate type: {dup_type}")
        raise typer.Exit(code=4)

    if not _validate_task_id(task_id):
        print_error(f"Invalid task_id format: {task_id}")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        # Determine endpoint based on type
        if dup_type in ("title", "description"):
            endpoint = "/on_page/duplicate_tags"
            tag_type = "title" if dup_type == "title" else "meta_description"
            payload = [{
                "id": task_id,
                "tag": tag_type,
                "limit": limit,
            }]
        else:  # content
            endpoint = "/on_page/duplicate_content"
            payload = [{
                "id": task_id,
                "limit": limit,
            }]
            if page:
                payload[0]["url"] = page

        data = client._request("POST", endpoint, json_data=payload)
        client.close()

        result = _parse_duplicates_response(data, task_id, dup_type)

        if output_format == "table":
            print(_format_duplicates_table(result))
        elif output_format == "csv":
            print(_format_duplicates_csv(result))
        else:
            print(format_output(result, output_format))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_duplicates_response(
    data: dict[str, Any],
    task_id: str,
    dup_type: str,
) -> dict[str, Any]:
    """Parse duplicate tags/content API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "task_id": task_id,
        "duplicate_type": dup_type,
        "duplicates": [],
        "total_count": 0,
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        result["total_count"] = task_result.get("total_count", 0)

        for item in task_result.get("items", []):
            dup = {
                "value": item.get("tag_value", item.get("content", "")),
                "urls": item.get("urls", []),
                "count": item.get("count", len(item.get("urls", []))),
            }
            result["duplicates"].append(dup)

    return result


def _format_duplicates_table(data: dict[str, Any]) -> str:
    """Format duplicates as table."""
    output_lines = []

    duplicates = data.get("duplicates", [])
    total = data.get("total_count", 0)
    dup_type = data.get("duplicate_type", "unknown")

    output_lines.append(f"  Duplicate {dup_type}s: {len(duplicates)} groups of {total} total")
    output_lines.append("")

    for dup in duplicates[:10]:
        value = dup.get("value", "")[:50] or "(empty)"
        count = dup.get("count", 0)
        output_lines.append(f"  [{count} pages] {value}")

    if len(duplicates) > 10:
        output_lines.append(f"\n  ... and {len(duplicates) - 10} more groups")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_duplicates_csv(data: dict[str, Any]) -> str:
    """Format duplicates as CSV."""
    import csv
    import io

    output = io.StringIO()
    duplicates = data.get("duplicates", [])

    if duplicates:
        writer = csv.writer(output)
        writer.writerow(["value", "count", "urls"])
        for dup in duplicates:
            writer.writerow([
                dup.get("value", ""),
                dup.get("count", 0),
                "|".join(dup.get("urls", [])),
            ])

    return output.getvalue()



@app.command("redirects")
def site_redirects(
    task_id: str = typer.Argument(..., help="Task ID from crawl command"),
    min_hops: int | None = typer.Option(None, "--min-hops", help="Only chains with >= N hops"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table/csv)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Find redirect chains."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if not _validate_task_id(task_id):
        print_error(f"Invalid task_id format: {task_id}")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        # Build filters
        filters = None
        if min_hops:
            filters = ["chain_length", ">=", min_hops]

        payload = [{
            "id": task_id,
            "limit": limit,
        }]

        if filters:
            payload[0]["filters"] = filters

        data = client._request("POST", "/on_page/redirect_chains", json_data=payload)
        client.close()

        result = _parse_redirects_response(data, task_id)

        if output_format == "table":
            print(_format_redirects_table(result))
        elif output_format == "csv":
            print(_format_redirects_csv(result))
        else:
            print(format_output(result, output_format))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_redirects_response(data: dict[str, Any], task_id: str) -> dict[str, Any]:
    """Parse redirect chains API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "task_id": task_id,
        "chains": [],
        "total_count": 0,
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        result["total_count"] = task_result.get("total_count", 0)

        for item in task_result.get("items", []):
            chain = {
                "start_url": item.get("start_url", ""),
                "end_url": item.get("end_url", ""),
                "chain_length": item.get("chain_length", 0),
                "urls": item.get("urls", []),
                "status_codes": item.get("status_codes", []),
            }
            result["chains"].append(chain)

    return result


def _format_redirects_table(data: dict[str, Any]) -> str:
    """Format redirect chains as table."""
    output_lines = []

    chains = data.get("chains", [])
    total = data.get("total_count", 0)

    output_lines.append(f"  Redirect chains: {len(chains)} of {total} total")
    output_lines.append("")

    for chain in chains[:10]:
        length = chain.get("chain_length", 0)
        start = chain.get("start_url", "")[:40]
        end = chain.get("end_url", "")[:40]
        output_lines.append(f"  [{length} hops] {start} -> {end}")

    if len(chains) > 10:
        output_lines.append(f"\n  ... and {len(chains) - 10} more chains")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_redirects_csv(data: dict[str, Any]) -> str:
    """Format redirect chains as CSV."""
    import csv
    import io

    output = io.StringIO()
    chains = data.get("chains", [])

    if chains:
        writer = csv.writer(output)
        writer.writerow(["start_url", "end_url", "chain_length", "urls", "status_codes"])
        for chain in chains:
            writer.writerow([
                chain.get("start_url", ""),
                chain.get("end_url", ""),
                chain.get("chain_length", 0),
                " -> ".join(chain.get("urls", [])),
                ",".join(str(s) for s in chain.get("status_codes", [])),
            ])

    return output.getvalue()


@app.command("non-indexable")
def site_non_indexable(
    task_id: str = typer.Argument(..., help="Task ID from crawl command"),
    reason: str | None = typer.Option(None, "--reason", help="Filter by reason: noindex, canonical, robots_txt, redirect"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table/csv)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """List pages blocked from indexing."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if reason and reason not in VALID_NONINDEX_REASONS:
        print_error(f"Invalid reason: {reason}")
        raise typer.Exit(code=4)

    if not _validate_task_id(task_id):
        print_error(f"Invalid task_id format: {task_id}")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        # Build filters
        filters = None
        if reason == "noindex":
            filters = ["has_noindex", "=", True]
        elif reason == "canonical":
            filters = ["has_canonical", "=", True]
        elif reason == "robots_txt":
            filters = ["blocked_by_robots_txt", "=", True]
        elif reason == "redirect":
            filters = ["is_redirect", "=", True]

        payload = [{
            "id": task_id,
            "limit": limit,
        }]

        if filters:
            payload[0]["filters"] = filters

        data = client._request("POST", "/on_page/non_indexable", json_data=payload)
        client.close()

        result = _parse_non_indexable_response(data, task_id, reason)

        if output_format == "table":
            print(_format_non_indexable_table(result))
        elif output_format == "csv":
            print(_format_non_indexable_csv(result))
        else:
            print(format_output(result, output_format))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_non_indexable_response(
    data: dict[str, Any],
    task_id: str,
    reason: str | None,
) -> dict[str, Any]:
    """Parse non-indexable pages API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "task_id": task_id,
        "reason_filter": reason,
        "pages": [],
        "total_count": 0,
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        result["total_count"] = task_result.get("total_count", 0)

        for item in task_result.get("items", []):
            page = {
                "url": item.get("url", ""),
                "status_code": item.get("status_code", 0),
                "reasons": [],
            }
            # Determine reasons
            checks = item.get("checks", {})
            if checks.get("has_noindex"):
                page["reasons"].append("noindex")
            if checks.get("has_canonical"):
                page["reasons"].append("canonical")
            if checks.get("blocked_by_robots_txt"):
                page["reasons"].append("robots_txt")
            if checks.get("is_redirect"):
                page["reasons"].append("redirect")

            result["pages"].append(page)

    return result


def _format_non_indexable_table(data: dict[str, Any]) -> str:
    """Format non-indexable pages as table."""
    output_lines = []

    pages = data.get("pages", [])
    total = data.get("total_count", 0)
    reason = data.get("reason_filter", "all")

    output_lines.append(f"  Non-indexable pages ({reason}): {len(pages)} of {total} total")
    output_lines.append("")

    for page in pages[:20]:
        status = page.get("status_code", 0)
        url = page.get("url", "")[:50]
        reasons = ", ".join(page.get("reasons", []))
        output_lines.append(f"  [{status}] {url} ({reasons})")

    if len(pages) > 20:
        output_lines.append(f"\n  ... and {len(pages) - 20} more pages")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_non_indexable_csv(data: dict[str, Any]) -> str:
    """Format non-indexable pages as CSV."""
    import csv
    import io

    output = io.StringIO()
    pages = data.get("pages", [])

    if pages:
        writer = csv.writer(output)
        writer.writerow(["url", "status_code", "reasons"])
        for page in pages:
            writer.writerow([
                page.get("url", ""),
                page.get("status_code", 0),
                "|".join(page.get("reasons", [])),
            ])

    return output.getvalue()



@app.command("resources")
def site_resources(
    task_id: str = typer.Argument(..., help="Task ID from crawl command"),
    resource_type: str | None = typer.Option(None, "--type", help="Filter by type: image, script, stylesheet, broken"),
    min_size: int | None = typer.Option(None, "--min-size", help="Minimum size in bytes"),
    external_only: bool = typer.Option(False, "--external-only", help="Only external resources"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table/csv)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """List site resources (images, scripts, stylesheets)."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if resource_type and resource_type not in VALID_RESOURCE_TYPES:
        print_error(f"Invalid resource type: {resource_type}")
        raise typer.Exit(code=4)

    if not _validate_task_id(task_id):
        print_error(f"Invalid task_id format: {task_id}")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        # Build filters
        filters = _build_filters(
            resource_type=resource_type if resource_type != "broken" else None,
            min_size=min_size,
            external_only=external_only,
        )

        # For broken resources, filter by status_code
        if resource_type == "broken":
            broken_filter = ["status_code", ">=", 400]
            if filters:
                # Combine with existing filters
                if isinstance(filters, list) and len(filters) == 3:
                    filters = [filters, "and", broken_filter]
                else:
                    filters = [filters, "and", broken_filter]
            else:
                filters = broken_filter

        payload = [{
            "id": task_id,
            "limit": limit,
        }]

        if filters:
            payload[0]["filters"] = filters

        data = client._request("POST", "/on_page/resources", json_data=payload)
        client.close()

        result = _parse_resources_response(data, task_id, resource_type)

        if output_format == "table":
            print(_format_resources_table(result))
        elif output_format == "csv":
            print(_format_resources_csv(result))
        else:
            print(format_output(result, output_format))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_resources_response(
    data: dict[str, Any],
    task_id: str,
    resource_type: str | None,
) -> dict[str, Any]:
    """Parse resources API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "task_id": task_id,
        "resource_type_filter": resource_type,
        "resources": [],
        "total_count": 0,
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        result["total_count"] = task_result.get("total_count", 0)

        for item in task_result.get("items", []):
            resource = {
                "url": item.get("url", ""),
                "resource_type": item.get("resource_type", ""),
                "status_code": item.get("status_code", 0),
                "size": item.get("size", 0),
                "is_external": item.get("is_external", False),
                "mime_type": item.get("mime_type", ""),
            }
            result["resources"].append(resource)

    return result


def _format_resources_table(data: dict[str, Any]) -> str:
    """Format resources as table."""
    output_lines = []

    resources = data.get("resources", [])
    total = data.get("total_count", 0)
    res_type = data.get("resource_type_filter", "all")

    output_lines.append(f"  Resources ({res_type}): {len(resources)} of {total} total")
    output_lines.append("")

    for res in resources[:20]:
        status = res.get("status_code", 0)
        rtype = res.get("resource_type", "unknown")[:4]
        size = res.get("size", 0)
        ext = "EXT" if res.get("is_external") else "INT"
        url = res.get("url", "")[:50]

        output_lines.append(f"  [{status}] {rtype} {size/1024:.1f}KB {ext} {url}")

    if len(resources) > 20:
        output_lines.append(f"\n  ... and {len(resources) - 20} more resources")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_resources_csv(data: dict[str, Any]) -> str:
    """Format resources as CSV."""
    import csv
    import io

    output = io.StringIO()
    resources = data.get("resources", [])

    if resources:
        writer = csv.DictWriter(
            output,
            fieldnames=["url", "resource_type", "status_code", "size", "is_external", "mime_type"],
        )
        writer.writeheader()
        for res in resources:
            writer.writerow(res)

    return output.getvalue()


@app.command("lighthouse")
def site_lighthouse(
    url: str = typer.Argument(..., help="URL to audit"),
    categories: str = typer.Option("all", "--categories", help="Comma-separated: performance,accessibility,seo,best-practices,pwa"),
    device: str = typer.Option("desktop", "--device", "-d", help="Device: desktop or mobile"),
    wait: bool = typer.Option(True, "--wait/--no-wait", "-w/", help="Wait for completion"),
    timeout: int = typer.Option(120, "--timeout", help="Timeout in seconds"),
    poll_interval: int = typer.Option(5, "--poll-interval", help="Seconds between checks"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Run Google Lighthouse audit on a URL."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if device not in ("desktop", "mobile"):
        print_error(f"Invalid device: {device}")
        raise typer.Exit(code=4)

    # Parse categories
    category_list = []
    if categories == "all":
        category_list = ["performance", "accessibility", "seo", "best_practices"]
    else:
        cat_map = {
            "performance": "performance",
            "accessibility": "accessibility",
            "seo": "seo",
            "best-practices": "best_practices",
            "pwa": "pwa",
        }
        for cat in categories.split(","):
            cat = cat.strip()
            if cat in cat_map:
                category_list.append(cat_map[cat])
            else:
                print_error(f"Invalid category: {cat}")
                raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        # Start Lighthouse task
        payload = [{
            "url": url,
            "for_mobile": device == "mobile",
            "categories": category_list,
        }]

        data = client._request("POST", "/on_page/lighthouse/task_post", json_data=payload)

        task_id = None
        if data.get("tasks") and len(data["tasks"]) > 0:
            task_id = data["tasks"][0].get("id")

        if not task_id:
            print_error("Failed to get task_id from API response")
            raise typer.Exit(code=1)

        # If not waiting, return task_id
        if not wait:
            client.close()
            result = {
                "task_id": task_id,
                "url": url,
                "device": device,
                "status": "processing",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            print(format_output(result, output_format))
            return

        # Wait for completion
        try:
            lighthouse_data = poll_lighthouse_task(
                client=client,
                task_id=task_id,
                interval=poll_interval,
                timeout=timeout,
                verbose=verbose,
            )
        except TimeoutError:
            print_error(f"Timeout waiting for Lighthouse task {task_id}")
            raise typer.Exit(code=1)
        finally:
            client.close()

        result = _parse_lighthouse_response(lighthouse_data, url, device)

        if output_format == "table":
            print(_format_lighthouse_table(result))
        else:
            print(format_output(result, output_format))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_lighthouse_response(
    data: dict[str, Any],
    url: str,
    device: str,
) -> dict[str, Any]:
    """Parse Lighthouse API response."""
    lighthouse = data.get("lighthouse", {})

    scores = {}
    metrics = {}

    # Extract scores
    categories = lighthouse.get("categories", {})
    for cat_key, cat_data in categories.items():
        score = cat_data.get("score", 0)
        # Score is 0-1, convert to 0-100
        scores[cat_key.replace("_", "-")] = int(score * 100) if score else 0

    # Extract metrics
    audits = lighthouse.get("audits", {})
    metric_keys = {
        "first-contentful-paint": "first_contentful_paint",
        "largest-contentful-paint": "largest_contentful_paint",
        "total-blocking-time": "total_blocking_time",
        "cumulative-layout-shift": "cumulative_layout_shift",
        "speed-index": "speed_index",
    }

    for audit_key, metric_name in metric_keys.items():
        audit = audits.get(audit_key, {})
        display_value = audit.get("displayValue", "")
        numeric_value = audit.get("numericValue", 0)

        # Try to extract numeric value from display value
        if numeric_value:
            metrics[metric_name] = numeric_value
        elif display_value:
            # Parse "1.2 s" or "150 ms"
            val_str = display_value.replace(" s", "").replace(" ms", "").strip()
            try:
                metrics[metric_name] = float(val_str)
            except ValueError:
                metrics[metric_name] = 0

    return {
        "url": url,
        "device": device,
        "scores": scores,
        "metrics": metrics,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _format_lighthouse_table(data: dict[str, Any]) -> str:
    """Format Lighthouse result as table."""
    output_lines = []

    output_lines.append(f"  URL: {data.get('url', '')} | Device: {data.get('device', '')}")
    output_lines.append("")

    scores = data.get("scores", {})
    if scores:
        output_lines.append("  Category          │ Score")
        output_lines.append("  ──────────────────┼────────────")

        for cat, score in sorted(scores.items()):
            bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
            cat_name = cat.replace("-", " ").title()
            output_lines.append(f"  {cat_name:<17} │ {score:>3} {bar}")

    metrics = data.get("metrics", {})
    if metrics:
        output_lines.append("")
        output_lines.append("  Core Web Vitals:")
        fcp = metrics.get("first_contentful_paint", 0)
        lcp = metrics.get("largest_contentful_paint", 0)
        tbt = metrics.get("total_blocking_time", 0)
        cls = metrics.get("cumulative_layout_shift", 0)
        si = metrics.get("speed_index", 0)

        output_lines.append(f"    FCP: {fcp:.1f}s | LCP: {lcp:.1f}s | TBT: {tbt:.0f}ms | CLS: {cls:.2f} | SI: {si:.1f}s")

    output_lines.append("")
    output_lines.append("  Cost: $0.002")  # Lighthouse has fixed cost

    return "\n".join(output_lines)



@app.command("tasks")
def site_tasks(
    ready_only: bool = typer.Option(False, "--ready", help="Only show tasks ready for retrieval"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """List On-Page API tasks."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        endpoint = "/on_page/tasks_ready" if ready_only else "/on_page/tasks_ready"
        data = client._request("GET", endpoint)
        client.close()

        result = _parse_tasks_response(data, ready_only)

        if output_format == "table":
            print(_format_tasks_table(result))
        else:
            print(format_output(result, output_format))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_tasks_response(data: dict[str, Any], ready_only: bool) -> dict[str, Any]:
    """Parse tasks API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "ready_only": ready_only,
        "tasks": [],
        "count": 0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]

        # The API returns different structure - handle both
        items = task_result.get("items", [])
        for item in items:
            task = {
                "id": item.get("id", ""),
                "target": item.get("data", {}).get("target", ""),
                "date_posted": item.get("date_posted", ""),
                "tag": item.get("tag", ""),
            }
            result["tasks"].append(task)

        result["count"] = len(result["tasks"])

    return result


def _format_tasks_table(data: dict[str, Any]) -> str:
    """Format tasks as table."""
    output_lines = []

    tasks = data.get("tasks", [])
    ready_filter = "ready" if data.get("ready_only") else "all"

    output_lines.append(f"  Tasks ({ready_filter}): {len(tasks)}")
    output_lines.append("")

    for task in tasks[:20]:
        task_id = task.get("id", "")[:20]
        target = task.get("target", "")[:30]
        date = task.get("date_posted", "")[:10]
        output_lines.append(f"  {date} | {task_id} | {target}")

    if len(tasks) > 20:
        output_lines.append(f"\n  ... and {len(tasks) - 20} more tasks")

    return "\n".join(output_lines)


@app.command("instant")
def site_instant(
    url: str = typer.Argument(..., help="URL to analyze"),
    enable_javascript: bool = typer.Option(False, "--enable-javascript", "--js", help="Execute JavaScript"),
    load_resources: bool = typer.Option(False, "--load-resources", help="Load resources"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Live instant analysis of a single page (no polling)."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        payload = [{
            "url": url,
            "enable_javascript": enable_javascript,
            "load_resources": load_resources,
        }]

        data = client._request("POST", "/on_page/instant_pages", json_data=payload)
        client.close()

        result = _parse_instant_pages_response(data, url)

        if output_format == "table":
            print(_format_instant_pages_table(result))
        else:
            print(format_output(result, output_format))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)
