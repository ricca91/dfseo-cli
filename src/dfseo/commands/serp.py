"""SERP commands for dfseo CLI."""

from typing import Any

import typer

from dfseo.client import AuthenticationError, DataForSeoClient, DataForSeoError, RateLimitError
from dfseo.config import Config
from dfseo.output import (
    filter_fields,
    format_compare,
    format_languages,
    format_locations,
    format_output,
    print_error,
)
from dfseo.pricing import format_dry_run_output
from dfseo.validation import validate_keyword, validate_raw_params

serp_app = typer.Typer(help="SERP API commands")

VALID_DEVICES = ["desktop", "mobile"]
VALID_OS = ["windows", "macos", "ios", "android"]
VALID_OUTPUTS = ["json", "json-pretty", "table", "csv"]


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
        "device": config.get_default("device"),
        "output": config.get_default("output"),
    }


@serp_app.command()
def google(
    keyword: str = typer.Argument(..., help="Search keyword"),
    location: str = typer.Option(None, "--location", "-l", help="Location name (e.g., 'Italy')"),
    language: str = typer.Option(None, "--language", "-L", help="Language name (e.g., 'Italian')"),
    device: str = typer.Option(None, "--device", "-d", help="Device type (desktop/mobile)"),
    os: str = typer.Option(None, "--os", help="Operating system (windows/macos/ios/android)"),
    depth: int = typer.Option(100, "--depth", "-n", help="Number of results (max 700)"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include (e.g., 'rank,domain,title')"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format (json/json-pretty/table/csv, default: auto-detect)"),
    features_only: bool = typer.Option(False, "--features-only", help="Show only SERP features"),
    raw: bool = typer.Option(False, "--raw", help="Output raw API response"),
    login: str = typer.Option(None, "--login", help="DataForSEO login (overrides config)"),
    password: str = typer.Option(None, "--password", help="DataForSEO password (overrides config)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Quiet mode (suppress non-errors)"),
) -> None:
    """Search Google SERP."""
    defaults = _get_defaults()

    # Use defaults if not provided
    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    device = device or defaults["device"]
    output_format = output or defaults["output"]

    # Validate inputs
    try:
        keyword = validate_keyword(keyword)
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(code=4)

    if device not in VALID_DEVICES:
        print_error(f"Invalid device: {device}. Valid: {', '.join(VALID_DEVICES)}")
        raise typer.Exit(code=4)

    if os and os not in VALID_OS:
        print_error(f"Invalid OS: {os}. Valid: {', '.join(VALID_OS)}")
        raise typer.Exit(code=4)

    # Handle raw-params (mutually exclusive with other flags)
    if raw_params:
        try:
            raw_payload = validate_raw_params(raw_params)
        except ValueError as e:
            print_error(str(e))
            raise typer.Exit(code=4)
    else:
        raw_payload = None

    # Build payload for dry-run or raw-params
    if raw_payload:
        payload = raw_payload
    else:
        payload = [{
            "keyword": keyword,
            "location_name": location,
            "language_name": language,
            "device": device,
            "depth": min(depth, 700),
        }]
        if os:
            payload[0]["os"] = os

    # Dry-run mode
    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/serp/google/organic/live/advanced",
            request_body=payload,
        )
        print(format_output(result, output_format))
        return

    try:
        client = _get_client(login, password, verbose)

        # Handle raw JSON params
        if raw_payload:
            data = client._request("POST", "/serp/google/organic/live/advanced", json_data=raw_payload)
            client.close()
            print(format_output(data, output_format))
            return

        result = client.serp_google(
            keyword=keyword,
            location_name=location,
            language_name=language,
            device=device,
            os=os,
            depth=depth,
        )
        client.close()

        # Filter for features only if requested
        data = result.model_dump(by_alias=True)
        if features_only:
            data = {
                "keyword": data["keyword"],
                "serp_features": data["serp_features"],
                "featured_snippet": data.get("featured_snippet"),
                "people_also_ask": data.get("people_also_ask"),
                "cost": data["cost"],
                "timestamp": data["timestamp"],
            }

        # Parse fields filter
        fields_list = fields.split(",") if fields else None
        print(format_output(data, output_format, fields=fields_list))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


@serp_app.command()
def bing(
    keyword: str = typer.Argument(..., help="Search keyword"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    device: str = typer.Option(None, "--device", "-d", help="Device type (desktop/mobile)"),
    depth: int = typer.Option(100, "--depth", "-n", help="Number of results (max 700)"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Search Bing SERP."""
    defaults = _get_defaults()

    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    device = device or defaults["device"]
    output_format = output or defaults["output"]

    try:
        keyword = validate_keyword(keyword)
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(code=4)

    if device not in VALID_DEVICES:
        print_error(f"Invalid device: {device}")
        raise typer.Exit(code=4)

    if raw_params:
        try:
            raw_payload = validate_raw_params(raw_params)
        except ValueError as e:
            print_error(str(e))
            raise typer.Exit(code=4)
    else:
        raw_payload = None

    payload = raw_payload or [{
        "keyword": keyword,
        "location_name": location,
        "language_name": language,
        "device": device,
        "depth": min(depth, 700),
    }]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/serp/bing/organic/live/advanced",
            request_body=payload,
        )
        print(format_output(result, output_format))
        return

    try:
        client = _get_client(login, password, verbose)

        if raw_payload:
            data = client._request("POST", "/serp/bing/organic/live/advanced", json_data=raw_payload)
            client.close()
            print(format_output(data, output_format))
            return

        result = client.serp_bing(
            keyword=keyword,
            location_name=location,
            language_name=language,
            device=device,
            depth=depth,
        )
        client.close()

        data = result.model_dump(by_alias=True)
        fields_list = fields.split(",") if fields else None
        print(format_output(data, output_format, fields=fields_list))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


@serp_app.command()
def youtube(
    keyword: str = typer.Argument(..., help="Search keyword"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    device: str = typer.Option(None, "--device", "-d", help="Device type"),
    depth: int = typer.Option(100, "--depth", "-n", help="Number of results"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Search YouTube SERP."""
    defaults = _get_defaults()

    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    device = device or defaults["device"]
    output_format = output or defaults["output"]

    try:
        keyword = validate_keyword(keyword)
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(code=4)

    if device not in VALID_DEVICES:
        print_error(f"Invalid device: {device}")
        raise typer.Exit(code=4)

    if raw_params:
        try:
            raw_payload = validate_raw_params(raw_params)
        except ValueError as e:
            print_error(str(e))
            raise typer.Exit(code=4)
    else:
        raw_payload = None

    payload = raw_payload or [{
        "keyword": keyword,
        "location_name": location,
        "language_name": language,
        "device": device,
        "depth": min(depth, 700),
    }]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/serp/youtube/organic/live/advanced",
            request_body=payload,
        )
        print(format_output(result, output_format))
        return

    try:
        client = _get_client(login, password, verbose)

        if raw_payload:
            data = client._request("POST", "/serp/youtube/organic/live/advanced", json_data=raw_payload)
            client.close()
            print(format_output(data, output_format))
            return

        result = client.serp_youtube(
            keyword=keyword,
            location_name=location,
            language_name=language,
            device=device,
            depth=depth,
        )
        client.close()

        data = result.model_dump(by_alias=True)
        fields_list = fields.split(",") if fields else None
        print(format_output(data, output_format, fields=fields_list))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


@serp_app.command()
def locations(
    search: str = typer.Option(None, "--search", "-s", help="Search filter"),
    output: str = typer.Option("table", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """List available locations."""
    try:
        client = _get_client(login, password, verbose)
        locations_list = client.get_locations(search=search)
        client.close()

        data = [loc.model_dump(by_alias=True) for loc in locations_list]
        print(format_locations(data, output))

    except Exception as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)


@serp_app.command()
def languages(
    search: str = typer.Option(None, "--search", "-s", help="Search filter"),
    output: str = typer.Option("table", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """List available languages."""
    try:
        client = _get_client(login, password, verbose)
        languages_list = client.get_languages(search=search)
        client.close()

        data = [lang.model_dump(by_alias=True) for lang in languages_list]
        print(format_languages(data, output))

    except Exception as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)


@serp_app.command()
def compare(
    keyword: str = typer.Argument(..., help="Search keyword"),
    engines: str = typer.Option(
        "google,bing", "--engines", "-e", help="Engines to compare (comma-separated)"
    ),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    language: str = typer.Option(None, "--language", "-L", help="Language name"),
    device: str = typer.Option(None, "--device", "-d", help="Device type"),
    depth: int = typer.Option(50, "--depth", "-n", help="Number of results"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("table", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Compare SERP results across search engines."""
    defaults = _get_defaults()

    location = location or defaults["location_name"]
    language = language or defaults["language_name"]
    device = device or defaults["device"]

    try:
        keyword = validate_keyword(keyword)
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(code=4)

    engine_list = [e.strip().lower() for e in engines.split(",")]
    valid_engines = ["google", "bing"]

    for engine in engine_list:
        if engine not in valid_engines:
            print_error(f"Invalid engine: {engine}. Valid: {', '.join(valid_engines)}")
            raise typer.Exit(code=4)

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/serp/*/organic/live/advanced",
            request_body=[{"keyword": keyword, "engines": engine_list}],
        )
        print(format_output(result, output))
        return

    try:
        client = _get_client(login, password, verbose)

        results = {}
        for engine in engine_list:
            if engine == "google":
                result = client.serp_google(
                    keyword=keyword,
                    location_name=location,
                    language_name=language,
                    device=device,
                    depth=depth,
                )
            elif engine == "bing":
                result = client.serp_bing(
                    keyword=keyword,
                    location_name=location,
                    language_name=language,
                    device=device,
                    depth=depth,
                )
            results[engine] = result

        client.close()

        # Build comparison
        comparison = _build_comparison(keyword, results, engine_list)
        if fields:
            comparison = filter_fields(comparison, fields)
        print(format_compare(comparison, output))

    except Exception as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)


def _build_comparison(
    keyword: str,
    results: dict[str, Any],
    engines: list[str],
) -> dict[str, Any]:
    """Build comparison data between search engines."""
    # Extract domains from each engine
    domains_by_engine: dict[str, set[str]] = {}
    positions_by_engine: dict[str, dict[str, int]] = {}

    for engine in engines:
        domains_by_engine[engine] = set()
        positions_by_engine[engine] = {}
        organic = results[engine].organic_results
        for item in organic:
            domain = item.domain
            domains_by_engine[engine].add(domain)
            positions_by_engine[engine][domain] = item.rank

    # Find common domains
    all_domains = set()
    for domains in domains_by_engine.values():
        all_domains.update(domains)

    common_domains = []
    unique_domains: dict[str, list[str]] = {engine: [] for engine in engines}

    for domain in all_domains:
        positions = {}
        found_in = []
        for engine in engines:
            if domain in domains_by_engine[engine]:
                positions[engine] = positions_by_engine[engine][domain]
                found_in.append(engine)

        if len(found_in) > 1:
            common_domains.append({
                "domain": domain,
                "positions": positions,
                "engines": found_in,
            })
        else:
            unique_domains[found_in[0]].append(domain)

    # Sort common domains by total rank
    common_domains.sort(key=lambda x: sum(x["positions"].values()))

    # Build summary
    summary = {}
    for engine in engines:
        summary[engine] = {
            "total": len(domains_by_engine[engine]),
            "unique_domains": len(unique_domains[engine]),
            "common_domains": len(common_domains),
        }

    return {
        "keyword": keyword,
        "engines": engines,
        "summary": summary,
        "common_domains": common_domains[:20],  # Top 20
        "unique_domains": {k: v[:20] for k, v in unique_domains.items()},
    }
