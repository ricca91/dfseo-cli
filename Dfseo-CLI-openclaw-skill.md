# dfseo-cli — OpenClaw Skill Integration Brief

> Brief per Claude Code — Pubblicazione come skill OpenClaw
> Autore: Ricc | Data: Marzo 2026
> Prerequisito: dfseo-cli installato e funzionante

-----

## Obiettivo

Creare una skill OpenClaw completa per `dfseo-cli` che permetta a qualsiasi agente OpenClaw di fare SEO research, keyword analysis, site audit e backlink analysis in autonomia.

La skill deve essere:

1. Installabile da ClawHub (`clawhub install dfseo`)
1. Installabile manualmente copiando la cartella in `~/.openclaw/skills/`
1. Completa di riferimenti per ogni command group

-----

## Struttura cartella skill

```
dfseo/
├── SKILL.md                    # Main skill file (frontmatter + istruzioni)
├── references/
│   ├── serp.md                 # Reference completo comandi SERP
│   ├── keywords.md             # Reference completo comandi Keywords
│   ├── site.md                 # Reference completo comandi Site Audit
│   └── backlinks.md            # Reference completo comandi Backlinks
├── examples/
│   ├── keyword-research.md     # Workflow: keyword research completo
│   ├── competitor-audit.md     # Workflow: audit competitor
│   └── link-building.md        # Workflow: trovare opportunità link building
└── scripts/
    └── install.sh              # Script di installazione (pip install dfseo)
```

-----

## SKILL.md — File principale

```markdown
---
name: dfseo
description: "SEO data from the terminal using DataForSEO APIs. Use when the user asks to check keyword rankings, analyze SERPs, run site audits, check backlink profiles, find keyword opportunities, compare competitors, do link gap analysis, check keyword difficulty or search volume, audit on-page SEO, or get Lighthouse scores. Triggers on: 'SEO', 'SERP', 'keyword research', 'backlinks', 'site audit', 'keyword difficulty', 'search volume', 'link building', 'competitor analysis', 'on-page SEO', 'Lighthouse', 'keyword ranking', 'referring domains', 'anchor text'."
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - dfseo
      env:
        - DATAFORSEO_LOGIN
        - DATAFORSEO_PASSWORD
    install:
      - id: pip
        kind: pip
        package: dfseo
        bins:
          - dfseo
        label: "Install dfseo CLI (pip)"
---

# dfseo-cli — SEO Data from Your Terminal

A CLI tool wrapping DataForSEO APIs. 43 commands for SERP analysis, keyword research, site audits, and backlink analysis. All output is JSON by default (machine-readable). Add `--output table` for human-readable format.

## Authentication

Requires DataForSEO API credentials. Set them as environment variables:

```bash
export DATAFORSEO_LOGIN="your@email.com"
export DATAFORSEO_PASSWORD="your_api_password"
```

Or run `dfseo auth setup` for interactive configuration (saves to `~/.config/dfseo/config.toml`).

Verify with: `dfseo auth status`

## Quick Reference

### SERP Analysis

```bash
# Google SERP for any keyword + location
dfseo serp google "keyword" --location "Country" --language "Language"

# Compare Google vs Bing
dfseo serp compare "keyword" --engines google,bing

# YouTube results
dfseo serp youtube "keyword"
```

### Keyword Research

```bash
# Volume, CPC, difficulty, search intent
dfseo keywords volume "kw1" "kw2" --location "Country" --include-serp-info

# Long-tail suggestions
dfseo keywords suggestions "seed keyword" --min-volume 100 --max-difficulty 40

# Semantically related keywords
dfseo keywords ideas "seed1" "seed2" --limit 100

# Bulk difficulty check (up to 1000)
dfseo keywords difficulty "kw1" "kw2" "kw3"
# Or from file:
dfseo keywords difficulty --from-file keywords.txt

# Keywords a domain ranks for
dfseo keywords for-site "domain.com" --min-volume 50 --sort volume
```

### Site Audit

```bash
# Full audit (crawl + wait + summary)
dfseo site audit "domain.com" --max-pages 100 --wait

# Quick single-page check
dfseo site audit "https://domain.com/page" --max-pages 1

# Drill down after audit
dfseo site pages "$TASK_ID" --errors-only
dfseo site links "$TASK_ID" --type broken
dfseo site duplicates "$TASK_ID" --type title

# Lighthouse performance
dfseo site lighthouse "https://domain.com" --categories performance --wait
```

### Backlink Analysis

```bash
# Backlink profile summary
dfseo backlinks summary "domain.com"

# List backlinks (new, lost, broken)
dfseo backlinks list "domain.com" --dofollow-only --sort rank
dfseo backlinks list "domain.com" --status new
dfseo backlinks list "domain.com" --status lost

# Anchor text analysis
dfseo backlinks anchors "domain.com" --search "brand" --sort backlinks

# Link gap: who links to competitors but not to you
dfseo backlinks gap "your-site.com" "competitor1.com" "competitor2.com"

# Bulk rank comparison (up to 1000 domains)
dfseo backlinks bulk ranks "site1.com" "site2.com" "site3.com"
dfseo backlinks bulk ranks --from-file domains.txt

# Historical backlink data (since 2019)
dfseo backlinks history "domain.com" --from 2024-01 --to 2026-03
```

## Output Conventions

- **Default output: JSON on stdout** — always parseable, no decorative text
- **Errors and progress: stderr** — never mixed with results
- **`--output table`** — human-readable formatted tables
- **`--output csv`** — for spreadsheets and data pipelines
- **`-q` / `--quiet`** — suppress everything except the result

Exit codes: 0 = success, 1 = error, 2 = auth failed, 3 = rate limited, 4 = bad params, 5 = insufficient funds.

## Common Patterns

### Keyword research workflow

```bash
# 1. Get seed keyword data
dfseo keywords volume "email hosting" --location "Italy" --language "Italian" --include-serp-info

# 2. Expand with suggestions
dfseo keywords suggestions "email hosting" --min-volume 50 --max-difficulty 40 --limit 50

# 3. Check difficulty for best candidates
dfseo keywords difficulty "email hosting professionale" "hosting email aziendale" --location "Italy"
```

### Competitor analysis workflow

```bash
# 1. Check competitor SERP presence
dfseo serp google "target keyword" --location "Italy" --depth 100

# 2. Find their keywords
dfseo keywords for-site "competitor.com" --location "Italy" --min-volume 100

# 3. Analyze their backlinks
dfseo backlinks summary "competitor.com"

# 4. Find link gap opportunities
dfseo backlinks gap "your-site.com" "competitor.com" --min-rank 200
```

### Site health check

```bash
# 1. Full audit
dfseo site audit "domain.com" --max-pages 200 --wait

# 2. Performance check
dfseo site lighthouse "https://domain.com" --wait

# 3. Check for broken links
dfseo site links "$TASK_ID" --type broken
```

## Service References

For detailed command documentation, load the specific reference file:

- **SERP commands** — See <references/serp.md>
- **Keywords commands** — See <references/keywords.md>
- **Site Audit commands** — See <references/site.md>
- **Backlinks commands** — See <references/backlinks.md>

## Important Notes

- Site audits are async: `dfseo site audit` with `--wait` blocks until crawl completes. Without `--wait`, it returns a task_id for later retrieval.
- Google Ads endpoints (`keywords ads-volume`, `keywords ads-suggestions`) have a 12 req/min rate limit.
- Backlinks API requires a $100/month minimum DataForSEO commitment.
- The `--from-file` flag accepts text files with one item per line (# comments and blank lines ignored).
- All location/language defaults can be set globally via `dfseo config set location "Italy"`.

```
---

## Reference Files

### references/serp.md

Deve contenere per ogni comando SERP:
- Sintassi completa con tutti i flag
- Descrizione di ogni flag
- Un esempio di comando
- Un esempio di output JSON (abbreviato)

Comandi da documentare:
- `dfseo serp google`
- `dfseo serp bing`
- `dfseo serp youtube`
- `dfseo serp compare`
- `dfseo serp locations`
- `dfseo serp languages`
- `dfseo auth setup`
- `dfseo auth status`
- `dfseo config set` / `dfseo config show`

### references/keywords.md

Comandi da documentare:
- `dfseo keywords volume`
- `dfseo keywords suggestions`
- `dfseo keywords ideas`
- `dfseo keywords difficulty`
- `dfseo keywords search-intent`
- `dfseo keywords for-site`
- `dfseo keywords ads-volume`
- `dfseo keywords ads-suggestions`

### references/site.md

Comandi da documentare:
- `dfseo site audit`
- `dfseo site crawl`
- `dfseo site summary`
- `dfseo site pages`
- `dfseo site links`
- `dfseo site duplicates`
- `dfseo site redirects`
- `dfseo site non-indexable`
- `dfseo site resources`
- `dfseo site lighthouse`
- `dfseo site tasks`

### references/backlinks.md

Comandi da documentare:
- `dfseo backlinks summary`
- `dfseo backlinks list`
- `dfseo backlinks anchors`
- `dfseo backlinks referring-domains`
- `dfseo backlinks history`
- `dfseo backlinks competitors`
- `dfseo backlinks gap`
- `dfseo backlinks pages`
- `dfseo backlinks bulk ranks`
- `dfseo backlinks bulk backlinks`
- `dfseo backlinks bulk spam-score`
- `dfseo backlinks bulk referring-domains`
- `dfseo backlinks bulk new-lost`

**Per ogni reference file:** genera il contenuto usando l'output di `dfseo <command> --help` come fonte primaria. Non inventare flag — leggi l'help reale.

---

## Example Files

### examples/keyword-research.md

```markdown
# Keyword Research Workflow

Complete workflow for finding and evaluating keyword opportunities.

## Step 1: Explore seed keywords
Run volume check for your initial ideas:
\`\`\`bash
dfseo keywords volume "email hosting" "smtp service" "business email" \
  --location "Italy" --language "Italian" --include-serp-info
\`\`\`
Look for: high volume, low-medium difficulty, commercial/transactional intent.

## Step 2: Expand with suggestions
\`\`\`bash
dfseo keywords suggestions "email hosting" \
  --location "Italy" --language "Italian" \
  --min-volume 50 --max-difficulty 40 --limit 100
\`\`\`

## Step 3: Find related ideas
\`\`\`bash
dfseo keywords ideas "email hosting" "smtp service" \
  --location "Italy" --limit 100
\`\`\`

## Step 4: Bulk difficulty check
Save best candidates to a file and check difficulty:
\`\`\`bash
dfseo keywords difficulty --from-file candidates.txt --location "Italy"
\`\`\`

## Step 5: Check SERP landscape
For top candidates, check what's currently ranking:
\`\`\`bash
dfseo serp google "best keyword" --location "Italy" --depth 20
\`\`\`
```

### examples/competitor-audit.md

```markdown
# Competitor Audit Workflow

Comprehensive competitor analysis: keywords, backlinks, on-page.

## Step 1: Find competitor keywords
\`\`\`bash
dfseo keywords for-site "competitor.com" \
  --location "Italy" --min-volume 100 --sort volume --limit 200
\`\`\`

## Step 2: Backlink profile
\`\`\`bash
dfseo backlinks summary "competitor.com"
\`\`\`

## Step 3: Top referring domains
\`\`\`bash
dfseo backlinks referring-domains "competitor.com" \
  --sort rank --limit 50 --exclude-internal
\`\`\`

## Step 4: Link gap (find their backlinks you don't have)
\`\`\`bash
dfseo backlinks gap "your-site.com" "competitor.com" --min-rank 200
\`\`\`

## Step 5: On-page audit comparison
\`\`\`bash
dfseo site audit "competitor.com" --max-pages 50 --wait
\`\`\`
```

### examples/link-building.md

```markdown
# Link Building Workflow

Find link building opportunities using backlink gap analysis.

## Step 1: Identify competitors
\`\`\`bash
dfseo backlinks competitors "your-site.com" --sort rank --limit 20
\`\`\`

## Step 2: Run link gap analysis
\`\`\`bash
dfseo backlinks gap "your-site.com" "competitor1.com" "competitor2.com" "competitor3.com" \
  --min-rank 200 --dofollow-only --limit 100
\`\`\`

## Step 3: Analyze top opportunities
For each high-rank domain from the gap:
\`\`\`bash
dfseo backlinks list "your-site.com" --from-domain "opportunity-domain.com"
\`\`\`

## Step 4: Check anchor text distribution
\`\`\`bash
dfseo backlinks anchors "your-site.com" --sort backlinks
\`\`\`
Healthy profile: branded anchors > exact-match keyword anchors.
```

-----

## scripts/install.sh

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Installing dfseo-cli..."

if command -v pip &> /dev/null; then
    pip install dfseo
elif command -v pip3 &> /dev/null; then
    pip3 install dfseo
else
    echo "Error: pip not found. Install Python 3.11+ first." >&2
    exit 1
fi

if command -v dfseo &> /dev/null; then
    echo "✓ dfseo-cli installed successfully"
    dfseo --version
else
    echo "Error: dfseo command not found after installation." >&2
    echo "Make sure ~/.local/bin is in your PATH." >&2
    exit 1
fi

echo ""
echo "Next steps:"
echo "  1. Set credentials:"
echo "     export DATAFORSEO_LOGIN='your@email.com'"
echo "     export DATAFORSEO_PASSWORD='your_api_password'"
echo "  2. Verify: dfseo auth status"
echo "  3. Try: dfseo serp google 'test keyword'"
```

-----

## Pubblicazione su ClawHub

### Step 1: Verifica la skill localmente

```bash
# Copia la skill nella cartella locale
cp -r dfseo/ ~/.openclaw/skills/dfseo/

# Apri OpenClaw e verifica che la skill appaia
# L'emoji 🔍 dovrebbe essere visibile nella lista skill
```

### Step 2: Pubblica su ClawHub

```bash
# Installa clawhub CLI se non presente
npm install -g clawhub

# Pubblica
clawhub publish ./dfseo/
```

### Step 3: Includi nel repo GitHub

Aggiungi la cartella `skill/` (o `openclaw-skill/`) nella root del repo `dfseo-cli` su GitHub, così chi clona il repo ha già la skill pronta:

```
dfseo-cli/
├── src/
├── tests/
├── skill/                    # OpenClaw skill
│   ├── SKILL.md
│   ├── references/
│   ├── examples/
│   └── scripts/
├── SKILL.md                  # Copia semplificata nella root (per Claude Code e altri agent)
├── pyproject.toml
└── README.md
```

La `SKILL.md` nella root è la versione compatta (già presente dalla v1.0). La cartella `skill/` è la versione completa per OpenClaw con reference files ed esempi.

-----

## Istruzioni per Claude Code

### Cosa fare

1. **Crea la struttura cartella** `skill/` con tutti i file
1. **Genera il SKILL.md** con il frontmatter esatto indicato sopra — il campo `description` è critico per il triggering automatico
1. **Genera i 4 reference files** usando `dfseo <command> --help` come fonte per ogni comando. Esegui i comandi help reali, non inventare flag
1. **Crea i 3 example files** con workflow completi e realistici
1. **Crea install.sh** e rendilo eseguibile (`chmod +x`)
1. **Testa localmente** copiando in `~/.openclaw/skills/` e verificando che OpenClaw la carichi
1. **Pubblica su ClawHub** con `clawhub publish`

### Cosa NON fare

- Non inventare flag o comandi — tutto deve corrispondere al CLI reale
- Non mettere troppo testo nel SKILL.md principale — gli agenti hanno context window limitati. I dettagli vanno nei reference files
- Non usare `metadata.clawdbot` — usa `metadata.openclaw` (il formato corrente)
- Non dimenticare il campo `requires.bins` — senza questo OpenClaw non sa che serve `dfseo` installato
- Non dimenticare `requires.env` — senza questo l’agente non chiederà le credenziali

-----

## Riferimenti

- OpenClaw Skills Docs: https://docs.openclaw.ai/tools/skills
- ClawHub (registry): https://github.com/openclaw/clawhub
- Skill format reference: https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md
- Example skills: https://github.com/VoltAgent/awesome-openclaw-skills
- gogcli skill (ispirazione): https://lobehub.com/skills/ninehills-skills-gogcli
