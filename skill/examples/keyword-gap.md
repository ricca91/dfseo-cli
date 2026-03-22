# Keyword Gap Analysis Workflow

## Goal

Find keyword opportunities by analyzing the overlap and gaps between domains or specific pages. Identify keywords competitors rank for that the user's site doesn't, and keywords where the user could improve positions.

## When to Use

- User wants to find keyword gaps between their site and competitors
- User asks "what keywords does [competitor] rank for that I don't?"
- User wants to compare organic visibility between domains
- User wants to compare specific pages for keyword overlap

---

## Step 1: Identify Competitors (if not provided)

```bash
dfseo keywords competitors-domain "user-site.com" --location "Country" --limit 10
```

### What to look for

- **avg_position**: competitors with similar average positions are the most relevant
- **intersections_count**: domains with high keyword overlap are direct competitors
- **estimated_traffic**: competitors getting more traffic with similar keywords = biggest opportunity

### Decision

- Pick 2-3 most relevant competitors for gap analysis
- If user already knows their competitors, skip this step

---

## Step 2: Domain Keyword Gap

```bash
dfseo keywords domain-intersection "user-site.com" "competitor1.com" --location "Country" --min-volume 100 --limit 100
```

### What to look for

The intersection shows keywords both domains rank for. Look at the differences:

- **Keywords where competitor ranks in top 10 but user ranks 20+**: biggest improvement opportunities
- **Keywords where only competitor ranks (user has no position)**: content gaps — new pages needed
- **Keywords where user ranks higher**: current strengths to protect and expand

### Decision

- If many content gaps exist: prioritize creating new content
- If many position gaps exist: prioritize improving existing content
- If user outranks competitor on most keywords: look at the next competitor

---

## Step 3: Expand with Multiple Competitors

```bash
dfseo keywords domain-intersection "user-site.com" "comp1.com" "comp2.com" "comp3.com" --min-volume 50 --limit 200
```

### What to look for

- Keywords where **multiple** competitors rank but user doesn't = highest-priority gaps
- If 3 out of 3 competitors rank for a keyword and user doesn't, that keyword is almost certainly relevant

---

## Step 4: Page-Level Intersection (optional)

When the user wants to compare specific pages (e.g., their product page vs competitor's product page):

```bash
dfseo keywords page-intersection "https://user-site.com/page" "https://competitor.com/similar-page" --min-volume 50 --limit 100
```

### What to look for

- Keywords the competitor page ranks for that the user's page doesn't
- These are on-page optimization opportunities: the user can update their page to target these keywords

---

## Step 5: Validate Opportunities

Take the top keyword gaps and check difficulty:

```bash
dfseo keywords difficulty "gap-kw1" "gap-kw2" "gap-kw3" --location "Country"
```

### What to look for

- Filter out keywords with difficulty > 70 (unless user has high authority)
- Prioritize: high volume + low difficulty + commercial intent

Then classify intent:

```bash
dfseo keywords search-intent "gap-kw1" "gap-kw2" "gap-kw3"
```

### What to look for

- Map each gap keyword to the right content type
- Informational gaps → blog posts
- Commercial gaps → comparison/review pages
- Transactional gaps → product/service pages

---

## Producing the Report

### Markdown Report Template

```markdown
# Keyword Gap Analysis: [user domain] vs [competitors]

## Executive Summary
- Domains compared: [list]
- Total keyword gaps found: [X]
- High-priority opportunities: [Y]

## Keyword Gaps (Competitor Ranks, You Don't)

| Keyword | Volume | Difficulty | Intent | Competitors Ranking |
|---------|--------|-----------|--------|-------------------|
| [kw] | [vol] | [diff] | [intent] | comp1 #3, comp2 #7 |

## Position Gaps (Both Rank, Competitor Higher)

| Keyword | Volume | Your Position | Best Competitor | Gap |
|---------|--------|--------------|----------------|-----|
| [kw] | [vol] | #[X] | comp1 #[Y] | [X-Y] |

## Your Strengths (You Outrank Competitors)

| Keyword | Volume | Your Position | Best Competitor |
|---------|--------|--------------|----------------|
| [kw] | [vol] | #[X] | comp1 #[Y] |

## Recommendations
1. **Create content for:** [top 5 content gap keywords with rationale]
2. **Improve existing pages for:** [top 5 position gap keywords]
3. **Protect rankings on:** [top 5 strengths to maintain]
```

### JSON Report Schema

```json
{
  "user_domain": "example.com",
  "competitors": ["comp1.com", "comp2.com"],
  "report_date": "YYYY-MM-DD",
  "content_gaps": [
    {"keyword": "", "volume": 0, "difficulty": 0, "intent": "", "competitor_positions": {}}
  ],
  "position_gaps": [
    {"keyword": "", "volume": 0, "user_position": 0, "best_competitor_position": 0}
  ],
  "strengths": [
    {"keyword": "", "volume": 0, "user_position": 0, "best_competitor_position": 0}
  ],
  "recommendations": []
}
```
