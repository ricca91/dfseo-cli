# dfseo Content Analysis Commands — Reference

Use these commands to analyze web content mentioning a keyword. They cover search, aggregation, and sentiment analysis across the web. All Content Analysis endpoints return results immediately (no polling needed).

---

## `dfseo content search`

Search web content mentioning a keyword.

```
Usage: dfseo content search [OPTIONS] KEYWORD

Arguments:
  keyword  TEXT  Search keyword [required]

Options:
  --search-mode   TEXT     Search mode: as_is, broad [default: as_is]
  --sentiment     TEXT     Filter by sentiment: positive, negative, neutral
  --from-date     TEXT     Start date (YYYY-MM-DD)
  --to-date       TEXT     End date (YYYY-MM-DD)
  --limit     -n  INTEGER  Max results [default: 10]
  --sort          TEXT     Sort by: rank, date, content_score
  --fields    -F  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run                Show estimated cost without executing
  --output    -o  TEXT     Output format: json, table [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Endpoint:** `POST /v3/content_analysis/search/live` — Cost: **$0.01**

**Examples:**

```bash
# Basic keyword search
dfseo content search "headless CMS"

# Only positive sentiment, sorted by content score
dfseo content search "headless CMS" --sentiment positive --sort content_score --limit 20

# Date-filtered search
dfseo content search "AI regulation" --from-date 2026-01-01 --to-date 2026-03-22
```

**Output JSON:**

```json
{
  "keyword": "headless CMS",
  "total_count": 4832,
  "returned_count": 10,
  "results": [
    {
      "url": "https://techblog.io/headless-cms-guide",
      "domain": "techblog.io",
      "title": "The Definitive Guide to Headless CMS in 2026",
      "date": "2026-02-18T09:30:00Z",
      "content_type": "article",
      "sentiment": "positive",
      "content_score": 872,
      "spam_score": 3
    }
  ],
  "cost": 0.01,
  "timestamp": "2026-03-22T14:00:00Z"
}
```

---

## `dfseo content summary`

Get aggregate content metrics for a keyword.

```
Usage: dfseo content summary [OPTIONS] KEYWORD

Arguments:
  keyword  TEXT  Search keyword [required]

Options:
  --from-date     TEXT  Start date (YYYY-MM-DD)
  --to-date       TEXT  End date (YYYY-MM-DD)
  --fields    -F  TEXT  Comma-separated fields to include
  --raw-params    TEXT  Raw JSON payload
  --dry-run              Show estimated cost without executing
  --output    -o  TEXT  Output format: json, table [default: auto]
  --login         TEXT  DataForSEO login
  --password      TEXT  DataForSEO password
  --verbose   -v        Verbose output
```

**Endpoint:** `POST /v3/content_analysis/summary/live` — Cost: **$0.01**

**Examples:**

```bash
# Summary for a keyword
dfseo content summary "remote work"

# Summary over a date range
dfseo content summary "remote work" --from-date 2025-06-01 --to-date 2026-03-01
```

**Output JSON:**

```json
{
  "keyword": "remote work",
  "summary": {
    "total_count": 18420,
    "sentiment": {
      "positive": 9210,
      "negative": 3105,
      "neutral": 6105
    },
    "content_types": {
      "article": 12540,
      "blog_post": 3880,
      "forum_post": 2000
    },
    "top_domains": [
      "forbes.com",
      "techcrunch.com",
      "linkedin.com"
    ],
    "text_categories": [
      "Business",
      "Technology",
      "Human Resources"
    ]
  },
  "cost": 0.01,
  "timestamp": "2026-03-22T14:05:00Z"
}
```

---

## `dfseo content sentiment`

Analyze sentiment of content mentioning a keyword.

```
Usage: dfseo content sentiment [OPTIONS] KEYWORD

Arguments:
  keyword  TEXT  Search keyword [required]

Options:
  --limit     -n  INTEGER  Max results [default: 10]
  --from-date     TEXT     Start date (YYYY-MM-DD)
  --to-date       TEXT     End date (YYYY-MM-DD)
  --fields    -F  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run                Show estimated cost without executing
  --output    -o  TEXT     Output format: json, table [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Endpoint:** `POST /v3/content_analysis/sentiment_analysis/live` — Cost: **$0.01**

**Examples:**

```bash
# Sentiment analysis for a brand
dfseo content sentiment "Shopify"

# Limited results with date range
dfseo content sentiment "Shopify" --limit 25 --from-date 2026-01-01
```

**Output JSON:**

```json
{
  "keyword": "Shopify",
  "total_count": 7640,
  "returned_count": 10,
  "results": [
    {
      "url": "https://ecommerce-weekly.com/shopify-review",
      "domain": "ecommerce-weekly.com",
      "title": "Shopify 2026 Review: Still the Best?",
      "date": "2026-03-10T11:20:00Z",
      "sentiment": "positive",
      "content_score": 745
    },
    {
      "url": "https://retailforum.net/thread/shopify-fees",
      "domain": "retailforum.net",
      "title": "Shopify fees are getting out of hand",
      "date": "2026-03-08T16:45:00Z",
      "sentiment": "negative",
      "content_score": 312
    }
  ],
  "cost": 0.01,
  "timestamp": "2026-03-22T14:10:00Z"
}
```
