# dfseo-cli v1.3 — Backlinks API

> Spec document v1.3 — Brief per Claude Code
> Autore: Ricc | Data: Marzo 2026
> Prerequisito: v1.0 (SERP), v1.1 (Keywords), v1.2 (On-Page) implementate

-----

## Overview

La v1.3 aggiunge il comando `dfseo backlinks` per l’analisi completa dei profili backlink: summary, lista backlink, anchor text, referring domains, competitor analysis, e link gap (domain/page intersection).

**Buona notizia architetturale:** a differenza della On-Page API (v1.2), la Backlinks API è **tutta Live** — ogni endpoint restituisce risultati immediati senza polling. Stessa semplicità della v1.0 e v1.1.

**Nota pricing:** la Backlinks API ha un commitment minimo di $100/mese (utilizzabile su qualsiasi API DataForSEO). Il CLI dovrebbe menzionarlo nel `--help` di `dfseo backlinks`.

-----

## Modifiche all’architettura

### Nuovo file

```
src/dfseo/commands/backlinks.py   # Tutti i comandi backlinks
```

### Aggiornamento cli.py

```python
from dfseo.commands import backlinks
app.add_typer(backlinks.app, name="backlinks")
```

-----

## Concetti chiave dell’API

### Target modes

Il target può essere un dominio, sottodominio, o URL specifica. L’API si comporta diversamente:

- `"qboxmail.it"` → dati per il dominio root
- `"blog.qboxmail.it"` → dati per il sottodominio
- `"https://qboxmail.it/page"` → dati per quella specifica pagina

Il flag `--include-subdomains` (default `true`) controlla se includere i sottodomini quando il target è un dominio.

### Rank scoring

DataForSEO usa un sistema di scoring proprietario ispirato a PageRank:

- **Rank** (0-1000) — rank del backlink
- **Page Rank** (0-1000) — rank della pagina sorgente
- **Domain Rank** (0-1000) — rank del dominio sorgente

### Backlink status

- `all` — tutti i backlink (default)
- `live` — solo backlink attualmente attivi
- `new` — backlink scoperti di recente
- `lost` — backlink persi di recente
- `broken` — backlink rotti (target restituisce 4xx/5xx)

-----

## Comandi

### `dfseo backlinks summary`

Panoramica completa del profilo backlink di un target.

```bash
# Summary dominio
dfseo backlinks summary "qboxmail.it"

# Con sottodomini
dfseo backlinks summary "qboxmail.it" --include-subdomains

# Summary pagina specifica
dfseo backlinks summary "https://qboxmail.it/email-hosting"

# Solo dofollow
dfseo backlinks summary "qboxmail.it" --dofollow-only
```

**Parametri:**

|Flag                  |Default|Descrizione                  |
|----------------------|-------|-----------------------------|
|`--include-subdomains`|`true` |Include sottodomini          |
|`--dofollow-only`     |`false`|Filtra solo backlink dofollow|
|`--status`            |`all`  |`all`, `live`, `new`, `lost` |
|`--output` / `-o`     |`json` |`json`, `table`              |

**Endpoint:** `POST /v3/backlinks/summary/live`

**Request body:**

```json
[{
  "target": "qboxmail.it",
  "include_subdomains": true,
  "backlinks_status_type": "all",
  "backlinks_filters": ["dofollow", "=", true]
}]
```

**Output JSON:**

```json
{
  "target": "qboxmail.it",
  "rank": 245,
  "backlinks": 1420,
  "referring_domains": 312,
  "referring_main_domains": 280,
  "referring_ips": 265,
  "referring_subnets": 198,
  "spam_score": 5,
  "broken_backlinks": 12,
  "broken_pages": 8,
  "first_seen": "2019-03-15T10:30:00Z",
  "info": {
    "server": "cloudflare",
    "cms": null,
    "ip_address": "104.26.6.202",
    "country": "IT"
  },
  "links_summary": {
    "dofollow": 980,
    "nofollow": 440,
    "anchor": 1050,
    "image": 180,
    "redirect": 45,
    "canonical": 12
  },
  "top_pages": [
    {"url": "https://qboxmail.it/", "backlinks": 450},
    {"url": "https://qboxmail.it/email-hosting", "backlinks": 120}
  ],
  "top_anchors": [
    {"anchor": "qboxmail", "backlinks": 230},
    {"anchor": "email hosting", "backlinks": 85}
  ],
  "cost": 0.02003,
  "timestamp": "2026-03-06T15:00:00Z"
}
```

**Output table:**

```
$ dfseo backlinks summary "qboxmail.it" -o table

  Target: qboxmail.it | Domain Rank: 245/1000

  Backlinks ........... 1,420 (980 dofollow / 440 nofollow)
  Referring domains ... 312 (280 main domains)
  Referring IPs ....... 265 (198 subnets)
  Broken backlinks .... 12
  Spam score .......... 5/100

  Top pages by backlinks:
    qboxmail.it/ ......................... 450
    qboxmail.it/email-hosting ............ 120

  Top anchors:
    "qboxmail" ........................... 230
    "email hosting" ...................... 85

  Cost: $0.020
```

-----

### `dfseo backlinks list`

Lista dettagliata dei backlink verso il target.

```bash
# Tutti i backlink
dfseo backlinks list "qboxmail.it"

# Solo dofollow, ordinati per rank
dfseo backlinks list "qboxmail.it" --dofollow-only --sort rank --limit 50

# Solo nuovi backlink
dfseo backlinks list "qboxmail.it" --status new

# Solo backlink persi
dfseo backlinks list "qboxmail.it" --status lost

# Solo backlink rotti
dfseo backlinks list "qboxmail.it" --status broken

# Filtra per dominio sorgente
dfseo backlinks list "qboxmail.it" --from-domain "example.com"
```

**Parametri:**

|Flag                  |Default|Descrizione                                                            |
|----------------------|-------|-----------------------------------------------------------------------|
|`--include-subdomains`|`true` |Include sottodomini                                                    |
|`--dofollow-only`     |`false`|Solo dofollow                                                          |
|`--status`            |`all`  |`all`, `live`, `new`, `lost`                                           |
|`--sort`              |`rank` |`rank`, `page_from_rank`, `domain_from_rank`, `first_seen`, `last_seen`|
|`--order`             |`desc` |`asc`, `desc`                                                          |
|`--from-domain`       |-      |Filtra per dominio sorgente                                            |
|`--min-rank`          |-      |Rank minimo del backlink                                               |
|`--limit` / `-n`      |`100`  |Max risultati (max 1000)                                               |
|`--offset`            |`0`    |Offset per paginazione                                                 |
|`--output` / `-o`     |`json` |`json`, `table`, `csv`                                                 |

**Endpoint:** `POST /v3/backlinks/backlinks/live`

**Request body:**

```json
[{
  "target": "qboxmail.it",
  "mode": "as_is",
  "include_subdomains": true,
  "backlinks_status_type": "live",
  "filters": [
    ["dofollow", "=", true],
    "and",
    ["rank", ">=", 100]
  ],
  "order_by": ["rank,desc"],
  "limit": 50
}]
```

**Output JSON (per backlink):**

```json
{
  "domain_from": "techblog.it",
  "url_from": "https://techblog.it/migliori-email-hosting",
  "domain_to": "qboxmail.it",
  "url_to": "https://qboxmail.it/email-hosting",
  "rank": 185,
  "page_from_rank": 120,
  "domain_from_rank": 310,
  "anchor": "Qboxmail email hosting",
  "text_pre": "Tra i migliori provider italiani c'è ",
  "text_post": " che offre servizi professionali",
  "dofollow": true,
  "item_type": "anchor",
  "is_new": false,
  "is_lost": false,
  "is_broken": false,
  "first_seen": "2024-06-15T08:30:00Z",
  "last_seen": "2026-03-01T12:00:00Z",
  "spam_score": 2,
  "page_from_external_links": 15,
  "page_from_internal_links": 42
}
```

-----

### `dfseo backlinks anchors`

Analisi degli anchor text usati nei backlink verso il target.

```bash
# Tutti gli anchor
dfseo backlinks anchors "qboxmail.it"

# Filtra per testo
dfseo backlinks anchors "qboxmail.it" --search "email"

# Ordina per numero di backlink
dfseo backlinks anchors "qboxmail.it" --sort backlinks --limit 20

# Solo dofollow
dfseo backlinks anchors "qboxmail.it" --dofollow-only
```

**Parametri:**

|Flag                  |Default    |Descrizione                                           |
|----------------------|-----------|------------------------------------------------------|
|`--include-subdomains`|`true`     |Include sottodomini                                   |
|`--dofollow-only`     |`false`    |Solo backlink dofollow                                |
|`--search`            |-          |Cerca testo nell’anchor (usa filtro `like`)           |
|`--sort`              |`backlinks`|`backlinks`, `referring_domains`, `rank`, `first_seen`|
|`--order`             |`desc`     |`asc`, `desc`                                         |
|`--limit` / `-n`      |`100`      |Max risultati                                         |
|`--output` / `-o`     |`json`     |`json`, `table`, `csv`                                |

**Endpoint:** `POST /v3/backlinks/anchors/live`

**Request body:**

```json
[{
  "target": "qboxmail.it",
  "include_subdomains": true,
  "backlinks_filters": ["dofollow", "=", true],
  "filters": ["anchor", "like", "%email%"],
  "order_by": ["backlinks,desc"],
  "limit": 20
}]
```

**Output table:**

```
$ dfseo backlinks anchors "qboxmail.it" --sort backlinks -n 10 -o table

  Target: qboxmail.it | Total anchors: 1,245

  Anchor                    │ Backlinks │ Ref. Domains │ Rank
  ──────────────────────────┼───────────┼──────────────┼─────
  qboxmail                  │       230 │           85 │  185
  email hosting             │        85 │           42 │  165
  qboxmail.it               │        72 │           38 │  150
  hosting email professionale│       45 │           22 │  140
  Qboxmail email hosting    │        38 │           18 │  130
```

-----

### `dfseo backlinks referring-domains`

Lista dei domini che puntano al target.

```bash
# Tutti i referring domains
dfseo backlinks referring-domains "qboxmail.it"

# Solo domini con molti backlink
dfseo backlinks referring-domains "qboxmail.it" --min-backlinks 10 --sort rank

# Escludi backlink interni
dfseo backlinks referring-domains "qboxmail.it" --exclude-internal
```

**Parametri:**

|Flag                  |Default|Descrizione                      |
|----------------------|-------|---------------------------------|
|`--include-subdomains`|`true` |Include sottodomini              |
|`--exclude-internal`  |`false`|Escludi backlink interni         |
|`--dofollow-only`     |`false`|Solo backlink dofollow           |
|`--min-backlinks`     |-      |Minimo backlink dal dominio      |
|`--sort`              |`rank` |`rank`, `backlinks`, `first_seen`|
|`--order`             |`desc` |`asc`, `desc`                    |
|`--limit` / `-n`      |`100`  |Max risultati                    |
|`--output` / `-o`     |`json` |`json`, `table`, `csv`           |

**Endpoint:** `POST /v3/backlinks/referring_domains/live`

-----

### `dfseo backlinks history`

Storico del profilo backlink (dati dal 2019 in poi).

```bash
# Storico completo
dfseo backlinks history "qboxmail.it"

# Range specifico
dfseo backlinks history "qboxmail.it" --from 2025-01 --to 2026-03
```

**Parametri:**

|Flag             |Default|Descrizione           |
|-----------------|-------|----------------------|
|`--from`         |-      |Data inizio (YYYY-MM) |
|`--to`           |-      |Data fine (YYYY-MM)   |
|`--output` / `-o`|`json` |`json`, `table`, `csv`|

**Endpoint:** `POST /v3/backlinks/history/live`

**Nota:** l’endpoint History accetta solo domini come target (non sottodomini o URL).

**Output JSON:**

```json
{
  "target": "qboxmail.it",
  "history": [
    {
      "date": "2026-03-01",
      "backlinks": 1420,
      "referring_domains": 312,
      "referring_main_domains": 280,
      "rank": 245
    },
    {
      "date": "2026-02-01",
      "backlinks": 1380,
      "referring_domains": 305,
      "referring_main_domains": 274,
      "rank": 240
    }
  ],
  "cost": 0.02003,
  "timestamp": "2026-03-06T15:00:00Z"
}
```

-----

### `dfseo backlinks competitors`

Trova i competitor che condividono parte del profilo backlink con il target.

```bash
# Competitor del dominio
dfseo backlinks competitors "qboxmail.it"

# Top 20 per rank
dfseo backlinks competitors "qboxmail.it" --sort rank --limit 20
```

**Parametri:**

|Flag                  |Default|Descrizione                             |
|----------------------|-------|----------------------------------------|
|`--include-subdomains`|`true` |Include sottodomini                     |
|`--sort`              |`rank` |`rank`, `backlinks`, `referring_domains`|
|`--order`             |`desc` |`asc`, `desc`                           |
|`--limit` / `-n`      |`50`   |Max risultati                           |
|`--output` / `-o`     |`json` |`json`, `table`, `csv`                  |

**Endpoint:** `POST /v3/backlinks/competitors/live`

-----

### `dfseo backlinks gap`

**Comando più potente:** Link Gap analysis. Trova domini/pagine che linkano ai competitor ma non al tuo sito. Essenziale per la strategia di link building.

```bash
# Domain intersection: chi linka competitor1 e competitor2 ma non me
dfseo backlinks gap "qboxmail.it" "competitor1.it" "competitor2.it"

# Page intersection
dfseo backlinks gap "qboxmail.it" "competitor.it" --mode page

# Escludi un dominio dai risultati
dfseo backlinks gap "qboxmail.it" "competitor.it" --exclude "spam-domain.com"

# Solo domini con rank > 200
dfseo backlinks gap "qboxmail.it" "competitor.it" --min-rank 200
```

**Comportamento:**

- Il primo target è il “tuo” sito
- I successivi (fino a 20) sono i competitor
- L’output mostra i domini/pagine che linkano i competitor ma **non** il primo target

**Parametri:**

|Flag             |Default |Descrizione                                                |
|-----------------|--------|-----------------------------------------------------------|
|`--mode`         |`domain`|`domain` (Domain Intersection) o `page` (Page Intersection)|
|`--exclude`      |-       |Domini da escludere dai risultati (ripetibile)             |
|`--dofollow-only`|`false` |Solo backlink dofollow                                     |
|`--min-rank`     |-       |Rank minimo del dominio sorgente                           |
|`--sort`         |`rank`  |`rank`, `backlinks`                                        |
|`--order`        |`desc`  |`asc`, `desc`                                              |
|`--limit` / `-n` |`100`   |Max risultati                                              |
|`--output` / `-o`|`json`  |`json`, `table`, `csv`                                     |

**Endpoint (domain mode):** `POST /v3/backlinks/domain_intersection/live`

**Request body:**

```json
[{
  "targets": {
    "1": "competitor1.it",
    "2": "competitor2.it"
  },
  "exclude_targets": ["qboxmail.it"],
  "filters": [
    ["1.dofollow", "=", true],
    "and",
    ["1.domain_from_rank", ">", 200]
  ],
  "order_by": ["1.rank,desc"],
  "limit": 100
}]
```

**Endpoint (page mode):** `POST /v3/backlinks/page_intersection/live`

**Nota sulla struttura targets:** l’API usa un dizionario numerato `{"1": "target1", "2": "target2"}`. I filtri e l’ordinamento usano il numero come prefisso: `"1.rank"`, `"2.domain_from_rank"`.

**Output table:**

```
$ dfseo backlinks gap "qboxmail.it" "competitor1.it" "competitor2.it" -o table

  Your site: qboxmail.it | Competitors: competitor1.it, competitor2.it
  Showing: domains that link to competitors but NOT to you

  Domain                    │ Rank │ Links to C1 │ Links to C2
  ──────────────────────────┼──────┼─────────────┼────────────
  techreview.it             │  520 │           3 │           2
  hostingblog.com           │  410 │           5 │           1
  emailgeeks.net            │  380 │           2 │           4
  ...

  Total link gap opportunities: 156
  Cost: $0.020
```

-----

### `dfseo backlinks bulk`

Comandi bulk per confronto rapido tra molti target (fino a 1000).

```bash
# Rank bulk (domain rank + page rank per fino a 1000 target)
dfseo backlinks bulk ranks "qboxmail.it" "competitor1.it" "competitor2.it"

# Da file
dfseo backlinks bulk ranks --from-file domains.txt

# Backlinks count bulk
dfseo backlinks bulk backlinks --from-file domains.txt

# Spam score bulk
dfseo backlinks bulk spam-score --from-file domains.txt

# Referring domains bulk
dfseo backlinks bulk referring-domains --from-file domains.txt

# New & Lost referring domains
dfseo backlinks bulk new-lost --from-file domains.txt --from-date 2025-09-01
```

**Sub-comandi bulk:**

|Sub-comando        |Endpoint API                                     |Descrizione                |
|-------------------|-------------------------------------------------|---------------------------|
|`ranks`            |`POST /v3/backlinks/bulk_ranks/live`             |Domain Rank e Page Rank    |
|`backlinks`        |`POST /v3/backlinks/bulk_backlinks/live`         |Conteggio backlink         |
|`spam-score`       |`POST /v3/backlinks/bulk_spam_score/live`        |Spam score                 |
|`referring-domains`|`POST /v3/backlinks/bulk_referring_domains/live` |Conteggio referring domains|
|`new-lost`         |`POST /v3/backlinks/bulk_new_lost_backlinks/live`|Nuovi e persi              |

**Parametri comuni:**

|Flag                |Default|Descrizione                             |
|--------------------|-------|----------------------------------------|
|`--from-file` / `-f`|-      |File con target (uno per riga, max 1000)|
|`--from-date`       |-      |Per `new-lost`: data inizio (YYYY-MM-DD)|
|`--output` / `-o`   |`json` |`json`, `table`, `csv`                  |

**Output table (ranks):**

```
$ dfseo backlinks bulk ranks "qboxmail.it" "competitor1.it" "competitor2.it" -o table

  Target            │ Domain Rank │ Page Rank │ Backlinks
  ──────────────────┼─────────────┼───────────┼──────────
  competitor1.it    │         520 │       380 │    8,450
  competitor2.it    │         410 │       290 │    5,230
  qboxmail.it       │         245 │       180 │    1,420
```

-----

### `dfseo backlinks pages`

Lista le pagine del target con più backlink.

```bash
# Top pages per backlink
dfseo backlinks pages "qboxmail.it" --sort backlinks --limit 20
```

**Parametri:**

|Flag                  |Default    |Descrizione                             |
|----------------------|-----------|----------------------------------------|
|`--include-subdomains`|`true`     |Include sottodomini                     |
|`--sort`              |`backlinks`|`backlinks`, `rank`, `referring_domains`|
|`--order`             |`desc`     |`asc`, `desc`                           |
|`--limit` / `-n`      |`50`       |Max risultati                           |
|`--output` / `-o`     |`json`     |`json`, `table`, `csv`                  |

**Endpoint:** `POST /v3/backlinks/domain_pages/live`

-----

## Endpoint Mappings v1.3

|Comando CLI                             |Endpoint API                                     |
|----------------------------------------|-------------------------------------------------|
|`dfseo backlinks summary`               |`POST /v3/backlinks/summary/live`                |
|`dfseo backlinks list`                  |`POST /v3/backlinks/backlinks/live`              |
|`dfseo backlinks anchors`               |`POST /v3/backlinks/anchors/live`                |
|`dfseo backlinks referring-domains`     |`POST /v3/backlinks/referring_domains/live`      |
|`dfseo backlinks history`               |`POST /v3/backlinks/history/live`                |
|`dfseo backlinks competitors`           |`POST /v3/backlinks/competitors/live`            |
|`dfseo backlinks gap` (domain)          |`POST /v3/backlinks/domain_intersection/live`    |
|`dfseo backlinks gap` (page)            |`POST /v3/backlinks/page_intersection/live`      |
|`dfseo backlinks bulk ranks`            |`POST /v3/backlinks/bulk_ranks/live`             |
|`dfseo backlinks bulk backlinks`        |`POST /v3/backlinks/bulk_backlinks/live`         |
|`dfseo backlinks bulk spam-score`       |`POST /v3/backlinks/bulk_spam_score/live`        |
|`dfseo backlinks bulk referring-domains`|`POST /v3/backlinks/bulk_referring_domains/live` |
|`dfseo backlinks bulk new-lost`         |`POST /v3/backlinks/bulk_new_lost_backlinks/live`|
|`dfseo backlinks pages`                 |`POST /v3/backlinks/domain_pages/live`           |

-----

## Filtri Backlinks API

L’API ha **due livelli di filtri** che è importante non confondere:

### `filters` — filtra i risultati principali

Usato negli endpoint `backlinks`, `domain_intersection`, `page_intersection`:

```json
"filters": [
  ["dofollow", "=", true],
  "and",
  ["rank", ">=", 100]
]
```

### `backlinks_filters` — filtra i backlink usati per il calcolo

Usato in `summary`, `anchors`, `domain_pages`, `referring_domains`, `referring_networks`:

```json
"backlinks_filters": [
  ["dofollow", "=", true]
]
```

**Il CLI deve mappare il flag `--dofollow-only` sul filtro corretto in base all’endpoint chiamato.**

**Operatori:** `=`, `<>`, `>`, `<`, `>=`, `<=`, `like`, `not_like`, `regex`, `not_regex`, `in`, `not_in`

-----

## Istruzioni per Claude Code — v1.3

### Cosa fare

1. **Crea `src/dfseo/commands/backlinks.py`** — nuovo Typer sub-app
1. **Implementa `backlinks summary`** — endpoint più semplice, ottimo per testare il flusso
1. **Implementa `backlinks list`** — core command, con gestione completa dei filtri
1. **Implementa `backlinks anchors`** — attenzione a usare `backlinks_filters` (non `filters`)
1. **Implementa `backlinks referring-domains`** — simile ad anchors
1. **Implementa `backlinks history`** — solo domini come target, niente filtri
1. **Implementa `backlinks competitors`** — semplice POST
1. **Implementa `backlinks gap`** — il più complesso: gestisce la struttura `targets` numerata, deve switchare endpoint in base a `--mode`, e costruire filtri con prefisso numerico (`"1.rank"`)
1. **Implementa `backlinks bulk`** come sub-command group con 5 sotto-comandi, riusa `load_keywords()` da v1.1 rinominato in `load_targets()`
1. **Implementa `backlinks pages`**
1. **Aggiorna SKILL.md**

### Dettagli implementativi

- **Tutti gli endpoint sono Live** — niente polling, stessa semplicità di v1.0/v1.1
- **Due tipi di filtri** — `filters` vs `backlinks_filters`. Il CLI deve sapere quale usare per ogni endpoint. Crea un mapping statico nel comando
- **`backlinks gap` ha la struttura targets più complessa** — dizionario numerato `{"1": "target1", "2": "target2"}` con prefissi numerici nei filtri. Il primo argomento posizionale è “il tuo sito” (va in `exclude_targets`), gli altri sono i competitor (vanno in `targets`)
- **I comandi bulk accettano target come argomenti posizionali O da file** — riusa il pattern `--from-file` della v1.1
- **`backlinks history` accetta solo domini** — validare l’input e restituire errore chiaro se l’utente passa un URL

### Cosa NON fare

- Non confondere `filters` con `backlinks_filters` — genera risultati completamente diversi
- Non passare URL a `backlinks history` — accetta solo domini root
- Non dimenticare `"mode": "as_is"` nel corpo di `backlinks list` — è richiesto dall’API
- Non hardcodare il numero di target in `backlinks gap` — l’API accetta fino a 20 target
- Non creare endpoint separati per new/lost/broken — usare il flag `--status` su `backlinks list`

-----

## Aggiornamento SKILL.md

Aggiungere alla skill esistente:

```markdown
### Backlink Profile Summary
\`\`\`bash
dfseo backlinks summary "domain.com"
\`\`\`

### List Backlinks (with filters)
\`\`\`bash
dfseo backlinks list "domain.com" --dofollow-only --sort rank --limit 50
# New/Lost/Broken:
dfseo backlinks list "domain.com" --status new
dfseo backlinks list "domain.com" --status lost
\`\`\`

### Anchor Text Analysis
\`\`\`bash
dfseo backlinks anchors "domain.com" --search "brand name" --sort backlinks
\`\`\`

### Referring Domains
\`\`\`bash
dfseo backlinks referring-domains "domain.com" --min-backlinks 5 --sort rank
\`\`\`

### Link Gap Analysis (find competitor-only backlinks)
\`\`\`bash
dfseo backlinks gap "your-site.com" "competitor1.com" "competitor2.com"
\`\`\`

### Bulk Rank Comparison (up to 1000 targets)
\`\`\`bash
dfseo backlinks bulk ranks "site1.com" "site2.com" "site3.com"
# Or from file:
dfseo backlinks bulk ranks --from-file domains.txt
\`\`\`

### Backlink History (since 2019)
\`\`\`bash
dfseo backlinks history "domain.com" --from 2024-01 --to 2026-03
\`\`\`
```

-----

## Riferimenti v1.3

- Backlinks API Overview: https://docs.dataforseo.com/v3/backlinks-overview/
- Summary endpoint: https://docs.dataforseo.com/v3/backlinks-summary-live/
- Backlinks endpoint: https://docs.dataforseo.com/v3/backlinks-backlinks-live/
- Anchors endpoint: https://docs.dataforseo.com/v3/backlinks-anchors-live/
- Referring Domains: https://docs.dataforseo.com/v3/backlinks-referring_domains-live/
- Domain Intersection: https://docs.dataforseo.com/v3/backlinks-domain_intersection-live/
- Page Intersection: https://docs.dataforseo.com/v3/backlinks-page_intersection-live/
- Bulk endpoints blog: https://dataforseo.com/blog/bulk-backlinks-api
- Backlinks API Pricing: https://dataforseo.com/pricing/backlinks/backlinks
- Build a Backlinks App guide: https://dataforseo.com/solutions/api-driven-backlinksapp
