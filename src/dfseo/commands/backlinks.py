"""Backlinks commands for dfseo CLI."""

from __future__ import annotations

import csv
import io
import sys
from datetime import datetime, timezone
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

from dfseo.client import (
    AuthenticationError,
    DataForSeoClient,
    DataForSeoError,
)
from dfseo.config import Config
from dfseo.output import format_output, print_error
from dfseo.pricing import format_dry_run_output
from dfseo.validation import validate_target, validate_raw_params

app = typer.Typer(
    help="""Backlinks API - Analyze backlink profiles.

Note: Backlinks API requires a $100/month minimum commitment.
""",
    no_args_is_help=True,
)

VALID_OUTPUTS = ["json", "json-pretty", "table", "csv"]
VALID_BACKLINK_STATUS = ["all", "live", "new", "lost", "broken"]
VALID_SORT_FIELDS = [
    "rank", "page_from_rank", "domain_from_rank", "first_seen", "last_seen"
]
VALID_ORDERS = ["asc", "desc"]

# Mapping: which filter type to use per endpoint
FILTER_TYPE_MAPPING = {
    "summary": "backlinks_filters",
    "list": "filters",
    "anchors": "backlinks_filters",
    "referring_domains": "backlinks_filters",
    "pages": "backlinks_filters",
    "competitors": "filters",
    "gap": "filters",
}


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


def load_targets(
    targets: list[str] | None,
    from_file: str | None,
) -> list[str]:
    """Load targets from arguments or file.

    Args:
        targets: List of targets from CLI arguments
        from_file: Path to file with targets (one per line)

    Returns:
        List of target strings
    """
    if from_file:
        try:
            with open(from_file, "r", encoding="utf-8") as f:
                file_targets = [
                    line.strip() for line in f
                    if line.strip() and not line.strip().startswith("#")
                ]
            return file_targets
        except FileNotFoundError:
            print_error(f"File not found: {from_file}")
            raise typer.Exit(code=4)
        except IOError as e:
            print_error(f"Error reading file: {e}")
            raise typer.Exit(code=4)

    return targets or []


def _is_domain(target: str) -> bool:
    """Check if target is a domain (not a full URL)."""
    return not target.startswith(("http://", "https://"))


def _build_filters(
    dofollow_only: bool = False,
    min_rank: int | None = None,
    from_domain: str | None = None,
) -> list[Any] | None:
    """Build API filters array."""
    filters = []

    if dofollow_only:
        filters.append(["dofollow", "=", True])

    if min_rank is not None:
        if filters:
            filters.append("and")
        filters.append(["rank", ">=", min_rank])

    if from_domain:
        if filters:
            filters.append("and")
        filters.append(["domain_from", "=", from_domain])

    return filters if filters else None


def _build_order_by(sort: str, order: str) -> list[str]:
    """Build order_by array for API."""
    return [f"{sort},{order}"]


@app.command("summary")
def backlinks_summary(
    target: str = typer.Argument(..., help="Target domain or URL"),
    include_subdomains: bool = typer.Option(True, "--include-subdomains/--exclude-subdomains", help="Include subdomains"),
    dofollow_only: bool = typer.Option(False, "--dofollow-only", help="Only dofollow backlinks"),
    status: str = typer.Option("all", "--status", help="Status: all, live, new, lost"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="Show estimated cost without executing"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get backlink profile summary for a target."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if status not in VALID_BACKLINK_STATUS:
        print_error(f"Invalid status: {status}. Valid: {', '.join(VALID_BACKLINK_STATUS)}")
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

    payload = raw_payload or [{
        "target": target,
        "include_subdomains": include_subdomains,
        "backlinks_status_type": status,
    }]

    if not raw_payload:
        # Use backlinks_filters for summary endpoint
        backlinks_filters = []
        if dofollow_only:
            backlinks_filters.append(["dofollow", "=", True])

        if backlinks_filters:
            payload[0]["backlinks_filters"] = backlinks_filters

    # Dry-run mode
    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/backlinks/summary/live",
            request_body=payload,
        )
        fields_list = fields.split(",") if fields else None
        print(format_output(result, output_format, fields=fields_list))
        return

    try:
        client = _get_client(login, password, verbose)

        data = client._request("POST", "/backlinks/summary/live", json_data=payload)
        client.close()

        result = _parse_summary_response(data, target)
        fields_list = fields.split(",") if fields else None

        if output_format == "table":
            print(_format_summary_table(result))
        else:
            print(format_output(result, output_format, fields=fields_list))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_summary_response(data: dict[str, Any], target: str) -> dict[str, Any]:
    """Parse backlinks summary API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "target": target,
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]

        result.update({
            "rank": task_result.get("rank", 0),
            "backlinks": task_result.get("backlinks", 0),
            "referring_domains": task_result.get("referring_domains", 0),
            "referring_main_domains": task_result.get("referring_main_domains", 0),
            "referring_ips": task_result.get("referring_ips", 0),
            "referring_subnets": task_result.get("referring_subnets", 0),
            "spam_score": task_result.get("spam_score", 0),
            "broken_backlinks": task_result.get("broken_backlinks", 0),
            "broken_pages": task_result.get("broken_pages", 0),
        })

        # Link summary
        link_summary = task_result.get("link_summary", {})
        result["links_summary"] = {
            "dofollow": link_summary.get("dofollow", 0),
            "nofollow": link_summary.get("nofollow", 0),
            "anchor": link_summary.get("anchor", 0),
            "image": link_summary.get("image", 0),
            "redirect": link_summary.get("redirect", 0),
            "canonical": link_summary.get("canonical", 0),
        }

        # Top pages
        result["top_pages"] = [
            {"url": p.get("url", ""), "backlinks": p.get("backlinks", 0)}
            for p in task_result.get("top_pages", [])[:10]
        ]

        # Top anchors
        result["top_anchors"] = [
            {"anchor": a.get("anchor", ""), "backlinks": a.get("backlinks", 0)}
            for a in task_result.get("top_anchors", [])[:10]
        ]

    return result


def _format_summary_table(data: dict[str, Any]) -> str:
    """Format summary as human-readable table."""
    output_lines = []

    target = data.get("target", "")
    rank = data.get("rank", 0)
    backlinks = data.get("backlinks", 0)
    domains = data.get("referring_domains", 0)
    spam_score = data.get("spam_score", 0)

    output_lines.append(f"  Target: {target} | Domain Rank: {rank}/1000")
    output_lines.append("")

    links_summary = data.get("links_summary", {})
    dofollow = links_summary.get("dofollow", 0)
    nofollow = links_summary.get("nofollow", 0)

    output_lines.append(f"  Backlinks: {backlinks:,} ({dofollow:,} dofollow / {nofollow:,} nofollow)")
    output_lines.append(f"  Referring domains: {domains:,}")
    output_lines.append(f"  Referring IPs: {data.get('referring_ips', 0):,}")
    output_lines.append(f"  Broken backlinks: {data.get('broken_backlinks', 0)}")
    output_lines.append(f"  Spam score: {spam_score}/100")
    output_lines.append("")

    # Top pages
    top_pages = data.get("top_pages", [])
    if top_pages:
        output_lines.append("  Top pages by backlinks:")
        for page in top_pages[:5]:
            url = page.get("url", "")[:40]
            count = page.get("backlinks", 0)
            output_lines.append(f"    {url:<40} {count}")
        output_lines.append("")

    # Top anchors
    top_anchors = data.get("top_anchors", [])
    if top_anchors:
        output_lines.append("  Top anchors:")
        for anchor in top_anchors[:5]:
            text = anchor.get("anchor", "")[:30]
            count = anchor.get("backlinks", 0)
            output_lines.append(f'    "{text:<30}" {count}')
        output_lines.append("")

    cost = data.get("cost", 0)
    output_lines.append(f"  Cost: ${cost:.3f}")

    return "\n".join(output_lines)


@app.command("list")
def backlinks_list(
    target: str = typer.Argument(..., help="Target domain or URL"),
    include_subdomains: bool = typer.Option(True, "--include-subdomains/--exclude-subdomains", help="Include subdomains"),
    dofollow_only: bool = typer.Option(False, "--dofollow-only", help="Only dofollow backlinks"),
    status: str = typer.Option("live", "--status", help="Status: all, live, new, lost, broken"),
    sort: str = typer.Option("rank", "--sort", help="Sort by: rank, page_from_rank, domain_from_rank, first_seen, last_seen"),
    order: str = typer.Option("desc", "--order", help="Sort order: asc, desc"),
    from_domain: str | None = typer.Option(None, "--from-domain", help="Filter by source domain"),
    min_rank: int | None = typer.Option(None, "--min-rank", help="Minimum backlink rank"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results (max 1000)"),
    offset: int = typer.Option(0, "--offset", help="Offset for pagination"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="Show estimated cost without executing"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """List detailed backlinks for a target."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if status not in VALID_BACKLINK_STATUS:
        print_error(f"Invalid status: {status}")
        raise typer.Exit(code=4)

    if sort not in VALID_SORT_FIELDS:
        print_error(f"Invalid sort: {sort}. Valid: {', '.join(VALID_SORT_FIELDS)}")
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

    payload = raw_payload or [{
        "target": target,
        "mode": "as_is",
        "include_subdomains": include_subdomains,
        "backlinks_status_type": status,
        "limit": min(limit, 1000),
        "offset": offset,
    }]

    if not raw_payload:
        # Use filters (not backlinks_filters) for list endpoint
        filters = _build_filters(
            dofollow_only=dofollow_only,
            min_rank=min_rank,
            from_domain=from_domain,
        )
        if filters:
            payload[0]["filters"] = filters

        # Add ordering
        payload[0]["order_by"] = _build_order_by(sort, order)

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/backlinks/backlinks/live",
            request_body=payload,
        )
        fields_list = fields.split(",") if fields else None
        print(format_output(result, output_format, fields=fields_list))
        return

    try:
        client = _get_client(login, password, verbose)

        data = client._request("POST", "/backlinks/backlinks/live", json_data=payload)
        client.close()

        result = _parse_backlinks_list_response(data, target)
        fields_list = fields.split(",") if fields else None

        if output_format == "table":
            print(_format_backlinks_list_table(result))
        elif output_format == "csv":
            print(_format_backlinks_list_csv(result))
        else:
            print(format_output(result, output_format, fields=fields_list))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_backlinks_list_response(data: dict[str, Any], target: str) -> dict[str, Any]:
    """Parse backlinks list API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "target": target,
        "backlinks": [],
        "total_count": 0,
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        result["total_count"] = task_result.get("total_count", 0)

        for item in task_result.get("items", []):
            backlink = {
                "domain_from": item.get("domain_from", ""),
                "url_from": item.get("url_from", ""),
                "domain_to": item.get("domain_to", ""),
                "url_to": item.get("url_to", ""),
                "rank": item.get("rank", 0),
                "page_from_rank": item.get("page_from_rank", 0),
                "domain_from_rank": item.get("domain_from_rank", 0),
                "anchor": item.get("anchor", ""),
                "text_pre": item.get("text_pre", ""),
                "text_post": item.get("text_post", ""),
                "dofollow": item.get("dofollow", False),
                "nofollow": item.get("nofollow", False),
                "first_seen": item.get("first_seen", ""),
                "last_seen": item.get("last_seen", ""),
            }
            result["backlinks"].append(backlink)

    return result


def _format_backlinks_list_table(data: dict[str, Any]) -> str:
    """Format backlinks list as table."""
    output_lines = []

    backlinks = data.get("backlinks", [])
    total = data.get("total_count", 0)

    output_lines.append(f"  Backlinks: {len(backlinks)} of {total} total")
    output_lines.append("")

    for bl in backlinks[:20]:
        domain = bl.get("domain_from", "")
        rank = bl.get("rank", 0)
        anchor = bl.get("anchor", "")[:40]
        dofollow = "D" if bl.get("dofollow") else "N"

        output_lines.append(f"  [{dofollow}] {rank:4} | {domain[:30]:<30} | \"{anchor}\"")

    if len(backlinks) > 20:
        output_lines.append(f"\n  ... and {len(backlinks) - 20} more backlinks")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _format_backlinks_list_csv(data: dict[str, Any]) -> str:
    """Format backlinks list as CSV."""
    output = io.StringIO()
    backlinks = data.get("backlinks", [])

    if backlinks:
        fieldnames = [
            "domain_from", "url_from", "domain_to", "url_to",
            "rank", "page_from_rank", "domain_from_rank",
            "anchor", "dofollow", "first_seen", "last_seen",
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for bl in backlinks:
            writer.writerow(bl)

    return output.getvalue()


@app.command("anchors")
def backlinks_anchors(
    target: str = typer.Argument(..., help="Target domain or URL"),
    include_subdomains: bool = typer.Option(True, "--include-subdomains/--exclude-subdomains", help="Include subdomains"),
    dofollow_only: bool = typer.Option(False, "--dofollow-only", help="Only dofollow backlinks"),
    search: str | None = typer.Option(None, "--search", help="Search in anchor text"),
    sort: str = typer.Option("backlinks", "--sort", help="Sort by: backlinks, referring_domains"),
    order: str = typer.Option("desc", "--order", help="Sort order: asc, desc"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="Show estimated cost without executing"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Analyze anchor text distribution."""
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

    payload = raw_payload or [{
        "target": target,
        "include_subdomains": include_subdomains,
        "limit": limit,
    }]

    if not raw_payload:
        # Use backlinks_filters for anchors endpoint
        backlinks_filters = []
        if dofollow_only:
            backlinks_filters.append(["dofollow", "=", True])

        if backlinks_filters:
            payload[0]["backlinks_filters"] = backlinks_filters

        if search:
            payload[0]["search"] = search

        payload[0]["order_by"] = [f"{sort},{order}"]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/backlinks/anchors/live",
            request_body=payload,
        )
        fields_list = fields.split(",") if fields else None
        print(format_output(result, output_format, fields=fields_list))
        return

    try:
        client = _get_client(login, password, verbose)

        data = client._request("POST", "/backlinks/anchors/live", json_data=payload)
        client.close()

        result = _parse_anchors_response(data, target)
        fields_list = fields.split(",") if fields else None

        if output_format == "table":
            print(_format_anchors_table(result))
        else:
            print(format_output(result, output_format, fields=fields_list))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_anchors_response(data: dict[str, Any], target: str) -> dict[str, Any]:
    """Parse anchors API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "target": target,
        "anchors": [],
        "total_count": 0,
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        result["total_count"] = task_result.get("total_count", 0)

        for item in task_result.get("items", []):
            anchor = {
                "anchor": item.get("anchor", ""),
                "backlinks": item.get("backlinks", 0),
                "referring_domains": item.get("referring_domains", 0),
                "dofollow": item.get("dofollow", False),
            }
            result["anchors"].append(anchor)

    return result


def _format_anchors_table(data: dict[str, Any]) -> str:
    """Format anchors as table."""
    output_lines = []

    anchors = data.get("anchors", [])
    total = data.get("total_count", 0)

    output_lines.append(f"  Anchors: {len(anchors)} of {total} total")
    output_lines.append("")

    for a in anchors[:20]:
        anchor_text = a.get("anchor", "")[:40] or "(empty)"
        backlinks = a.get("backlinks", 0)
        domains = a.get("referring_domains", 0)
        dofollow = "D" if a.get("dofollow") else "N"

        output_lines.append(f"  [{dofollow}] {backlinks:5} | {domains:4} | \"{anchor_text}\"")

    if len(anchors) > 20:
        output_lines.append(f"\n  ... and {len(anchors) - 20} more anchors")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


@app.command("referring-domains")
def backlinks_referring_domains(
    target: str = typer.Argument(..., help="Target domain or URL"),
    include_subdomains: bool = typer.Option(True, "--include-subdomains/--exclude-subdomains", help="Include subdomains"),
    dofollow_only: bool = typer.Option(False, "--dofollow-only", help="Only dofollow backlinks"),
    min_backlinks: int | None = typer.Option(None, "--min-backlinks", help="Minimum backlinks from domain"),
    sort: str = typer.Option("rank", "--sort", help="Sort by: rank, backlinks"),
    order: str = typer.Option("desc", "--order", help="Sort order"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="Show estimated cost without executing"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """List referring domains."""
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

    payload = raw_payload or [{
        "target": target,
        "include_subdomains": include_subdomains,
        "limit": limit,
    }]

    if not raw_payload:
        # Use backlinks_filters
        backlinks_filters = []
        if dofollow_only:
            backlinks_filters.append(["dofollow", "=", True])

        if backlinks_filters:
            payload[0]["backlinks_filters"] = backlinks_filters

        if min_backlinks:
            payload[0]["filters"] = [["backlinks", ">=", min_backlinks]]

        payload[0]["order_by"] = [f"{sort},{order}"]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/backlinks/referring_domains/live",
            request_body=payload,
        )
        fields_list = fields.split(",") if fields else None
        print(format_output(result, output_format, fields=fields_list))
        return

    try:
        client = _get_client(login, password, verbose)

        data = client._request("POST", "/backlinks/referring_domains/live", json_data=payload)
        client.close()

        result = _parse_referring_domains_response(data, target)
        fields_list = fields.split(",") if fields else None

        if output_format == "table":
            print(_format_referring_domains_table(result))
        else:
            print(format_output(result, output_format, fields=fields_list))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_referring_domains_response(data: dict[str, Any], target: str) -> dict[str, Any]:
    """Parse referring domains API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "target": target,
        "domains": [],
        "total_count": 0,
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        result["total_count"] = task_result.get("total_count", 0)

        for item in task_result.get("items", []):
            domain = {
                "domain": item.get("domain", ""),
                "rank": item.get("rank", 0),
                "backlinks": item.get("backlinks", 0),
                "dofollow": item.get("dofollow", False),
            }
            result["domains"].append(domain)

    return result


def _format_referring_domains_table(data: dict[str, Any]) -> str:
    """Format referring domains as table."""
    output_lines = []

    domains = data.get("domains", [])
    total = data.get("total_count", 0)

    output_lines.append(f"  Referring domains: {len(domains)} of {total} total")
    output_lines.append("")

    for d in domains[:20]:
        domain = d.get("domain", "")[:35]
        rank = d.get("rank", 0)
        backlinks = d.get("backlinks", 0)
        dofollow = "D" if d.get("dofollow") else "N"

        output_lines.append(f"  [{dofollow}] {rank:4} | {backlinks:5} | {domain}")

    if len(domains) > 20:
        output_lines.append(f"\n  ... and {len(domains) - 20} more domains")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


@app.command("history")
def backlinks_history(
    target: str = typer.Argument(..., help="Target domain"),
    date_from: str | None = typer.Option(None, "--from", help="Start date (YYYY-MM)"),
    date_to: str | None = typer.Option(None, "--to", help="End date (YYYY-MM)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="Show estimated cost without executing"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get backlink profile history (data from 2019 onwards)."""
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

    payload: list[dict[str, Any]] = raw_payload or [{"target": target}]
    if not raw_payload:
        if date_from:
            payload[0]["date_from"] = date_from
        if date_to:
            payload[0]["date_to"] = date_to

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/backlinks/history/live",
            request_body=payload,
        )
        fields_list = fields.split(",") if fields else None
        print(format_output(result, output_format, fields=fields_list))
        return

    try:
        client = _get_client(login, password, verbose)

        data = client._request("POST", "/backlinks/history/live", json_data=payload)
        client.close()

        result = _parse_history_response(data, target)
        fields_list = fields.split(",") if fields else None

        if output_format == "table":
            print(_format_history_table(result))
        else:
            print(format_output(result, output_format, fields=fields_list))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_history_response(data: dict[str, Any], target: str) -> dict[str, Any]:
    """Parse history API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result: dict[str, Any] = {
        "target": target,
        "history": [],
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        for item in api_response.tasks[0].result:
            entry = {
                "date": item.get("date", ""),
                "backlinks": item.get("backlinks", 0),
                "referring_domains": item.get("referring_domains", 0),
                "referring_main_domains": item.get("referring_main_domains", 0),
                "rank": item.get("rank", 0),
            }
            result["history"].append(entry)

    return result


def _format_history_table(data: dict[str, Any]) -> str:
    """Format history as table."""
    output_lines = []
    output_lines.append(f"  Target: {data.get('target', '')}")
    output_lines.append("")

    for entry in data.get("history", []):
        date = entry.get("date", "")[:10]
        rank = entry.get("rank", 0)
        backlinks = entry.get("backlinks", 0)
        domains = entry.get("referring_domains", 0)
        output_lines.append(f"  {date} | Rank: {rank:4} | BL: {backlinks:6} | RD: {domains:4}")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")
    return "\n".join(output_lines)


@app.command("competitors")
def backlinks_competitors(
    target: str = typer.Argument(..., help="Target domain or URL"),
    include_subdomains: bool = typer.Option(True, "--include-subdomains/--exclude-subdomains", help="Include subdomains"),
    sort: str = typer.Option("rank", "--sort", help="Sort by: rank, backlinks, referring_domains"),
    order: str = typer.Option("desc", "--order", help="Sort order: asc, desc"),
    limit: int = typer.Option(50, "--limit", "-n", help="Max results"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="Show estimated cost without executing"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Find competitors sharing backlink profile with the target."""
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

    payload = raw_payload or [{
        "target": target,
        "include_subdomains": include_subdomains,
        "limit": limit,
        "order_by": [f"{sort},{order}"],
    }]

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/backlinks/competitors/live",
            request_body=payload,
        )
        fields_list = fields.split(",") if fields else None
        print(format_output(result, output_format, fields=fields_list))
        return

    try:
        client = _get_client(login, password, verbose)

        data = client._request("POST", "/backlinks/competitors/live", json_data=payload)
        client.close()

        result = _parse_competitors_response(data, target)
        fields_list = fields.split(",") if fields else None

        if output_format == "table":
            print(_format_competitors_table(result))
        else:
            print(format_output(result, output_format, fields=fields_list))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_competitors_response(data: dict[str, Any], target: str) -> dict[str, Any]:
    """Parse competitors API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result: dict[str, Any] = {
        "target": target,
        "competitors": [],
        "total_count": 0,
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        result["total_count"] = task_result.get("total_count", 0)

        for item in task_result.get("items", []):
            competitor = {
                "domain": item.get("domain", ""),
                "avg_position": item.get("avg_position", 0),
                "backlinks": item.get("backlinks", 0),
                "referring_domains": item.get("referring_domains", 0),
                "rank": item.get("rank", 0),
            }
            result["competitors"].append(competitor)

    return result


def _format_competitors_table(data: dict[str, Any]) -> str:
    """Format competitors as table."""
    output_lines = []
    output_lines.append(f"  Target: {data.get('target', '')} | Competitors: {data.get('total_count', 0)}")
    output_lines.append("")

    for c in data.get("competitors", [])[:20]:
        domain = c.get("domain", "")[:35]
        rank = c.get("rank", 0)
        backlinks = c.get("backlinks", 0)
        output_lines.append(f"  {rank:4} | {backlinks:6} | {domain}")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")
    return "\n".join(output_lines)


@app.command("gap")
def backlinks_gap(
    targets: list[str] = typer.Argument(..., help="Targets: your site first, then competitors"),
    mode: str = typer.Option("domain", "--mode", help="Intersection mode: domain, page"),
    exclude: list[str] = typer.Option([], "--exclude", help="Domains to exclude from results"),
    dofollow_only: bool = typer.Option(False, "--dofollow-only", help="Only dofollow backlinks"),
    min_rank: int | None = typer.Option(None, "--min-rank", help="Minimum domain rank"),
    sort: str = typer.Option("rank", "--sort", help="Sort by: rank, backlinks"),
    order: str = typer.Option("desc", "--order", help="Sort order: asc, desc"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max results"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="Show estimated cost without executing"),
    fields: str = typer.Option(None, "--fields", "-f", help="Comma-separated fields to include"),
    raw_params: str = typer.Option(None, "--raw-params", help="Raw JSON payload (bypasses all other flags)"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Link gap analysis — find domains linking to competitors but not to you."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    if len(targets) < 2:
        print_error("At least 2 targets required (your site + competitor)")
        raise typer.Exit(code=4)

    if len(targets) > 21:
        print_error("Maximum 20 competitors allowed")
        raise typer.Exit(code=4)

    if mode not in ("domain", "page"):
        print_error("Invalid mode. Use 'domain' or 'page'")
        raise typer.Exit(code=4)

    # Validate each target
    validated_targets = []
    for t in targets:
        try:
            validated_targets.append(validate_target(t))
        except ValueError as e:
            print_error(str(e))
            raise typer.Exit(code=4)
    targets = validated_targets

    if raw_params:
        try:
            raw_payload = validate_raw_params(raw_params)
        except ValueError as e:
            print_error(str(e))
            raise typer.Exit(code=4)
    else:
        raw_payload = None

    if raw_payload:
        payload = raw_payload
    else:
        # Build numbered targets dict (competitors only, exclude first target)
        numbered_targets = {}
        for i, t in enumerate(targets[1:], start=1):
            numbered_targets[str(i)] = t

        payload: list[dict[str, Any]] = [{
            "targets": numbered_targets,
            "exclude_targets": [targets[0]],
            "limit": limit,
            "order_by": [f"1.{sort},{order}"],
        }]

        # Filters use numbered prefixes
        filters: list[Any] = []
        if dofollow_only:
            filters.append(["1.dofollow", "=", True])
        if min_rank is not None:
            if filters:
                filters.append("and")
            filters.append(["1.domain_from_rank", ">", min_rank])
        if filters:
            payload[0]["filters"] = filters

        if exclude:
            payload[0]["exclude_targets"].extend(exclude)

    if dry_run:
        result = format_dry_run_output(
            endpoint="POST /v3/backlinks/domain_intersection/live",
            request_body=payload,
        )
        fields_list = fields.split(",") if fields else None
        print(format_output(result, output_format, fields=fields_list))
        return

    try:
        client = _get_client(login, password, verbose)

        endpoint = "/backlinks/domain_intersection/live" if mode == "domain" else "/backlinks/page_intersection/live"
        data = client._request("POST", endpoint, json_data=payload)
        client.close()

        result = _parse_gap_response(data, targets)
        fields_list = fields.split(",") if fields else None

        if output_format == "table":
            print(_format_gap_table(result))
        else:
            print(format_output(result, output_format, fields=fields_list))

    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        raise typer.Exit(code=2)
    except DataForSeoError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _parse_gap_response(data: dict[str, Any], targets: list[str]) -> dict[str, Any]:
    """Parse gap/intersection API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result: dict[str, Any] = {
        "your_site": targets[0],
        "competitors": targets[1:],
        "opportunities": [],
        "total_count": 0,
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        result["total_count"] = task_result.get("total_count", 0)

        for item in task_result.get("items", []):
            opportunity: dict[str, Any] = {
                "domain": item.get("domain", ""),
                "rank": item.get("rank", 0),
            }
            # Include per-competitor backlink counts
            for i in range(1, len(targets)):
                key = str(i)
                comp_data = item.get(key, {})
                if isinstance(comp_data, dict):
                    opportunity[f"links_to_c{i}"] = comp_data.get("backlinks", 0)
            result["opportunities"].append(opportunity)

    return result


def _format_gap_table(data: dict[str, Any]) -> str:
    """Format gap analysis as table."""
    output_lines = []
    your_site = data.get("your_site", "")
    competitors = data.get("competitors", [])

    output_lines.append(f"  Your site: {your_site} | Competitors: {', '.join(competitors)}")
    output_lines.append("  Showing: domains that link to competitors but NOT to you")
    output_lines.append("")

    for opp in data.get("opportunities", [])[:20]:
        domain = opp.get("domain", "")[:30]
        rank = opp.get("rank", 0)
        links = " | ".join(str(opp.get(f"links_to_c{i}", 0)) for i in range(1, len(competitors) + 1))
        output_lines.append(f"  {domain:<30} | {rank:4} | {links}")

    total = data.get("total_count", 0)
    output_lines.append(f"\n  Total link gap opportunities: {total}")
    cost = data.get("cost", 0)
    output_lines.append(f"  Cost: ${cost:.4f}")
    return "\n".join(output_lines)


@app.command("pages")
def backlinks_pages(
    target: str = typer.Argument(..., help="Target domain or URL"),
    include_subdomains: bool = typer.Option(True, "--include-subdomains/--exclude-subdomains", help="Include subdomains"),
    sort: str = typer.Option("backlinks", "--sort", help="Sort by: backlinks, rank, referring_domains"),
    order: str = typer.Option("desc", "--order", help="Sort order: asc, desc"),
    limit: int = typer.Option(50, "--limit", "-n", help="Max results"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """List pages with most backlinks for a target."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        payload = [{
            "target": target,
            "include_subdomains": include_subdomains,
            "limit": limit,
            "order_by": [f"{sort},{order}"],
        }]

        data = client._request("POST", "/backlinks/domain_pages/live", json_data=payload)
        client.close()

        result = _parse_pages_response(data, target)

        if output_format == "table":
            print(_format_pages_table(result))
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


def _parse_pages_response(data: dict[str, Any], target: str) -> dict[str, Any]:
    """Parse domain pages API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result: dict[str, Any] = {
        "target": target,
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
                "url": item.get("page", ""),
                "backlinks": item.get("backlinks", 0),
                "referring_domains": item.get("referring_domains", 0),
                "rank": item.get("rank", 0),
            }
            result["pages"].append(page)

    return result


def _format_pages_table(data: dict[str, Any]) -> str:
    """Format pages as table."""
    output_lines = []
    output_lines.append(f"  Target: {data.get('target', '')} | Pages: {data.get('total_count', 0)}")
    output_lines.append("")

    for p in data.get("pages", [])[:20]:
        url = p.get("url", "")[:50]
        backlinks = p.get("backlinks", 0)
        rank = p.get("rank", 0)
        output_lines.append(f"  {rank:4} | {backlinks:6} | {url}")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")
    return "\n".join(output_lines)


# Create bulk subcommand group
bulk_app = typer.Typer(help="Bulk operations for multiple targets", no_args_is_help=True)
app.add_typer(bulk_app, name="bulk")


@bulk_app.command("ranks")
def bulk_ranks(
    targets: list[str] = typer.Argument(None, help="Target domains/URLs to analyze"),
    from_file: str = typer.Option(None, "--from-file", "-f", help="Read targets from file"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get ranks for multiple targets (up to 1000)."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]

    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)

    try:
        target_list = load_targets(targets, from_file)
    except typer.Exit:
        raise

    if not target_list:
        print_error("No targets provided")
        raise typer.Exit(code=4)

    if len(target_list) > 1000:
        print_error("Maximum 1000 targets allowed")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        payload = [{"targets": target_list}]

        data = client._request("POST", "/backlinks/bulk_ranks/live", json_data=payload)
        client.close()

        result = _parse_bulk_ranks_response(data, target_list)

        if output_format == "table":
            print(_format_bulk_ranks_table(result))
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


def _parse_bulk_ranks_response(data: dict[str, Any], targets: list[str]) -> dict[str, Any]:
    """Parse bulk ranks API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result = {
        "targets_count": len(targets),
        "results": [],
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]

        for item in task_result.get("items", []):
            result_item = {
                "target": item.get("target", ""),
                "rank": item.get("rank", 0),
                "backlinks": item.get("backlinks", 0),
                "referring_domains": item.get("referring_domains", 0),
            }
            result["results"].append(result_item)

    return result


def _format_bulk_ranks_table(data: dict[str, Any]) -> str:
    """Format bulk ranks as table."""
    output_lines = []

    results = data.get("results", [])

    output_lines.append(f"  Targets: {data.get('targets_count', 0)} | Results: {len(results)}")
    output_lines.append("")

    for r in results[:30]:
        target = r.get("target", "")[:40]
        rank = r.get("rank", 0)
        backlinks = r.get("backlinks", 0)
        domains = r.get("referring_domains", 0)

        output_lines.append(f"  {rank:4} | {backlinks:6} | {domains:4} | {target}")

    if len(results) > 30:
        output_lines.append(f"\n  ... and {len(results) - 30} more results")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")

    return "\n".join(output_lines)


def _bulk_command(
    endpoint: str,
    item_fields: list[str],
    targets: list[str] | None,
    from_file: str | None,
    output_format: str,
    login: str | None,
    password: str | None,
    verbose: bool,
    extra_payload: dict[str, Any] | None = None,
) -> None:
    """Generic bulk command implementation."""
    try:
        target_list = load_targets(targets, from_file)
    except typer.Exit:
        raise

    if not target_list:
        print_error("No targets provided")
        raise typer.Exit(code=4)

    if len(target_list) > 1000:
        print_error("Maximum 1000 targets allowed")
        raise typer.Exit(code=4)

    try:
        client = _get_client(login, password, verbose)

        payload: list[dict[str, Any]] = [{"targets": target_list}]
        if extra_payload:
            payload[0].update(extra_payload)

        data = client._request("POST", endpoint, json_data=payload)
        client.close()

        result = _parse_bulk_generic_response(data, target_list, item_fields)

        if output_format == "table":
            print(_format_bulk_generic_table(result, item_fields))
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


def _parse_bulk_generic_response(
    data: dict[str, Any], targets: list[str], fields: list[str]
) -> dict[str, Any]:
    """Parse generic bulk API response."""
    from dfseo.models import ApiResponse

    api_response = ApiResponse.model_validate(data)

    result: dict[str, Any] = {
        "targets_count": len(targets),
        "results": [],
        "cost": api_response.cost or 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if api_response.tasks and api_response.tasks[0].result:
        task_result = api_response.tasks[0].result[0]
        for item in task_result.get("items", []):
            entry: dict[str, Any] = {"target": item.get("target", "")}
            for field in fields:
                entry[field] = item.get(field, 0)
            result["results"].append(entry)

    return result


def _format_bulk_generic_table(data: dict[str, Any], fields: list[str]) -> str:
    """Format generic bulk results as table."""
    output_lines = []
    results = data.get("results", [])
    output_lines.append(f"  Targets: {data.get('targets_count', 0)} | Results: {len(results)}")
    output_lines.append("")

    for r in results[:30]:
        target = r.get("target", "")[:40]
        values = " | ".join(f"{r.get(f, 0):>6}" for f in fields)
        output_lines.append(f"  {values} | {target}")

    if len(results) > 30:
        output_lines.append(f"\n  ... and {len(results) - 30} more results")

    cost = data.get("cost", 0)
    output_lines.append(f"\n  Cost: ${cost:.4f}")
    return "\n".join(output_lines)


@bulk_app.command("backlinks")
def bulk_backlinks(
    targets: list[str] = typer.Argument(None, help="Target domains/URLs"),
    from_file: str = typer.Option(None, "--from-file", "-f", help="Read targets from file"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get backlink counts for multiple targets (up to 1000)."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]
    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)
    _bulk_command(
        "/backlinks/bulk_backlinks/live",
        ["backlinks", "referring_domains", "rank"],
        targets, from_file, output_format, login, password, verbose,
    )


@bulk_app.command("spam-score")
def bulk_spam_score(
    targets: list[str] = typer.Argument(None, help="Target domains/URLs"),
    from_file: str = typer.Option(None, "--from-file", "-f", help="Read targets from file"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get spam scores for multiple targets (up to 1000)."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]
    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)
    _bulk_command(
        "/backlinks/bulk_spam_score/live",
        ["spam_score", "rank", "backlinks"],
        targets, from_file, output_format, login, password, verbose,
    )


@bulk_app.command("referring-domains")
def bulk_referring_domains_cmd(
    targets: list[str] = typer.Argument(None, help="Target domains/URLs"),
    from_file: str = typer.Option(None, "--from-file", "-f", help="Read targets from file"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get referring domain counts for multiple targets (up to 1000)."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]
    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)
    _bulk_command(
        "/backlinks/bulk_referring_domains/live",
        ["referring_domains", "referring_main_domains", "rank"],
        targets, from_file, output_format, login, password, verbose,
    )


@bulk_app.command("new-lost")
def bulk_new_lost(
    targets: list[str] = typer.Argument(None, help="Target domains/URLs"),
    from_file: str = typer.Option(None, "--from-file", "-f", help="Read targets from file"),
    from_date: str | None = typer.Option(None, "--from-date", help="Start date (YYYY-MM-DD)"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format"),
    login: str = typer.Option(None, "--login", help="DataForSEO login"),
    password: str | None = typer.Option(None, "--password", help="DataForSEO password"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Get new and lost backlinks for multiple targets (up to 1000)."""
    defaults = _get_defaults()
    output_format = output or defaults["output"]
    if output_format not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {output_format}")
        raise typer.Exit(code=4)
    extra: dict[str, Any] | None = None
    if from_date:
        extra = {"date_from": from_date}
    _bulk_command(
        "/backlinks/bulk_new_lost_backlinks/live",
        ["new_backlinks", "lost_backlinks", "new_referring_domains", "lost_referring_domains"],
        targets, from_file, output_format, login, password, verbose,
        extra_payload=extra,
    )
