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
        output_format: Output format (json, json-pretty, table, csv)
        quiet: Suppress non-essential output

    Returns:
        Formatted string
    """
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
    """Format SERP result as table.

    Args:
        data: SERP result data

    Returns:
        Formatted table string
    """
    console = Console(force_terminal=True)
    output_lines = []

    # Header info
    keyword = data.get("keyword", "")
    location = data.get("location", "")
    device = data.get("device", "")
    results_count = data.get("results_count", 0)

    output_lines.append(
        f"Keyword: {keyword} | Location: {location} | Device: {device} | Results: {results_count}"
    )
    output_lines.append("")

    # Organic results table
    organic = data.get("organic_results", [])
    if organic:
        table = Table(show_header=True, header_style="bold")
        table.add_column("#", style="cyan", width=4)
        table.add_column("Domain", style="green", min_width=20)
        table.add_column("Title", style="white", min_width=30)
        table.add_column("URL", style="blue", min_width=20)

        for item in organic[:20]:  # Limit to 20 for table view
            rank = str(item.get("rank", ""))
            domain = item.get("domain", "")[:25]
            title = item.get("title", "")[:40]
            url = item.get("url", "")[:35]
            if len(url) == 35:
                url = url[:32] + "..."
            table.add_row(rank, domain, title, url)

        # Capture table output
        with console.capture() as capture:
            console.print(table)
        output_lines.append(capture.get())

    # SERP features
    features = data.get("serp_features", [])
    if features:
        output_lines.append(f"\nSERP Features: {', '.join(features)}")

    # Featured snippet
    snippet = data.get("featured_snippet")
    if snippet:
        output_lines.append(f"\nFeatured Snippet:")
        text = snippet.get("text", "")[:100]
        if len(snippet.get("text", "")) > 100:
            text += "..."
        output_lines.append(f"  {text}")
        output_lines.append(f"  Source: {snippet.get('source_domain', '')}")

    # People Also Ask
    paa = data.get("people_also_ask", [])
    if paa:
        output_lines.append(f"\nPeople Also Ask ({len(paa)} items):")
        for item in paa[:5]:
            q = item.get("question", "")
            output_lines.append(f"  • {q[:60]}{'...' if len(q) > 60 else ''}")

    # Cost
    cost = data.get("cost", 0)
    output_lines.append(f"\nCost: ${cost:.4f}")

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
