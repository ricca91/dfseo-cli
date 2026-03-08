"""Schema introspection commands for dfseo CLI.

Provides machine-readable schema information for agent consumption.
"""

from __future__ import annotations

from typing import Any

import typer

from dfseo.output import format_output, print_error

app = typer.Typer(help="Schema introspection for agent consumption")


@app.command("command")
def describe_command(
    command_path: str = typer.Argument(..., help="Command path to describe (e.g., 'serp google', 'keywords volume')"),
    output: str = typer.Option("json", "--output", "-o", help="Output format (json/table)"),
) -> None:
    """Describe a command's schema for agent consumption.
    
    Examples:
        dfseo describe "serp google"
        dfseo describe "keywords volume"
        dfseo describe "site audit"
    """
    # Parse command path
    parts = command_path.split()
    
    # Build schema info
    schema = {
        "command": command_path,
        "description": _get_command_description(parts),
        "parameters": _get_command_parameters(parts),
        "examples": _get_command_examples(parts),
    }
    
    if output == "table":
        print(_format_schema_table(schema))
    else:
        print(format_output(schema, "json"))


def _get_command_description(parts: list[str]) -> str:
    """Get description for command path."""
    descriptions = {
        "serp google": "Search Google SERP and get organic results with rankings.",
        "serp bing": "Search Bing SERP and get organic results.",
        "keywords volume": "Get search volume, CPC, and keyword difficulty.",
        "keywords suggestions": "Find long-tail keyword suggestions.",
        "site audit": "Run comprehensive site audit with crawl + summary.",
        "site crawl": "Start async site crawl and return task_id.",
        "backlinks summary": "Get backlink profile summary for a target.",
        "backlinks list": "List detailed backlinks with filters.",
    }
    return descriptions.get(" ".join(parts), f"Command: {parts}")


def _get_command_parameters(parts: list[str]) -> list[dict[str, Any]]:
    """Get parameters for command path."""
    # Common parameters across commands
    common_params = [
        {"name": "login", "type": "string", "required": False, "env": "DATAFORSEO_LOGIN"},
        {"name": "password", "type": "string", "required": False, "env": "DATAFORSEO_PASSWORD"},
        {"name": "output", "type": "enum", "options": ["json", "json-pretty", "table", "csv"], "default": "auto"},
        {"name": "verbose", "type": "boolean", "default": False},
    ]
    
    # Command-specific parameters
    command_params = {
        "serp": [
            {"name": "keyword", "type": "string", "required": True, "help": "Search keyword"},
            {"name": "location", "type": "string", "required": False, "default": "United States"},
            {"name": "language", "type": "string", "required": False, "default": "English"},
            {"name": "device", "type": "enum", "options": ["desktop", "mobile"], "default": "desktop"},
            {"name": "depth", "type": "integer", "min": 1, "max": 700, "default": 100},
        ],
        "keywords volume": [
            {"name": "keywords", "type": "array", "required": True, "help": "Keywords to analyze"},
            {"name": "location", "type": "string", "required": False, "default": "United States"},
            {"name": "language", "type": "string", "required": False, "default": "English"},
            {"name": "include_serp_info", "type": "boolean", "default": False},
        ],
        "site audit": [
            {"name": "target", "type": "string", "required": True, "help": "Domain or URL to audit"},
            {"name": "max_pages", "type": "integer", "min": 1, "default": 100},
            {"name": "enable_javascript", "type": "boolean", "default": False},
            {"name": "load_resources", "type": "boolean", "default": False},
            {"name": "dry_run", "type": "boolean", "default": False, "help": "Show estimated cost"},
        ],
        "backlinks summary": [
            {"name": "target", "type": "string", "required": True, "help": "Domain or URL"},
            {"name": "include_subdomains", "type": "boolean", "default": True},
            {"name": "dofollow_only", "type": "boolean", "default": False},
            {"name": "status", "type": "enum", "options": ["all", "live", "new", "lost"], "default": "all"},
            {"name": "dry_run", "type": "boolean", "default": False, "help": "Show estimated cost"},
        ],
    }
    
    key = " ".join(parts[:2]) if len(parts) >= 2 else parts[0]
    specific = command_params.get(key, [])
    
    return specific + common_params


def _get_command_examples(parts: list[str]) -> list[str]:
    """Get examples for command path."""
    examples = {
        "serp google": [
            'dfseo serp google "email hosting"',
            'dfseo serp google "pizza" --location "Italy" --language "Italian"',
        ],
        "keywords volume": [
            'dfseo keywords volume "seo tools" "keyword research"',
            'dfseo keywords volume "ai agents" --location "United States"',
        ],
        "site audit": [
            'dfseo site audit "example.com" --max-pages 50',
            'dfseo site audit "example.com" --dry-run',
        ],
        "backlinks summary": [
            'dfseo backlinks summary "example.com"',
            'dfseo backlinks summary "example.com" --dofollow-only',
        ],
    }
    key = " ".join(parts[:2]) if len(parts) >= 2 else parts[0]
    return examples.get(key, [])


def _format_schema_table(schema: dict[str, Any]) -> str:
    """Format schema as human-readable table."""
    lines = []
    lines.append(f"Command: {schema['command']}")
    lines.append(f"Description: {schema['description']}")
    lines.append("")
    lines.append("Parameters:")
    for param in schema['parameters']:
        req = "required" if param.get('required') else f"default: {param.get('default', 'none')}"
        lines.append(f"  --{param['name']} ({param['type']}) {req}")
    lines.append("")
    lines.append("Examples:")
    for ex in schema['examples']:
        lines.append(f"  {ex}")
    return "\n".join(lines)
