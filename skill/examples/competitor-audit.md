# Competitor Analysis Workflow

## Goal
Benchmark the user's domain against organic competitors to surface keyword
gaps, authority differences, and backlink opportunities, then turn every
finding into a concrete action.

## When to Use
- The user names one or more competitor domains and wants a comparison.
- The user asks "who are my competitors?" or "why do they outrank me?"
- The user needs a competitive landscape overview before planning content.

---

## Step 1: Discover Organic Competitors

```bash
dfseo keywords competitors-domain "domain.com" --limit 10
```

### What to look for
- Domains sharing the largest keyword overlap with the user's site.
  These are the true organic competitors regardless of whether the user
  considers them business competitors.
- Discard generic giants (Wikipedia, Amazon, YouTube) unless the user
  explicitly wants them included.
- Select 3-5 competitors for the remaining steps.

### Decision
- User already supplied competitor names: skip discovery entirely.
- Fewer than 3 useful competitors returned: raise the limit to 20 or
  try a secondary seed domain owned by the user.

---

## Step 2: Keyword Gap Analysis

```bash
dfseo keywords domain-intersection "user-site.com" "competitor.com"
```

### What to look for
- Keywords the competitor owns exclusively represent new content
  opportunities for the user.
- Keywords both sites rank for where the competitor sits higher are
  on-page optimization targets.
- Focus on search volume: a gap on a high-volume term is worth more
  than dozens of low-volume misses.

### Decision
- Heavy overlap with the user ranking lower on most terms: prioritize
  refreshing and strengthening existing pages.
- Minimal overlap: the two sites target different audiences. Verify the
  competitor's unique keywords matter to the user before acting.
- User already leads on shared keywords: pivot toward the competitor's
  exclusive terms as expansion targets.

---

## Step 3: Domain Authority Comparison

```bash
dfseo backlinks bulk ranks "user.com" "comp1.com" "comp2.com"
```

### What to look for
- The domain rank score for every site in the set.
- The size of the gap between the user and the strongest competitor.

### Decision
- User's rank is substantially lower: recommend a link building campaign
  before expecting ranking gains from content alone.
- Ranks are close: competition is decided by content quality and
  technical SEO, not raw authority.

---

## Step 4: Backlink Gap

```bash
dfseo backlinks gap "user.com" "comp1.com" "comp2.com" --min-rank 200
```

### What to look for
- Referring domains that link to competitors but not the user. These
  sites have demonstrated willingness to link within the niche, making
  them high-probability outreach targets.
- Domains with rank 300+ deserve personalized outreach.
- Note domain types (blog, news, directory, resource page) so the
  outreach pitch matches each prospect.

### Decision
- Plenty of high-authority gap domains: build a tiered outreach list
  starting from the highest rank downward.
- Most gap domains are low quality: skip direct outreach and invest in
  linkable assets that attract links organically.

---

## Step 5: Competitor Traffic Deep Dive (Optional)

```bash
dfseo keywords ranked-keywords "competitor.com" --sort traffic --limit 50
```

### What to look for
- The competitor's biggest traffic drivers reveal which pages earn the
  most organic visits.
- High-traffic keywords with moderate difficulty are the best targets
  for new content on the user's site.

### Decision
- A few pillar pages drive most traffic: the user should create
  competing long-form content on those topics.
- Traffic is spread across many long-tail terms: the competitor relies
  on breadth. Target topical clusters to compete efficiently.

---

## Report Template

Organize the deliverable into these sections:

1. **Executive Summary** -- one paragraph on overall competitive
   position and the single highest-impact finding.
2. **Authority Comparison** -- table of domain ranks with a short note
   on what the gap means in practice.
3. **Keyword Gaps** -- top missed opportunities sorted by volume.
4. **Keyword Overlaps** -- terms where the user trails a competitor,
   with position differences.
5. **Backlink Opportunities** -- prioritized prospect list with domain
   rank and domain type.
6. **Competitor Strengths** -- tactics or content patterns worth
   learning from.
7. **Recommended Actions** -- numbered checklist ordered by expected
   impact, each item specific enough to act on immediately.
