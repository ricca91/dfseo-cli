# Keyword Research Workflow

## Goal

Find and prioritize keyword opportunities for a website or content plan.
Given a set of seed terms (or a domain), produce a ranked list of keywords
grouped by search intent, with difficulty and volume data to guide decisions.

## When to Use

- User asks to find keywords for a topic or niche
- User wants to expand a seed list into a full content plan
- User needs to identify ranking opportunities with low competition
- User wants to know what a competitor ranks for

---

## Step 1: Baseline Seed Analysis

Start by checking whether the seed keywords have any real demand.

```bash
dfseo keywords volume "seed1" "seed2" "seed3" \
  --location "United States" --include-serp-info
```

### What to look for

- **search_volume**: Is there meaningful demand? Anything above 100/month is worth exploring.
- **keyword_difficulty**: Can we realistically compete? Under 40 is approachable for newer sites.
- **cpc**: Higher CPC signals commercial value — advertisers pay more for keywords that convert.
- **competition**: The paid-search competition index (0-1) confirms commercial interest.

### Decision

- If volume < 50 for ALL seeds: the niche may be too narrow. Try broader or more generic terms.
- If difficulty > 70 for ALL seeds: go to Step 2 immediately and focus on long-tail variants.
- If some seeds show volume > 500 with difficulty < 50: these are strong candidates — carry them forward.

---

## Step 2: Expand with Long-Tail Suggestions

Take your best-performing seed and expand it into longer, more specific phrases.

```bash
dfseo keywords suggestions "best seed keyword" \
  --min-volume 100 --max-difficulty 40 --limit 50
```

### What to look for

- **Volume/difficulty sweet spots**: High volume + low difficulty = quick wins.
- **Question keywords** (how, what, why, can I): These signal informational intent and are ideal for blog posts, guides, and FAQ pages.
- **Modifier patterns** (best, top, cheap, vs, alternative): These indicate comparison or commercial intent.

### Decision

- If you get fewer than 10 results: loosen the filters (lower min-volume to 50 or raise max-difficulty to 60).
- If results are dominated by questions: you have an informational topic — plan educational content.
- If results contain "buy", "price", "deal" modifiers: there is transactional opportunity.

---

## Step 3: Semantic Expansion

Discover related keywords you may not have considered. This surfaces the broader topic cluster.

```bash
dfseo keywords ideas "seed1" "seed2" --limit 100
```

### What to look for

- **Unexpected angles**: Keywords that reframe the topic in ways you had not considered.
- **Topic clusters**: Groups of related terms that could each become a page or section.
- **Overlapping terms**: If the same keyword appears in both Step 2 and Step 3 results, it is a strong signal.

### Decision

- If clusters emerge around 3-5 themes: plan a content hub with a pillar page and supporting articles.
- If results are scattered with no clear grouping: the seed may be too broad — pick a sub-theme and repeat.

---

## Step 4: Difficulty Check on Best Candidates

Collect the most promising keywords from Steps 2 and 3, then verify difficulty in bulk.

```bash
dfseo keywords difficulty "candidate kw1" "candidate kw2" "candidate kw3"
```

Or from a file, one keyword per line:

```bash
dfseo keywords difficulty --from-file candidates.txt
```

### What to look for

- **Surprises**: Keywords that looked easy based on volume data but have hidden difficulty due to strong domains ranking for them.
- **Consistency**: If difficulty scores roughly match what you saw earlier, the data is reliable.

### Decision

- Drop any keyword where difficulty jumped above your threshold after this check.
- Keep keywords where difficulty is confirmed low — these are your priority targets.

---

## Step 5: Intent Classification

Map each surviving keyword to the right content type.

```bash
dfseo keywords search-intent "kw1" "kw2" "kw3" "kw4"
```

### What to look for

- **Informational**: Blog posts, how-to guides, tutorials.
- **Commercial**: Comparison pages, reviews, "best of" lists.
- **Transactional**: Product pages, landing pages, pricing pages.
- **Navigational**: Brand pages — usually not worth targeting unless it is your brand.

### Decision

- Group keywords by intent. Each group becomes a different content type.
- If most keywords are informational: build a blog-first strategy.
- If most keywords are transactional: focus on product and landing pages.

---

## Step 6: SERP Landscape for Top Candidates

For your highest-priority keywords, check who currently owns the first page.

```bash
dfseo serp google "top keyword" --depth 20
```

### What to look for

- **Domain authority of ranking sites**: All Fortune 500 companies? Or smaller, beatable sites?
- **SERP features**: Featured snippets, People Also Ask, video carousels — each is an opportunity to appear without a traditional #1 ranking.
- **Content type ranking**: Are the top results blog posts, product pages, or tools? Match the format.

### Decision

- If the top 10 is dominated by major brands (Amazon, Wikipedia, Forbes): target a more specific long-tail variant.
- If you see smaller or niche sites ranking: this is winnable with quality content.
- If featured snippets are present: structure your content to capture them (clear answers, lists, tables).

---

## Optional: Trend and Seasonality Analysis

Check whether your keywords are growing, declining, or seasonal.

```bash
dfseo keywords historical-volume "kw1" "kw2"
```

### What to look for

- **Upward trend**: Invest now before competition catches up.
- **Downward trend**: Proceed with caution — the topic may be fading.
- **Seasonal spikes**: Time your content to publish 4-6 weeks before peak season.

---

## Optional: Competitor Keyword Mining

Find keywords that a competitor ranks for and you do not.

```bash
dfseo keywords for-site "competitor.com" \
  --min-volume 50 --sort volume --limit 200
```

### What to look for

- **High-volume keywords** where the competitor ranks on page 2 or 3 — these are vulnerable positions you can overtake.
- **Keywords outside your current topic map** — potential new content areas.

---

## Output: Final Report Structure

After completing the workflow, compile results into a prioritized keyword list:

| Keyword | Volume | Difficulty | CPC | Intent | Priority |
|---------|--------|------------|-----|--------|----------|
| ...     | ...    | ...        | ... | ...    | ...      |

**Priority scoring guideline**:
- High: volume > 500, difficulty < 40, commercial or transactional intent
- Medium: volume 100-500, difficulty 40-60, any intent
- Low: volume < 100 or difficulty > 60

Group the final list by intent cluster to guide the content calendar.
