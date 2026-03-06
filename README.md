# dfseo-cli — DataForSEO CLI for AI Agents

> SEO data from your terminal. JSON-first, machine-readable, human-friendly.

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

## Usage

### Google SERP

```bash
# Basic search
dfseo serp google "email hosting provider"

# With location and language
dfseo serp google "email hosting" --location "Italy" --language "Italian"

# Mobile search
dfseo serp google "email hosting" --device mobile --os android

# Human-readable table output
dfseo serp google "email hosting" --output table
```

### Bing SERP

```bash
dfseo serp bing "email hosting provider" --location "United States"
```

### YouTube SERP

```bash
dfseo serp youtube "email marketing tutorial"
```

### Compare Search Engines

```bash
dfseo serp compare "email hosting" --engines google,bing --location "Italy"
```

### Configuration

```bash
# Set defaults
dfseo config set location "Italy"
dfseo config set language "Italian"
dfseo config set device desktop

# Show current config
dfseo config show
```

### Authentication

```bash
# Check credentials and balance
dfseo auth status

# Interactive setup
dfseo auth setup
```

## Output Formats

- `json` (default) - Compact JSON on stdout
- `json-pretty` - Indented JSON for debugging
- `table` - Formatted table for humans (uses rich)
- `csv` - CSV with headers

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Generic error |
| 2 | Authentication error |
| 3 | Rate limit exceeded |
| 4 | Invalid parameters |
| 5 | Insufficient balance |

## License

MIT
