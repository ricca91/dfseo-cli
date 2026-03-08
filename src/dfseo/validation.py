"""Input validation for dfseo CLI — anti-hallucination guards.

Validates and sanitizes all user inputs before they reach the API.
Agents hallucinate differently from humans: path traversal in keywords,
misspelled locations, control characters, impossibly long strings.
"""

from __future__ import annotations

import re
from difflib import get_close_matches
from typing import Any

# Common valid locations (subset — full list from API cached locally)
COMMON_LOCATIONS = {
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
    "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus",
    "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
    "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada",
    "Chad", "Chile", "China", "Colombia", "Costa Rica",
    "Croatia", "Cuba", "Cyprus", "Czechia", "Denmark",
    "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Estonia",
    "Ethiopia", "Fiji", "Finland", "France", "Georgia",
    "Germany", "Ghana", "Greece", "Guatemala", "Honduras",
    "Hong Kong", "Hungary", "Iceland", "India", "Indonesia",
    "Iran", "Iraq", "Ireland", "Israel", "Italy",
    "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya",
    "Kuwait", "Laos", "Latvia", "Lebanon", "Libya",
    "Lithuania", "Luxembourg", "Madagascar", "Malaysia", "Mali",
    "Malta", "Mauritius", "Mexico", "Moldova", "Mongolia",
    "Montenegro", "Morocco", "Mozambique", "Myanmar", "Nepal",
    "Netherlands", "New Zealand", "Nicaragua", "Nigeria", "North Macedonia",
    "Norway", "Oman", "Pakistan", "Panama", "Paraguay",
    "Peru", "Philippines", "Poland", "Portugal", "Qatar",
    "Romania", "Russia", "Rwanda", "Saudi Arabia", "Senegal",
    "Serbia", "Singapore", "Slovakia", "Slovenia", "Somalia",
    "South Africa", "South Korea", "Spain", "Sri Lanka", "Sudan",
    "Sweden", "Switzerland", "Syria", "Taiwan", "Tanzania",
    "Thailand", "Tunisia", "Turkey", "Uganda", "Ukraine",
    "United Arab Emirates", "United Kingdom", "United States",
    "Uruguay", "Uzbekistan", "Venezuela", "Vietnam", "Yemen",
    "Zambia", "Zimbabwe",
}


def validate_location(location: str) -> str:
    """Validate location name, suggest corrections if not found.

    Args:
        location: Location name to validate

    Returns:
        Validated location name

    Raises:
        ValueError: If location is unknown (with suggestions)
    """
    if location in COMMON_LOCATIONS:
        return location

    # Fuzzy match
    matches = get_close_matches(location, COMMON_LOCATIONS, n=3, cutoff=0.6)

    if matches:
        raise ValueError(
            f"Unknown location '{location}'. Did you mean: {', '.join(matches)}? "
            f"Run 'dfseo serp locations --search {location}' for valid options."
        )

    raise ValueError(
        f"Unknown location '{location}'. "
        f"Run 'dfseo serp locations' for the full list."
    )


def validate_target(target: str) -> str:
    """Validate and sanitize a domain/URL target.

    Args:
        target: Domain or URL to validate

    Returns:
        Sanitized target string

    Raises:
        ValueError: If target is invalid
    """
    if not target:
        raise ValueError("Target cannot be empty")

    if len(target) > 2048:
        raise ValueError(f"Target too long ({len(target)} chars, max 2048)")

    # Reject path traversal
    if ".." in target:
        raise ValueError(f"Invalid target '{target}': contains path traversal")

    # Reject control characters
    if any(ord(c) < 0x20 for c in target):
        raise ValueError(f"Invalid target: contains control characters")

    # Reject embedded query params in domain
    if "?" in target and not target.startswith("http"):
        raise ValueError(
            f"Invalid target '{target}': contains query parameters. "
            f"Pass a clean domain name (e.g. 'example.com') or a full URL."
        )

    # Reject percent-encoded strings in domain mode
    if "%" in target and not target.startswith("http"):
        raise ValueError(f"Invalid target '{target}': contains percent-encoded characters")

    return target


def validate_keyword(keyword: str) -> str:
    """Validate and sanitize a search keyword.

    Args:
        keyword: Keyword to validate

    Returns:
        Sanitized keyword

    Raises:
        ValueError: If keyword is invalid
    """
    if not keyword:
        raise ValueError("Keyword cannot be empty")

    # Reject control characters
    if any(ord(c) < 0x20 and c not in ('\n', '\r', '\t') for c in keyword):
        raise ValueError("Invalid keyword: contains control characters")

    # Reject extremely long keywords (likely hallucination)
    if len(keyword) > 500:
        raise ValueError(f"Keyword too long ({len(keyword)} chars, max 500)")

    # Warn on suspicious patterns (URL-like keywords)
    if keyword.startswith("http://") or keyword.startswith("https://"):
        import sys
        print(
            f"Warning: keyword looks like a URL: '{keyword}'. "
            f"Did you mean to use a target flag instead?",
            file=sys.stderr,
        )

    return keyword.strip()


def reject_control_chars(value: str, field_name: str) -> str:
    """Reject any input with control characters (below ASCII 0x20).

    Args:
        value: String to validate
        field_name: Name of field (for error messages)

    Returns:
        The validated string

    Raises:
        ValueError: If control characters found
    """
    if any(ord(c) < 0x20 and c not in ('\n', '\r', '\t') for c in value):
        raise ValueError(f"Invalid {field_name}: contains control characters")
    return value


def validate_positive_int(value: int, field_name: str, max_value: int | None = None) -> int:
    """Validate that an integer is positive and under the maximum.

    Args:
        value: Integer to validate
        field_name: Name of field (for error messages)
        max_value: Optional maximum value

    Returns:
        The validated integer

    Raises:
        ValueError: If value is out of range
    """
    if value < 1:
        raise ValueError(f"{field_name} must be positive, got {value}")
    if max_value and value > max_value:
        raise ValueError(f"{field_name} must be <= {max_value}, got {value}")
    return value


def validate_raw_params(raw_params: str) -> list[dict[str, Any]]:
    """Validate and parse raw JSON params.

    Wraps single objects in an array (DataForSEO expects arrays).
    Validates that string values don't contain control characters.

    Args:
        raw_params: Raw JSON string

    Returns:
        Parsed and validated list of dicts

    Raises:
        ValueError: If JSON is invalid or contains unsafe values
    """
    import json

    try:
        parsed = json.loads(raw_params)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in --raw-params: {e}")

    # Wrap in array if needed
    if isinstance(parsed, dict):
        parsed = [parsed]
    elif isinstance(parsed, list):
        pass
    else:
        raise ValueError("--raw-params must be a JSON object or array")

    # Validate string values for control chars
    _validate_json_values(parsed, "raw-params")

    return parsed


def _validate_json_values(obj: Any, path: str) -> None:
    """Recursively validate string values in a JSON structure."""
    if isinstance(obj, str):
        if any(ord(c) < 0x20 and c not in ('\n', '\r', '\t') for c in obj):
            raise ValueError(f"Invalid value in {path}: contains control characters")
        if ".." in obj and "/" in obj:
            raise ValueError(f"Invalid value in {path}: possible path traversal")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _validate_json_values(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _validate_json_values(v, f"{path}[{i}]")
