"""Cost estimation for DataForSEO API calls.

Approximate costs per endpoint. Not contractual — actual costs may vary.
See https://dataforseo.com/pricing for current pricing.
"""

from __future__ import annotations

import json
from typing import Any

# Cost per request by endpoint (approximate, USD)
COST_PER_REQUEST: dict[str, float] = {
    # SERP
    "serp/google/organic/live/advanced": 0.002,
    "serp/bing/organic/live/advanced": 0.002,
    "serp/youtube/organic/live/advanced": 0.002,
    # Keywords / DataForSEO Labs
    "dataforseo_labs/google/keyword_overview/live": 0.0105,
    "dataforseo_labs/google/keyword_suggestions/live": 0.021,
    "dataforseo_labs/google/keyword_ideas/live": 0.021,
    "dataforseo_labs/google/bulk_keyword_difficulty/live": 0.0103,
    "dataforseo_labs/google/search_intent/live": 0.01,
    "dataforseo_labs/google/relevant_pages/live": 0.021,
    "dataforseo_labs/google/keywords_for_site/live": 0.021,
    "dataforseo_labs/google/ranked_keywords/live": 0.021,
    "dataforseo_labs/google/domain_rank_overview/live": 0.021,
    "dataforseo_labs/google/historical_rank_overview/live": 0.021,
    "dataforseo_labs/google/historical_search_volume/live": 0.021,
    "dataforseo_labs/google/serp_competitors/live": 0.021,
    "dataforseo_labs/google/competitors_domain/live": 0.021,
    "dataforseo_labs/google/domain_intersection/live": 0.021,
    "dataforseo_labs/google/subdomains/live": 0.021,
    "dataforseo_labs/google/top_searches/live": 0.021,
    "dataforseo_labs/google/categories_for_domain/live": 0.021,
    "dataforseo_labs/google/page_intersection/live": 0.021,
    # Google Ads
    "keywords_data/google_ads/search_volume/live": 0.005,
    "keywords_data/google_ads/keywords_for_keywords/live": 0.005,
    # On-Page
    "on_page/task_post": 0.0005,  # per page crawled
    "on_page/instant_pages": 0.00025,
    "on_page/lighthouse/task_post": 0.002,
    # Backlinks
    "backlinks/summary/live": 0.02,
    "backlinks/backlinks/live": 0.02,
    "backlinks/anchors/live": 0.02,
    "backlinks/referring_domains/live": 0.02,
    "backlinks/domain_intersection/live": 0.02,
    "backlinks/bulk_ranks/live": 0.02,
    "backlinks/bulk_backlinks/live": 0.02,
    "backlinks/bulk_spam_score/live": 0.02,
    "backlinks/bulk_referring_domains/live": 0.02,
    "backlinks/bulk_new_lost_summary/live": 0.02,
    "backlinks/history/live": 0.02,
    "backlinks/competitors/live": 0.02,
    "backlinks/page_intersection/live": 0.02,
    "backlinks/pages_summary/live": 0.02,
    # Content Analysis
    "content_analysis/search/live": 0.01,
    "content_analysis/summary/live": 0.01,
    "content_analysis/sentiment_analysis/live": 0.01,
    # Domain Analytics
    "domain_analytics/technologies/domain_technologies/live": 0.01,
    # SERP Autocomplete
    "serp/google/autocomplete/live/advanced": 0.002,
    # On-Page extras
    "on_page/keyword_density": 0.0005,
    "on_page/microdata": 0.0005,
    "on_page/waterfall": 0.001,
}


def estimate_cost(endpoint: str, params: dict[str, Any] | None = None) -> float:
    """Estimate the cost of a single API call.

    Args:
        endpoint: API endpoint path (without /v3/ prefix)
        params: Request parameters (for per-unit calculations)

    Returns:
        Estimated cost in USD
    """
    # Strip leading/trailing slashes and /v3/ prefix
    clean = endpoint.strip("/")
    if clean.startswith("v3/"):
        clean = clean[3:]

    base = COST_PER_REQUEST.get(clean, 0)

    # For on_page/task_post, multiply by max_crawl_pages
    if "on_page/task_post" in clean and params:
        pages = params.get("max_crawl_pages", 100)
        # Cost multipliers for JS/resources
        multiplier = 1.0
        if params.get("enable_browser_rendering"):
            multiplier = max(multiplier, 3.0)
        elif params.get("enable_javascript"):
            multiplier = max(multiplier, 2.0)
        if params.get("load_resources"):
            multiplier = max(multiplier, 1.5)
        base = base * pages * multiplier

    return base


def format_cost(cost: float) -> str:
    """Format a cost value as a USD string."""
    return f"${cost:.4f}"


def format_dry_run_output(
    endpoint: str,
    request_body: list[dict[str, Any]] | None,
    params: dict[str, Any] | None = None,
    validation: str = "passed",
    errors: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Build standardized dry-run output.

    Args:
        endpoint: Full API endpoint (e.g. "POST /v3/serp/google/organic/live/advanced")
        request_body: The request body that would be sent
        params: Parameters for cost estimation
        validation: "passed" or "failed"
        errors: List of validation errors (if any)

    Returns:
        Standardized dry-run output dict
    """
    cost = estimate_cost(endpoint.split(" ", 1)[-1] if " " in endpoint else endpoint, params)

    result: dict[str, Any] = {
        "dry_run": True,
        "endpoint": endpoint,
        "request_body": request_body,
        "estimated_cost": format_cost(cost),
        "estimated_cost_note": "Estimated cost, actual cost may vary",
        "validation": validation,
    }

    if errors:
        result["errors"] = errors
        result["validation"] = "failed"
        result["request_body"] = None
        result["estimated_cost"] = None

    return result
