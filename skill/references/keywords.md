# dfseo Keywords Commands — Reference

Complete reference for all keyword research commands.

## `dfseo keywords volume`

Get search volume, CPC, competition, keyword difficulty, and search intent for up to 700 keywords at once.

```
Usage: dfseo keywords volume [OPTIONS] [KEYWORDS]...

Arguments:
  keywords  [KEYWORDS]...  Keywords to analyze (max 700)

Options:
  --location         -l  TEXT  Location name (e.g., 'Italy')
  --language         -L  TEXT  Language name (e.g., 'Italian')
  --include-serp-info        Include SERP data (featured snippets, PAA count)
  --from-file        -f  TEXT  Read keywords from file (one per line)
  --fields           -F  TEXT  Comma-separated fields to include in output
  --raw-params           TEXT  Raw JSON payload (bypasses all other flags)
  --dry-run                   Show estimated cost without executing
  --output           -o  TEXT  Output format: json, table, csv
  --login                TEXT  DataForSEO login
  --password             TEXT  DataForSEO password
  --verbose          -v        Verbose output
```

**Examples:**

```bash
# Single keyword
dfseo keywords volume "email hosting" --location "Italy"

# Multiple keywords
dfseo keywords volume "email hosting" "smtp provider" "email server" --location "Italy"

# From file with SERP data
dfseo keywords volume --from-file keywords.txt --include-serp-info

# Pipe to jq
dfseo keywords volume "email hosting" -q | jq '.[0].search_volume'
```

**Output JSON (per keyword):**

```json
{
  "keyword": "email hosting",
  "search_volume": 4400,
  "cpc": 2.15,
  "competition": 0.72,
  "keyword_difficulty": 68,
  "search_intent": "commercial",
  "monthly_searches": [
    {"year": 2026, "month": 2, "search_volume": 4200},
    {"year": 2026, "month": 1, "search_volume": 4600}
  ]
}
```

---

## `dfseo keywords suggestions`

Find long-tail keywords that contain your seed keyword. Great for finding specific, lower-competition variants.

```
Usage: dfseo keywords suggestions [OPTIONS] KEYWORD

Arguments:
  keyword  TEXT  Seed keyword [required]

Options:
  --location        -l  TEXT     Location name
  --language        -L  TEXT     Language name
  --limit           -n  INTEGER  Max results (max 1000) [default: 50]
  --min-volume          INTEGER  Minimum search volume filter
  --max-volume          INTEGER  Maximum search volume filter
  --min-difficulty      INTEGER  Minimum keyword difficulty (0-100)
  --max-difficulty      INTEGER  Maximum keyword difficulty (0-100)
  --include-seed                 Include the seed keyword in results
  --sort                TEXT     Sort by: relevance, volume, cpc, difficulty [default: relevance]
  --order               TEXT     Sort order: asc, desc [default: desc]
  --fields          -F  TEXT     Comma-separated fields to include
  --raw-params          TEXT     Raw JSON payload
  --dry-run                      Show estimated cost
  --output          -o  TEXT     Output format [default: auto]
  --login               TEXT     DataForSEO login
  --password            TEXT     DataForSEO password
  --verbose         -v           Verbose output
```

**Examples:**

```bash
# Long-tail keywords with filters
dfseo keywords suggestions "email hosting" \
  --location "Italy" --language "Italian" \
  --min-volume 100 --max-difficulty 40 --limit 50

# Sort by volume
dfseo keywords suggestions "smtp server" --sort volume --limit 100
```

---

## `dfseo keywords ideas`

Find semantically related keywords — not just those containing the seed. Uses DataForSEO's semantic analysis to find associated concepts.

```
Usage: dfseo keywords ideas [OPTIONS] KEYWORDS...

Arguments:
  keywords  KEYWORDS...  Seed keywords (max 20) [required]

Options:
  --location        -l  TEXT     Location name
  --language        -L  TEXT     Language name
  --limit           -n  INTEGER  Max results [default: 100]
  --min-volume          INTEGER  Minimum search volume
  --max-volume          INTEGER  Maximum search volume
  --min-difficulty      INTEGER  Minimum keyword difficulty
  --max-difficulty      INTEGER  Maximum keyword difficulty
  --sort                TEXT     Sort by: relevance, volume, cpc, difficulty [default: relevance]
  --order               TEXT     Sort order: asc, desc [default: desc]
  --fields          -F  TEXT     Comma-separated fields to include
  --raw-params          TEXT     Raw JSON payload
  --dry-run                      Show estimated cost
  --output          -o  TEXT     Output format [default: auto]
  --login               TEXT     DataForSEO login
  --password            TEXT     DataForSEO password
  --verbose         -v           Verbose output
```

**Example:**

```bash
dfseo keywords ideas "email hosting" "smtp service" \
  --location "Italy" --limit 100 --min-volume 50
```

---

## `dfseo keywords difficulty`

Get keyword difficulty score (0-100) for up to 1000 keywords at once. Useful for bulk analysis of content opportunities.

```
Usage: dfseo keywords difficulty [OPTIONS] [KEYWORDS]...

Arguments:
  keywords  [KEYWORDS]...  Keywords to analyze (max 1000)

Options:
  --location  -l  TEXT  Location name
  --language  -L  TEXT  Language name
  --from-file -f  TEXT  Read keywords from file (one per line)
  --fields    -F  TEXT  Comma-separated fields to include
  --raw-params    TEXT  Raw JSON payload
  --dry-run           Show estimated cost
  --output    -o  TEXT  Output format [default: auto]
  --login         TEXT  DataForSEO login
  --password      TEXT  DataForSEO password
  --verbose   -v        Verbose output
```

**Examples:**

```bash
# Inline keywords
dfseo keywords difficulty "email hosting" "smtp server" --location "Italy"

# From file (up to 1000 keywords)
dfseo keywords difficulty --from-file candidates.txt --location "Italy"
```

**Difficulty levels:** 0-14 easy, 15-29 medium, 30-49 difficult, 50-69 hard, 70-84 very hard, 85-100 super hard.

---

## `dfseo keywords search-intent`

Classify the search intent for up to 1000 keywords. Intent categories: informational, navigational, commercial, transactional.

```
Usage: dfseo keywords search-intent [OPTIONS] [KEYWORDS]...

Arguments:
  keywords  [KEYWORDS]...  Keywords to classify (max 1000)

Options:
  --location  -l  TEXT  Location name
  --language  -L  TEXT  Language name
  --from-file -f  TEXT  Read keywords from file
  --fields    -F  TEXT  Comma-separated fields to include
  --raw-params    TEXT  Raw JSON payload
  --dry-run           Show estimated cost
  --output    -o  TEXT  Output format [default: auto]
  --login         TEXT  DataForSEO login
  --password      TEXT  DataForSEO password
  --verbose   -v        Verbose output
```

**Example:**

```bash
dfseo keywords search-intent "buy hosting" "what is smtp" "gmail login" "best email server"
```

**Output (per keyword):**

```json
{"keyword": "buy hosting", "search_intent": "transactional", "secondary_intents": ["commercial"]}
```

---

## `dfseo keywords for-site`

Find keywords that a specific domain is ranking for. Useful for competitor keyword analysis.

```
Usage: dfseo keywords for-site [OPTIONS] TARGET

Arguments:
  target  TEXT  Target domain (e.g., example.com) [required]

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --limit     -n  INTEGER  Max results [default: 100]
  --min-volume    INTEGER  Minimum search volume
  --max-volume    INTEGER  Maximum search volume
  --sort          TEXT     Sort by: relevance, volume, cpc, difficulty [default: relevance]
  --order         TEXT     Sort order: asc, desc [default: desc]
  --fields    -F  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run               Show estimated cost
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Example:**

```bash
dfseo keywords for-site "competitor.com" \
  --location "Italy" --min-volume 100 --sort volume --limit 200
```

---

## `dfseo keywords ads-volume`

Get pure Google Ads search volume data (different from organic volume). Max 20 keywords per request. Rate limit: 12 requests/minute.

```
Usage: dfseo keywords ads-volume [OPTIONS] [KEYWORDS]...

Arguments:
  keywords  [KEYWORDS]...  Keywords to analyze (max 20)

Options:
  --location  -l  TEXT  Location name
  --language  -L  TEXT  Language name
  --date-from     TEXT  Start date for historical data (YYYY-MM)
  --date-to       TEXT  End date for historical data (YYYY-MM)
  --from-file -f  TEXT  Read keywords from file
  --fields    -F  TEXT  Comma-separated fields to include
  --raw-params    TEXT  Raw JSON payload
  --dry-run           Show estimated cost
  --output    -o  TEXT  Output format [default: auto]
  --login         TEXT  DataForSEO login
  --password      TEXT  DataForSEO password
  --verbose   -v        Verbose output
```

**Example:**

```bash
dfseo keywords ads-volume "email hosting" "smtp provider" --location "Italy"
```

---

## `dfseo keywords ads-suggestions`

Get keyword suggestions from Google Ads. Max 20 seed keywords. Rate limit: 12 requests/minute.

```
Usage: dfseo keywords ads-suggestions [OPTIONS] KEYWORDS...

Arguments:
  keywords  KEYWORDS...  Seed keywords (max 20) [required]

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --limit     -n  INTEGER  Max results [default: 100]
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Example:**

```bash
dfseo keywords ads-suggestions "email hosting" "smtp" --location "Italy" --limit 100
```

---

## `dfseo keywords ranked-keywords`

Get all keywords a domain currently ranks for in organic search, with position, URL, search volume, and traffic estimates.

**Endpoint:** `POST /v3/dataforseo_labs/google/ranked_keywords/live` — $0.021 per request.

```
Usage: dfseo keywords ranked-keywords [OPTIONS] DOMAIN

Arguments:
  domain  TEXT  Target domain (e.g., example.com) [required]

Options:
  --location        -l  TEXT     Location name
  --language        -L  TEXT     Language name
  --min-position        INTEGER  Minimum SERP position filter
  --max-position        INTEGER  Maximum SERP position filter
  --min-volume          INTEGER  Minimum search volume filter
  --sort                TEXT     Sort by: relevance, volume, cpc, difficulty [default: relevance]
  --limit           -n  INTEGER  Max results [default: 100]
  --fields          -F  TEXT     Comma-separated fields to include
  --raw-params          TEXT     Raw JSON payload
  --dry-run                      Show estimated cost
  --output          -o  TEXT     Output format [default: auto]
  --login               TEXT     DataForSEO login
  --password            TEXT     DataForSEO password
  --verbose         -v           Verbose output
```

**Examples:**

```bash
# All top-10 keywords for a domain
dfseo keywords ranked-keywords "example.com" --max-position 10 --limit 200

# High-volume keywords in positions 11-20 (quick wins)
dfseo keywords ranked-keywords "example.com" \
  --min-position 11 --max-position 20 --min-volume 500 --sort volume
```

**Output JSON (per keyword):**

```json
{
  "keyword": "email hosting provider",
  "search_volume": 3200,
  "rank_group": 7,
  "rank_absolute": 7,
  "url": "https://example.com/email-hosting",
  "cpc": 3.45,
  "keyword_difficulty": 54,
  "etv": 185.3,
  "competition": 0.68
}
```

---

## `dfseo keywords domain-rank`

Get a domain rank overview including organic and paid traffic estimates, total keyword count, and visibility metrics.

**Endpoint:** `POST /v3/dataforseo_labs/google/domain_rank_overview/live` — $0.021 per request.

```
Usage: dfseo keywords domain-rank [OPTIONS] DOMAIN

Arguments:
  domain  TEXT  Target domain (e.g., example.com) [required]

Options:
  --location  -l  TEXT  Location name
  --language  -L  TEXT  Language name
  --fields    -F  TEXT  Comma-separated fields to include
  --raw-params    TEXT  Raw JSON payload
  --dry-run           Show estimated cost
  --output    -o  TEXT  Output format [default: auto]
  --login         TEXT  DataForSEO login
  --password      TEXT  DataForSEO password
  --verbose   -v        Verbose output
```

**Example:**

```bash
dfseo keywords domain-rank "example.com" --location "United States"
```

**Output JSON:**

```json
{
  "target": "example.com",
  "rank": 4521,
  "organic_etv": 128450.6,
  "organic_count": 18340,
  "organic_is_up": 2105,
  "organic_is_down": 1830,
  "organic_is_new": 412,
  "organic_is_lost": 287,
  "paid_etv": 3200.0,
  "paid_count": 85
}
```

---

## `dfseo keywords historical-rank`

View historical domain ranking trends over time, showing how organic traffic, keyword count, and visibility have changed.

**Endpoint:** `POST /v3/dataforseo_labs/google/historical_rank_overview/live` — $0.021 per request.

```
Usage: dfseo keywords historical-rank [OPTIONS] DOMAIN

Arguments:
  domain  TEXT  Target domain (e.g., example.com) [required]

Options:
  --location  -l  TEXT  Location name
  --language  -L  TEXT  Language name
  --fields    -F  TEXT  Comma-separated fields to include
  --raw-params    TEXT  Raw JSON payload
  --dry-run           Show estimated cost
  --output    -o  TEXT  Output format [default: auto]
  --login         TEXT  DataForSEO login
  --password      TEXT  DataForSEO password
  --verbose   -v        Verbose output
```

**Example:**

```bash
dfseo keywords historical-rank "example.com" --location "United States"
```

**Output JSON (array of monthly snapshots):**

```json
{
  "year": 2026,
  "month": 2,
  "rank": 4521,
  "organic_etv": 128450.6,
  "organic_count": 18340,
  "organic_is_up": 2105,
  "organic_is_down": 1830
}
```

---

## `dfseo keywords historical-volume`

Get historical search volume trends for keywords, showing monthly volume over time. Useful for identifying seasonal patterns.

**Endpoint:** `POST /v3/dataforseo_labs/google/historical_search_volume/live` — $0.021 per request.

```
Usage: dfseo keywords historical-volume [OPTIONS] [KEYWORDS]...

Arguments:
  keywords  [KEYWORDS]...  Keywords to analyze

Options:
  --location  -l  TEXT  Location name
  --language  -L  TEXT  Language name
  --from-file -f  TEXT  Read keywords from file (one per line)
  --fields    -F  TEXT  Comma-separated fields to include
  --raw-params    TEXT  Raw JSON payload
  --dry-run           Show estimated cost
  --output    -o  TEXT  Output format [default: auto]
  --login         TEXT  DataForSEO login
  --password      TEXT  DataForSEO password
  --verbose   -v        Verbose output
```

**Examples:**

```bash
# Multiple keywords
dfseo keywords historical-volume "email hosting" "smtp server" --location "Italy"

# From file
dfseo keywords historical-volume --from-file keywords.txt
```

**Output JSON (per keyword):**

```json
{
  "keyword": "email hosting",
  "search_volume": 4400,
  "monthly_searches": [
    {"year": 2026, "month": 2, "search_volume": 4200},
    {"year": 2026, "month": 1, "search_volume": 4600},
    {"year": 2025, "month": 12, "search_volume": 5100},
    {"year": 2025, "month": 11, "search_volume": 3900}
  ]
}
```

---

## `dfseo keywords serp-competitors`

Find domains that compete in SERP results for the given keywords. Shows which sites rank for the same terms.

**Endpoint:** `POST /v3/dataforseo_labs/google/serp_competitors/live` — $0.021 per request.

```
Usage: dfseo keywords serp-competitors [OPTIONS] [KEYWORDS]...

Arguments:
  keywords  [KEYWORDS]...  Keywords to analyze

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --limit     -n  INTEGER  Max results [default: 100]
  --from-file -f  TEXT     Read keywords from file (one per line)
  --fields    -F  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run               Show estimated cost
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Examples:**

```bash
# Find SERP competitors for a set of keywords
dfseo keywords serp-competitors "email hosting" "smtp provider" --limit 20

# From file
dfseo keywords serp-competitors --from-file keywords.txt --limit 50
```

**Output JSON (per competitor):**

```json
{
  "domain": "competitor.com",
  "avg_position": 4.2,
  "median_position": 3,
  "keywords_count": 8,
  "etv": 12500.5,
  "visibility": 0.35
}
```

---

## `dfseo keywords competitors-domain`

Find domains that compete for the same organic keywords as the target domain.

**Endpoint:** `POST /v3/dataforseo_labs/google/competitors_domain/live` — $0.021 per request.

```
Usage: dfseo keywords competitors-domain [OPTIONS] DOMAIN

Arguments:
  domain  TEXT  Target domain (e.g., example.com) [required]

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --limit     -n  INTEGER  Max results [default: 100]
  --fields    -F  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run               Show estimated cost
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Example:**

```bash
dfseo keywords competitors-domain "example.com" --location "United States" --limit 20
```

**Output JSON (per competitor):**

```json
{
  "domain": "rival.com",
  "avg_position": 12.4,
  "keywords_count": 3420,
  "etv": 45200.8,
  "intersections": 1850,
  "full_domain_rank": 6230
}
```

---

## `dfseo keywords domain-intersection`

Find keyword overlap between 2 to 20 domains. Shows keywords where multiple domains rank, useful for competitive gap analysis.

**Endpoint:** `POST /v3/dataforseo_labs/google/domain_intersection/live` — $0.021 per request.

```
Usage: dfseo keywords domain-intersection [OPTIONS] DOMAINS...

Arguments:
  domains  DOMAINS...  Two to twenty domains to compare [required]

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --min-volume    INTEGER  Minimum search volume filter
  --limit     -n  INTEGER  Max results [default: 100]
  --fields    -F  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run               Show estimated cost
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Examples:**

```bash
# Compare two domains
dfseo keywords domain-intersection "example.com" "rival.com" --limit 200

# Three domains, high volume only
dfseo keywords domain-intersection "a.com" "b.com" "c.com" \
  --min-volume 500 --limit 100
```

**Output JSON (per keyword):**

```json
{
  "keyword": "email hosting plans",
  "search_volume": 2400,
  "keyword_difficulty": 45,
  "intersections": [
    {"domain": "example.com", "position": 3, "url": "https://example.com/plans"},
    {"domain": "rival.com", "position": 8, "url": "https://rival.com/hosting"}
  ]
}
```

---

## `dfseo keywords page-intersection`

Find keyword overlap between 2 to 20 specific URLs. Like domain-intersection, but scoped to individual pages.

**Endpoint:** `POST /v3/dataforseo_labs/google/page_intersection/live` — $0.021 per request.

```
Usage: dfseo keywords page-intersection [OPTIONS] URLS...

Arguments:
  urls  URLS...  Two to twenty URLs to compare [required]

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --min-volume    INTEGER  Minimum search volume filter
  --limit     -n  INTEGER  Max results [default: 100]
  --fields    -F  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run               Show estimated cost
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Example:**

```bash
dfseo keywords page-intersection \
  "https://example.com/email-hosting" \
  "https://rival.com/hosting-plans" \
  --min-volume 200 --limit 50
```

**Output JSON (per keyword):**

```json
{
  "keyword": "affordable email hosting",
  "search_volume": 1800,
  "keyword_difficulty": 38,
  "intersections": [
    {"url": "https://example.com/email-hosting", "position": 5},
    {"url": "https://rival.com/hosting-plans", "position": 12}
  ]
}
```

---

## `dfseo keywords relevant-pages`

Find the most relevant pages on a domain based on organic keyword rankings and traffic contribution.

**Endpoint:** `POST /v3/dataforseo_labs/google/relevant_pages/live` — $0.021 per request.

```
Usage: dfseo keywords relevant-pages [OPTIONS] DOMAIN

Arguments:
  domain  TEXT  Target domain (e.g., example.com) [required]

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --limit     -n  INTEGER  Max results [default: 100]
  --fields    -F  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run               Show estimated cost
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Example:**

```bash
dfseo keywords relevant-pages "example.com" --location "United States" --limit 50
```

**Output JSON (per page):**

```json
{
  "page": "https://example.com/email-hosting",
  "keywords_count": 342,
  "etv": 8540.2,
  "median_position": 6,
  "main_keyword": "email hosting",
  "main_keyword_volume": 4400
}
```

---

## `dfseo keywords subdomains`

Analyze subdomains of a target domain with their organic ranking metrics and traffic distribution.

**Endpoint:** `POST /v3/dataforseo_labs/google/subdomains/live` — $0.021 per request.

```
Usage: dfseo keywords subdomains [OPTIONS] DOMAIN

Arguments:
  domain  TEXT  Target domain (e.g., example.com) [required]

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --limit     -n  INTEGER  Max results [default: 100]
  --fields    -F  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run               Show estimated cost
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Example:**

```bash
dfseo keywords subdomains "example.com" --location "United States" --limit 20
```

**Output JSON (per subdomain):**

```json
{
  "subdomain": "blog.example.com",
  "keywords_count": 5620,
  "etv": 34200.5,
  "organic_is_up": 480,
  "organic_is_down": 310,
  "organic_is_new": 125,
  "organic_is_lost": 67
}
```

---

## `dfseo keywords top-searches`

Get trending and top searches related to a keyword. Shows rising queries and their popularity.

**Endpoint:** `POST /v3/dataforseo_labs/google/top_searches/live` — $0.021 per request.

```
Usage: dfseo keywords top-searches [OPTIONS] KEYWORD

Arguments:
  keyword  TEXT  Seed keyword [required]

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --limit     -n  INTEGER  Max results [default: 100]
  --fields    -F  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run               Show estimated cost
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Example:**

```bash
dfseo keywords top-searches "email hosting" --location "United States" --limit 30
```

**Output JSON (per result):**

```json
{
  "keyword": "free email hosting 2026",
  "search_volume": 6200,
  "cpc": 1.85,
  "keyword_difficulty": 42,
  "search_intent": "commercial"
}
```

---

## `dfseo keywords categories-for-domain`

Get topic categories that a domain is associated with, based on its organic keyword profile.

**Endpoint:** `POST /v3/dataforseo_labs/google/categories_for_domain/live` — $0.021 per request.

```
Usage: dfseo keywords categories-for-domain [OPTIONS] DOMAIN

Arguments:
  domain  TEXT  Target domain (e.g., example.com) [required]

Options:
  --location  -l  TEXT  Location name
  --language  -L  TEXT  Language name
  --fields    -F  TEXT  Comma-separated fields to include
  --raw-params    TEXT  Raw JSON payload
  --dry-run           Show estimated cost
  --output    -o  TEXT  Output format [default: auto]
  --login         TEXT  DataForSEO login
  --password      TEXT  DataForSEO password
  --verbose   -v        Verbose output
```

**Example:**

```bash
dfseo keywords categories-for-domain "example.com" --location "United States"
```

**Output JSON (per category):**

```json
{
  "category": "Internet & Telecom > Email & Messaging",
  "category_code": 13006,
  "keywords_count": 1240,
  "etv": 18500.3,
  "share": 0.28
}
```
