"""Configuration management for dfseo CLI."""

import os
from pathlib import Path
from typing import Any

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Fallback for older Python

DEFAULT_CONFIG_DIR = Path.home() / ".config" / "dfseo"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.toml"

DEFAULTS = {
    "location_name": "United States",
    "language_name": "English",
    "device": "desktop",
    "output": "json",
}


class Config:
    """Configuration manager for dfseo CLI."""

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize configuration.

        Args:
            config_path: Path to config file. Defaults to ~/.config/dfseo/config.toml
        """
        self.config_path = config_path or DEFAULT_CONFIG_FILE
        self._data: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "rb") as f:
                    self._data = tomli.load(f)
            except Exception:
                self._data = {}
        else:
            self._data = {}

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            section: Configuration section (e.g., 'auth', 'defaults')
            key: Configuration key
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        return self._data.get(section, {}).get(key, default)

    def get_auth(self) -> tuple[str | None, str | None]:
        """Get authentication credentials from config file.

        Returns:
            Tuple of (login, password) or (None, None) if not set
        """
        login = self.get("auth", "login")
        password = self.get("auth", "password")
        return login, password

    def get_default(self, key: str) -> Any:
        """Get a default value from configuration.

        Args:
            key: Configuration key (e.g., 'location_name', 'device')

        Returns:
            Configuration value or built-in default
        """
        return self.get("defaults", key, DEFAULTS.get(key))

    def resolve_auth(
        self,
        login: str | None = None,
        password: str | None = None,
    ) -> tuple[str, str]:
        """Resolve authentication credentials.

        Priority:
        1. Inline flags (login, password)
        2. Environment variables (DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD)
        3. Config file (~/.config/dfseo/config.toml)

        Args:
            login: Optional inline login
            password: Optional inline password

        Returns:
            Tuple of (login, password)

        Raises:
            ValueError: If credentials cannot be resolved
        """
        # Priority 1: Inline flags
        if login and password:
            return login, password

        # Priority 2: Environment variables
        env_login = os.environ.get("DATAFORSEO_LOGIN")
        env_password = os.environ.get("DATAFORSEO_PASSWORD")
        if env_login and env_password:
            return env_login, env_password

        # Priority 3: Config file
        config_login, config_password = self.get_auth()
        if config_login and config_password:
            return config_login, config_password

        raise ValueError(
            "Authentication credentials not found. "
            "Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD environment variables, "
            "or run 'dfseo auth setup' to configure credentials."
        )

    def set(self, section: str, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if section not in self._data:
            self._data[section] = {}
        self._data[section][key] = value

    def save(self) -> None:
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        # Simple TOML serialization (no tomli_w, so we write manually)
        lines = []
        for section, values in self._data.items():
            lines.append(f"[{section}]")
            for key, value in values.items():
                if isinstance(value, str):
                    escaped = value.replace('\\', '\\\\').replace('"', '\\"')
                    lines.append(f'{key} = "{escaped}"')
                elif isinstance(value, bool):
                    lines.append(f"{key} = {str(value).lower()}")
                elif isinstance(value, (int, float)):
                    lines.append(f"{key} = {value}")
            lines.append("")

        with open(self.config_path, "w") as f:
            f.write("\n".join(lines))

    def to_dict(self) -> dict[str, Any]:
        """Return configuration as dictionary."""
        return {
            "auth": {
                "login": self.get("auth", "login", "***") if self.get("auth", "login") else None,
                "password": "***" if self.get("auth", "password") else None,
            },
            "defaults": {
                "location_name": self.get_default("location_name"),
                "language_name": self.get_default("language_name"),
                "device": self.get_default("device"),
                "output": self.get_default("output"),
            },
        }
