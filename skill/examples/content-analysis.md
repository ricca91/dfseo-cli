# Content & Brand Analysis Workflow

## Goal

Analyze the online content landscape around a keyword, brand, or topic. Understand who's writing about it, what the sentiment is, and where mentions appear.

## When to Use

- User asks about brand reputation or online mentions
- User wants to understand content landscape around a topic
- User asks about sentiment analysis for a brand or keyword
- User wants to find who's writing about a subject

---

## Step 1: Content Landscape Overview

```bash
dfseo content summary "brand name"
```

### What to look for

- **total_count**: how much content exists about this topic
- **top_domains**: which sites write about it most (are they authoritative? competitors? news sites?)
- **content_types**: distribution of article types
- **sentiment breakdown**: overall positive/negative/neutral split

### Decision

- If total_count is very low (< 100): brand has minimal online presence — could be opportunity or concern
- If one domain dominates top_domains: investigate if it's a competitor or media partner
- If sentiment skews heavily negative: drill down into negative mentions (Step 3b)

---

## Step 2: Find Specific Mentions

```bash
dfseo content search "brand name" --limit 20 --sort content_score
```

### What to look for

- **url/domain**: where is the brand mentioned?
- **content_score**: quality of the content (higher = more authoritative)
- **spam_score**: is it from a legitimate source? (> 5 = suspicious)
- **date**: how recent are the mentions?

### Decision

- If most mentions are from low-quality/spam sites: brand perception issue
- If mentions are concentrated in recent dates: something is trending (news, viral content, controversy)
- If no recent mentions: brand may have low visibility — content marketing opportunity

---

## Step 3a: Sentiment Deep Dive

```bash
dfseo content sentiment "brand name" --limit 20
```

### What to look for

- **sentiment per result**: which specific articles are positive/negative?
- **domain + sentiment combination**: are authoritative sources positive or negative?
- **content_score + sentiment**: high-quality negative content is more damaging than low-quality negative content

---

## Step 3b: Focus on Negative Mentions (if needed)

```bash
dfseo content search "brand name" --sentiment negative --limit 20
```

### What to look for

- **What are the complaints?** Read the titles for patterns
- **Who's writing negative content?** News sites? Review sites? Competitors?
- **How recent?** Recent negative content needs faster response

---

## Step 4: Time-Bounded Analysis (optional)

```bash
dfseo content search "brand name" --from-date 2025-01-01 --to-date 2026-01-01 --limit 20
```

Useful for:
- Measuring impact of a PR campaign
- Comparing before/after a product launch
- Tracking seasonal patterns

---

## Producing the Report

### Markdown Report Template

```markdown
# Content & Brand Analysis: [brand/keyword]

## Overview
- Total mentions found: [X]
- Date range analyzed: [from] to [to]
- Top mentioning domains: [list top 5]

## Sentiment Distribution
| Sentiment | Count | Percentage |
|-----------|-------|-----------|
| Positive | [X] | [Y]% |
| Neutral | [X] | [Y]% |
| Negative | [X] | [Y]% |

## Key Findings
1. [Most significant finding]
2. [Second finding]
3. [Third finding]

## Notable Mentions
| Source | Title | Sentiment | Quality Score |
|--------|-------|-----------|--------------|
| [domain] | [title] | [pos/neg/neutral] | [score] |

## Recommendations
- [Action item based on findings]
```

### JSON Report Schema

```json
{
  "brand": "example",
  "report_date": "YYYY-MM-DD",
  "total_mentions": 0,
  "sentiment": {
    "positive": 0,
    "neutral": 0,
    "negative": 0
  },
  "top_domains": [],
  "notable_mentions": [],
  "recommendations": []
}
```
