# dfseo-cli — Landing Page Brief

> Brief per Claude Code — Landing page da deployare su Vercel
> Autore: Ricc | Data: Marzo 2026
> CTA: GitHub star + pip install

-----

## Obiettivo

Creare una landing page single-page per dfseo-cli. Il target è developer, SEO tecnici, e builder che lavorano con AI agents. La pagina deve convertire in **GitHub stars** e **pip install**.

Deploy su Vercel → il progetto deve essere un Next.js app minimale o un sito statico (HTML/CSS/JS) con `vercel.json`.

-----

## Stack Consigliato

|Componente|Scelta                                                               |Motivazione                    |
|----------|---------------------------------------------------------------------|-------------------------------|
|Framework |**Next.js (App Router)** o **HTML statico**                          |Vercel-native, zero config     |
|Styling   |**Tailwind CSS**                                                     |Veloce, responsive, consistente|
|Font      |**JetBrains Mono** (code) + **Instrument Sans** o **Satoshi** (testo)|Dev-oriented, non generico     |
|Animazioni|**CSS only** o **Framer Motion** se Next.js                          |Leggere, no bloat              |
|Icone     |**Lucide**                                                           |Coerente, leggero              |
|Deploy    |`vercel deploy`                                                      |Push e finito                  |

**Se HTML statico:** un singolo `index.html` con Tailwind via CDN e tutto inline.
**Se Next.js:** `npx create-next-app`, una sola page, niente routing complesso.

-----

## Design Direction

### Estetica: **Terminal-native minimal**

La landing page deve sembrare un prodotto fatto da chi vive nel terminale. Non un SaaS colorato, non un template generico. Pensa: **stripe.com incontra una man page**.

- **Sfondo scuro** (non nero puro: `#0a0a0f` o `#111118`)
- **Testo chiaro** (`#e4e4e7` per body, `#ffffff` per heading)
- **Accent color unico:** verde terminale (`#4ade80`) o blu elettrico (`#38bdf8`)
- **Code blocks** prominenti con syntax highlighting reale
- **Zero stock photos, zero illustrazioni generiche**
- I visual sono **solo code blocks e output del CLI**
- Whitespace generoso, niente densità da dashboard
- Border sottili (`1px solid rgba(255,255,255,0.06)`) per separare sezioni

### Typography

```css
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
--font-sans: 'Satoshi', 'Inter', system-ui, sans-serif;
```

- Heading: font-sans, bold, tracking tight
- Body: font-sans, regular, line-height rilassata (1.7)
- Code: font-mono, con sfondo leggermente più chiaro del body background
- Dimensioni generose: h1 `3.5rem`, h2 `2rem`, body `1.125rem`

### Effetti

- Code blocks con **typing animation** sull’hero (il comando viene “digitato”)
- Fade-in on scroll per le sezioni
- Hover sugli snippet: leggero glow sull’accent color
- **Niente parallax, niente particelle, niente 3D** — è un tool per professionisti

-----

## Struttura Pagina — 8 Sezioni

### SECTION 1: Hero

**Scopo:** catturare, spiegare, convertire in 5 secondi

**Layout:**

- Sinistra: headline + subheadline + CTA
- Destra (o sotto su mobile): terminal window animato

**Headline:**

```
SEO data from your terminal.
```

**Subheadline:**

```
43 commands to search, analyze, and audit — built for AI agents and humans who prefer the command line.
```

**CTA (due bottoni affiancati):**

```
[⭐ Star on GitHub]  [pip install dfseo]
```

Il bottone “pip install” deve essere stilizzato come un code block cliccabile (copia negli appunti al click).

**Terminal window animato (destra):**

```
$ dfseo serp google "email hosting" --location Italy --output json

{
  "keyword": "email hosting",
  "results_count": 100,
  "organic_results": [
    {
      "rank": 1,
      "domain": "qboxmail.it",
      "title": "Email Hosting Professionale",
      ...
    }
  ],
  "cost": "$0.002"
}
```

L’animazione deve simulare la digitazione del comando e poi il “rendering” del JSON output.

-----

### SECTION 2: The Problem (One-liner)

**Scopo:** creare tensione con un contrasto

**Layout:** centrato, ampio, una frase

```
SEO tools charge $100+/month for data you can get with a single API call.
dfseo-cli cuts the middleman.
```

Sotto, tre card minimali con i numeri:

|Ahrefs|SEMrush|dfseo-cli   |
|------|-------|------------|
|$99/mo|$129/mo|$0.002/query|

Le prime due card: sfondo grigio spento, testo barrato o opaco.
La terza card: sfondo accent, testo bold, bordo glow.

-----

### SECTION 3: Command Showcase (4 blocchi)

**Scopo:** mostrare cosa fa il tool con esempi reali

**Layout:** griglia 2x2 (stack su mobile)

Ogni blocco ha:

- Titolo breve (es. “SERP Analysis”)
- Un comando reale in code block
- Una riga di descrizione

**Blocco 1 — SERP**

```
SERP Analysis

$ dfseo serp google "your keyword" --location "Italy" --depth 100

Google, Bing, YouTube. Any keyword, any location, real-time results.
```

**Blocco 2 — Keywords**

```
Keyword Research

$ dfseo keywords volume "email hosting" "smtp provider" --include-serp-info

Volume, CPC, difficulty, search intent. Up to 700 keywords per request.
```

**Blocco 3 — Site Audit**

```
Site Audit

$ dfseo site audit "domain.com" --max-pages 500 --wait

60+ on-page checks. Broken links. Duplicate content. Lighthouse scores.
```

**Blocco 4 — Backlinks**

```
Backlink Analysis

$ dfseo backlinks gap "you.com" "competitor1.com" "competitor2.com"

Find who links to competitors but not to you. The ultimate link building weapon.
```

-----

### SECTION 4: Built for Agents

**Scopo:** differenziare — questo non è un tool SEO qualsiasi

**Layout:** sinistra testo, destra code block

**Testo:**

```
Built for AI agents.
Usable by humans.

JSON on stdout. Errors on stderr. Semantic exit codes.
Your agent parses the output. You read the table.
Same data, different format.
```

**Code block (destra):**

```bash
# For agents
result=$(dfseo keywords difficulty "seo tool" -q)
echo $result | jq '.results[0].keyword_difficulty'

# For humans
dfseo keywords difficulty "seo tool" --output table

  Keyword   │ KD  │ Level
  ──────────┼─────┼──────────
  seo tool  │  72 │ ████████ Hard
```

-----

### SECTION 5: Full Command Reference

**Scopo:** mostrare la profondità del tool (43 comandi!)

**Layout:** 4 colonne (tab o accordion su mobile), un titolo per gruppo

**SERP (8 commands)**

```
serp google      serp bing
serp youtube     serp compare
serp locations   serp languages
auth setup       auth status
```

**Keywords (8 commands)**

```
keywords volume        keywords suggestions
keywords ideas         keywords difficulty
keywords search-intent keywords for-site
keywords ads-volume    keywords ads-suggestions
```

**Site Audit (11 commands)**

```
site audit       site crawl
site summary     site pages
site links       site duplicates
site redirects   site non-indexable
site resources   site lighthouse
site tasks
```

**Backlinks (14 commands)**

```
backlinks summary      backlinks list
backlinks anchors      backlinks referring-domains
backlinks history      backlinks competitors
backlinks gap          backlinks pages
backlinks bulk ranks   backlinks bulk backlinks
backlinks bulk spam-score
backlinks bulk referring-domains
backlinks bulk new-lost
```

Ogni gruppo ha un badge con il conteggio: `8`, `8`, `11`, `14`.

Sotto la griglia, centrato:

```
41 commands. 4 APIs. One CLI.
```

-----

### SECTION 6: Quick Start

**Scopo:** abbassare la frizione all’installazione

**Layout:** 3 step verticali, numerati, con code blocks

```
1. Install

$ pip install dfseo


2. Authenticate

$ export DATAFORSEO_LOGIN="you@email.com"
$ export DATAFORSEO_PASSWORD="your_api_password"


3. Search

$ dfseo serp google "your first keyword"
```

Sotto lo step 3, nota piccola:

```
Requires a DataForSEO API account. Free trial available at dataforseo.com
```

-----

### SECTION 7: Agent Integration

**Scopo:** mostrare l’uso con AI agent frameworks (il vero differenziatore)

**Layout:** centrato, code block grande

**Titolo:**

```
Drop it into any AI agent.
```

**Sottotitolo:**

```
dfseo-cli ships with a SKILL.md file. Any agent that reads skill files can discover and use all 41 commands automatically.
```

**Code block — esempio SKILL.md:**

```yaml
---
name: dfseo-cli
description: >
  SEO data CLI powered by DataForSEO APIs.
  Triggers on: "SERP", "keyword ranking", "SEO data",
  "backlink analysis", "site audit"
---
```

**Sotto, loghi/nomi di framework compatibili (testo, non immagini):**

```
Works with: Claude Code · OpenClaw · Gemini CLI · Any shell-executing agent
```

-----

### SECTION 8: Footer CTA + Links

**Scopo:** chiusura con seconda CTA e link essenziali

**Layout:** centrato, minimale

**CTA repeat:**

```
Ready to try it?
```

**Due bottoni (stessi dell’hero):**

```
[⭐ Star on GitHub]  [pip install dfseo]
```

**Link footer (una riga, piccoli):**

```
GitHub · PyPI · DataForSEO Docs · MIT License
```

**Riga finale:**

```
Built with Python + Typer. Powered by DataForSEO APIs.
```

-----

## Responsive Design

### Desktop (>1024px)

- Hero: 2 colonne (testo + terminal)
- Command showcase: griglia 2x2
- Command reference: 4 colonne
- Agent section: testo + code side by side

### Tablet (768-1024px)

- Hero: stack verticale
- Command showcase: griglia 2x1
- Command reference: 2 colonne
- Tutto il resto: stack

### Mobile (<768px)

- Tutto stacked
- Command reference: accordion o scroll orizzontale
- Code blocks: scroll orizzontale con `-webkit-overflow-scrolling: touch`
- Font size ridotte: h1 `2rem`, body `1rem`

-----

## Interazioni

### Copy to clipboard

Ogni code block deve avere un bottone “copy” nell’angolo in alto a destra. Al click:

- Copia il contenuto
- Il bottone cambia in “Copied!” per 2 secondi
- Torna allo stato originale

### Terminal animation (hero)

- Typing effect sul comando (40ms per carattere)
- Pausa 500ms dopo il comando
- JSON output appare riga per riga (20ms per riga)
- Loop: pausa 5 secondi, poi ricomincia con un comando diverso

Comandi da ciclare:

1. `dfseo serp google "email hosting" --location Italy`
1. `dfseo keywords difficulty "seo" "sem" "ppc"`
1. `dfseo backlinks summary "competitor.com"`

### Smooth scroll

Click sui link interni → smooth scroll alla sezione corrispondente.

### Star count (opzionale)

Se vuoi il conteggio live degli star GitHub, usa l’API:

```
https://api.github.com/repos/USERNAME/dfseo-cli
```

Mostra il badge `⭐ 42` aggiornato. Se non vuoi, metti solo `⭐ Star on GitHub`.

-----

## SEO della pagina stessa

```html
<title>dfseo-cli — SEO Data from Your Terminal</title>
<meta name="description" content="Open source CLI for DataForSEO APIs. 43 commands for SERP analysis, keyword research, site audits, and backlink analysis. Built for AI agents.">
<meta name="keywords" content="seo cli, dataforseo, serp api, keyword research tool, site audit cli, backlink analysis, ai agent tools">

<!-- Open Graph -->
<meta property="og:title" content="dfseo-cli — SEO Data from Your Terminal">
<meta property="og:description" content="43 commands for SERP, Keywords, Site Audit, and Backlinks. Built for AI agents and humans who prefer the command line.">
<meta property="og:image" content="[URL_TO_OG_IMAGE]">
<meta property="og:type" content="website">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="dfseo-cli — SEO Data from Your Terminal">
<meta name="twitter:description" content="Open source CLI wrapping DataForSEO APIs. pip install dfseo">
```

Per l’OG image: crea un’immagine 1200x630 con sfondo scuro, il comando `dfseo serp google "keyword"` e il JSON output. Stile coerente con la landing page.

-----

## File Structure per Vercel

### Se Next.js:

```
dfseo-landing/
├── app/
│   ├── layout.tsx
│   ├── page.tsx          # La landing page
│   └── globals.css
├── components/
│   ├── Hero.tsx
│   ├── Problem.tsx
│   ├── CommandShowcase.tsx
│   ├── BuiltForAgents.tsx
│   ├── CommandReference.tsx
│   ├── QuickStart.tsx
│   ├── AgentIntegration.tsx
│   ├── Footer.tsx
│   ├── TerminalAnimation.tsx
│   └── CopyButton.tsx
├── public/
│   └── og-image.png
├── tailwind.config.ts
├── next.config.ts
├── package.json
└── vercel.json          # Opzionale, Vercel auto-detect Next.js
```

### Se HTML statico:

```
dfseo-landing/
├── index.html           # Tutto in un file
├── og-image.png
└── vercel.json
```

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

-----

## Istruzioni per Claude Code

### Cosa fare

1. **Scegli Next.js** se sei comodo con React, altrimenti HTML statico va benissimo
1. **Implementa il terminal animation** sull’hero — è l’elemento che cattura
1. **Implementa copy-to-clipboard** su ogni code block — è il micro-interaction più utile
1. **Usa Tailwind** con dark theme come default (no toggle light/dark)
1. **Testa su mobile** — i code block devono scrollare orizzontalmente senza rompere il layout
1. **Genera l’OG image** — può essere un semplice HTML-to-image con lo stile della pagina
1. **Fai il deploy su Vercel** — `vercel deploy` dalla cartella del progetto

### Cosa NON fare

- **Niente template generici** — non usare template hero con gradient viola, non usare Inter, non usare layout preconfezionati
- **Niente immagini** — i visual sono SOLO code blocks e output CLI
- **Niente toggle dark/light** — è dark only, punto
- **Niente animazioni pesanti** — no parallax, no particelle, no Three.js
- **Niente sezione pricing** — il tool è gratis, il pricing è di DataForSEO
- **Niente form email** — la CTA è solo GitHub star e pip install
- **Niente cookie banner** — nessun tracking, nessun analytics (per ora)

-----

## Riferimenti Design

Pagine con estetica simile a quello che vogliamo:

- https://linear.app — minimal, dark, code-oriented
- https://warp.dev — terminal tool landing page
- https://fig.io — CLI tool, developer audience
- https://charm.sh — Go CLI tools, terminale estetica
