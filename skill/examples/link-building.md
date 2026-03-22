# Link Building Workflow

## Goal

Audit the current backlink profile, identify the strongest outreach
prospects, and deliver a prioritized link building plan the user can
execute immediately.

## When to Use

- The user asks for a link building strategy or outreach target list.
- The user wants to understand their backlink health or anchor text
  distribution.
- The user mentions "link building", "backlinks", "outreach", or
  "referring domains" in any context.

---

## Step 1: Profile Overview

```bash
dfseo backlinks summary "domain.com"
```

### What to look for

- Referring domain count matters more than raw backlink count because
  search engines reward link diversity over link volume.
- Dofollow ratio: a natural profile typically falls between 70% and
  90% dofollow.
- Broken backlinks signal redirect or reclaim opportunities that can
  recover lost link equity quickly.

### Decision

- Referring domains far below competitor levels: link acquisition is
  the top priority before any other SEO work.
- A large number of broken backlinks exist: fix those first because
  recovering existing equity is faster than earning new links.

---

## Step 2: Anchor Text Health Check

```bash
dfseo backlinks anchors "domain.com" --sort backlinks --limit 30
```

### What to look for

- Branded anchors (company name, domain URL, brand variations) should
  account for at least 30% of the profile to look natural.
- Exact-match keyword anchors should remain below 10% to stay clear
  of algorithmic penalties.
- Unexpected or irrelevant anchors may point to negative SEO attacks
  or low-quality link sources.

### Decision

- Anchor distribution is over-optimized: all future outreach should
  use branded, URL, or generic anchor text to dilute the ratio.
- Distribution looks healthy: move on to opportunity discovery
  without imposing anchor constraints.
- Spammy anchors detected: recommend building a disavow file before
  pursuing any new links.

---

## Step 3: Link Gap Analysis

```bash
dfseo backlinks gap "user.com" "comp1.com" "comp2.com" --min-rank 200
```

### What to look for

- Domains linking to every listed competitor but not the user are
  first-tier prospects. They already link within the niche, so the
  probability of earning a link is highest.
- Domains linking to at least one competitor are second-tier prospects
  worth reviewing individually.
- Apply an authority filter to keep the list focused on quality.

### Decision

- Many high-authority prospects available: the user can grow quickly
  through structured outreach campaigns.
- Few quality prospects in the gap: shift toward content-driven link
  earning by creating tools, studies, or visual assets that attract
  links without direct outreach.

---

## Step 4: Prospect Prioritization

```bash
dfseo backlinks referring-domains "competitor.com" --sort rank --limit 50
```

### What to look for

- Domains with rank 300 or higher deserve personalized, one-to-one
  outreach.
- Categorize each prospect by type: editorial blog, news publication,
  niche directory, or resource page. Each type requires a different
  pitch style.
- Topical relevance outweighs raw authority. A relevant site at rank
  300 is a better target than an unrelated site at rank 500.

### Decision

- Competitor's links come mainly from news outlets: the user needs a
  digital PR strategy with newsworthy angles.
- Most links originate from blogs: guest posting and collaborative
  content are the best approaches.
- Directory links dominate: submit to the same directories and
  resource lists as a quick-win tactic.

---

## Step 5: Monitor New and Lost Links

```bash
dfseo backlinks list "domain.com" --status new
```

```bash
dfseo backlinks list "domain.com" --status lost
```

### What to look for

- New links: confirm that outreach campaigns are producing measurable
  results over time.
- Lost links: flag any high-authority losses that warrant a recovery
  email to the webmaster.
- Link velocity: a sudden burst of low-quality new links may indicate
  a negative SEO attack. A sudden drop may mean linking pages were
  removed or domains expired.

### Decision

- Steady flow of quality new links: the current strategy is working.
  Continue and look for ways to scale.
- Lost links outpace new links: pause outreach and investigate root
  causes (content changes, expired domains, page removals).
- Negative SEO pattern detected: compile a disavow list and submit
  it through Search Console.

---

## Report Template

Organize the deliverable into these sections:

1. **Profile Snapshot** -- backlink total, referring domain count,
   domain rank, dofollow ratio, and overall spam risk.
2. **Anchor Text Audit** -- current distribution percentages with a
   clear verdict on whether rebalancing is needed.
3. **Prospect List** -- ranked table of outreach targets showing
   domain rank, domain type, and suggested pitch angle.
4. **Outreach Playbook** -- recommended approach for each prospect
   category (blogs, news, directories, resource pages).
5. **Recovery Opportunities** -- broken or lost backlinks worth
   reclaiming, with the original linking URL for each.
6. **Monitoring Cadence** -- how often to re-run each check and what
   thresholds should trigger action.
7. **Action Items** -- numbered list of next steps sorted by a
   combination of expected impact and required effort.
