"""Authentication commands for dfseo CLI."""

import sys

import typer

from dfseo.client import AuthenticationError, DataForSeoClient
from dfseo.config import Config, DEFAULT_CONFIG_FILE
from dfseo.output import print_error, print_output

auth_app = typer.Typer(help="Manage authentication")


@auth_app.command()
def setup(
    login: str = typer.Option(None, prompt="Login", help="DataForSEO login email"),
    password: str = typer.Option(
        None, prompt="Password", hide_input=True, help="DataForSEO API password"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Set up DataForSEO credentials interactively."""
    try:
        # Validate credentials
        client = DataForSeoClient(login=login, password=password, verbose=verbose)
        user_data = client.get_user_data()
        client.close()

        # Save to config
        config = Config()
        config.set("auth", "login", login)
        config.set("auth", "password", password)
        config.save()

        # Output success
        result = {
            "status": "success",
            "message": f"Credentials saved to {DEFAULT_CONFIG_FILE}",
            "login": login,
            "balance": user_data.balance,
        }
        print_output(result, output_format="json")

    except AuthenticationError as e:
        print_error(f"Authentication failed: {e}")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)


@auth_app.command()
def status(
    login: str = typer.Option(None, "--login", help="DataForSEO login (overrides config)"),
    password: str = typer.Option(None, "--password", help="DataForSEO password (overrides config)"),
    output: str = typer.Option("json", "--output", "-o", help="Output format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Check authentication status and account balance."""
    try:
        client = DataForSeoClient(login=login, password=password, verbose=verbose)
        user_data = client.get_user_data()
        client.close()

        result = {
            "status": "authenticated",
            "login": user_data.login,
            "balance": user_data.balance,
            "rate_limit": user_data.rate_limit,
        }

        if output == "table":
            print(f"✓ Authenticated as {user_data.login}")
            print(f"Balance: ${user_data.balance:.2f}")
            print(f"Rate limit: {user_data.rate_limit} req/min")
        else:
            print_output(result, output_format=output)

    except AuthenticationError as e:
        print_error(f"✗ Not authenticated: {e}")
        if output != "json":
            print_error("Run 'dfseo auth setup' to configure credentials.")
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)
