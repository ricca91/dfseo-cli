# dfseo Domain Analytics Commands — Reference

Use these commands to analyze technologies and infrastructure behind a domain. Useful for competitive research, lead generation, and understanding a site's tech stack. All endpoints return results immediately (no polling needed).

---

## `dfseo domain technologies`

Detect technologies used by a domain (CMS, analytics, frameworks, CDN, etc.).

```
Usage: dfseo domain technologies [OPTIONS] TARGET

Arguments:
  target  TEXT  Target domain (e.g., example.com) [required]

Options:
  --fields    -F  TEXT  Comma-separated fields to include
  --raw-params    TEXT  Raw JSON payload
  --dry-run              Show estimated cost without executing
  --output    -o  TEXT  Output format: json, table [default: auto]
  --login         TEXT  DataForSEO login
  --password      TEXT  DataForSEO password
  --verbose   -v        Verbose output
```

**Endpoint:** `POST /v3/domain_analytics/technologies/domain_technologies/live` — Cost: **$0.01**

**Examples:**

```bash
# Detect all technologies on a domain
dfseo domain technologies "stripe.com"

# Dry run to check cost
dfseo domain technologies "stripe.com" --dry-run

# JSON output with specific fields
dfseo domain technologies "shopify.com" --output json -F "technologies"
```

**Output JSON:**

```json
{
  "target": "stripe.com",
  "technologies_count": 14,
  "technologies": [
    {
      "category": "Web Framework",
      "name": "React"
    },
    {
      "category": "CDN",
      "name": "Cloudflare"
    },
    {
      "category": "Analytics",
      "name": "Google Analytics"
    },
    {
      "category": "Tag Manager",
      "name": "Google Tag Manager"
    },
    {
      "category": "Programming Language",
      "name": "Ruby"
    },
    {
      "category": "SSL Certificate",
      "name": "DigiCert"
    }
  ],
  "cost": 0.01,
  "timestamp": "2026-03-22T14:15:00Z"
}
```
