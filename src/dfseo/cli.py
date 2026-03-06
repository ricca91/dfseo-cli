"""Main CLI entry point for dfseo."""

from __future__ import annotations

import sys

import typer

from dfseo.commands.auth import auth_app
from dfseo.commands.config import config_app
from dfseo.commands.keywords import keywords_app
from dfseo.commands.serp import serp_app
from dfseo.output import print_error

app = typer.Typer(
    name="dfseo",
    help="DataForSEO CLI for AI Agents - SERP data from your terminal",
    no_args_is_help=True,
)

# Register subcommands
app.add_typer(auth_app, name="auth")
app.add_typer(config_app, name="config")
app.add_typer(keywords_app, name="keywords")
app.add_typer(serp_app, name="serp")


def _version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        from dfseo import __version__

        print(__version__)
        raise typer.Exit(0)


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-V", help="Show version", callback=_version_callback
    ),
) -> None:
    """DataForSEO CLI - SEO data from your terminal.

    JSON-first, machine-readable, human-friendly.
    """
    pass


def cli_main() -> None:
    """Entry point for the CLI."""
    try:
        app()
    except KeyboardInterrupt:
        print_error("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli_main()
