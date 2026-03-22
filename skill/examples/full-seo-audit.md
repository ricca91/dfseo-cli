# Full SEO Audit Workflow

## Goal

Produce a comprehensive SEO analysis of a domain covering authority, organic visibility, technical health, and actionable recommendations. This is the all-in-one workflow — run it when a user asks for a complete picture of where a site stands and what to fix first.

## When to Use

- The user asks for an "SEO audit", "SEO analysis", or "site overview"
- The user wants to know the overall health of a domain before starting optimization
- A new client onboarding where you need a baseline report

## Estimated Cost

A full audit typically costs $0.15–0.30 in API credits depending on site size and the number of keywords returned.

---

## Step 1: Verify Credentials

```bash
dfseo auth status
```

### What to check

- Credentials are valid and the API responds
- Account balance is sufficient (at least $0.50 recommended for a full audit with margin)

### Decision

- If balance < $0.15: stop and warn the user that the audit may be incomplete
- If credentials are invalid: guide the user through `dfseo auth login`

---

## Step 2: Domain Authority & Traffic

```bash
dfseo keywords domain-rank "domain.com" --location "Country"
```

### What to look for

- **domain_rank**: overall authority signal. Interpretation:
  - 0–20: new or very small site
  - 20–40: growing site with some authority
  - 40–60: established mid-tier site
  - 60–80: strong authority in its niche
  - 80+: top-tier domain (major brand, news outlet, etc.)
- **organic_traffic**: estimated monthly organic visitors — this is the baseline to beat
- **organic_cost**: estimated value of that traffic in USD (what you would pay in ads)

### Decision

- If domain_rank is 0 or missing: the domain may be brand new or not indexed. Flag this early and adjust expectations for later steps.

---

## Step 3: Top Organic Keywords

```bash
dfseo keywords ranked-keywords "domain.com" \
  --location "Country" --sort traffic --limit 50
```

### What to look for

- **Top-10 vs top-100 split**: how many keywords actually drive traffic from page one?
- **Traffic concentration**: if the top 3 keywords account for >60% of traffic, the site is vulnerable to ranking drops
- **Keyword difficulty**: are the top positions defended against hard competition, or are they low-difficulty wins?
- **Brand vs non-brand**: separate branded keywords (containing the company name) from generic terms to get a true organic reach picture

### Decision

- If fewer than 10 keywords in top 10: organic visibility is weak, keyword strategy needed
- If traffic is concentrated on 1–3 keywords: flag diversification as a priority

---

## Step 4: Backlink Profile

```bash
dfseo backlinks summary "domain.com"
```

### What to look for

- **referring_domains vs total backlinks**: a healthy ratio is roughly 1:5. A ratio of 1:100+ suggests spammy link patterns.
- **dofollow vs nofollow ratio**: healthy profiles are 60–80% dofollow. Below 50% may indicate low-quality sources.
- **broken_backlinks**: links pointing to 404 pages. Each one is a wasted authority signal and a redirect opportunity.
- **spam_score**: overall toxicity indicator

### Decision

- If spam_score > 15: flag for toxic link audit. Consider running `dfseo backlinks anchors "domain.com"` to check for suspicious anchor text patterns.
- If referring_domains < 50: flag weak authority. Link building should be a primary recommendation.
- If broken_backlinks > 0: note these for the recommendations section — quick wins via 301 redirects.

---

## Step 5: Technical Health

```bash
dfseo site audit "domain.com" --max-pages 100
```

This command blocks until the crawl completes. Save the returned `task_id` for drill-down commands.

### What to look for

- **onpage_score**: overall technical health (0–100)
- **pages_crawled** vs **pages with errors**: what percentage of the site has issues?
- **Critical issues**: broken pages, missing titles, duplicate content, redirect chains

### Decision

- If onpage_score < 70: the site has significant technical debt. Drill down:

```bash
# Find pages returning errors (4xx, 5xx)
dfseo site pages TASK_ID --errors-only

# Find broken internal and external links
dfseo site links TASK_ID --type broken

# Find duplicate title tags (a common content issue)
dfseo site duplicates TASK_ID --type title
```

- If onpage_score >= 80: technical health is solid. Focus recommendations on content and authority instead.
- Between 70–80: address critical issues but do not overhaul — targeted fixes will suffice.

---

## Step 6: Performance (Lighthouse)

```bash
dfseo site lighthouse "https://domain.com" \
  --categories performance,seo,accessibility
```

### What to look for

- **performance_score**: Core Web Vitals (LCP, FID, CLS). Below 50 is a ranking liability.
- **seo_score**: basic SEO compliance (meta tags, crawlability, structured data). Should be 90+.
- **accessibility_score**: WCAG compliance. Below 70 means usability issues that also affect SEO.

### Decision

- If performance_score < 50: flag as urgent. Slow sites lose rankings and conversions.
- If seo_score < 80: there are fundamental SEO hygiene issues to resolve before worrying about content.

---

## Step 7: Tech Stack

```bash
dfseo domain technologies "domain.com"
```

### What to look for

- **CMS platform**: WordPress, Shopify, custom, etc. — this shapes what technical fixes are feasible
- **Analytics tools**: Google Analytics, Matomo, etc. — confirms tracking is in place
- **CDN usage**: Cloudflare, Fastly, etc. — affects performance recommendations
- **Security headers and SSL**: missing HTTPS or security headers is both a ranking and trust issue

---

## Producing the Report

After gathering all data, generate the report in both formats below.

### Markdown Report Template

```markdown
# SEO Audit Report: [domain.com]

**Date:** [YYYY-MM-DD]
**Analyst:** AI-assisted via dfseo CLI
**Scope:** [X] pages crawled | [Country] market

---

## Executive Summary

[domain.com] has a domain rank of [X] with an estimated [X] monthly organic visitors
valued at $[X]. The site ranks for [X] keywords in the top 100, with [X] in the top 10.

**Overall health:** [Good / Needs Work / Critical]
**Top priority:** [One sentence describing the single highest-impact action]

---

## Authority Profile

| Metric              | Value   | Assessment      |
|---------------------|---------|-----------------|
| Domain Rank         | [X]     | [Interpretation] |
| Backlinks           | [X]     | —               |
| Referring Domains   | [X]     | [Healthy/Weak]  |
| Dofollow Ratio      | [X]%   | [Healthy/Low]   |
| Spam Score          | [X]     | [Safe/At Risk]  |
| Broken Backlinks    | [X]     | [Action needed?] |

---

## Organic Visibility

**Total keywords (top 100):** [X]
**Keywords in top 10:** [X]
**Estimated monthly traffic:** [X]
**Traffic value:** $[X]

### Top Keywords by Traffic

| Keyword            | Position | Volume  | Traffic | Difficulty |
|--------------------|----------|---------|---------|------------|
| [keyword 1]        | [X]      | [X]     | [X]     | [X]        |
| [keyword 2]        | [X]      | [X]     | [X]     | [X]        |
| [keyword 3]        | [X]      | [X]     | [X]     | [X]        |
| [keyword 4]        | [X]      | [X]     | [X]     | [X]        |
| [keyword 5]        | [X]      | [X]     | [X]     | [X]        |

**Traffic concentration risk:** [Low / Medium / High] — top 3 keywords account for [X]% of traffic.

---

## Technical Health

| Metric             | Value   | Assessment      |
|--------------------|---------|-----------------|
| Onpage Score       | [X]/100 | [Good/Fair/Poor] |
| Pages Crawled      | [X]     | —               |
| Pages with Errors  | [X]     | [X]% error rate |
| Broken Links       | [X]     | [Action needed?] |
| Duplicate Titles   | [X]     | [Action needed?] |

### Critical Issues

1. [Issue description and affected URLs]
2. [Issue description and affected URLs]
3. [Issue description and affected URLs]

---

## Performance (Lighthouse)

| Category       | Score   | Assessment      |
|----------------|---------|-----------------|
| Performance    | [X]/100 | [Good/Fair/Poor] |
| SEO            | [X]/100 | [Good/Fair/Poor] |
| Accessibility  | [X]/100 | [Good/Fair/Poor] |

**Key findings:** [Summary of Core Web Vitals and any failed audits]

---

## Tech Stack

| Category       | Technology      |
|----------------|-----------------|
| CMS            | [X]             |
| Analytics      | [X]             |
| CDN            | [X]             |
| SSL            | [Yes/No]        |
| Security       | [Headers found] |

---

## Opportunities

1. **[Opportunity title]** — [description and estimated impact]
2. **[Opportunity title]** — [description and estimated impact]
3. **[Opportunity title]** — [description and estimated impact]

---

## Prioritized Recommendations

### High Priority (do first)
1. [Recommendation with specific action]
2. [Recommendation with specific action]

### Medium Priority (next 30 days)
1. [Recommendation with specific action]
2. [Recommendation with specific action]

### Low Priority (backlog)
1. [Recommendation with specific action]
2. [Recommendation with specific action]
```

### JSON Report Schema

```json
{
  "domain": "example.com",
  "report_date": "YYYY-MM-DD",
  "authority": {
    "domain_rank": 0,
    "backlinks": 0,
    "referring_domains": 0,
    "dofollow_ratio": 0,
    "spam_score": 0,
    "broken_backlinks": 0
  },
  "organic": {
    "traffic": 0,
    "traffic_value": 0,
    "keywords_total": 0,
    "keywords_top10": 0,
    "traffic_concentration_top3_pct": 0,
    "top_keywords": [
      {
        "keyword": "",
        "position": 0,
        "volume": 0,
        "traffic": 0,
        "difficulty": 0
      }
    ]
  },
  "technical": {
    "onpage_score": 0,
    "pages_crawled": 0,
    "pages_with_errors": 0,
    "broken_links": 0,
    "duplicate_titles": 0,
    "critical_issues": []
  },
  "performance": {
    "lighthouse_performance": 0,
    "lighthouse_seo": 0,
    "lighthouse_accessibility": 0
  },
  "tech_stack": {
    "cms": "",
    "analytics": [],
    "cdn": "",
    "ssl": true
  },
  "opportunities": [],
  "recommendations": {
    "high": [],
    "medium": [],
    "low": []
  }
}
```
