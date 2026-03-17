# dfseo-cli v1.2 — On-Page API (Site Audit)

> Spec document v1.2 — Brief per Claude Code
> Autore: Ricc | Data: Marzo 2026
> Prerequisito: v1.0 (SERP) e v1.1 (Keywords) implementate

-----

## Overview

La v1.2 aggiunge il comando `dfseo site` che permette di eseguire audit SEO tecnici su qualsiasi sito web, analizzando 60+ parametri on-page: meta tags, link interni/esterni, contenuti duplicati, redirect chain, status code, performance e molto altro.

**Differenza architetturale fondamentale:** a differenza di SERP e Keywords (che usano solo il metodo Live), la On-Page API è prevalentemente **asincrona**. Il flusso standard è:

1. **Task POST** → invia il sito per il crawling, ricevi un `task_id`
1. **Poll** → controlla `crawl_progress` tramite Summary
1. **GET risultati** → una volta completato il crawl, recupera summary, pages, errors, ecc.

L’unica eccezione è **Instant Pages**, che è Live (risultato immediato per singole URL).

Il CLI deve gestire entrambi i flussi in modo trasparente per l’utente/agente.

-----

## Nota importante: costi

La On-Page API ha un modello di pricing diverso: si paga **per pagina crawlata**, con costi aggiuntivi per parametri opzionali come `enable_javascript`, `load_resources`, `enable_browser_rendering`. Il CLI deve mostrare chiaramente il costo stimato prima di lanciare un crawl di molte pagine.

-----

## Modifiche all’architettura

### Nuovo file

```
src/dfseo/commands/site.py     # Tutti i comandi site audit
```

### Aggiornamento cli.py

```python
from dfseo.commands import site
app.add_typer(site.app, name="site")
```

### Nuovo modulo: task polling

Il flusso asincrono richiede un nuovo modulo condiviso per il task polling:

```
src/dfseo/polling.py           # Task polling logic (riusabile per future API async)
```

```python
async def poll_task(client, task_id: str, interval: int = 5, timeout: int = 300) -> dict:
    """
    Polling asincrono su un task DataForSEO.
    
    Controlla crawl_progress tramite /v3/on_page/summary/{task_id}.
    Ritorna il summary quando crawl_progress == "finished".
    Timeout dopo `timeout` secondi.
    
    In modalità JSON, stampa progress su stderr:
        {"status": "crawling", "pages_crawled": 45, "pages_in_queue": 120}
    """
```

-----

## Comandi

### Flusso principale: Crawl → Analisi

Il pattern tipico per un agente è:

```bash
# 1. Lancia il crawl
task_id=$(dfseo site crawl "qboxmail.it" --max-pages 100 -q)

# 2. Attendi completamento e ottieni summary
dfseo site summary $task_id

# 3. Drill down su problemi specifici
dfseo site pages $task_id --errors-only
dfseo site links $task_id --type broken
dfseo site duplicates $task_id --type title
```

Oppure, il comando **all-in-one** che aspetta il completamento:

```bash
# Crawl + attendi + summary (blocca fino a completamento)
dfseo site audit "qboxmail.it" --max-pages 100 --wait
```

-----

### `dfseo site audit`

Comando all-in-one: lancia il crawl, attende il completamento, restituisce il summary completo. Pensato per l’uso da parte di agenti che vogliono un singolo comando.

```bash
# Audit base
dfseo site audit "qboxmail.it"

# Con parametri
dfseo site audit "qboxmail.it" \
  --max-pages 500 \
  --enable-javascript \
  --load-resources \
  --wait \
  --timeout 600

# Solo una singola pagina (usa Instant Pages internamente, niente polling)
dfseo site audit "https://qboxmail.it/email-hosting" --max-pages 1
```

**Comportamento:**

- Se `--max-pages 1` e target è un URL completo → usa endpoint **Instant Pages** (Live, risultato immediato)
- Altrimenti → usa **Task POST** + polling + **Summary**
- Con `--wait` (default per `audit`) → blocca fino a completamento
- Senza `--wait` → restituisce il `task_id` e basta

**Parametri:**

|Flag                          |Default|Descrizione                                  |
|------------------------------|-------|---------------------------------------------|
|`--max-pages` / `-n`          |`100`  |Numero massimo pagine da crawlare            |
|`--enable-javascript` / `--js`|`false`|Esegue JS sulle pagine (costo extra)         |
|`--load-resources`            |`false`|Carica immagini, CSS, JS (costo extra)       |
|`--enable-browser-rendering`  |`false`|Rendering completo browser (CWV, costo extra)|
|`--wait` / `-w`               |`true` |Attende il completamento del crawl           |
|`--timeout`                   |`300`  |Timeout in secondi per il polling            |
|`--poll-interval`             |`10`   |Secondi tra i check di avanzamento           |
|`--start-url`                 |-      |URL di partenza specifica (default: homepage)|
|`--respect-sitemap`           |`true` |Segue il sitemap.xml                         |
|`--output` / `-o`             |`json` |`json`, `table`, `csv`                       |

**Endpoint API (crawl completo):**

```
POST https://api.dataforseo.com/v3/on_page/task_post
```

**Request body:**

```json
[{
  "target": "qboxmail.it",
  "max_crawl_pages": 100,
  "load_resources": false,
  "enable_javascript": false,
  "enable_browser_rendering": false,
  "respect_sitemap": true
}]
```

**Endpoint API (singola pagina):**

```
POST https://api.dataforseo.com/v3/on_page/instant_pages
```

**Request body (Instant Pages):**

```json
[{
  "url": "https://qboxmail.it/email-hosting",
  "enable_javascript": true
}]
```

**Output JSON (summary):**

```json
{
  "target": "qboxmail.it",
  "task_id": "07281559-0695-0216-0000-c269be8b7592",
  "crawl_progress": "finished",
  "crawl_status": {
    "max_crawl_pages": 100,
    "pages_crawled": 87
  },
  "domain_info": {
    "name": "qboxmail.it",
    "ip": "104.26.6.202",
    "server": "cloudflare",
    "cms": null,
    "crawl_start": "2026-03-06T14:30:00Z",
    "crawl_end": "2026-03-06T14:32:15Z"
  },
  "onpage_score": 78.5,
  "pages_summary": {
    "total": 87,
    "with_errors": 12,
    "with_warnings": 23,
    "with_notices": 45
  },
  "errors": {
    "critical": {
      "broken_links": 3,
      "duplicate_title": 5,
      "no_title": 1,
      "redirect_loop": 0,
      "is_http": 2
    },
    "warnings": {
      "title_too_long": 8,
      "no_description": 4,
      "low_content": 6,
      "missing_alt_tags": 15
    }
  },
  "links_summary": {
    "internal": 342,
    "external": 56,
    "broken": 3
  },
  "cost": 0.087,
  "timestamp": "2026-03-06T14:32:15Z"
}
```

**Output table:**

```
$ dfseo site audit "qboxmail.it" -n 100 -o table

  Target: qboxmail.it | Pages crawled: 87/100 | OnPage Score: 78.5/100

  ✗ CRITICAL ERRORS (3 types)
    Broken links .............. 3
    Duplicate titles .......... 5
    Missing HTTPS ............. 2

  ⚠ WARNINGS (4 types)
    Title too long ............ 8
    No meta description ....... 4
    Low content pages ......... 6
    Missing alt tags .......... 15

  Links: 342 internal | 56 external | 3 broken

  Cost: $0.087
```

-----

### `dfseo site crawl`

Lancia solo il crawl senza attendere. Restituisce il `task_id`. Utile quando l’agente vuole lanciare crawl multipli in parallelo.

```bash
# Lancia crawl, ottieni task_id
dfseo site crawl "qboxmail.it" --max-pages 500

# Output: {"task_id": "07281559-0695-0216-0000-c269be8b7592", "target": "qboxmail.it"}

# Lancia multipli
for site in qboxmail.it example.com test.it; do
  dfseo site crawl "$site" --max-pages 100 -q
done
```

**Parametri:** stessi di `audit` tranne `--wait` e `--timeout` (non applicabili).

**Endpoint:** `POST /v3/on_page/task_post`

-----

### `dfseo site summary`

Ottiene il summary di un crawl (completato o in corso).

```bash
# Con task_id
dfseo site summary "07281559-0695-0216-0000-c269be8b7592"

# Attendi completamento
dfseo site summary "07281559-0695-0216-0000-c269be8b7592" --wait --timeout 600
```

**Parametri:**

|Flag             |Default|Descrizione                                |
|-----------------|-------|-------------------------------------------|
|`--wait` / `-w`  |`false`|Attende il completamento se ancora in corso|
|`--timeout`      |`300`  |Timeout in secondi                         |
|`--output` / `-o`|`json` |`json`, `table`, `csv`                     |

**Endpoint:** `GET /v3/on_page/summary/{task_id}`

**Nota:** se il crawl è ancora in corso, il JSON include `crawl_progress: "in_progress"` con `pages_crawled` e `pages_in_queue` per monitorare l’avanzamento.

-----

### `dfseo site pages`

Lista le pagine crawlate con le relative metriche e check-up.

```bash
# Tutte le pagine
dfseo site pages "task_id"

# Solo pagine con errori
dfseo site pages "task_id" --errors-only

# Filtra per status code
dfseo site pages "task_id" --status-code 404

# Filtra per tipo di risorsa
dfseo site pages "task_id" --type html

# Ordina per score
dfseo site pages "task_id" --sort onpage_score --order asc --limit 20
```

**Parametri:**

|Flag             |Default|Descrizione                                       |
|-----------------|-------|--------------------------------------------------|
|`--errors-only`  |`false`|Solo pagine con errori                            |
|`--status-code`  |-      |Filtra per HTTP status code                       |
|`--type`         |-      |`html`, `image`, `script`, `stylesheet`           |
|`--sort`         |-      |`onpage_score`, `status_code`, `size`, `load_time`|
|`--order`        |`desc` |`asc`, `desc`                                     |
|`--limit` / `-n` |`100`  |Max risultati                                     |
|`--offset`       |`0`    |Offset per paginazione                            |
|`--output` / `-o`|`json` |`json`, `table`, `csv`                            |

**Endpoint:** `POST /v3/on_page/pages`

**Request body:**

```json
[{
  "id": "07281559-0695-0216-0000-c269be8b7592",
  "filters": [
    ["resource_type", "=", "html"],
    "and",
    ["meta.scripts_count", ">", 40]
  ],
  "order_by": ["meta.content.plain_text_word_count,desc"],
  "limit": 20
}]
```

**Output JSON (per pagina):**

```json
{
  "url": "https://qboxmail.it/email-hosting",
  "status_code": 200,
  "onpage_score": 82.3,
  "title": "Email Hosting Professionale | Qboxmail",
  "title_length": 42,
  "description": "Hosting email professionale per aziende...",
  "description_length": 120,
  "h1": ["Email Hosting Professionale"],
  "word_count": 850,
  "internal_links": 24,
  "external_links": 3,
  "images_without_alt": 2,
  "load_time": 1.2,
  "checks": {
    "no_title": false,
    "duplicate_title_tag": true,
    "title_too_long": false,
    "no_description": false,
    "no_h1_tag": false,
    "broken_links": false,
    "is_http": false,
    "low_content_rate": false
  }
}
```

-----

### `dfseo site links`

Lista i link trovati durante il crawl.

```bash
# Tutti i link
dfseo site links "task_id"

# Solo link rotti
dfseo site links "task_id" --type broken

# Solo link esterni
dfseo site links "task_id" --type external

# Solo link interni
dfseo site links "task_id" --type internal

# Link da una pagina specifica
dfseo site links "task_id" --page-from "https://qboxmail.it/"
```

**Parametri:**

|Flag             |Default|Descrizione                                 |
|-----------------|-------|--------------------------------------------|
|`--type`         |-      |`broken`, `internal`, `external`, `redirect`|
|`--page-from`    |-      |Filtra link dalla pagina specificata        |
|`--page-to`      |-      |Filtra link verso la pagina specificata     |
|`--dofollow-only`|`false`|Solo link dofollow                          |
|`--limit` / `-n` |`100`  |Max risultati                               |
|`--output` / `-o`|`json` |`json`, `table`, `csv`                      |

**Endpoint:** `POST /v3/on_page/links`

**Request body:**

```json
[{
  "id": "07281559-0695-0216-0000-c269be8b7592",
  "filters": [
    ["status_code", ">=", 400]
  ],
  "limit": 100
}]
```

-----

### `dfseo site duplicates`

Trova contenuti o tag duplicati.

```bash
# Title duplicati
dfseo site duplicates "task_id" --type title

# Description duplicate
dfseo site duplicates "task_id" --type description

# Contenuto duplicato (rispetto a una pagina specifica)
dfseo site duplicates "task_id" --type content --page "https://qboxmail.it/page"
```

**Parametri:**

|Flag             |Default|Descrizione                                   |
|-----------------|-------|----------------------------------------------|
|`--type` / `-t`  |`title`|`title`, `description`, `content`             |
|`--page`         |-      |Per `content`: URL della pagina da confrontare|
|`--limit` / `-n` |`100`  |Max risultati                                 |
|`--output` / `-o`|`json` |`json`, `table`, `csv`                        |

**Endpoint mappings:**

- `--type title` / `--type description` → `POST /v3/on_page/duplicate_tags`
- `--type content` → `POST /v3/on_page/duplicate_content`

-----

### `dfseo site redirects`

Identifica catene di redirect.

```bash
# Tutte le redirect chain
dfseo site redirects "task_id"

# Solo catene > 2 hop
dfseo site redirects "task_id" --min-hops 3
```

**Parametri:**

|Flag             |Default|Descrizione                        |
|-----------------|-------|-----------------------------------|
|`--min-hops`     |-      |Filtra catene con almeno N redirect|
|`--limit` / `-n` |`100`  |Max risultati                      |
|`--output` / `-o`|`json` |`json`, `table`, `csv`             |

**Endpoint:** `POST /v3/on_page/redirect_chains`

-----

### `dfseo site non-indexable`

Lista pagine bloccate dall’indicizzazione.

```bash
dfseo site non-indexable "task_id"
dfseo site non-indexable "task_id" --reason noindex
```

**Parametri:**

|Flag             |Default|Descrizione                                     |
|-----------------|-------|------------------------------------------------|
|`--reason`       |-      |`noindex`, `canonical`, `robots_txt`, `redirect`|
|`--limit` / `-n` |`100`  |Max risultati                                   |
|`--output` / `-o`|`json` |`json`, `table`, `csv`                          |

**Endpoint:** `POST /v3/on_page/non_indexable`

-----

### `dfseo site resources`

Lista le risorse del sito (immagini, script, stylesheet).

```bash
# Tutte le risorse
dfseo site resources "task_id"

# Solo immagini grandi
dfseo site resources "task_id" --type image --min-size 500000

# Script esterni
dfseo site resources "task_id" --type script --external-only
```

**Parametri:**

|Flag             |Default|Descrizione                              |
|-----------------|-------|-----------------------------------------|
|`--type`         |-      |`image`, `script`, `stylesheet`, `broken`|
|`--min-size`     |-      |Dimensione minima in bytes               |
|`--external-only`|`false`|Solo risorse esterne                     |
|`--limit` / `-n` |`100`  |Max risultati                            |
|`--output` / `-o`|`json` |`json`, `table`, `csv`                   |

**Endpoint:** `POST /v3/on_page/resources`

-----

### `dfseo site lighthouse`

Esegue un audit Lighthouse (Google PageSpeed) su una URL specifica. Anche questo è asincrono (Task POST → GET).

```bash
# Lighthouse completo
dfseo site lighthouse "https://qboxmail.it" --wait

# Solo performance
dfseo site lighthouse "https://qboxmail.it" --categories performance --wait

# Mobile
dfseo site lighthouse "https://qboxmail.it" --device mobile --wait
```

**Parametri:**

|Flag             |Default  |Descrizione                                                                     |
|-----------------|---------|--------------------------------------------------------------------------------|
|`--categories`   |`all`    |`performance`, `accessibility`, `seo`, `best-practices`, `pwa` (comma-separated)|
|`--device` / `-d`|`desktop`|`desktop`, `mobile`                                                             |
|`--wait` / `-w`  |`true`   |Attende completamento                                                           |
|`--timeout`      |`120`    |Timeout in secondi                                                              |
|`--output` / `-o`|`json`   |`json`, `table`                                                                 |

**Endpoint POST:** `POST /v3/on_page/lighthouse/task_post`

**Request body:**

```json
[{
  "url": "https://qboxmail.it",
  "for_mobile": false,
  "categories": ["performance", "seo", "accessibility", "best_practices"]
}]
```

**Endpoint GET:** `GET /v3/on_page/lighthouse/task_get/json/{task_id}`

**Output JSON (semplificato):**

```json
{
  "url": "https://qboxmail.it",
  "device": "desktop",
  "scores": {
    "performance": 85,
    "accessibility": 92,
    "seo": 88,
    "best_practices": 95
  },
  "metrics": {
    "first_contentful_paint": 1.2,
    "largest_contentful_paint": 2.1,
    "total_blocking_time": 150,
    "cumulative_layout_shift": 0.05,
    "speed_index": 1.8
  },
  "cost": 0.002,
  "timestamp": "2026-03-06T14:35:00Z"
}
```

**Output table:**

```
$ dfseo site lighthouse "https://qboxmail.it" -o table

  URL: https://qboxmail.it | Device: desktop

  Category          │ Score
  ──────────────────┼────────────
  Performance       │  85 ████████▌
  Accessibility     │  92 █████████▏
  SEO               │  88 ████████▊
  Best Practices    │  95 █████████▌

  Core Web Vitals:
    FCP: 1.2s | LCP: 2.1s | TBT: 150ms | CLS: 0.05 | SI: 1.8s

  Cost: $0.002
```

-----

### `dfseo site tasks`

Utility: lista i task on-page attivi/completati.

```bash
# Task pronti (risultati non ancora recuperati)
dfseo site tasks --ready

# Tutti i task recenti
dfseo site tasks
```

**Endpoint:** `GET /v3/on_page/tasks_ready`

-----

## Endpoint Mappings v1.2

|Comando CLI                      |Metodo       |Endpoint API                                       |
|---------------------------------|-------------|---------------------------------------------------|
|`dfseo site crawl`               |POST (async) |`POST /v3/on_page/task_post`                       |
|`dfseo site audit` (multi-page)  |POST+Poll+GET|`task_post` → `summary`                            |
|`dfseo site audit` (single page) |POST (live)  |`POST /v3/on_page/instant_pages`                   |
|`dfseo site summary`             |GET          |`GET /v3/on_page/summary/{id}`                     |
|`dfseo site pages`               |POST         |`POST /v3/on_page/pages`                           |
|`dfseo site links`               |POST         |`POST /v3/on_page/links`                           |
|`dfseo site duplicates` (tags)   |POST         |`POST /v3/on_page/duplicate_tags`                  |
|`dfseo site duplicates` (content)|POST         |`POST /v3/on_page/duplicate_content`               |
|`dfseo site redirects`           |POST         |`POST /v3/on_page/redirect_chains`                 |
|`dfseo site non-indexable`       |POST         |`POST /v3/on_page/non_indexable`                   |
|`dfseo site resources`           |POST         |`POST /v3/on_page/resources`                       |
|`dfseo site lighthouse`          |POST+Poll+GET|`lighthouse/task_post` → `lighthouse/task_get/json`|
|`dfseo site tasks`               |GET          |`GET /v3/on_page/tasks_ready`                      |

-----

## Task Polling — Dettagli implementativi

Il polling è l’aspetto più critico della v1.2 perché introduce concetti assenti nella v1.0 e v1.1.

### Flusso polling

```
1. POST /v3/on_page/task_post → ricevi task_id
2. Loop:
   a. GET /v3/on_page/summary/{task_id}
   b. Controlla result[0].crawl_progress
   c. Se "finished" → esci dal loop
   d. Se "in_progress" → stampa progress su stderr, attendi poll_interval
   e. Se timeout raggiunto → exit 1 con errore
3. Restituisci summary su stdout
```

### Progress su stderr (per agenti)

Durante il polling, il CLI stampa aggiornamenti su **stderr** in formato JSON (una riga per update):

```
{"status":"crawling","pages_crawled":15,"pages_in_queue":142,"elapsed_seconds":10}
{"status":"crawling","pages_crawled":45,"pages_in_queue":87,"elapsed_seconds":20}
{"status":"finished","pages_crawled":87,"pages_in_queue":0,"elapsed_seconds":35}
```

Questo permette all’agente di leggere il progress senza interferire con lo stdout (che conterrà il risultato finale).

### Modalità non-blocking

Con `dfseo site crawl` (senza `--wait`), il CLI restituisce immediatamente il task_id:

```json
{"task_id": "07281559-0695-0216-0000-c269be8b7592", "target": "qboxmail.it", "max_crawl_pages": 100}
```

L’agente può poi fare polling manuale con `dfseo site summary {task_id}`.

-----

## Filtri On-Page API

Come per Labs, la On-Page API supporta filtri. Il CLI deve tradurre i flag in filtri API.

**Operatori:** `=`, `<>`, `>`, `<`, `>=`, `<=`, `like`, `not_like`, `regex`, `not_regex`

**Campi filtrabili principali (per `pages`):**

- `resource_type` — tipo risorsa (`html`, `image`, `script`, `stylesheet`)
- `status_code` — HTTP status code
- `meta.title` — titolo della pagina
- `meta.description` — meta description
- `meta.content.plain_text_word_count` — conteggio parole
- `onpage_score` — score SEO della pagina
- `checks.*` — qualsiasi parametro di check (es. `checks.no_title`, `checks.broken_links`)

-----

## Istruzioni per Claude Code — v1.2

### Cosa fare

1. **Crea `src/dfseo/polling.py`** — modulo di task polling con progress su stderr. Deve essere generico e riusabile (servirà anche per future API async)
1. **Crea `src/dfseo/commands/site.py`** — nuovo Typer sub-app
1. **Implementa `site crawl`** — puro POST, restituisce task_id
1. **Implementa `site summary`** — GET con opzione `--wait` che usa il polling
1. **Implementa `site audit`** — combinazione di crawl + wait + summary. Deve switchare automaticamente su Instant Pages quando `--max-pages 1` e il target è un URL completo
1. **Implementa `site pages`** — POST con filtri
1. **Implementa `site links`** — POST con traduzione da `--type broken` a filtro `["status_code", ">=", 400]`
1. **Implementa `site duplicates`** — deve switchare endpoint in base a `--type`
1. **Implementa `site redirects`** e `site non-indexable`** — semplici POST con filtri
1. **Implementa `site resources`** — POST con filtri per tipo e dimensione
1. **Implementa `site lighthouse`** — flusso async separato (`lighthouse/task_post` → `lighthouse/task_get/json`)
1. **Implementa `site tasks`** — utility GET per lista task
1. **Aggiorna SKILL.md** con i nuovi comandi

### Principi specifici v1.2

- **Il polling è il cuore della v1.2** — dedicaci tempo, deve essere robusto con timeout, retry, e progress su stderr
- **Instant Pages è l’eccezione** — per singole pagine, evita il flusso asincrono
- **I comandi GET (summary, pages, links, ecc.) richiedono un `task_id`** — valida che sia un ID valido prima di chiamare l’API
- **Mostra il costo stimato** su stderr prima di lanciare crawl con `--enable-javascript` o `--load-resources` (costi extra)
- **Il modulo polling deve essere generico** — accetta un callable per controllare lo stato, così può essere riusato per Lighthouse e future API
- **I filtri on-page sono più complessi** — supportano `regex` e `not_regex`, campi annidati con dot notation (`checks.no_title`)

### Cosa NON fare

- Non usare il metodo Standard con pingback/postback — per un CLI il polling è sufficiente
- Non ignorare il `crawl_progress` — mai restituire dati parziali senza avvisare l’utente
- Non lanciare crawl di 1000+ pagine senza conferma su stderr (mostra costo stimato)
- Non duplicare la logica di polling tra `site audit` e `site lighthouse` — usa il modulo `polling.py`
- Non mischiare output di progress (stderr) con risultati (stdout)

-----

## Aggiornamento SKILL.md

Aggiungere alla skill esistente:

```markdown
### Site Audit (full crawl + summary)
\`\`\`bash
dfseo site audit "domain.com" --max-pages 100 --wait
\`\`\`

### Quick Page Check (single URL, instant)
\`\`\`bash
dfseo site audit "https://domain.com/page" --max-pages 1
\`\`\`

### Broken Links
\`\`\`bash
dfseo site links "TASK_ID" --type broken
\`\`\`

### Duplicate Titles
\`\`\`bash
dfseo site duplicates "TASK_ID" --type title
\`\`\`

### Lighthouse Performance
\`\`\`bash
dfseo site lighthouse "https://domain.com" --categories performance --wait
\`\`\`

### Non-blocking Crawl + Manual Check
\`\`\`bash
task_id=$(dfseo site crawl "domain.com" --max-pages 500 -q)
dfseo site summary "$task_id" --wait
dfseo site pages "$task_id" --errors-only
\`\`\`
```

-----

## Riferimenti v1.2

- On-Page API Overview: https://docs.dataforseo.com/v3/on_page-overview/
- Task POST: https://docs.dataforseo.com/v3/on_page-task_post/
- Summary: https://docs.dataforseo.com/v3/on_page-summary/
- Pages: https://docs.dataforseo.com/v3/on_page-pages/
- Instant Pages (Live): https://docs.dataforseo.com/v3/on_page-instant_pages/
- Links: https://docs.dataforseo.com/v3/on_page-links/
- Duplicate Tags: https://docs.dataforseo.com/v3/on_page-duplicate_tags/
- Redirect Chains: https://docs.dataforseo.com/v3/on_page-redirect_chains/
- Non-Indexable: https://docs.dataforseo.com/v3/on_page-non_indexable/
- Resources: https://docs.dataforseo.com/v3/on_page-resources/
- Lighthouse: https://docs.dataforseo.com/v3/on_page/lighthouse/task_get/json/
- 120 OnPage Metrics Explained: https://dataforseo.com/blog/120-onpage-api-metrics-explained
