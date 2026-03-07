"""Main CLI entry point for dfseo."""

from __future__ import annotations

import sys

import typer

from dfseo.commands.auth import auth_app
from dfseo.commands.config import config_app
from dfseo.commands.keywords import keywords_app
from dfseo.commands.serp import serp_app
from dfseo.commands.site import app as site_app
from dfseo.commands.backlinks import app as backlinks_app
from dfseo.output import print_error

app = typer.Typer(
    name="dfseo",
    help="DataForSEO CLI for AI Agents - SERP data from your terminal",
    no_args_is_help=False,  # We'll handle this manually to show banner
)

# Register subcommands
app.add_typer(auth_app, name="auth")
app.add_typer(config_app, name="config")
app.add_typer(keywords_app, name="keywords")
app.add_typer(serp_app, name="serp")
app.add_typer(site_app, name="site")
app.add_typer(backlinks_app, name="backlinks")


def _version_callback(value: bool) -> None:
    """Print version with banner and exit."""
    if value:
        from dfseo.banner import show_version_banner
        from dfseo import __version__
        show_version_banner(__version__)
        raise typer.Exit(0)


def _show_banner_callback(ctx: typer.Context) -> None:
    """Show banner when no command is provided."""
    if ctx.invoked_subcommand is None:
        from dfseo.banner import show_banner
        show_banner()
        # Also show help
        print(ctx.get_help())
        raise typer.Exit(0)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False, "--version", "-V", help="Show version", callback=_version_callback,
        is_eager=True,  # Process version before banner
    ),
) -> None:
    """DataForSEO CLI - SEO data from your terminal.

    JSON-first, machine-readable, human-friendly.
    """
    _show_banner_callback(ctx)


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
