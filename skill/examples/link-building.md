# Link Building Workflow

## Goal
Audit the current backlink profile, identify the strongest outreach
prospects, and deliver a prioritized link building plan.

## When to Use
- The user asks for a link building strategy or outreach target list.
- The user wants to understand backlink health or anchor distribution.
- The user mentions "link building", "backlinks", or "referring domains".

---

## Step 1: Profile Overview

```bash
dfseo backlinks summary "domain.com"
```

### What to look for
- Referring domain count matters more than raw backlink count because
  search engines reward diversity over volume.
- Dofollow ratio: a natural profile falls between 70% and 90% dofollow.
- Broken backlinks signal reclaim opportunities to recover link equity.

### Decision
- Referring domains far below competitor levels: link acquisition is
  the top priority.
- Many broken backlinks: fix those first because recovering existing
  equity is faster than earning new links.

---

## Step 2: Anchor Text Health Check

```bash
dfseo backlinks anchors "domain.com" --sort backlinks --limit 30
```

### What to look for
- Branded anchors (company name, domain URL, brand variations) should
  account for at least 30% of the profile to appear natural.
- Exact-match keyword anchors should stay below 10% to avoid penalties.
- Unexpected or irrelevant anchors may point to negative SEO attacks.

### Decision
- Over-optimized distribution: future outreach should use branded, URL,
  or generic anchor text to dilute the ratio.
- Healthy distribution: move on to opportunity discovery without
  imposing anchor constraints.
- Spammy anchors detected: build a disavow file before pursuing new
  links.

---

## Step 3: Link Gap Analysis

```bash
dfseo backlinks gap "user.com" "comp1.com" "comp2.com" --min-rank 200
```

### What to look for
- Domains linking to every listed competitor but not the user are
  first-tier prospects with the highest conversion probability.
- Domains linking to at least one competitor are second-tier prospects.
- Apply an authority filter to keep the list focused on quality.

### Decision
- Many high-authority prospects: the user can grow quickly through
  structured outreach campaigns.
- Few quality prospects: shift toward content-driven link earning by
  creating tools, studies, or visual assets.

---

## Step 4: Prospect Prioritization

```bash
dfseo backlinks referring-domains "competitor.com" --sort rank --limit 50
```

### What to look for
- Domains with rank 300+ deserve personalized one-to-one outreach.
- Categorize each prospect by type: blog, news, directory, or resource
  page. Each needs a different pitch.
- Topical relevance outweighs raw authority. A relevant site at rank
  300 beats an unrelated site at rank 500.

### Decision
- Links mainly from news outlets: the user needs a digital PR strategy
  with newsworthy angles.
- Most links from blogs: guest posting and content collaboration are
  the best approaches.
- Directory links dominate: submit to the same directories and resource
  lists as a quick win.

---

## Step 5: Monitor New and Lost Links

```bash
dfseo backlinks list "domain.com" --status new
```

```bash
dfseo backlinks list "domain.com" --status lost
```

### What to look for
- New links: confirm outreach campaigns are producing results.
- Lost links: flag high-authority losses that warrant a recovery email
  to the webmaster.
- Link velocity: a sudden burst of low-quality links may indicate
  negative SEO; a sudden drop may mean linking pages were removed.

### Decision
- Steady flow of quality new links: the current strategy is working.
  Continue and scale.
- Lost links outpace new links: pause outreach and investigate root
  causes (content changes, expired domains, page removals).
- Negative SEO pattern detected: compile a disavow list and submit it
  through Search Console.

---

## Report Template

Organize the deliverable into these sections:

1. **Profile Snapshot** -- backlink total, referring domains, domain
   rank, dofollow ratio, and spam risk.
2. **Anchor Text Audit** -- distribution percentages with a verdict on
   whether rebalancing is needed.
3. **Prospect List** -- ranked outreach targets with domain rank, type,
   and suggested pitch angle.
4. **Outreach Playbook** -- recommended approach per prospect category
   (blogs, news, directories, resource pages).
5. **Recovery Opportunities** -- broken or lost backlinks worth
   reclaiming, with the original linking URL.
6. **Monitoring Cadence** -- re-run frequency and thresholds that
   should trigger action.
7. **Action Items** -- numbered next steps sorted by expected impact
   and required effort.
