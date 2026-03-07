# dfseo-cli — DataForSEO CLI for AI Agents

> SEO data from your terminal. JSON-first for agents, human-friendly for you.

```bash
# Auto-detects your terminal — outputs table for humans, JSON for pipes
dfseo serp google "sovranità digitale" --location Italy
```

## Installation

```bash
pip install dfseo
```

## Quick Start

Set your DataForSEO credentials:

```bash
# Via environment variables (recommended for agents)
export DATAFORSEO_LOGIN="your@email.com"
export DATAFORSEO_PASSWORD="your_api_password"

# Or via interactive setup
dfseo auth setup
```

Test your setup:

```bash
dfseo auth status
```

## Usage Examples

### Google SERP

```bash
# Basic search — auto-detects output format (table in terminal)
dfseo serp google "email hosting provider"

# With location and language
dfseo serp google "email hosting" --location "Italy" --language "Italian"

# Force JSON for scripting
dfseo serp google "email hosting" --output json | jq '.organic_results[0].url'

# CSV for Excel import
dfseo serp google "email hosting" --output csv > results.csv
```

**Example output:**

```
Query: email hosting provider
Location: Italy | Language: Italian | Device: desktop
Results: 100 | Cost: $0.0020

SERP Features: featured_snippet, people_also_ask

┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  # ┃ Domain         ┃ Title / Description                            ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  1 │ example.com    │ Best Email Hosting Provider 2026               │
│    │                │ Compare the top email hosting services...      │
│  2 │ another.com    │ Email Hosting for Small Business               │
│    │                │ Affordable and reliable email solutions...     │
└────┴────────────────┴────────────────────────────────────────────────┘
```

### Keyword Research

```bash
# Get search volume and keyword difficulty
dfseo keywords volume "email hosting" "smtp provider" "email server" \
  --location "Italy"

# Find long-tail keyword suggestions
dfseo keywords suggestions "email hosting" \
  --min-volume 100 \
  --max-difficulty 40 \
  --limit 50

# Bulk keyword difficulty (up to 1000 keywords)
dfseo keywords difficulty --from-file keywords.txt --location "Italy"
```

### Site Audit

```bash
# Full site audit (crawls up to 100 pages)
dfseo site audit "example.com" --max-pages 100

# Quick single-page check
dfseo site audit "https://example.com/page" --max-pages 1

# With JavaScript execution
dfseo site audit "example.com" --enable-javascript --load-resources
```

### Backlink Analysis

```bash
# Backlink profile summary
dfseo backlinks summary "example.com"

# List backlinks with filters
dfseo backlinks list "example.com" --dofollow-only --sort rank --limit 50

# Referring domains
dfseo backlinks referring-domains "example.com" --min-backlinks 5

# Link gap analysis (find competitor backlinks you're missing)
dfseo backlinks gap "your-site.com" "competitor1.com" "competitor2.com"
```

### Compare Search Engines

```bash
dfseo serp compare "email hosting" --engines google,bing --location "Italy"
```

### Available Locations & Languages

```bash
# List all locations
dfseo serp locations

# Search for specific location
dfseo serp locations --search "italy"

# List languages
dfseo serp languages --search "italian"
```

## Output Formats

The CLI auto-detects your environment:

- **Interactive terminal** → `table` (human-readable, uses rich)
- **Pipe/redirect** → `json` (compact, machine-readable)

Override with `--output`:

```bash
dfseo serp google "keyword" --output json        # Force JSON
dfseo serp google "keyword" --output json-pretty  # Indented JSON
dfseo serp google "keyword" --output table        # Human table
dfseo serp google "keyword" --output csv          # CSV export
```

## Configuration

Set defaults to avoid repeating flags:

```bash
# Set defaults
dfseo config set location "Italy"
dfseo config set language "Italian"
dfseo config set device desktop

# Show current config
dfseo config show
```

Now you can run:
```bash
dfseo serp google "keyword"  # Uses Italy/Italian/desktop automatically
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

## API Coverage

| API | Commands | Status |
|-----|----------|--------|
| **SERP** | google, bing, youtube, compare, locations, languages | ✅ |
| **Keywords** | volume, suggestions, ideas, difficulty, search-intent, for-site, ads-volume, ads-suggestions | ✅ |
| **On-Page** | crawl, summary, audit, pages, links, duplicates, redirects, non-indexable, resources, lighthouse, tasks | ✅ |
| **Backlinks** | summary, list, anchors, referring-domains, gap, bulk | ✅ |

## For AI Agents

```bash
# JSON output for parsing
dfseo serp google "keyword" --output json | jq -r '.organic_results[0].url'

# Quiet mode (no progress bars)
dfseo serp google "keyword" --quiet

# Check SKILL.md for integration examples
```

## License

MIT
