"""Output formatting for dfseo CLI."""

import csv
import json
import sys
from typing import Any

from rich.console import Console
from rich.table import Table


def format_output(
    data: dict[str, Any],
    output_format: str = "json",
    quiet: bool = False,
) -> str:
    """Format data for output.

    Args:
        data: Data to format
        output_format: Output format (json, json-pretty, table, csv, auto)
        quiet: Suppress non-essential output

    Returns:
        Formatted string
    """
    # Auto-detect: use table for TTY, json for pipes
    if output_format == "auto" or output_format is None:
        if sys.stdout.isatty():
            output_format = "table"
        else:
            output_format = "json"
    
    if output_format == "json":
        return json.dumps(data, separators=(",", ":"))
    elif output_format == "json-pretty":
        return json.dumps(data, indent=2)
    elif output_format == "table":
        return _format_table(data)
    elif output_format == "csv":
        return _format_csv(data)
    else:
        return json.dumps(data, separators=(",", ":"))


def print_output(
    data: dict[str, Any],
    output_format: str = "json",
    quiet: bool = False,
) -> None:
    """Print formatted output to stdout.

    Args:
        data: Data to print
        output_format: Output format
        quiet: Suppress non-essential output
    """
    formatted = format_output(data, output_format, quiet)
    print(formatted)


def print_error(message: str) -> None:
    """Print error message to stderr.

    Args:
        message: Error message
    """
    print(message, file=sys.stderr)


def _format_table(data: dict[str, Any]) -> str:
    """Format SERP result as human-readable table.

    Args:
        data: SERP result data

    Returns:
        Formatted table string
    """
    console = Console(force_terminal=True)
    output_lines = []

    # Header info
    keyword = data.get("keyword", "N/A")
    location = data.get("location", "N/A")
    language = data.get("language", "N/A")
    device = data.get("device", "N/A")
    results_count = data.get("results_count", 0)
    cost = data.get("cost", 0)

    output_lines.append("")
    output_lines.append(f"[bold]Query:[/bold] {keyword}")
    output_lines.append(f"[bold]Location:[/bold] {location} | [bold]Language:[/bold] {language} | [bold]Device:[/bold] {device}")
    output_lines.append(f"[bold]Results:[/bold] {results_count} | [bold]Cost:[/bold] ${cost:.4f}")
    output_lines.append("")

    # SERP features summary
    features = data.get("serp_features", [])
    if features:
        output_lines.append(f"[dim]SERP Features: {', '.join(features)}[/dim]")
        output_lines.append("")

    # Organic results table
    organic = data.get("organic_results", [])
    if organic:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("#", style="cyan", width=4, justify="right")
        table.add_column("Domain", style="green", min_width=15, max_width=25)
        table.add_column("Title / Description", style="white", min_width=40)

        for item in organic[:15]:  # Limit to 15 for readability
            rank = str(item.get("rank", ""))
            domain = item.get("domain", "")[:23]
            
            # Combine title and description
            title = item.get("title", "")
            description = item.get("description", "")
            
            if description:
                content = f"[bold]{title[:50]}[/bold]\n[dim]{description[:80]}{'...' if len(description) > 80 else ''}[/dim]"
            else:
                content = f"[bold]{title[:80]}[/bold]"
            
            table.add_row(rank, domain, content)

        # Capture table output
        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

        if len(organic) > 15:
            output_lines.append(f"\n[dim]... and {len(organic) - 15} more results[/dim]")

    # Featured snippet
    snippet = data.get("featured_snippet")
    if snippet:
        output_lines.append("")
        output_lines.append("[bold yellow]Featured Snippet:[/bold yellow]")
        text = snippet.get("text", "")[:200]
        if len(snippet.get("text", "")) > 200:
            text += "..."
        output_lines.append(f"  {text}")
        output_lines.append(f"  [dim]Source: {snippet.get('source_domain', '')}[/dim]")

    # People Also Ask
    paa = data.get("people_also_ask", [])
    if paa:
        output_lines.append("")
        output_lines.append(f"[bold yellow]People Also Ask ({len(paa)}):[/bold yellow]")
        for item in paa[:5]:
            q = item.get("question", "")
            output_lines.append(f"  [cyan]•[/cyan] {q[:70]}{'...' if len(q) > 70 else ''}")

    output_lines.append("")
    return "\n".join(output_lines)


def _format_csv(data: dict[str, Any]) -> str:
    """Format organic results as CSV.

    Args:
        data: SERP result data

    Returns:
        CSV string
    """
    import io

    organic = data.get("organic_results", [])
    if not organic:
        return ""

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["rank", "rank_group", "domain", "url", "title", "description"],
        extrasaction="ignore",
    )
    writer.writeheader()
    for item in organic:
        writer.writerow(item)

    return output.getvalue()


def format_locations(locations: list[dict[str, Any]], output_format: str = "json") -> str:
    """Format locations list.

    Args:
        locations: List of location dictionaries
        output_format: Output format

    Returns:
        Formatted string
    """
    if output_format == "table":
        console = Console(force_terminal=True)
        table = Table(show_header=True, header_style="bold")
        table.add_column("Code", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Country", style="white")
        table.add_column("Type", style="blue")

        for loc in locations[:50]:  # Limit for display
            table.add_row(
                str(loc.get("location_code", "")),
                loc.get("location_name", "")[:40],
                loc.get("country_iso_code", "") or "-",
                loc.get("location_type", "") or "-",
            )

        with console.capture() as capture:
            console.print(table)
        return capture.get()
    elif output_format == "csv":
        import io

        output = io.StringIO()
        if locations:
            writer = csv.DictWriter(
                output,
                fieldnames=["location_code", "location_name", "country_iso_code", "location_type"],
                extrasaction="ignore",
            )
            writer.writeheader()
            for loc in locations:
                writer.writerow(loc)
        return output.getvalue()
    else:
        return json.dumps(locations, indent=2 if output_format == "json-pretty" else None)


def format_languages(languages: list[dict[str, Any]], output_format: str = "json") -> str:
    """Format languages list.

    Args:
        languages: List of language dictionaries
        output_format: Output format

    Returns:
        Formatted string
    """
    if output_format == "table":
        console = Console(force_terminal=True)
        table = Table(show_header=True, header_style="bold")
        table.add_column("Code", style="cyan")
        table.add_column("Name", style="green")

        for lang in languages[:50]:
            table.add_row(
                lang.get("language_code", ""),
                lang.get("language_name", ""),
            )

        with console.capture() as capture:
            console.print(table)
        return capture.get()
    elif output_format == "csv":
        import io

        output = io.StringIO()
        if languages:
            writer = csv.DictWriter(
                output,
                fieldnames=["language_code", "language_name"],
                extrasaction="ignore",
            )
            writer.writeheader()
            for lang in languages:
                writer.writerow(lang)
        return output.getvalue()
    else:
        return json.dumps(languages, indent=2 if output_format == "json-pretty" else None)


def format_compare(
    results: dict[str, Any],
    output_format: str = "json",
) -> str:
    """Format SERP compare results.

    Args:
        results: Compare results data
        output_format: Output format

    Returns:
        Formatted string
    """
    if output_format == "table":
        console = Console(force_terminal=True)
        output_lines = []

        keyword = results.get("keyword", "")
        engines = results.get("engines", [])

        output_lines.append(f"SERP Compare: '{keyword}'")
        output_lines.append(f"Engines: {', '.join(engines)}\n")

        # Summary
        summary = results.get("summary", {})
        table = Table(show_header=True, header_style="bold")
        table.add_column("Metric", style="cyan")
        for engine in engines:
            table.add_column(engine.capitalize(), style="green")

        table.add_row(
            "Total Results",
            *[str(summary.get(engine, {}).get("total", 0)) for engine in engines],
        )
        table.add_row(
            "Unique Domains",
            *[str(summary.get(engine, {}).get("unique_domains", 0)) for engine in engines],
        )
        table.add_row(
            "Common Domains",
            *[str(summary.get(engine, {}).get("common_domains", 0)) for engine in engines],
        )

        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

        # Common domains detail
        common = results.get("common_domains", [])
        if common:
            output_lines.append(f"\nCommon Domains ({len(common)}):")
            for domain in common[:10]:
                positions = domain.get("positions", {})
                pos_str = ", ".join([f"{e}: #{p}" for e, p in positions.items()])
                output_lines.append(f"  • {domain.get('domain', '')} ({pos_str})")

        return "\n".join(output_lines)
    else:
        return json.dumps(results, indent=2 if output_format == "json-pretty" else None)
