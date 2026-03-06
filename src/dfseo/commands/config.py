"""Configuration commands for dfseo CLI."""

import sys

import typer

from dfseo.config import Config, DEFAULT_CONFIG_FILE, DEFAULTS
from dfseo.output import print_error, print_output

config_app = typer.Typer(help="Manage configuration")

VALID_KEYS = ["location", "language", "device", "output"]
VALID_OUTPUTS = ["json", "json-pretty", "table", "csv"]
VALID_DEVICES = ["desktop", "mobile"]


@config_app.command()
def set(
    key: str = typer.Argument(..., help="Configuration key (location, language, device, output)"),
    value: str = typer.Argument(..., help="Configuration value"),
) -> None:
    """Set a default configuration value."""
    # Normalize key
    key_mapping = {
        "location": "location_name",
        "language": "language_name",
        "device": "device",
        "output": "output",
    }

    if key not in key_mapping:
        print_error(f"Invalid key: {key}. Valid keys: {', '.join(VALID_KEYS)}")
        raise typer.Exit(code=4)

    config_key = key_mapping[key]

    # Validate value for certain keys
    if key == "output" and value not in VALID_OUTPUTS:
        print_error(f"Invalid output format: {value}. Valid: {', '.join(VALID_OUTPUTS)}")
        raise typer.Exit(code=4)

    if key == "device" and value not in VALID_DEVICES:
        print_error(f"Invalid device: {value}. Valid: {', '.join(VALID_DEVICES)}")
        raise typer.Exit(code=4)

    try:
        config = Config()
        config.set("defaults", config_key, value)
        config.save()

        result = {
            "status": "success",
            "key": key,
            "value": value,
            "config_file": str(DEFAULT_CONFIG_FILE),
        }
        print_output(result, output_format="json")

    except Exception as e:
        print_error(f"Error saving configuration: {e}")
        raise typer.Exit(code=1)


@config_app.command("show")
def show_config(
    output: str = typer.Option("json", "--output", "-o", help="Output format"),
) -> None:
    """Show current configuration."""
    try:
        config = Config()
        config_dict = config.to_dict()

        if output == "table":
            print(f"Configuration file: {DEFAULT_CONFIG_FILE}")
            print()
            print("[auth]")
            auth = config_dict.get("auth", {})
            print(f"  login: {auth.get('login', 'not set')}")
            print(f"  password: {auth.get('password', 'not set')}")
            print()
            print("[defaults]")
            defaults = config_dict.get("defaults", {})
            for k, v in defaults.items():
                print(f"  {k}: {v}")
        else:
            print_output(config_dict, output_format=output)

    except Exception as e:
        print_error(f"Error reading configuration: {e}")
        raise typer.Exit(code=1)
