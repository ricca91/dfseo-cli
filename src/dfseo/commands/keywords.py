"""Keywords commands for dfseo CLI."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import typer

from dfseo.client import AuthenticationError, DataForSeoClient, DataForSeoError
from dfseo.config import Config
from dfseo.output import filter_fields, format_output, print_error
from dfseo.pricing import format_dry_run_output
from dfseo.validation import validate_keyword, validate_raw_params

keywords_app = typer.Typer(help="Keywords Data API commands")

VALID_OUTPUTS = ["json", "json-pretty", "table", "csv"]
VALID_SORT_FIELDS = ["relevance", "volume", "cpc", "difficulty"]
VALID_ORDERS = ["asc", "desc"]

# Google Ads rate limit: 12 requests per minute
GOOGLE_ADS_RATE_LIMIT = 12
GOOGLE_ADS_RATE_LIMIT_WINDOW = 60  # seconds
_last_google_ads_request_time: float = 0
_google_ads_request_count: int = 0


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
        "location_name": config.get_default("location_name"),
        "language_name": config.get_default("language_name"),
        "output": config.get_default("output"),
    }


def load_keywords(keywords: list[str], from_file: str | None) -> list[str]:
    """Load keywords from CLI arguments or file.

    Args:
        keywords: Keywords from CLI arguments
        from_file: Path to file containing keywords (one per line)

    Returns:
        List of keywords

    Raises:
        typer.Exit: If file not found or invalid
    """
    if from_file:
        path = Path(from_file)
        if not path.exists():
            print_error(f"File not found: {from_file}")
            raise typer.Exit(code=4)

        try:
            with open(path, "r", encoding="utf-8") as f:
                file_keywords = []
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith("#"):
                        file_keywords.append(line)
                return file_keywords
        except Exception as e:
            print_error(f"Error reading file: {e}")
            raise typer.Exit(code=4)

    return list(keywords)


def build_filters(
    min_volume: int | None = None,
    max_volume: int | None = None,
    min_difficulty: int | None = None,
    max_difficulty: int | None = None,
) -> list[Any] | None:
    """Build DataForSEO Labs API filter array.

    Args:
        min_volume: Minimum search volume
        max_volume: Maximum search volume
        min_difficulty: Minimum keyword difficulty
        max_difficulty: Maximum keyword difficulty

    Returns:
        Filter array or None if no filters
    """
    filters = []

    if min_volume is not None:
        filters.append(["keyword_info.search_volume", ">=", min_volume])

    if max_volume is not None:
        filters.append(["keyword_info.search_volume", "<=", max_volume])

    if min_difficulty is not None:
        filters.append(["keyword_properties.keyword_difficulty", ">=", min_difficulty])

    if max_difficulty is not None:
        filters.append(["keyword_properties.keyword_difficulty", "<=", max_difficulty])

    if not filters:
        return None

    if len(filters) == 1:
        return filters[0]

    # Combine multiple filters with "and"
    result = []
    for i, f in enumerate(filters):
        if i > 0:
            result.append("and")
        result.append(f)
    return result


def build_order_by(sort: str, order: str) -> list[str]:
    """Build order_by array for Labs API.

    Args:
        sort: Sort field
        order: Sort order

    Returns:
        Order by array
    """
    field_map = {
        "relevance": "relevance",
        "volume": "keyword_info.search_volume",
        "cpc": "keyword_info.cpc",
        "difficulty": "keyword_properties.keyword_difficulty",
    }

    field = field_map.get(sort, "relevance")
    return [f"{field},{order}"]


def build_labs_order_by(sort: str, order: str) -> list[str]:
    """Build order_by array for Labs API with extended sort fields.

    Args:
        sort: Sort field
        order: Sort order

    Returns:
        Order by array
    """
    field_map = {
        "relevance": "relevance",
        "volume": "keyword_data.keyword_info.search_volume",
        "cpc": "keyword_data.keyword_info.cpc",
        "difficulty": "keyword_data.keyword_properties.keyword_difficulty",
        "position": "ranked_serp_element.serp_item.rank_group",
        "traffic": "ranked_serp_element.serp_item.etv",
    }

    field = field_map.get(sort, "relevance")
    return [f"{field},{order}"]


def build_ranked_filters(
    min_volume: int | None = None,
    max_volume: int | None = None,
    min_position: int | None = None,
    max_position: int | None = None,
) -> list[Any] | None:
    """Build filter array for ranked keywords API.

    Args:
        min_volume: Minimum search volume
        max_volume: Maximum search volume
        min_position: Minimum position
        max_position: Maximum position

    Returns:
        Filter array or None if no filters
    """
    filters = []

    if min_volume is not None:
        filters.append(["keyword_data.keyword_info.search_volume", ">=", min_volume])

    if max_volume is not None:
        filters.append(["keyword_data.keyword_info.search_volume", "<=", max_volume])

    if min_position is not None:
        filters.append(["ranked_serp_element.serp_item.rank_group", ">=", min_position])

    if max_position is not None:
        filters.append(["ranked_serp_element.serp_item.rank_group", "<=", max_position])

    if not filters:
        return None

    if len(filters) == 1:
        return filters[0]

    # Combine multiple filters with "and"
    result = []
    for i, f in enumerate(filters):
        if i > 0:
            result.append("and")
        result.append(f)
    return result


def _apply_google_ads_rate_limit() -> None:
    """Apply rate limiting for Google Ads endpoints (12 req/min)."""
    global _last_google_ads_request_time, _google_ads_request_count

    current_time = time.time()

    # Reset counter if window has passed
    if current_time - _last_google_ads_request_time > GOOGLE_ADS_RATE_LIMIT_WINDOW:
        _google_ads_request_count = 0
        _last_google_ads_request_time = current_time

    # Check if we need to wait
    if _google_ads_request_count >= GOOGLE_ADS_RATE_LIMIT:
        # Calculate wait time
        elapsed = current_time - _last_google_ads_request_time
        wait_time = GOOGLE_ADS_RATE_LIMIT_WINDOW - elapsed
        if wait_time > 0:
            time.sleep(wait_time)
        _google_ads_request_count = 0
        _last_google_ads_request_time = time.time()

    _google_ads_request_count += 1


def _get_difficulty_level(kd: int) -> tuple[str, str]:
    """Get difficulty level and color for a keyword difficulty score.

    Args:
        kd: Keyword difficulty score (0-100)

    Returns:
        Tuple of (level name, color)
    """
    if kd <= 29:
        return ("Easy", "green")
    elif kd <= 49:
        return ("Medium", "yellow")
    elif kd <= 69:
        return ("Hard", "orange")
    else:
        return ("Very Hard", "red")


def _format_difficulty_bar(kd: int, width: int = 10) -> str:
    """Format a visual difficulty bar.

    Args:
        kd: Keyword difficulty score
        width: Width of the bar

    Returns:
        Visual bar string
    """
    filled = int((kd / 100) * width)
    bar = "█" * filled + "░" * (width - filled)
    return bar


@keywords_app.command("volume")
def keywords_volume(
    keywords: list[str] = typer.Argument(None, help="Keywords to analyze (max 700)"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    include_serp_info: bool = typer.Option(False, "--include-serp-info", help="Include SERP data"),
    from_file: str = typer.Option(None, "--from-file", "-f", help="Read keywords from file"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option(None, "--output", "-o", help="Output format (json/table/csv)"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get keyword volume, CPC, competition, KD and search intent."""
    defaults = _get_defaults()

    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    # Load keywords
    try:
        keyword_list = load_keywords(keywords, from_file)
    except typer.Exit:
        raise

    if not keyword_list:
        print_error("No keywords provided")
        raise typer.Exit(code=4)

    if len(keyword_list) > 700:
        print_error("Maximum 700 keywords allowed")
        raise typer.Exit(code=4)

    try:
        keyword_list = [validate_keyword(k) for k in keyword_list]
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
        "keywords": keyword_list,
        "location_name": location,
        "language_name": language,
        "include_serp_info": include_serp_info,
    }]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/dataforseo_labs/google/keyword_overview/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)

        if raw_payload:
            data = client._request(
                "POST",
                "/dataforseo_labs/google/keyword_overview/live",
                json_data=raw_payload,
            )
        else:
            data = client._request(
                "POST",
                "/dataforseo_labs/google/keyword_overview/live",
                json_data=payload,
            )

        result = _parse_volume_response(data, keyword_list, location, language)
        client.close()

        if fields_list:
            result = filter_fields(result, fields_list)
        formatted = _format_volume_output(result, output_format)
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


def _parse_volume_response(
    data: dict[str, Any],
    keywords: list[str],
    location: str,
    language: str,
) -> dict[str, Any]:
    """Parse keyword overview API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    results = []
    cost = api_response.cost or 0.0

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        items = task_result.get("items", [])

        for item in items:
            keyword_data = item.get("keyword_data", {})
            keyword_info = keyword_data.get("keyword_info", {})
            serp_info = item.get("serp_info", {})

            result_item = {
                "keyword": item.get("keyword", ""),
                "search_volume": keyword_info.get("search_volume", 0),
                "cpc": keyword_info.get("cpc", 0.0),
                "competition": keyword_info.get("competition", 0.0),
                "competition_level": keyword_info.get("competition_level", ""),
                "keyword_difficulty": item.get("keyword_properties", {}).get("keyword_difficulty", 0),
                "search_intent": keyword_data.get("search_intent_info", {}),
                "monthly_searches": keyword_info.get("monthly_searches", []),
                "serp_info": {
                    "serp_count": serp_info.get("serp_count", 0),
                    "features": serp_info.get("features", []),
                } if serp_info else None,
            }
            results.append(result_item)

    return {
        "keywords_count": len(keywords),
        "location": location,
        "language": language,
        "results": results,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _format_volume_output(result: dict[str, Any], output_format: str) -> str:
    """Format volume command output."""
    if output_format == "json":
        return format_output(result, "json")
    elif output_format == "json-pretty":
        return format_output(result, "json-pretty")
    elif output_format == "csv":
        return _format_volume_csv(result)
    else:  # table
        return _format_volume_table(result)


def _format_volume_table(result: dict[str, Any]) -> str:
    """Format volume results as table."""
    from rich.console import Console
    from rich.table import Table

    console = Console(force_terminal=True)
    output_lines = []

    location = result.get("location", "")
    language = result.get("language", "")
    count = result.get("keywords_count", 0)

    output_lines.append(f"  Location: {location} | Language: {language} | Keywords: {count}")
    output_lines.append("")

    results = result.get("results", [])
    if results:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Keyword", style="white", min_width=20)
        table.add_column("Volume", style="cyan", justify="right")
        table.add_column("CPC", style="green", justify="right")
        table.add_column("Comp", style="yellow")
        table.add_column("KD", style="magenta", justify="right")
        table.add_column("Intent", style="blue")

        for item in results:
            comp_level = item.get("competition_level", "")
            comp_short = {
                "HIGH": "HIGH",
                "MEDIUM": "MED",
                "LOW": "LOW",
            }.get(comp_level, comp_level)

            intent_info = item.get("search_intent", {})
            intent = intent_info.get("main_intent", "-") if intent_info else "-"

            cpc = item.get("cpc", 0.0)
            cpc_str = f"${cpc:.2f}" if cpc else "-"

            table.add_row(
                item.get("keyword", "")[:30],
                f"{item.get('search_volume', 0):,}",
                cpc_str,
                comp_short,
                str(item.get("keyword_difficulty", "-")),
                intent,
            )

        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

    cost = result.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_volume_csv(result: dict[str, Any]) -> str:
    """Format volume results as CSV."""
    import csv
    import io

    output = io.StringIO()
    results = result.get("results", [])

    if results:
        writer = csv.DictWriter(
            output,
            fieldnames=["keyword", "search_volume", "cpc", "competition", "competition_level", "keyword_difficulty", "search_intent"],
            extrasaction="ignore",
        )
        writer.writeheader()
        for item in results:
            row = {
                "keyword": item.get("keyword", ""),
                "search_volume": item.get("search_volume", 0),
                "cpc": item.get("cpc", 0.0),
                "competition": item.get("competition", 0.0),
                "competition_level": item.get("competition_level", ""),
                "keyword_difficulty": item.get("keyword_difficulty", 0),
                "search_intent": item.get("search_intent", {}).get("main_intent", "") if item.get("search_intent") else "",
            }
            writer.writerow(row)

    return output.getvalue()


@keywords_app.command("suggestions")
def keywords_suggestions(
    keyword: str = typer.Argument(..., help="Seed keyword"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    limit: int = typer.Option(50, "--limit", "-n", help="Max results (max 1000)"),
    min_volume: int = typer.Option(None, "--min-volume", help="Minimum search volume"),
    max_volume: int = typer.Option(None, "--max-volume", help="Maximum search volume"),
    min_difficulty: int = typer.Option(None, "--min-difficulty", help="Minimum keyword difficulty"),
    max_difficulty: int = typer.Option(None, "--max-difficulty", help="Maximum keyword difficulty"),
    include_seed: bool = typer.Option(False, "--include-seed", help="Include seed keyword"),
    sort: str = typer.Option("relevance", "--sort", help="Sort by (relevance/volume/cpc/difficulty)"),
    order: str = typer.Option("desc", "--order", help="Sort order (asc/desc)"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get keyword suggestions (long-tail containing seed)."""
    defaults = _get_defaults()

    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if sort not in VALID_SORT_FIELDS:
        print_error(f"Invalid sort field: {sort}")
        raise typer.Exit(code=4)

    if order not in VALID_ORDERS:
        print_error(f"Invalid order: {order}")
        raise typer.Exit(code=4)

    if limit > 1000:
        print_error("Maximum limit is 1000")
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
        "location_name": location,
        "language_name": language,
        "include_seed_keyword": include_seed,
        "include_serp_info": True,
        "limit": limit,
        "filters": build_filters(min_volume, max_volume, min_difficulty, max_difficulty),
        "order_by": build_order_by(sort, order),
    }]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/dataforseo_labs/google/keyword_suggestions/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)

        if raw_payload:
            data = client._request(
                "POST",
                "/dataforseo_labs/google/keyword_suggestions/live",
                json_data=raw_payload,
            )
        else:
            data = client._request(
                "POST",
                "/dataforseo_labs/google/keyword_suggestions/live",
                json_data=payload,
            )

        result = _parse_suggestions_response(data, keyword, location, language)
        client.close()

        if fields_list:
            result = filter_fields(result, fields_list)
        formatted = _format_suggestions_output(result, output_format)
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


def _parse_suggestions_response(
    data: dict[str, Any],
    seed_keyword: str,
    location: str,
    language: str,
) -> dict[str, Any]:
    """Parse keyword suggestions API response."""
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
            keyword_data = item.get("keyword_data", {})
            keyword_info = keyword_data.get("keyword_info", {})

            result_item = {
                "keyword": item.get("keyword", ""),
                "search_volume": keyword_info.get("search_volume", 0),
                "cpc": keyword_info.get("cpc", 0.0),
                "competition": keyword_info.get("competition", 0.0),
                "keyword_difficulty": item.get("keyword_properties", {}).get("keyword_difficulty", 0),
                "search_intent": keyword_data.get("search_intent_info", {}).get("main_intent", ""),
                "monthly_searches": keyword_info.get("monthly_searches", []),
            }
            results.append(result_item)

    return {
        "seed_keyword": seed_keyword,
        "location": location,
        "language": language,
        "total_count": total_count,
        "returned_count": len(results),
        "results": results,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _format_suggestions_output(result: dict[str, Any], output_format: str) -> str:
    """Format suggestions command output."""
    if output_format in ("json", "json-pretty"):
        return format_output(result, output_format)
    elif output_format == "csv":
        return _format_suggestions_csv(result)
    else:
        return _format_suggestions_table(result)


def _format_suggestions_table(result: dict[str, Any]) -> str:
    """Format suggestions as table."""
    from rich.console import Console
    from rich.table import Table

    console = Console(force_terminal=True)
    output_lines = []

    seed = result.get("seed_keyword", "")
    location = result.get("location", "")
    returned = result.get("returned_count", 0)
    total = result.get("total_count", 0)

    output_lines.append(f"  Seed: {seed} | Location: {location} | Showing: {returned} of {total:,}")
    output_lines.append("")

    results = result.get("results", [])
    if results:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Keyword", style="white", min_width=25)
        table.add_column("Volume", style="cyan", justify="right")
        table.add_column("CPC", style="green", justify="right")
        table.add_column("KD", style="magenta", justify="right")
        table.add_column("Intent", style="blue")

        for item in results:
            cpc = item.get("cpc", 0.0)
            cpc_str = f"${cpc:.2f}" if cpc else "-"

            table.add_row(
                item.get("keyword", "")[:40],
                f"{item.get('search_volume', 0):,}",
                cpc_str,
                str(item.get("keyword_difficulty", "-")),
                item.get("search_intent", "-") or "-",
            )

        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

    cost = result.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_suggestions_csv(result: dict[str, Any]) -> str:
    """Format suggestions as CSV."""
    import csv
    import io

    output = io.StringIO()
    results = result.get("results", [])

    if results:
        writer = csv.DictWriter(
            output,
            fieldnames=["keyword", "search_volume", "cpc", "competition", "keyword_difficulty", "search_intent"],
            extrasaction="ignore",
        )
        writer.writeheader()
        for item in results:
            writer.writerow(item)

    return output.getvalue()


@keywords_app.command("ideas")
def keywords_ideas(
    keywords: list[str] = typer.Argument(..., help="Seed keywords (max 20)"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    min_volume: int = typer.Option(None, "--min-volume", help="Minimum search volume"),
    max_volume: int = typer.Option(None, "--max-volume", help="Maximum search volume"),
    min_difficulty: int = typer.Option(None, "--min-difficulty", help="Minimum keyword difficulty"),
    max_difficulty: int = typer.Option(None, "--max-difficulty", help="Maximum keyword difficulty"),
    sort: str = typer.Option("relevance", "--sort", help="Sort by"),
    order: str = typer.Option("desc", "--order", help="Sort order"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get keyword ideas (semantically related keywords)."""
    defaults = _get_defaults()

    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if len(keywords) > 20:
        print_error("Maximum 20 seed keywords allowed")
        raise typer.Exit(code=4)

    try:
        kw_list = [validate_keyword(k) for k in keywords]
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
        "keywords": kw_list,
        "location_name": location,
        "language_name": language,
        "include_serp_info": True,
        "limit": limit,
        "filters": build_filters(min_volume, max_volume, min_difficulty, max_difficulty),
        "order_by": build_order_by(sort, order),
        "closely_variants": False,
    }]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/dataforseo_labs/google/keyword_ideas/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)

        if raw_payload:
            data = client._request(
                "POST",
                "/dataforseo_labs/google/keyword_ideas/live",
                json_data=raw_payload,
            )
        else:
            data = client._request(
                "POST",
                "/dataforseo_labs/google/keyword_ideas/live",
                json_data=payload,
            )

        result = _parse_suggestions_response(data, ", ".join(kw_list), location, language)
        client.close()

        if fields_list:
            result = filter_fields(result, fields_list)
        formatted = _format_suggestions_output(result, output_format)
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


@keywords_app.command("difficulty")
def keywords_difficulty(
    keywords: list[str] = typer.Argument(None, help="Keywords to analyze (max 1000)"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    from_file: str = typer.Option(None, "--from-file", "-f", help="Read keywords from file"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get keyword difficulty for up to 1000 keywords."""
    defaults = _get_defaults()

    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        keyword_list = load_keywords(keywords, from_file)
    except typer.Exit:
        raise

    if not keyword_list:
        print_error("No keywords provided")
        raise typer.Exit(code=4)

    if len(keyword_list) > 1000:
        print_error("Maximum 1000 keywords allowed")
        raise typer.Exit(code=4)

    try:
        keyword_list = [validate_keyword(k) for k in keyword_list]
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
        "keywords": keyword_list,
        "location_name": location,
        "language_name": language,
    }]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/dataforseo_labs/google/bulk_keyword_difficulty/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)

        data = client._request(
            "POST",
            "/dataforseo_labs/google/bulk_keyword_difficulty/live",
            json_data=raw_payload or payload,
        )

        result = _parse_difficulty_response(data, keyword_list, location, language)
        client.close()

        if fields_list:
            result = filter_fields(result, fields_list)
        formatted = _format_difficulty_output(result, output_format)
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


def _parse_difficulty_response(
    data: dict[str, Any],
    keywords: list[str],
    location: str,
    language: str,
) -> dict[str, Any]:
    """Parse bulk keyword difficulty API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    results = []
    cost = api_response.cost or 0.0

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        items = task_result.get("items", [])

        for item in items:
            result_item = {
                "keyword": item.get("keyword", ""),
                "keyword_difficulty": item.get("keyword_difficulty", 0),
            }
            results.append(result_item)

    return {
        "keywords_count": len(keywords),
        "location": location,
        "language": language,
        "results": results,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _format_difficulty_output(result: dict[str, Any], output_format: str) -> str:
    """Format difficulty command output."""
    if output_format in ("json", "json-pretty"):
        return format_output(result, output_format)
    elif output_format == "csv":
        return _format_difficulty_csv(result)
    else:
        return _format_difficulty_table(result)


def _format_difficulty_table(result: dict[str, Any]) -> str:
    """Format difficulty results as table with visual indicators."""
    from rich.console import Console
    from rich.table import Table

    console = Console(force_terminal=True)
    output_lines = []

    location = result.get("location", "")
    count = result.get("keywords_count", 0)

    output_lines.append(f"  Location: {location} | Keywords: {count}")
    output_lines.append("")

    results = result.get("results", [])
    if results:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Keyword", style="white", min_width=20)
        table.add_column("KD", style="cyan", justify="right")
        table.add_column("Level", style="white", min_width=20)

        for item in results:
            kd = item.get("keyword_difficulty", 0)
            level, color = _get_difficulty_level(kd)
            bar = _format_difficulty_bar(kd)

            table.add_row(
                item.get("keyword", "")[:30],
                str(kd),
                f"[{color}]{bar} {level}[/{color}]",
            )

        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

    cost = result.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_difficulty_csv(result: dict[str, Any]) -> str:
    """Format difficulty results as CSV."""
    import csv
    import io

    output = io.StringIO()
    results = result.get("results", [])

    if results:
        writer = csv.DictWriter(
            output,
            fieldnames=["keyword", "keyword_difficulty", "level"],
            extrasaction="ignore",
        )
        writer.writeheader()
        for item in results:
            kd = item.get("keyword_difficulty", 0)
            level, _ = _get_difficulty_level(kd)
            row = {
                "keyword": item.get("keyword", ""),
                "keyword_difficulty": kd,
                "level": level,
            }
            writer.writerow(row)

    return output.getvalue()


@keywords_app.command("search-intent")
def keywords_search_intent(
    keywords: list[str] = typer.Argument(None, help="Keywords to classify (max 1000)"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    from_file: str = typer.Option(None, "--from-file", "-f", help="Read keywords from file"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Classify search intent for keywords."""
    defaults = _get_defaults()

    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        keyword_list = load_keywords(keywords, from_file)
    except typer.Exit:
        raise

    if not keyword_list:
        print_error("No keywords provided")
        raise typer.Exit(code=4)

    if len(keyword_list) > 1000:
        print_error("Maximum 1000 keywords allowed")
        raise typer.Exit(code=4)

    try:
        keyword_list = [validate_keyword(k) for k in keyword_list]
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
        "keywords": keyword_list,
        "location_name": location,
        "language_name": language,
    }]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/dataforseo_labs/google/search_intent/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)

        data = client._request(
            "POST",
            "/dataforseo_labs/google/search_intent/live",
            json_data=raw_payload or payload,
        )

        result = _parse_search_intent_response(data, keyword_list, location, language)
        client.close()

        if fields_list:
            result = filter_fields(result, fields_list)
        formatted = _format_search_intent_output(result, output_format)
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


def _parse_search_intent_response(
    data: dict[str, Any],
    keywords: list[str],
    location: str,
    language: str,
) -> dict[str, Any]:
    """Parse search intent API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    results = []
    cost = api_response.cost or 0.0

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        items = task_result.get("items", [])

        for item in items:
            result_item = {
                "keyword": item.get("keyword", ""),
                "main_intent": item.get("main_intent", ""),
                "foreign_intents": item.get("foreign_intents", []),
                "probability": item.get("probability", 0.0),
            }
            results.append(result_item)

    return {
        "keywords_count": len(keywords),
        "location": location,
        "language": language,
        "results": results,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _format_search_intent_output(result: dict[str, Any], output_format: str) -> str:
    """Format search intent command output."""
    if output_format in ("json", "json-pretty"):
        return format_output(result, output_format)
    elif output_format == "csv":
        return _format_search_intent_csv(result)
    else:
        return _format_search_intent_table(result)


def _format_search_intent_table(result: dict[str, Any]) -> str:
    """Format search intent as table."""
    from rich.console import Console
    from rich.table import Table

    console = Console(force_terminal=True)
    output_lines = []

    location = result.get("location", "")
    count = result.get("keywords_count", 0)

    output_lines.append(f"  Location: {location} | Keywords: {count}")
    output_lines.append("")

    results = result.get("results", [])
    if results:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Keyword", style="white", min_width=25)
        table.add_column("Main Intent", style="cyan")
        table.add_column("Probability", style="green", justify="right")
        table.add_column("Other Intents", style="blue")

        for item in results:
            foreign = item.get("foreign_intents", [])
            foreign_str = ", ".join(foreign) if foreign else "-"

            table.add_row(
                item.get("keyword", "")[:35],
                item.get("main_intent", "-"),
                f"{item.get('probability', 0):.0%}",
                foreign_str[:25],
            )

        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

    cost = result.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_search_intent_csv(result: dict[str, Any]) -> str:
    """Format search intent as CSV."""
    import csv
    import io

    output = io.StringIO()
    results = result.get("results", [])

    if results:
        writer = csv.DictWriter(
            output,
            fieldnames=["keyword", "main_intent", "probability", "foreign_intents"],
            extrasaction="ignore",
        )
        writer.writeheader()
        for item in results:
            row = {
                "keyword": item.get("keyword", ""),
                "main_intent": item.get("main_intent", ""),
                "probability": item.get("probability", 0.0),
                "foreign_intents": ", ".join(item.get("foreign_intents", [])),
            }
            writer.writerow(row)

    return output.getvalue()


@keywords_app.command("for-site")
def keywords_for_site(
    target: str = typer.Argument(..., help="Target domain (e.g., example.com)"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    min_volume: int = typer.Option(None, "--min-volume", help="Minimum search volume"),
    max_volume: int = typer.Option(None, "--max-volume", help="Maximum search volume"),
    sort: str = typer.Option("relevance", "--sort", help="Sort by"),
    order: str = typer.Option("desc", "--order", help="Sort order"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Find keywords relevant for a domain."""
    defaults = _get_defaults()
    from dfseo.validation import validate_target

    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        target = validate_target(target)
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
        "target": target,
        "location_name": location,
        "language_name": language,
        "include_serp_info": True,
        "limit": limit,
        "filters": build_filters(min_volume, max_volume),
        "order_by": build_order_by(sort, order),
    }]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/dataforseo_labs/google/keywords_for_site/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)

        data = client._request(
            "POST",
            "/dataforseo_labs/google/keywords_for_site/live",
            json_data=raw_payload or payload,
        )

        result = _parse_for_site_response(data, target, location, language)
        client.close()

        if fields_list:
            result = filter_fields(result, fields_list)
        formatted = _format_for_site_output(result, output_format)
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


def _parse_for_site_response(
    data: dict[str, Any],
    target: str,
    location: str,
    language: str,
) -> dict[str, Any]:
    """Parse keywords for site API response."""
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
            keyword_data = item.get("keyword_data", {})
            keyword_info = keyword_data.get("keyword_info", {})
            serp_info = item.get("serp_info", {})

            result_item = {
                "keyword": item.get("keyword", ""),
                "search_volume": keyword_info.get("search_volume", 0),
                "cpc": keyword_info.get("cpc", 0.0),
                "competition": keyword_info.get("competition", 0.0),
                "keyword_difficulty": item.get("keyword_properties", {}).get("keyword_difficulty", 0),
                "search_intent": keyword_data.get("search_intent_info", {}).get("main_intent", ""),
                "serp_info": {
                    "serp_count": serp_info.get("serp_count", 0),
                    "features": serp_info.get("features", []),
                } if serp_info else None,
            }
            results.append(result_item)

    return {
        "target": target,
        "location": location,
        "language": language,
        "total_count": total_count,
        "returned_count": len(results),
        "results": results,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _format_for_site_output(result: dict[str, Any], output_format: str) -> str:
    """Format for-site command output."""
    if output_format in ("json", "json-pretty"):
        return format_output(result, output_format)
    elif output_format == "csv":
        return _format_for_site_csv(result)
    else:
        return _format_for_site_table(result)


def _format_for_site_table(result: dict[str, Any]) -> str:
    """Format for-site results as table."""
    from rich.console import Console
    from rich.table import Table

    console = Console(force_terminal=True)
    output_lines = []

    target = result.get("target", "")
    location = result.get("location", "")
    returned = result.get("returned_count", 0)
    total = result.get("total_count", 0)

    output_lines.append(f"  Target: {target} | Location: {location} | Showing: {returned} of {total:,}")
    output_lines.append("")

    results = result.get("results", [])
    if results:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Keyword", style="white", min_width=25)
        table.add_column("Volume", style="cyan", justify="right")
        table.add_column("CPC", style="green", justify="right")
        table.add_column("KD", style="magenta", justify="right")
        table.add_column("Intent", style="blue")

        for item in results:
            cpc = item.get("cpc", 0.0)
            cpc_str = f"${cpc:.2f}" if cpc else "-"

            table.add_row(
                item.get("keyword", "")[:35],
                f"{item.get('search_volume', 0):,}",
                cpc_str,
                str(item.get("keyword_difficulty", "-")),
                item.get("search_intent", "-") or "-",
            )

        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

    cost = result.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_for_site_csv(result: dict[str, Any]) -> str:
    """Format for-site results as CSV."""
    import csv
    import io

    output = io.StringIO()
    results = result.get("results", [])

    if results:
        writer = csv.DictWriter(
            output,
            fieldnames=["keyword", "search_volume", "cpc", "competition", "keyword_difficulty", "search_intent"],
            extrasaction="ignore",
        )
        writer.writeheader()
        for item in results:
            writer.writerow(item)

    return output.getvalue()


@keywords_app.command("ads-volume")
def keywords_ads_volume(
    keywords: list[str] = typer.Argument(None, help="Keywords to analyze (max 20)"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    date_from: str = typer.Option(None, "--date-from", help="Start date (YYYY-MM)"),
    date_to: str = typer.Option(None, "--date-to", help="End date (YYYY-MM)"),
    from_file: str = typer.Option(None, "--from-file", "-f", help="Read keywords from file"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get Google Ads search volume data (pure Google Ads data)."""
    defaults = _get_defaults()

    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        keyword_list = load_keywords(keywords, from_file)
    except typer.Exit:
        raise

    if not keyword_list:
        print_error("No keywords provided")
        raise typer.Exit(code=4)

    if len(keyword_list) > 20:
        print_error("Maximum 20 keywords allowed for Google Ads")
        raise typer.Exit(code=4)

    try:
        keyword_list = [validate_keyword(k) for k in keyword_list]
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
        "keywords": keyword_list,
        "location_name": location,
        "language_name": language,
    }]
    if date_from:
        payload[0]["date_from"] = date_from
    if date_to:
        payload[0]["date_to"] = date_to

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/keywords_data/google_ads/search_volume/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)
        _apply_google_ads_rate_limit()

        data = client._request(
            "POST",
            "/keywords_data/google_ads/search_volume/live",
            json_data=raw_payload or payload,
        )

        result = _parse_ads_volume_response(data, keyword_list, location, language)
        client.close()

        if fields_list:
            result = filter_fields(result, fields_list)
        formatted = _format_ads_volume_output(result, output_format)
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


def _parse_ads_volume_response(
    data: dict[str, Any],
    keywords: list[str],
    location: str,
    language: str,
) -> dict[str, Any]:
    """Parse Google Ads search volume API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    results = []
    cost = api_response.cost or 0.0

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        items = task_result.get("items", [])

        for item in items:
            result_item = {
                "keyword": item.get("keyword", ""),
                "search_volume": item.get("search_volume", 0),
                "cpc": item.get("cpc", 0.0),
                "competition": item.get("competition", 0.0),
                "competition_level": item.get("competition_level", ""),
                "monthly_searches": item.get("monthly_searches", []),
            }
            results.append(result_item)

    return {
        "keywords_count": len(keywords),
        "location": location,
        "language": language,
        "results": results,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _format_ads_volume_output(result: dict[str, Any], output_format: str) -> str:
    """Format ads-volume command output."""
    if output_format in ("json", "json-pretty"):
        return format_output(result, output_format)
    elif output_format == "csv":
        return _format_ads_volume_csv(result)
    else:
        return _format_ads_volume_table(result)


def _format_ads_volume_table(result: dict[str, Any]) -> str:
    """Format ads-volume results as table."""
    from rich.console import Console
    from rich.table import Table

    console = Console(force_terminal=True)
    output_lines = []

    location = result.get("location", "")
    language = result.get("language", "")
    count = result.get("keywords_count", 0)

    output_lines.append(f"  Google Ads Data | Location: {location} | Language: {language} | Keywords: {count}")
    output_lines.append("")

    results = result.get("results", [])
    if results:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Keyword", style="white", min_width=20)
        table.add_column("Volume", style="cyan", justify="right")
        table.add_column("CPC", style="green", justify="right")
        table.add_column("Competition", style="yellow")

        for item in results:
            comp_level = item.get("competition_level", "")
            cpc = item.get("cpc", 0.0)
            cpc_str = f"${cpc:.2f}" if cpc else "-"

            table.add_row(
                item.get("keyword", "")[:30],
                f"{item.get('search_volume', 0):,}",
                cpc_str,
                comp_level or "-",
            )

        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

    cost = result.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_ads_volume_csv(result: dict[str, Any]) -> str:
    """Format ads-volume results as CSV."""
    import csv
    import io

    output = io.StringIO()
    results = result.get("results", [])

    if results:
        writer = csv.DictWriter(
            output,
            fieldnames=["keyword", "search_volume", "cpc", "competition", "competition_level"],
            extrasaction="ignore",
        )
        writer.writeheader()
        for item in results:
            writer.writerow(item)

    return output.getvalue()


@keywords_app.command("ads-suggestions")
def keywords_ads_suggestions(
    keywords: list[str] = typer.Argument(..., help="Seed keywords (max 20)"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get keyword suggestions from Google Ads."""
    defaults = _get_defaults()

    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if len(keywords) > 20:
        print_error("Maximum 20 seed keywords allowed for Google Ads")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        # Apply Google Ads rate limiting
        _apply_google_ads_rate_limit()

        payload = [{
            "keywords": keywords,
            "location_name": location,
            "language_name": language,
            "limit": limit,
        }]

        data = client._request(
            "POST",
            "/keywords_data/google_ads/keywords_for_keywords/live",
            json_data=payload,
        )

        result = _parse_ads_suggestions_response(data, keywords, location, language)
        client.close()

        formatted = _format_ads_suggestions_output(result, output_format)
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


def _parse_ads_suggestions_response(
    data: dict[str, Any],
    keywords: list[str],
    location: str,
    language: str,
) -> dict[str, Any]:
    """Parse Google Ads keyword suggestions API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    results = []
    cost = api_response.cost or 0.0

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        items = task_result.get("items", [])

        for item in items:
            result_item = {
                "keyword": item.get("keyword", ""),
                "search_volume": item.get("search_volume", 0),
                "cpc": item.get("cpc", 0.0),
                "competition": item.get("competition", 0.0),
                "competition_level": item.get("competition_level", ""),
            }
            results.append(result_item)

    return {
        "seed_keywords": keywords,
        "location": location,
        "language": language,
        "results_count": len(results),
        "results": results,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _format_ads_suggestions_output(result: dict[str, Any], output_format: str) -> str:
    """Format ads-suggestions command output."""
    if output_format in ("json", "json-pretty"):
        return format_output(result, output_format)
    elif output_format == "csv":
        return _format_ads_suggestions_csv(result)
    else:
        return _format_ads_suggestions_table(result)


def _format_ads_suggestions_table(result: dict[str, Any]) -> str:
    """Format ads-suggestions results as table."""
    from rich.console import Console
    from rich.table import Table

    console = Console(force_terminal=True)
    output_lines = []

    seeds = result.get("seed_keywords", [])
    location = result.get("location", "")
    count = result.get("results_count", 0)

    output_lines.append(f"  Google Ads Suggestions | Seeds: {len(seeds)} | Location: {location} | Results: {count}")
    output_lines.append("")

    results = result.get("results", [])
    if results:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Keyword", style="white", min_width=25)
        table.add_column("Volume", style="cyan", justify="right")
        table.add_column("CPC", style="green", justify="right")
        table.add_column("Competition", style="yellow")

        for item in results[:100]:  # Limit to 100 for display
            comp_level = item.get("competition_level", "")
            cpc = item.get("cpc", 0.0)
            cpc_str = f"${cpc:.2f}" if cpc else "-"

            table.add_row(
                item.get("keyword", "")[:35],
                f"{item.get('search_volume', 0):,}",
                cpc_str,
                comp_level or "-",
            )

        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

        if len(results) > 100:
            output_lines.append(f"\n  ... and {len(results) - 100} more results")

    cost = result.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_ads_suggestions_csv(result: dict[str, Any]) -> str:
    """Format ads-suggestions results as CSV."""
    import csv
    import io

    output = io.StringIO()
    results = result.get("results", [])

    if results:
        writer = csv.DictWriter(
            output,
            fieldnames=["keyword", "search_volume", "cpc", "competition", "competition_level"],
            extrasaction="ignore",
        )
        writer.writeheader()
        for item in results:
            writer.writerow(item)

    return output.getvalue()


# ---------------------------------------------------------------------------
# Labs competitive intelligence commands
# ---------------------------------------------------------------------------


VALID_RANKED_SORT_FIELDS = ["relevance", "volume", "position", "traffic"]


def _labs_target_command(
    target: str,
    endpoint: str,
    location: str | None,
    language: str | None,
    limit: int,
    fields: str | None,
    raw_params: str | None,
    dry_run: bool,
    output: str,
    login: str | None,
    password: str | None,
    verbose: bool,
    extra_payload: dict[str, Any] | None = None,
) -> None:
    """Generic handler for Labs target-based commands."""
    from dfseo.validation import validate_target

    defaults = _get_defaults()
    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        target = validate_target(target)
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
        "target": target,
        "location_name": location,
        "language_name": language,
        "limit": limit,
    }]
    if extra_payload:
        payload[0].update(extra_payload)

    if dry_run:
        result = format_dry_run_output(
            endpoint=f"POST /v3/{endpoint}",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)
        data = client._request("POST", f"/{endpoint}", json_data=raw_payload or payload)
        client.close()

        from dfseo.models import ApiResponse
        api_response = ApiResponse.model_validate(data)
        cost = api_response.cost or 0.0

        items = []
        total_count = 0
        if api_response.tasks and api_response.tasks[0].result:
            task_result = api_response.tasks[0].result[0]
            total_count = task_result.get("total_count", 0)
            items = task_result.get("items", [])

        result = {
            "target": target,
            "location": location,
            "language": language,
            "total_count": total_count,
            "returned_count": len(items),
            "items": items,
            "cost": cost,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

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


@keywords_app.command("ranked-keywords")
def keywords_ranked_keywords(
    target: str = typer.Argument(..., help="Domain to analyze (e.g., example.com)"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    min_volume: int = typer.Option(None, "--min-volume", help="Minimum search volume"),
    max_volume: int = typer.Option(None, "--max-volume", help="Maximum search volume"),
    min_position: int = typer.Option(None, "--min-position", help="Minimum SERP position"),
    max_position: int = typer.Option(None, "--max-position", help="Maximum SERP position"),
    sort: str = typer.Option("relevance", "--sort", help="Sort by (relevance/volume/position/traffic)"),
    order: str = typer.Option("desc", "--order", help="Sort order (asc/desc)"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get all keywords a domain currently ranks for."""
    from dfseo.validation import validate_target

    defaults = _get_defaults()
    loc = location or defaults["location_name"]
    lang = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if sort not in VALID_RANKED_SORT_FIELDS:
        print_error(f"Invalid sort field: {sort}")
        raise typer.Exit(code=4)

    try:
        target = validate_target(target)
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

    filters = build_ranked_filters(min_volume, max_volume, min_position, max_position)

    payload = [{
        "target": target,
        "location_name": loc,
        "language_name": lang,
        "limit": limit,
    }]
    if filters:
        payload[0]["filters"] = filters
    if sort != "relevance":
        payload[0]["order_by"] = build_labs_order_by(sort, order)

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/dataforseo_labs/google/ranked_keywords/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)
        data = client._request(
            "POST",
            "/dataforseo_labs/google/ranked_keywords/live",
            json_data=raw_payload or payload,
        )
        client.close()

        result = _parse_ranked_keywords_response(data, target, loc, lang)

        if fields_list:
            result = filter_fields(result, fields_list)
        formatted = _format_ranked_keywords_output(result, output_format)
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


def _parse_ranked_keywords_response(
    data: dict[str, Any], target: str, location: str, language: str
) -> dict[str, Any]:
    """Parse ranked keywords API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    results = []
    total_count = 0
    cost = api_response.cost or 0.0

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        total_count = task_result.get("total_count", 0)

        for item in task_result.get("items", []):
            kd = item.get("keyword_data", {})
            ki = kd.get("keyword_info", {})
            rse = item.get("ranked_serp_element", {})
            si = rse.get("serp_item", {})

            results.append({
                "keyword": kd.get("keyword", ""),
                "position": si.get("rank_group", 0),
                "url": si.get("relative_url", "") or si.get("url", ""),
                "search_volume": ki.get("search_volume", 0),
                "cpc": ki.get("cpc", 0.0),
                "keyword_difficulty": kd.get("keyword_properties", {}).get("keyword_difficulty", 0),
                "etv": si.get("etv", 0),
                "search_intent": kd.get("search_intent_info", {}).get("main_intent", ""),
            })

    return {
        "target": target,
        "location": location,
        "language": language,
        "total_count": total_count,
        "returned_count": len(results),
        "results": results,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _format_ranked_keywords_output(result: dict[str, Any], output_format: str) -> str:
    """Format ranked keywords output."""
    if output_format in ("json", "json-pretty"):
        return format_output(result, output_format)
    elif output_format == "csv":
        import csv
        import io
        out = io.StringIO()
        results = result.get("results", [])
        if results:
            writer = csv.DictWriter(
                out,
                fieldnames=["keyword", "position", "url", "search_volume", "cpc", "keyword_difficulty", "etv", "search_intent"],
                extrasaction="ignore",
            )
            writer.writeheader()
            for item in results:
                writer.writerow(item)
        return out.getvalue()
    else:
        return _format_ranked_keywords_table(result)


def _format_ranked_keywords_table(result: dict[str, Any]) -> str:
    """Format ranked keywords as table."""
    from rich.console import Console
    from rich.table import Table

    console = Console(force_terminal=True)
    output_lines = []

    target = result.get("target", "")
    total = result.get("total_count", 0)
    returned = result.get("returned_count", 0)

    output_lines.append(f"  Ranked Keywords: {target} | Showing {returned} of {total:,}")
    output_lines.append("")

    results = result.get("results", [])
    if results:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Keyword", style="white", min_width=20)
        table.add_column("Pos", style="cyan", justify="right")
        table.add_column("URL", style="blue")
        table.add_column("Volume", style="green", justify="right")
        table.add_column("KD", style="magenta", justify="right")
        table.add_column("ETV", style="yellow", justify="right")
        table.add_column("Intent", style="dim")

        for item in results:
            table.add_row(
                item.get("keyword", "")[:25],
                str(item.get("position", "-")),
                item.get("url", "")[:35],
                f"{item.get('search_volume', 0):,}",
                str(item.get("keyword_difficulty", "-")),
                str(item.get("etv", 0)),
                item.get("search_intent", "-") or "-",
            )

        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

    cost = result.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


@keywords_app.command("domain-rank")
def keywords_domain_rank(
    target: str = typer.Argument(..., help="Domain to analyze"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get domain rank overview with traffic and position metrics."""
    _labs_target_command(
        target, "dataforseo_labs/google/domain_rank_overview/live",
        location, language, 1, fields, raw_params, dry_run, output, login, password, verbose,
    )


@keywords_app.command("historical-rank")
def keywords_historical_rank(
    target: str = typer.Argument(..., help="Domain to analyze"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """View historical domain ranking trends over time."""
    _labs_target_command(
        target, "dataforseo_labs/google/historical_rank_overview/live",
        location, language, 100, fields, raw_params, dry_run, output, login, password, verbose,
    )


@keywords_app.command("historical-volume")
def keywords_historical_volume(
    keywords: list[str] = typer.Argument(None, help="Keywords to analyze"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    from_file: str = typer.Option(None, "--from-file", "-f", help="Read keywords from file"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get historical search volume trends for keywords."""
    defaults = _get_defaults()
    loc = location or defaults["location_name"]
    lang = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        keyword_list = load_keywords(keywords, from_file)
    except typer.Exit:
        raise

    if not keyword_list:
        print_error("No keywords provided")
        raise typer.Exit(code=4)

    try:
        keyword_list = [validate_keyword(k) for k in keyword_list]
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

    payload = [{"keywords": keyword_list, "location_name": loc, "language_name": lang}]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/dataforseo_labs/google/historical_search_volume/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)
        data = client._request("POST", "/dataforseo_labs/google/historical_search_volume/live", json_data=raw_payload or payload)
        client.close()

        from dfseo.models import ApiResponse
        api_response = ApiResponse.model_validate(data)
        cost = api_response.cost or 0.0
        items = []
        if api_response.tasks and api_response.tasks[0].result:
            items = api_response.tasks[0].result[0].get("items", [])

        result = {"keywords_count": len(keyword_list), "location": loc, "language": lang, "items": items, "cost": cost, "timestamp": datetime.now(timezone.utc).isoformat()}
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


@keywords_app.command("serp-competitors")
def keywords_serp_competitors(
    keywords: list[str] = typer.Argument(None, help="Keywords to analyze"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    limit: int = typer.Option(20, "--limit", "-n", help="Max results"),
    from_file: str = typer.Option(None, "--from-file", "-f", help="Read keywords from file"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Find SERP competitors for given keywords."""
    defaults = _get_defaults()
    loc = location or defaults["location_name"]
    lang = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        keyword_list = load_keywords(keywords, from_file)
    except typer.Exit:
        raise

    if not keyword_list:
        print_error("No keywords provided")
        raise typer.Exit(code=4)

    try:
        keyword_list = [validate_keyword(k) for k in keyword_list]
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

    payload = [{"keywords": keyword_list, "location_name": loc, "language_name": lang, "limit": limit}]

    if dry_run:
        result = format_dry_run_output(endpoint="POST /v3/dataforseo_labs/google/serp_competitors/live", request_body=raw_payload or payload)
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)
        data = client._request("POST", "/dataforseo_labs/google/serp_competitors/live", json_data=raw_payload or payload)
        client.close()

        from dfseo.models import ApiResponse
        api_response = ApiResponse.model_validate(data)
        cost = api_response.cost or 0.0
        items, total_count = [], 0
        if api_response.tasks and api_response.tasks[0].result:
            task_result = api_response.tasks[0].result[0]
            total_count = task_result.get("total_count", 0)
            items = task_result.get("items", [])

        result = {"seed_keywords": keyword_list, "location": loc, "language": lang, "total_count": total_count, "returned_count": len(items), "items": items, "cost": cost, "timestamp": datetime.now(timezone.utc).isoformat()}
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


@keywords_app.command("competitors-domain")
def keywords_competitors_domain(
    target: str = typer.Argument(..., help="Domain to analyze"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    limit: int = typer.Option(20, "--limit", "-n", help="Max results"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Find domains competing for the same keywords."""
    _labs_target_command(
        target, "dataforseo_labs/google/competitors_domain/live",
        location, language, limit, fields, raw_params, dry_run, output, login, password, verbose,
    )


@keywords_app.command("domain-intersection")
def keywords_domain_intersection(
    targets: list[str] = typer.Argument(..., help="Domains to compare (2-20)"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    min_volume: int = typer.Option(None, "--min-volume", help="Minimum search volume"),
    max_volume: int = typer.Option(None, "--max-volume", help="Maximum search volume"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Find keyword overlap between domains (keyword gap analysis)."""
    from dfseo.validation import validate_target

    defaults = _get_defaults()
    loc = location or defaults["location_name"]
    lang = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if len(targets) < 2:
        print_error("At least 2 targets required")
        raise typer.Exit(code=4)
    if len(targets) > 20:
        print_error("Maximum 20 targets allowed")
        raise typer.Exit(code=4)

    try:
        targets = [validate_target(t) for t in targets]
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

    targets_dict = {str(i + 1): t for i, t in enumerate(targets)}
    filters = build_filters(min_volume, max_volume)

    payload = [{"targets": targets_dict, "location_name": loc, "language_name": lang, "limit": limit}]
    if filters:
        payload[0]["filters"] = filters

    if dry_run:
        result = format_dry_run_output(endpoint="POST /v3/dataforseo_labs/google/domain_intersection/live", request_body=raw_payload or payload)
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)
        data = client._request("POST", "/dataforseo_labs/google/domain_intersection/live", json_data=raw_payload or payload)
        client.close()

        from dfseo.models import ApiResponse
        api_response = ApiResponse.model_validate(data)
        cost = api_response.cost or 0.0
        items, total_count = [], 0
        if api_response.tasks and api_response.tasks[0].result:
            task_result = api_response.tasks[0].result[0]
            total_count = task_result.get("total_count", 0)
            items = task_result.get("items", [])

        result = {"targets": targets, "location": loc, "language": lang, "total_count": total_count, "returned_count": len(items), "items": items, "cost": cost, "timestamp": datetime.now(timezone.utc).isoformat()}
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


@keywords_app.command("relevant-pages")
def keywords_relevant_pages(
    target: str = typer.Argument(..., help="Domain to analyze"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Find most relevant pages for a domain with ranking metrics."""
    _labs_target_command(
        target, "dataforseo_labs/google/relevant_pages/live",
        location, language, limit, fields, raw_params, dry_run, output, login, password, verbose,
    )


@keywords_app.command("subdomains")
def keywords_subdomains(
    target: str = typer.Argument(..., help="Domain to analyze"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Analyze subdomains and their ranking metrics."""
    _labs_target_command(
        target, "dataforseo_labs/google/subdomains/live",
        location, language, limit, fields, raw_params, dry_run, output, login, password, verbose,
    )


@keywords_app.command("top-searches")
def keywords_top_searches(
    keyword: str = typer.Argument(..., help="Seed keyword"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get trending/top searches related to a keyword."""
    defaults = _get_defaults()
    loc = location or defaults["location_name"]
    lang = language or defaults["language_name"]
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

    payload = [{"keyword": keyword, "location_name": loc, "language_name": lang, "limit": limit}]

    if dry_run:
        result = format_dry_run_output(endpoint="POST /v3/dataforseo_labs/google/top_searches/live", request_body=raw_payload or payload)
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)
        data = client._request("POST", "/dataforseo_labs/google/top_searches/live", json_data=raw_payload or payload)
        client.close()

        from dfseo.models import ApiResponse
        api_response = ApiResponse.model_validate(data)
        cost = api_response.cost or 0.0
        items, total_count = [], 0
        if api_response.tasks and api_response.tasks[0].result:
            task_result = api_response.tasks[0].result[0]
            total_count = task_result.get("total_count", 0)
            items = task_result.get("items", [])

        result = {"keyword": keyword, "location": loc, "language": lang, "total_count": total_count, "returned_count": len(items), "items": items, "cost": cost, "timestamp": datetime.now(timezone.utc).isoformat()}
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


@keywords_app.command("categories-for-domain")
def keywords_categories_for_domain(
    target: str = typer.Argument(..., help="Domain to analyze"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get topic categories a domain belongs to."""
    _labs_target_command(
        target, "dataforseo_labs/google/categories_for_domain/live",
        location, language, 100, fields, raw_params, dry_run, output, login, password, verbose,
    )


@keywords_app.command("page-intersection")
def keywords_page_intersection(
    pages: list[str] = typer.Argument(..., help="Page URLs to compare (2-20)"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    min_volume: int = typer.Option(None, "--min-volume", help="Minimum search volume"),
    max_volume: int = typer.Option(None, "--max-volume", help="Maximum search volume"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Find keyword overlap between specific pages (page-level gap analysis)."""
    defaults = _get_defaults()
    loc = location or defaults["location_name"]
    lang = language or defaults["language_name"]
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if len(pages) < 2:
        print_error("At least 2 pages required")
        raise typer.Exit(code=4)
    if len(pages) > 20:
        print_error("Maximum 20 pages allowed")
        raise typer.Exit(code=4)

    if raw_params:
        try:
            raw_payload = validate_raw_params(raw_params)
        except ValueError as e:
            print_error(str(e))
            raise typer.Exit(code=4)
    else:
        raw_payload = None

    pages_dict = {str(i + 1): p for i, p in enumerate(pages)}
    filters = build_filters(min_volume, max_volume)

    payload = [{"pages": pages_dict, "location_name": loc, "language_name": lang, "limit": limit}]
    if filters:
        payload[0]["filters"] = filters

    if dry_run:
        result = format_dry_run_output(endpoint="POST /v3/dataforseo_labs/google/page_intersection/live", request_body=raw_payload or payload)
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)
        data = client._request("POST", "/dataforseo_labs/google/page_intersection/live", json_data=raw_payload or payload)
        client.close()

        from dfseo.models import ApiResponse
        api_response = ApiResponse.model_validate(data)
        cost = api_response.cost or 0.0
        items, total_count = [], 0
        if api_response.tasks and api_response.tasks[0].result:
            task_result = api_response.tasks[0].result[0]
            total_count = task_result.get("total_count", 0)
            items = task_result.get("items", [])

        result = {"pages": pages, "location": loc, "language": lang, "total_count": total_count, "returned_count": len(items), "items": items, "cost": cost, "timestamp": datetime.now(timezone.utc).isoformat()}
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
