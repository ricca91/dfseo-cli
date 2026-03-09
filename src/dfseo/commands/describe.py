"""Schema introspection commands for dfseo CLI.

Provides machine-readable schema information for agent consumption.
Usage:
    dfseo describe "serp google"   # JSON schema of one command
    dfseo describe serp            # All commands in a group
    dfseo describe --list          # All available commands
"""

from __future__ import annotations

import json
from typing import Any

import typer

app = typer.Typer(help="Schema introspection for agent consumption")


# ---------------------------------------------------------------------------
# COMMAND_META — one entry per leaf command
# ---------------------------------------------------------------------------

COMMAND_META: dict[str, dict[str, Any]] = {
    # ---- SERP ----
    "serp google": {
        "description": "Search Google SERP for a keyword with location and language targeting",
        "api_endpoint": "POST /v3/serp/google/organic/live/advanced",
        "cost_estimate": "$0.002 per request",
        "arguments": [
            {"name": "keyword", "type": "string", "required": True, "description": "The search keyword"},
        ],
        "options": [
            {"name": "--location", "short": "-l", "type": "string", "default": "from config", "description": "Location name (e.g. 'Italy')"},
            {"name": "--language", "short": "-L", "type": "string", "default": "from config", "description": "Language name (e.g. 'Italian')"},
            {"name": "--device", "short": "-d", "type": "enum", "default": "desktop", "valid_values": ["desktop", "mobile"]},
            {"name": "--os", "type": "enum", "valid_values": ["windows", "macos", "ios", "android"]},
            {"name": "--depth", "short": "-n", "type": "integer", "default": 100, "description": "Number of results (max 700)"},
            {"name": "--output", "short": "-o", "type": "enum", "default": "json", "valid_values": ["json", "json-pretty", "table", "csv"]},
            {"name": "--dry-run", "type": "boolean", "default": False, "description": "Validate and show estimated cost without sending"},
            {"name": "--fields", "short": "-f", "type": "string", "description": "Comma-separated fields to include in output (supports dot notation)"},
            {"name": "--raw-params", "type": "json", "description": "Raw JSON payload sent directly to the API, bypasses all flags"},
        ],
        "output_fields": ["keyword", "location", "language", "device", "results_count", "serp_features", "organic_results", "featured_snippet", "people_also_ask", "cost", "timestamp"],
        "output_fields_nested": {
            "organic_results[]": ["rank", "rank_group", "domain", "url", "title", "description", "breadcrumb"],
        },
    },
    "serp bing": {
        "description": "Search Bing SERP for a keyword",
        "api_endpoint": "POST /v3/serp/bing/organic/live/advanced",
        "cost_estimate": "$0.002 per request",
        "arguments": [{"name": "keyword", "type": "string", "required": True}],
        "options": [
            {"name": "--location", "short": "-l", "type": "string", "default": "from config"},
            {"name": "--language", "short": "-L", "type": "string", "default": "from config"},
            {"name": "--device", "short": "-d", "type": "enum", "default": "desktop", "valid_values": ["desktop", "mobile"]},
            {"name": "--depth", "short": "-n", "type": "integer", "default": 100},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["keyword", "location", "language", "device", "results_count", "organic_results", "cost", "timestamp"],
    },
    "serp youtube": {
        "description": "Search YouTube SERP for a keyword",
        "api_endpoint": "POST /v3/serp/youtube/organic/live/advanced",
        "cost_estimate": "$0.002 per request",
        "arguments": [{"name": "keyword", "type": "string", "required": True}],
        "options": [
            {"name": "--location", "short": "-l", "type": "string", "default": "from config"},
            {"name": "--language", "short": "-L", "type": "string", "default": "from config"},
            {"name": "--depth", "short": "-n", "type": "integer", "default": 100},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["keyword", "location", "language", "device", "results_count", "organic_results", "cost", "timestamp"],
    },
    "serp compare": {
        "description": "Compare SERP results across search engines",
        "api_endpoint": "Multiple (one per engine)",
        "cost_estimate": "$0.002 per engine",
        "arguments": [{"name": "keyword", "type": "string", "required": True}],
        "options": [
            {"name": "--engines", "short": "-e", "type": "string", "default": "google,bing"},
            {"name": "--location", "short": "-l", "type": "string", "default": "from config"},
            {"name": "--depth", "short": "-n", "type": "integer", "default": 50},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
        ],
        "output_fields": ["keyword", "engines", "summary", "common_domains", "unique_domains"],
    },
    "serp locations": {
        "description": "List available locations for SERP targeting",
        "api_endpoint": "GET /v3/serp/google/locations",
        "cost_estimate": "Free",
        "options": [{"name": "--search", "short": "-s", "type": "string", "description": "Filter locations by name"}],
        "output_fields": ["location_code", "location_name", "country_iso_code", "location_type"],
    },
    "serp languages": {
        "description": "List available languages for SERP targeting",
        "api_endpoint": "GET /v3/serp/google/languages",
        "cost_estimate": "Free",
        "options": [{"name": "--search", "short": "-s", "type": "string"}],
        "output_fields": ["language_code", "language_name"],
    },

    # ---- KEYWORDS ----
    "keywords volume": {
        "description": "Get search volume, CPC, competition, and keyword difficulty",
        "api_endpoint": "POST /v3/dataforseo_labs/google/keyword_overview/live",
        "cost_estimate": "$0.0105 per request",
        "arguments": [{"name": "keywords", "type": "string[]", "required": True, "description": "Keywords to analyze (up to 700)"}],
        "options": [
            {"name": "--location", "short": "-l", "type": "string", "default": "from config"},
            {"name": "--language", "short": "-L", "type": "string", "default": "from config"},
            {"name": "--from-file", "type": "string", "description": "Load keywords from file (one per line)"},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["keyword", "search_volume", "cpc", "competition", "keyword_difficulty", "monthly_searches"],
    },
    "keywords suggestions": {
        "description": "Find long-tail keyword suggestions containing the seed keyword",
        "api_endpoint": "POST /v3/dataforseo_labs/google/keyword_suggestions/live",
        "cost_estimate": "$0.021 per request",
        "arguments": [{"name": "keyword", "type": "string", "required": True}],
        "options": [
            {"name": "--location", "short": "-l", "type": "string", "default": "from config"},
            {"name": "--min-volume", "type": "integer"},
            {"name": "--max-difficulty", "type": "integer"},
            {"name": "--limit", "type": "integer", "default": 100},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["keyword", "search_volume", "cpc", "competition", "keyword_difficulty"],
    },
    "keywords ideas": {
        "description": "Find semantically related keywords (not necessarily containing the seed)",
        "api_endpoint": "POST /v3/dataforseo_labs/google/keyword_ideas/live",
        "cost_estimate": "$0.021 per request",
        "arguments": [{"name": "keywords", "type": "string[]", "required": True}],
        "options": [
            {"name": "--location", "short": "-l", "type": "string"},
            {"name": "--limit", "type": "integer", "default": 100},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["keyword", "search_volume", "cpc", "competition", "keyword_difficulty"],
    },
    "keywords difficulty": {
        "description": "Get keyword difficulty for up to 1000 keywords at once",
        "api_endpoint": "POST /v3/dataforseo_labs/google/bulk_keyword_difficulty/live",
        "cost_estimate": "$0.0103 per request",
        "arguments": [{"name": "keywords", "type": "string[]", "required": True}],
        "options": [
            {"name": "--location", "short": "-l", "type": "string"},
            {"name": "--from-file", "type": "string"},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["keyword", "keyword_difficulty"],
    },
    "keywords search-intent": {
        "description": "Classify search intent for up to 1000 keywords",
        "api_endpoint": "POST /v3/dataforseo_labs/google/search_intent/live",
        "cost_estimate": "$0.01 per request",
        "arguments": [{"name": "keywords", "type": "string[]", "required": True}],
        "options": [
            {"name": "--location", "short": "-l", "type": "string"},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["keyword", "search_intent", "secondary_intent"],
    },
    "keywords for-site": {
        "description": "Find keywords relevant to a specific domain",
        "api_endpoint": "POST /v3/dataforseo_labs/google/keywords_for_site/live",
        "cost_estimate": "$0.021 per request",
        "arguments": [{"name": "target", "type": "string", "required": True, "description": "Domain to analyze"}],
        "options": [
            {"name": "--location", "short": "-l", "type": "string"},
            {"name": "--min-volume", "type": "integer"},
            {"name": "--sort", "type": "enum", "valid_values": ["relevance", "volume", "cpc", "difficulty"]},
            {"name": "--limit", "type": "integer", "default": 100},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["keyword", "search_volume", "cpc", "competition", "keyword_difficulty"],
    },
    "keywords ads-volume": {
        "description": "Get Google Ads volume data (max 20 keywords, 12 req/min)",
        "api_endpoint": "POST /v3/keywords_data/google_ads/search_volume/live",
        "cost_estimate": "$0.005 per request",
        "arguments": [{"name": "keywords", "type": "string[]", "required": True}],
        "options": [
            {"name": "--location", "short": "-l", "type": "string"},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["keyword", "search_volume", "cpc", "competition", "monthly_searches"],
    },
    "keywords ads-suggestions": {
        "description": "Get keyword suggestions from Google Ads (max 20 seeds, 12 req/min)",
        "api_endpoint": "POST /v3/keywords_data/google_ads/keywords_for_keywords/live",
        "cost_estimate": "$0.005 per request",
        "arguments": [{"name": "keywords", "type": "string[]", "required": True}],
        "options": [
            {"name": "--location", "short": "-l", "type": "string"},
            {"name": "--limit", "type": "integer", "default": 100},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["keyword", "search_volume", "cpc", "competition"],
    },

    # ---- SITE ----
    "site audit": {
        "description": "Run comprehensive site audit with crawl + summary",
        "api_endpoint": "POST /v3/on_page/task_post",
        "cost_estimate": "$0.001 per page (more with JS/browser)",
        "arguments": [{"name": "target", "type": "string", "required": True, "description": "Domain or URL to audit"}],
        "options": [
            {"name": "--max-pages", "short": "-n", "type": "integer", "default": 100},
            {"name": "--enable-javascript", "type": "boolean", "default": False, "description": "Execute JavaScript (costs extra)"},
            {"name": "--load-resources", "type": "boolean", "default": False},
            {"name": "--enable-browser-rendering", "type": "boolean", "default": False},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
        ],
        "output_fields": ["target", "crawl_progress", "pages_crawled", "onpage_score", "errors", "warnings", "cost", "timestamp"],
    },
    "site crawl": {
        "description": "Start async site crawl and return task_id",
        "api_endpoint": "POST /v3/on_page/task_post",
        "cost_estimate": "$0.001 per page",
        "arguments": [{"name": "target", "type": "string", "required": True}],
        "options": [
            {"name": "--max-pages", "short": "-n", "type": "integer", "default": 100},
            {"name": "--enable-javascript", "type": "boolean", "default": False},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
        ],
        "output_fields": ["task_id", "target", "status", "cost", "timestamp"],
    },
    "site summary": {
        "description": "Get crawl summary for a task",
        "api_endpoint": "POST /v3/on_page/summary",
        "cost_estimate": "Free (reads existing task)",
        "arguments": [{"name": "task_id", "type": "string", "required": True}],
        "options": [
            {"name": "--wait", "type": "boolean", "default": True},
            {"name": "--timeout", "type": "integer", "default": 300},
            {"name": "--fields", "type": "string"},
        ],
        "output_fields": ["task_id", "crawl_progress", "pages_crawled", "onpage_score", "errors", "warnings"],
    },
    "site pages": {
        "description": "List crawled pages with metrics",
        "api_endpoint": "POST /v3/on_page/pages",
        "cost_estimate": "Free (reads existing task)",
        "arguments": [{"name": "task_id", "type": "string", "required": True}],
        "options": [
            {"name": "--errors-only", "type": "boolean", "default": False},
            {"name": "--status-code", "type": "integer"},
            {"name": "--sort", "type": "enum", "valid_values": ["onpage_score", "status_code", "size", "load_time"]},
            {"name": "--fields", "type": "string"},
        ],
        "output_fields": ["url", "status_code", "onpage_score", "size", "load_time", "meta_title", "meta_description"],
    },
    "site links": {
        "description": "Analyze links (internal, external, broken)",
        "api_endpoint": "POST /v3/on_page/links",
        "cost_estimate": "Free (reads existing task)",
        "arguments": [{"name": "task_id", "type": "string", "required": True}],
        "options": [{"name": "--type", "type": "enum", "valid_values": ["broken", "internal", "external", "redirect"]}],
        "output_fields": ["url_from", "url_to", "type", "dofollow", "anchor"],
    },
    "site duplicates": {
        "description": "Find duplicate content",
        "api_endpoint": "POST /v3/on_page/duplicate_tags",
        "cost_estimate": "Free (reads existing task)",
        "arguments": [{"name": "task_id", "type": "string", "required": True}],
        "options": [{"name": "--type", "type": "enum", "valid_values": ["title", "description", "content"]}],
        "output_fields": ["url", "duplicate_type", "value", "count"],
    },
    "site redirects": {
        "description": "Analyze redirect chains",
        "api_endpoint": "POST /v3/on_page/redirect_chains",
        "cost_estimate": "Free (reads existing task)",
        "arguments": [{"name": "task_id", "type": "string", "required": True}],
        "output_fields": ["url_from", "url_to", "status_code", "is_redirect"],
    },
    "site non-indexable": {
        "description": "Find pages that can't be indexed",
        "api_endpoint": "POST /v3/on_page/non_indexable",
        "cost_estimate": "Free (reads existing task)",
        "arguments": [{"name": "task_id", "type": "string", "required": True}],
        "output_fields": ["url", "reason", "meta_robots"],
    },
    "site resources": {
        "description": "Analyze resources (images, CSS, JS)",
        "api_endpoint": "POST /v3/on_page/resources",
        "cost_estimate": "Free (reads existing task)",
        "arguments": [{"name": "task_id", "type": "string", "required": True}],
        "options": [
            {"name": "--type", "type": "enum", "valid_values": ["image", "script", "stylesheet", "broken"]},
            {"name": "--min-size", "type": "string"},
        ],
        "output_fields": ["url", "resource_type", "size", "status_code"],
    },
    "site lighthouse": {
        "description": "Run Lighthouse performance audit",
        "api_endpoint": "POST /v3/on_page/lighthouse/task_post",
        "cost_estimate": "$0.002 per URL",
        "arguments": [{"name": "url", "type": "string", "required": True, "description": "URL to audit"}],
        "options": [
            {"name": "--categories", "type": "string", "description": "Comma-separated: performance,seo,accessibility,best-practices,pwa"},
            {"name": "--wait", "type": "boolean", "default": True},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
        ],
        "output_fields": ["url", "scores", "audits", "cost", "timestamp"],
    },
    "site tasks": {
        "description": "List all your On-Page tasks",
        "api_endpoint": "GET /v3/on_page/tasks_ready",
        "cost_estimate": "Free",
        "output_fields": ["task_id", "target", "status", "date_posted", "pages_crawled"],
    },

    # ---- BACKLINKS ----
    "backlinks summary": {
        "description": "Get comprehensive backlink profile overview",
        "api_endpoint": "POST /v3/backlinks/summary/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "target", "type": "string", "required": True, "description": "Domain or URL"}],
        "options": [
            {"name": "--include-subdomains", "type": "boolean", "default": True},
            {"name": "--dofollow-only", "type": "boolean", "default": False},
            {"name": "--status", "type": "enum", "valid_values": ["all", "live", "new", "lost"]},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["target", "rank", "backlinks", "referring_domains", "spam_score", "links_summary", "cost", "timestamp"],
    },
    "backlinks list": {
        "description": "Get detailed list of backlinks with filtering",
        "api_endpoint": "POST /v3/backlinks/backlinks/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "target", "type": "string", "required": True}],
        "options": [
            {"name": "--dofollow-only", "type": "boolean", "default": False},
            {"name": "--status", "type": "enum", "valid_values": ["all", "live", "new", "lost", "broken"]},
            {"name": "--sort", "type": "enum", "valid_values": ["rank", "page_from_rank", "domain_from_rank", "first_seen", "last_seen"]},
            {"name": "--limit", "type": "integer", "default": 100},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["url_from", "url_to", "domain_from", "anchor", "rank", "dofollow"],
    },
    "backlinks anchors": {
        "description": "Analyze anchor text distribution",
        "api_endpoint": "POST /v3/backlinks/anchors/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "target", "type": "string", "required": True}],
        "options": [
            {"name": "--search", "type": "string"},
            {"name": "--sort", "type": "enum", "valid_values": ["backlinks", "referring_domains"]},
            {"name": "--limit", "type": "integer", "default": 100},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["anchor", "backlinks", "referring_domains"],
    },
    "backlinks referring-domains": {
        "description": "List domains linking to the target",
        "api_endpoint": "POST /v3/backlinks/referring_domains/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "target", "type": "string", "required": True}],
        "options": [
            {"name": "--min-backlinks", "type": "integer"},
            {"name": "--sort", "type": "enum", "valid_values": ["rank", "backlinks"]},
            {"name": "--limit", "type": "integer", "default": 100},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["domain", "rank", "backlinks"],
    },
    "backlinks history": {
        "description": "View backlink profile history over time",
        "api_endpoint": "POST /v3/backlinks/history/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "target", "type": "string", "required": True}],
        "options": [
            {"name": "--from", "type": "string", "description": "Start date (YYYY-MM)"},
            {"name": "--to", "type": "string", "description": "End date (YYYY-MM)"},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["date", "backlinks", "referring_domains", "rank"],
    },
    "backlinks competitors": {
        "description": "Find competitors sharing backlink profile",
        "api_endpoint": "POST /v3/backlinks/competitors/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "target", "type": "string", "required": True}],
        "options": [
            {"name": "--sort", "type": "enum", "valid_values": ["rank", "backlinks"]},
            {"name": "--limit", "type": "integer", "default": 20},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["domain", "rank", "backlinks", "referring_domains"],
    },
    "backlinks gap": {
        "description": "Find domains linking to competitors but not to you",
        "api_endpoint": "POST /v3/backlinks/domain_intersection/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "targets", "type": "string[]", "required": True, "description": "Your domain + competitor domains"}],
        "options": [
            {"name": "--mode", "type": "enum", "valid_values": ["domain", "page"]},
            {"name": "--min-rank", "type": "integer"},
            {"name": "--dofollow-only", "type": "boolean"},
            {"name": "--limit", "type": "integer", "default": 100},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["domain", "targets_positions"],
    },
    "backlinks pages": {
        "description": "List pages with most backlinks for a target",
        "api_endpoint": "POST /v3/backlinks/pages_summary/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "target", "type": "string", "required": True}],
        "options": [
            {"name": "--sort", "type": "enum", "valid_values": ["backlinks", "referring_domains"]},
            {"name": "--limit", "type": "integer", "default": 20},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["url", "backlinks", "referring_domains", "rank"],
    },
    "backlinks bulk ranks": {
        "description": "Compare domain ranks for up to 1000 targets",
        "api_endpoint": "POST /v3/backlinks/bulk_ranks/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "targets", "type": "string[]", "required": True}],
        "options": [
            {"name": "--from-file", "type": "string"},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
            {"name": "--raw-params", "type": "json"},
        ],
        "output_fields": ["target", "rank", "backlinks", "referring_domains"],
    },
    "backlinks bulk backlinks": {
        "description": "Compare backlink counts for up to 1000 targets",
        "api_endpoint": "POST /v3/backlinks/bulk_backlinks/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "targets", "type": "string[]", "required": True}],
        "options": [{"name": "--from-file", "type": "string"}, {"name": "--dry-run", "type": "boolean", "default": False}, {"name": "--fields", "type": "string"}],
        "output_fields": ["target", "backlinks"],
    },
    "backlinks bulk spam-score": {
        "description": "Compare spam scores for up to 1000 targets",
        "api_endpoint": "POST /v3/backlinks/bulk_spam_score/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "targets", "type": "string[]", "required": True}],
        "options": [{"name": "--from-file", "type": "string"}, {"name": "--dry-run", "type": "boolean", "default": False}, {"name": "--fields", "type": "string"}],
        "output_fields": ["target", "spam_score"],
    },
    "backlinks bulk referring-domains": {
        "description": "Compare referring domain counts for up to 1000 targets",
        "api_endpoint": "POST /v3/backlinks/bulk_referring_domains/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "targets", "type": "string[]", "required": True}],
        "options": [{"name": "--from-file", "type": "string"}, {"name": "--dry-run", "type": "boolean", "default": False}, {"name": "--fields", "type": "string"}],
        "output_fields": ["target", "referring_domains"],
    },
    "backlinks bulk new-lost": {
        "description": "Compare new and lost backlinks for up to 1000 targets",
        "api_endpoint": "POST /v3/backlinks/bulk_new_lost_summary/live",
        "cost_estimate": "$0.02 per request",
        "arguments": [{"name": "targets", "type": "string[]", "required": True}],
        "options": [
            {"name": "--from-file", "type": "string"},
            {"name": "--from-date", "type": "string"},
            {"name": "--dry-run", "type": "boolean", "default": False},
            {"name": "--fields", "type": "string"},
        ],
        "output_fields": ["target", "new_backlinks", "lost_backlinks"],
    },

    # ---- AUTH / CONFIG ----
    "auth setup": {
        "description": "Interactive credential setup",
        "api_endpoint": "None",
        "cost_estimate": "Free",
    },
    "auth status": {
        "description": "Verify credentials and check account balance",
        "api_endpoint": "GET /v3/appendix/user_data",
        "cost_estimate": "Free",
        "output_fields": ["login", "balance", "rate_limit"],
    },
    "config set": {
        "description": "Set default configuration values",
        "api_endpoint": "None (local config)",
        "cost_estimate": "Free",
        "arguments": [
            {"name": "key", "type": "string", "required": True, "valid_values": ["location", "language", "device", "output"]},
            {"name": "value", "type": "string", "required": True},
        ],
    },
    "config show": {
        "description": "Show current configuration",
        "api_endpoint": "None (local config)",
        "cost_estimate": "Free",
        "output_fields": ["auth", "defaults"],
    },
}

# Group structure for --list
GROUPS: dict[str, list[str]] = {
    "serp": ["google", "bing", "youtube", "compare", "locations", "languages"],
    "keywords": ["volume", "suggestions", "ideas", "difficulty", "search-intent", "for-site", "ads-volume", "ads-suggestions"],
    "site": ["audit", "crawl", "summary", "pages", "links", "duplicates", "redirects", "non-indexable", "resources", "lighthouse", "tasks"],
    "backlinks": ["summary", "list", "anchors", "referring-domains", "history", "competitors", "gap", "pages", "bulk ranks", "bulk backlinks", "bulk spam-score", "bulk referring-domains", "bulk new-lost"],
    "auth": ["setup", "status"],
    "config": ["set", "show"],
}


@app.callback(invoke_without_command=True)
def describe_main(
    ctx: typer.Context,
    command_path: str = typer.Argument(None, help="Command path to describe (e.g., 'serp google', 'keywords volume')"),
    list_all: bool = typer.Option(False, "--list", help="List all available commands"),
    output: str = typer.Option("json-pretty", "--output", "-o", help="Output format (json/json-pretty)"),
) -> None:
    """Describe a command's schema for agent consumption.

    Examples:
        dfseo describe "serp google"
        dfseo describe serp
        dfseo describe --list
    """
    if list_all:
        _print_list(output)
        return

    if command_path is None:
        _print_list(output)
        return

    # Check if it's a group name
    if command_path in GROUPS:
        _print_group(command_path, output)
        return

    # Look up exact command
    meta = COMMAND_META.get(command_path)
    if meta is None:
        from difflib import get_close_matches
        matches = get_close_matches(command_path, COMMAND_META.keys(), n=3, cutoff=0.5)
        if matches:
            print(json.dumps({"error": f"Unknown command '{command_path}'", "did_you_mean": matches}, indent=2))
        else:
            print(json.dumps({"error": f"Unknown command '{command_path}'", "hint": "Run 'dfseo describe --list' for all commands"}, indent=2))
        raise typer.Exit(code=4)

    schema = {"command": f"dfseo {command_path}", **meta}
    _print_json(schema, output)


def _print_list(output: str) -> None:
    """Print list of all commands."""
    from dfseo import __version__

    result = {
        "version": __version__,
        "total_commands": len(COMMAND_META),
        "groups": GROUPS,
    }
    _print_json(result, output)


def _print_group(group: str, output: str) -> None:
    """Print all commands in a group."""
    commands = {}
    for cmd_path, meta in COMMAND_META.items():
        if cmd_path.startswith(f"{group} "):
            commands[cmd_path] = {
                "description": meta.get("description", ""),
                "api_endpoint": meta.get("api_endpoint", ""),
                "cost_estimate": meta.get("cost_estimate", ""),
            }

    result = {
        "group": group,
        "commands": commands,
    }
    _print_json(result, output)


def _print_json(data: dict, output: str) -> None:
    """Print data as JSON."""
    if output == "json":
        print(json.dumps(data, separators=(",", ":")))
    else:
        print(json.dumps(data, indent=2))
