"""Content Analysis commands for dfseo CLI.

Provides content search, summary, and sentiment analysis
using the DataForSEO Content Analysis API.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import typer

from dfseo.client import AuthenticationError, DataForSeoClient, DataForSeoError
from dfseo.config import Config
from dfseo.output import filter_fields, format_output, print_error
from dfseo.pricing import format_dry_run_output
from dfseo.validation import validate_keyword, validate_raw_params

content_app = typer.Typer(help="Content Analysis API commands")

VALID_OUTPUTS = ["json", "json-pretty", "table", "csv"]
VALID_SEARCH_MODES = ["as_is", "broad"]
VALID_SENTIMENTS = ["positive", "negative", "neutral"]


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
        "output": config.get_default("output"),
    }


@content_app.command("search")
def content_search(
    keyword: str = typer.Argument(..., help="Keyword to search for in web content"),
    search_mode: str = typer.Option("as_is", "--search-mode", help="Search mode: as_is or broad"),
    sentiment: str = typer.Option(None, "--sentiment", help="Filter by sentiment: positive/negative/neutral"),
    from_date: str = typer.Option(None, "--from-date", help="Start date (YYYY-MM-DD)"),
    to_date: str = typer.Option(None, "--to-date", help="End date (YYYY-MM-DD)"),
    limit: int = typer.Option(10, "--limit", "-n", help="Max results"),
    sort: str = typer.Option(None, "--sort", help="Sort by: rank, date, content_score"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Search web content mentioning a keyword."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if search_mode not in VALID_SEARCH_MODES:
        print_error(f"Invalid search mode: {search_mode}")
        raise typer.Exit(code=4)

    if sentiment and sentiment not in VALID_SENTIMENTS:
        print_error(f"Invalid sentiment: {sentiment}")
        raise typer.Exit(code=4)

    try:
        keyword = validate_keyword(keyword)
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(code=4)

    if raw_params:
        try:
            raw_payload = validate_raw_params(raw_params)
        except ValueError as e:
            print_error(str(e))
            raise typer.Exit(code=4)
    else:
        raw_payload = None

    payload = [{
        "keyword": keyword,
        "search_mode": search_mode,
        "limit": limit,
    }]
    if sentiment:
        payload[0]["connotation_types"] = {"filter": sentiment}
    if from_date:
        payload[0]["search_from"] = from_date
    if to_date:
        payload[0]["search_to"] = to_date
    if sort:
        payload[0]["order_by"] = [f"{sort},desc"]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/content_analysis/search/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)

        data = client._request(
            "POST",
            "/content_analysis/search/live",
            json_data=raw_payload or payload,
        )

        result = _parse_search_response(data, keyword)
        client.close()

        if fields_list:
            result = filter_fields(result, fields_list)
        formatted = _format_search_output(result, output_format)
        print(formatted)

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_search_response(data: dict[str, Any], keyword: str) -> dict[str, Any]:
    """Parse content search API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    results = []
    total_count = 0
    cost = api_response.cost or 0.0

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        total_count = task_result.get("total_count", 0)
        items = task_result.get("items", [])

        for item in items:
            result_item = {
                "url": item.get("url", ""),
                "domain": item.get("main_domain", ""),
                "title": item.get("title", ""),
                "date": item.get("date_published", ""),
                "content_type": item.get("content_type", ""),
                "sentiment": item.get("connotation_types", {}),
                "content_score": item.get("content_quality_score", 0),
                "spam_score": item.get("spam_score", 0),
                "group_date": item.get("group_date", ""),
            }
            results.append(result_item)

    return {
        "keyword": keyword,
        "total_count": total_count,
        "returned_count": len(results),
        "results": results,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _format_search_output(result: dict[str, Any], output_format: str) -> str:
    """Format search command output."""
    if output_format in ("json", "json-pretty"):
        return format_output(result, output_format)
    elif output_format == "csv":
        return _format_search_csv(result)
    else:
        return _format_search_table(result)


def _format_search_table(result: dict[str, Any]) -> str:
    """Format search results as table."""
    from rich.console import Console
    from rich.table import Table

    console = Console(force_terminal=True)
    output_lines = []

    keyword = result.get("keyword", "")
    total = result.get("total_count", 0)
    returned = result.get("returned_count", 0)

    output_lines.append(f"  Content Search: \"{keyword}\" | Showing {returned} of {total:,}")
    output_lines.append("")

    results = result.get("results", [])
    if results:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Domain", style="cyan", min_width=20)
        table.add_column("Title", style="white", min_width=30)
        table.add_column("Date", style="yellow")
        table.add_column("Score", style="green", justify="right")

        for item in results:
            table.add_row(
                item.get("domain", "")[:25],
                item.get("title", "")[:40],
                item.get("date", "-")[:10] if item.get("date") else "-",
                str(item.get("content_score", "-")),
            )

        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

    cost = result.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_search_csv(result: dict[str, Any]) -> str:
    """Format search results as CSV."""
    import csv
    import io

    output = io.StringIO()
    results = result.get("results", [])

    if results:
        writer = csv.DictWriter(
            output,
            fieldnames=["url", "domain", "title", "date", "content_type", "content_score", "spam_score"],
            extrasaction="ignore",
        )
        writer.writeheader()
        for item in results:
            writer.writerow(item)

    return output.getvalue()


@content_app.command("summary")
def content_summary(
    keyword: str = typer.Argument(..., help="Keyword to analyze"),
    from_date: str = typer.Option(None, "--from-date", help="Start date (YYYY-MM-DD)"),
    to_date: str = typer.Option(None, "--to-date", help="End date (YYYY-MM-DD)"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get aggregate content metrics for a keyword."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        keyword = validate_keyword(keyword)
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(code=4)

    if raw_params:
        try:
            raw_payload = validate_raw_params(raw_params)
        except ValueError as e:
            print_error(str(e))
            raise typer.Exit(code=4)
    else:
        raw_payload = None

    payload = [{"keyword": keyword}]
    if from_date:
        payload[0]["search_from"] = from_date
    if to_date:
        payload[0]["search_to"] = to_date

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/content_analysis/summary/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)

        data = client._request(
            "POST",
            "/content_analysis/summary/live",
            json_data=raw_payload or payload,
        )

        result = _parse_summary_response(data, keyword)
        client.close()

        if fields_list:
            result = filter_fields(result, fields_list)
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


def _parse_summary_response(data: dict[str, Any], keyword: str) -> dict[str, Any]:
    """Parse content summary API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)
    cost = api_response.cost or 0.0

    summary = {}
    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        summary = {
            "total_count": task_result.get("total_count", 0),
            "sentiment": task_result.get("connotation_types", {}),
            "content_types": task_result.get("content_type", {}),
            "top_domains": task_result.get("top_domains", []),
            "text_categories": task_result.get("text_categories", []),
        }

    return {
        "keyword": keyword,
        "summary": summary,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@content_app.command("sentiment")
def content_sentiment(
    keyword: str = typer.Argument(..., help="Keyword to analyze sentiment for"),
    limit: int = typer.Option(10, "--limit", "-n", help="Max results"),
    from_date: str = typer.Option(None, "--from-date", help="Start date (YYYY-MM-DD)"),
    to_date: str = typer.Option(None, "--to-date", help="End date (YYYY-MM-DD)"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Analyze sentiment of content mentioning a keyword."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        keyword = validate_keyword(keyword)
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(code=4)

    if raw_params:
        try:
            raw_payload = validate_raw_params(raw_params)
        except ValueError as e:
            print_error(str(e))
            raise typer.Exit(code=4)
    else:
        raw_payload = None

    payload = [{
        "keyword": keyword,
        "limit": limit,
    }]
    if from_date:
        payload[0]["search_from"] = from_date
    if to_date:
        payload[0]["search_to"] = to_date

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/content_analysis/sentiment_analysis/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)

        data = client._request(
            "POST",
            "/content_analysis/sentiment_analysis/live",
            json_data=raw_payload or payload,
        )

        result = _parse_sentiment_response(data, keyword)
        client.close()

        if fields_list:
            result = filter_fields(result, fields_list)
        formatted = _format_sentiment_output(result, output_format)
        print(formatted)

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_sentiment_response(data: dict[str, Any], keyword: str) -> dict[str, Any]:
    """Parse content sentiment API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    results = []
    total_count = 0
    cost = api_response.cost or 0.0

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        total_count = task_result.get("total_count", 0)
        items = task_result.get("items", [])

        for item in items:
            result_item = {
                "url": item.get("url", ""),
                "domain": item.get("main_domain", ""),
                "title": item.get("title", ""),
                "date": item.get("date_published", ""),
                "sentiment": item.get("connotation_types", {}),
                "content_score": item.get("content_quality_score", 0),
            }
            results.append(result_item)

    return {
        "keyword": keyword,
        "total_count": total_count,
        "returned_count": len(results),
        "results": results,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _format_sentiment_output(result: dict[str, Any], output_format: str) -> str:
    """Format sentiment command output."""
    if output_format in ("json", "json-pretty"):
        return format_output(result, output_format)
    elif output_format == "csv":
        return _format_sentiment_csv(result)
    else:
        return _format_sentiment_table(result)


def _format_sentiment_table(result: dict[str, Any]) -> str:
    """Format sentiment results as table."""
    from rich.console import Console
    from rich.table import Table

    console = Console(force_terminal=True)
    output_lines = []

    keyword = result.get("keyword", "")
    total = result.get("total_count", 0)

    output_lines.append(f"  Sentiment Analysis: \"{keyword}\" | Total: {total:,}")
    output_lines.append("")

    results = result.get("results", [])
    if results:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Domain", style="cyan", min_width=20)
        table.add_column("Title", style="white", min_width=25)
        table.add_column("Sentiment", style="yellow")
        table.add_column("Score", style="green", justify="right")

        for item in results:
            sentiment = item.get("sentiment", {})
            sentiment_str = ", ".join(f"{k}: {v}" for k, v in sentiment.items()) if sentiment else "-"

            table.add_row(
                item.get("domain", "")[:25],
                item.get("title", "")[:30],
                sentiment_str[:20],
                str(item.get("content_score", "-")),
            )

        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

    cost = result.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_sentiment_csv(result: dict[str, Any]) -> str:
    """Format sentiment results as CSV."""
    import csv
    import io

    output = io.StringIO()
    results = result.get("results", [])

    if results:
        writer = csv.DictWriter(
            output,
            fieldnames=["url", "domain", "title", "date", "content_score"],
            extrasaction="ignore",
        )
        writer.writeheader()
        for item in results:
            writer.writerow(item)

    return output.getvalue()
