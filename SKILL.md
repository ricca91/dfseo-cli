---
name: dfseo-cli
description: >
  SEO data CLI powered by DataForSEO APIs. Use when the user needs SERP data,
  keyword rankings, search engine results for any keyword/location/language.
  Triggers on: "SERP", "search results", "keyword ranking", "SEO data",
  "Google results for", "check ranking", "search position".
---

# dfseo-cli — SEO Data from your terminal

A command-line interface for DataForSEO APIs, designed for AI agents and human users alike. Provides real-time SERP data from Google, Bing, and YouTube in JSON-first, machine-readable format.

## Quick Start

Requires `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` environment variables (get them from https://app.dataforseo.com/api-access).

```bash
# Set credentials via environment (recommended for agents)
export DATAFORSEO_LOGIN="your@email.com"
export DATAFORSEO_PASSWORD="your_api_password"

# Or use interactive setup
dfseo auth setup
```

## Core Commands

### Google SERP

Get organic search results from Google with SERP features (featured snippets, People Also Ask, etc.).

```bash
# Basic search
dfseo serp google "keyword"

# With location and language
dfseo serp google "email hosting" --location "Italy" --language "Italian"

# Mobile search with specific OS
dfseo serp google "keyword" --device mobile --os android

# Limit number of results (max 700)
dfseo serp google "keyword" --depth 50

# Only show SERP features (no organic results)
dfseo serp google "keyword" --features-only
```

### Bing SERP

Same interface as Google, for Bing search results.

```bash
dfseo serp bing "keyword" --location "United States" --language "English"
```

### YouTube SERP

Search results from YouTube.

```bash
dfseo serp youtube "email marketing tutorial" --depth 20
```

### Compare Search Engines

Compare results between Google and Bing to find common domains and ranking differences.

```bash
dfseo serp compare "keyword" --engines google,bing --location "Italy"
```

### Available Locations

List all available location codes for targeting.

```bash
# List all locations
dfseo serp locations

# Search for specific location
dfseo serp locations --search "italy"

# JSON output for processing
dfseo serp locations --output json
```

### Available Languages

List all available language codes.

```bash
dfseo serp languages --search "ital"
```

### Authentication

Check credentials and account balance.

```bash
# Verify authentication
dfseo auth status

# Interactive credential setup
dfseo auth setup
```

### Configuration

Set default values for common parameters.

```bash
# Set defaults
dfseo config set location "Italy"
dfseo config set language "Italian"
dfseo config set device desktop
dfseo config set output json

# Show current configuration
dfseo config show
```

## Output Formats

- `json` (default) — Compact JSON on stdout, machine-readable
- `json-pretty` — Indented JSON for debugging
- `table` — Formatted table for human reading
- `csv` — CSV with headers for spreadsheet import

## Common Patterns

### Get top 10 results for a keyword in a specific location

```bash
dfseo serp google "best coffee shops" \
  --location "New York,New York,United States" \
  --language "English" \
  --depth 10 \
  --output json-pretty
```

### Extract first result URL with jq

```bash
dfseo serp google "keyword" -q | jq -r '.organic_results[0].url'
```

### Check for featured snippet

```bash
dfseo serp google "what is API" --features-only | jq '.featured_snippet'
```

### Compare your domain's position across engines

```bash
dfseo serp compare "your keyword" --engines google,bing | \
  jq '.common_domains[] | select(.domain == "yourdomain.com")'
```

### Find all "People Also Ask" questions

```bash
dfseo serp google "keyword" | jq '.people_also_ask[].question'
```

## Authentication Priority

Credentials are resolved in this order:

1. **CLI flags** — `--login` and `--password`
2. **Environment variables** — `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`
3. **Config file** — `~/.config/dfseo/config.toml`

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Generic error |
| 2 | Authentication error (check credentials) |
| 3 | Rate limit exceeded (wait and retry) |
| 4 | Invalid parameters |
| 5 | Insufficient balance (add funds) |

## Response Structure

### SERP Result JSON

```json
{
  "keyword": "email hosting provider",
  "location": "Italy",
  "language": "Italian",
  "device": "desktop",
  "results_count": 100,
  "serp_features": ["featured_snippet", "people_also_ask", "local_pack"],
  "organic_results": [
    {
      "rank": 1,
      "rank_group": 1,
      "domain": "example.com",
      "url": "https://example.com/email-hosting",
      "title": "Best Email Hosting Provider 2026",
      "description": "Compare the top email hosting...",
      "breadcrumb": "example.com › email › hosting"
    }
  ],
  "featured_snippet": {
    "text": "An email hosting service is...",
    "source_url": "https://en.wikipedia.org/wiki/Email_hosting_service",
    "source_domain": "en.wikipedia.org"
  },
  "people_also_ask": [
    {
      "question": "What is the best email hosting for business?",
      "expanded_text": "The best email hosting depends on..."
    }
  ],
  "cost": 0.002,
  "timestamp": "2026-03-06T14:30:00+00:00"
}
```

### SERP Features Detected

- `featured_snippet` — Quick answer box at top of results
- `people_also_ask` — Expandable questions section
- `local_pack` — Map with local business listings
- `knowledge_graph` — Information panel on right side
- `top_stories` — News carousel
- `images` — Image results block
- `videos` — Video results block
- `shopping` — Product listings

## Flags Reference

| Flag | Short | Description |
|------|-------|-------------|
| `--location` | `-l` | Location name (e.g., "Italy", "United States") |
| `--language` | `-L` | Language name (e.g., "Italian", "English") |
| `--device` | `-d` | Device type: `desktop` or `mobile` |
| `--os` | | Operating system: `windows`, `macos`, `ios`, `android` |
| `--depth` | `-n` | Number of results (max 700) |
| `--output` | `-o` | Output format: `json`, `json-pretty`, `table`, `csv` |
| `--features-only` | | Show only SERP features, no organic results |
| `--raw` | | Output raw API response |
| `--login` | | Override login credential |
| `--password` | | Override password credential |
| `--verbose` | `-v` | Show request/response details on stderr |
| `--quiet` | `-q` | Suppress non-error output |
| `--version` | `-V` | Show version |

## When to Use

Use `dfseo-cli` when you need:

- **Real-time SERP data** — Current rankings, not cached
- **SERP feature analysis** — Featured snippets, PAA, local packs
- **Multi-engine comparison** — Google vs Bing results
- **SEO audit data** — Position tracking, competitor analysis
- **Location-specific results** — See SERPs from different countries
- **Device-specific results** — Mobile vs desktop differences

## Rate Limiting

- Max 2000 requests per minute
- Client automatically retries on 429 errors with exponential backoff (max 3 retries)
- Check rate limit status: `dfseo auth status`

## Costs

DataForSEO uses a pay-per-use model. Each request displays its cost in the output:

```json
{
  "cost": 0.002
}
```

Check your balance with `dfseo auth status`.

## Tips for AI Agents

1. **Always check exit codes** — Non-zero means the data may be incomplete
2. **Parse stderr separately** — Only stdout contains the JSON output
3. **Use `--quiet`** — Prevents any non-JSON output on stdout
4. **Set environment variables** — Faster than config file operations
5. **Use `jq` for filtering** — The JSON structure is stable and documented
6. **Handle rate limits** — Exit code 3 means you should wait and retry
7. **Check cost in response** — Track API usage from the response

## Installation

```bash
pip install dfseo
```

## Links

- DataForSEO API Docs: https://docs.dataforseo.com/v3/
- Project Repository: https://github.com/example/dfseo-cli
