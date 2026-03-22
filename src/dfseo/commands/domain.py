"""Domain Analytics commands for dfseo CLI.

Provides technology stack detection using the DataForSEO
Domain Analytics / Technologies API.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import typer

from dfseo.client import AuthenticationError, DataForSeoClient, DataForSeoError
from dfseo.config import Config
from dfseo.output import filter_fields, format_output, print_error
from dfseo.pricing import format_dry_run_output
from dfseo.validation import validate_raw_params, validate_target

domain_app = typer.Typer(help="Domain Analytics commands")

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
        "output": config.get_default("output"),
    }


@domain_app.command("technologies")
def domain_technologies(
    target: str = typer.Argument(..., help="Domain to analyze (e.g., example.com)"),
    fields: str = typer.Option(None, "--fields", "-F", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show estimated cost without executing"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Detect technologies used by a domain (CMS, analytics, frameworks, etc.)."""
    defaults = _get_defaults()
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
    }]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/domain_analytics/technologies/domain_technologies/live",
            request_body=raw_payload or payload,
        )
        print(format_output(result, output_format))
        return

    fields_list = fields.split(",") if fields else None

    try:
        client = _get_client(login, password, verbose)

        data = client._request(
            "POST",
            "/domain_analytics/technologies/domain_technologies/live",
            json_data=raw_payload or payload,
        )

        result = _parse_technologies_response(data, target)
        client.close()

        if fields_list:
            result = filter_fields(result, fields_list)
        formatted = _format_technologies_output(result, output_format)
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


def _parse_technologies_response(data: dict[str, Any], target: str) -> dict[str, Any]:
    """Parse domain technologies API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    technologies = []
    cost = api_response.cost or 0.0

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        items = task_result.get("items", [])

        for item in items:
            tech_groups = item.get("technologies", {})
            for category, tech_list in tech_groups.items():
                if isinstance(tech_list, list):
                    for tech in tech_list:
                        technologies.append({
                            "category": category,
                            "name": tech.get("name", "") if isinstance(tech, dict) else str(tech),
                        })
                elif isinstance(tech_list, dict):
                    for subcategory, subtechs in tech_list.items():
                        if isinstance(subtechs, list):
                            for tech in subtechs:
                                technologies.append({
                                    "category": f"{category}/{subcategory}",
                                    "name": tech.get("name", "") if isinstance(tech, dict) else str(tech),
                                })

    return {
        "target": target,
        "technologies_count": len(technologies),
        "technologies": technologies,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _format_technologies_output(result: dict[str, Any], output_format: str) -> str:
    """Format technologies command output."""
    if output_format in ("json", "json-pretty"):
        return format_output(result, output_format)
    elif output_format == "csv":
        return _format_technologies_csv(result)
    else:
        return _format_technologies_table(result)


def _format_technologies_table(result: dict[str, Any]) -> str:
    """Format technologies results as table."""
    from rich.console import Console
    from rich.table import Table

    console = Console(force_terminal=True)
    output_lines = []

    target = result.get("target", "")
    count = result.get("technologies_count", 0)

    output_lines.append(f"  Domain Technologies: {target} | Found: {count}")
    output_lines.append("")

    technologies = result.get("technologies", [])
    if technologies:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Category", style="cyan", min_width=20)
        table.add_column("Technology", style="white", min_width=25)

        for tech in technologies:
            table.add_row(
                tech.get("category", "")[:30],
                tech.get("name", ""),
            )

        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

    cost = result.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_technologies_csv(result: dict[str, Any]) -> str:
    """Format technologies results as CSV."""
    import csv
    import io

    output = io.StringIO()
    technologies = result.get("technologies", [])

    if technologies:
        writer = csv.DictWriter(
            output,
            fieldnames=["category", "name"],
            extrasaction="ignore",
        )
        writer.writeheader()
        for tech in technologies:
            writer.writerow(tech)

    return output.getvalue()
