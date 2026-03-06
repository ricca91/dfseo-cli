# dfseo-cli v1.1 — Keywords Data

> Spec document v1.1 — Brief per Claude Code
> Autore: Ricc | Data: Marzo 2026
> Prerequisito: v1.0 (SERP API) deve essere implementata

-----

## Overview

La v1.1 aggiunge il comando `dfseo keywords` che dà accesso ai dati keyword da **due fonti DataForSEO diverse**:

1. **Keywords Data API** (Google Ads) — volume di ricerca, CPC, competition dal database Google Ads
1. **DataForSEO Labs API** (database proprietario) — keyword suggestions, keyword ideas, keyword difficulty, search intent

L’interfaccia CLI unifica entrambe le fonti sotto un unico namespace `keywords`, nascondendo la complessità degli endpoint all’utente/agente.

-----

## Nota importante sulle API

DataForSEO ha un limite di **12 request/minuto** per gli endpoint Google Ads Live. Il client deve gestire questo rate limit separatamente da quello generale (2000/min). Gli endpoint DataForSEO Labs non hanno questo vincolo.

Google aggiorna i dati keyword **a metà mese**. L’endpoint `google_ads/status` permette di verificare se i dati del mese precedente sono già disponibili.

Le keyword che rientrano nelle categorie proibite da Google Ads (armi, tabacco, droghe, ecc.) restituiscono errore. Se anche **una sola keyword** nel batch è proibita, l’intero batch fallisce.

-----

## Modifiche all’architettura

### Nuovo file

```
src/dfseo/commands/keywords.py   # Tutti i comandi keywords
```

### Aggiornamento cli.py

```python
# Aggiungere il sub-command group
from dfseo.commands import keywords
app.add_typer(keywords.app, name="keywords")
```

-----

## Comandi

### `dfseo keywords volume`

Ottiene volume di ricerca, CPC e competition per una o più keyword. Usa l’endpoint **Keyword Overview** di DataForSEO Labs (più completo del Google Ads puro, include keyword_difficulty e search_intent).

```bash
# Singola keyword
dfseo keywords volume "email hosting"

# Multiple keyword (fino a 700 per request)
dfseo keywords volume "email hosting" "smtp provider" "email server"

# Da file (una keyword per riga)
dfseo keywords volume --from-file keywords.txt

# Con parametri
dfseo keywords volume "email hosting" \
  --location "Italy" \
  --language "Italian" \
  --include-serp-info \
  --output json
```

**Parametri:**

|Flag                 |Default  |Descrizione                                      |
|---------------------|---------|-------------------------------------------------|
|`--location` / `-l`  |da config|Location name                                    |
|`--language` / `-L`  |da config|Language name                                    |
|`--include-serp-info`|`false`  |Aggiunge dati SERP (num risultati, SERP features)|
|`--from-file` / `-f` |-        |Legge keyword da file (una per riga, max 700)    |
|`--output` / `-o`    |`json`   |`json`, `table`, `csv`                           |

**Endpoint API:**

```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_overview/live
```

**Request body:**

```json
[{
  "keywords": ["email hosting", "smtp provider"],
  "location_name": "Italy",
  "language_name": "Italian",
  "include_serp_info": true
}]
```

**Output JSON:**

```json
{
  "keywords_count": 2,
  "location": "Italy",
  "language": "Italian",
  "results": [
    {
      "keyword": "email hosting",
      "search_volume": 2400,
      "cpc": 3.45,
      "competition": 0.82,
      "competition_level": "HIGH",
      "keyword_difficulty": 67,
      "search_intent": {
        "main": "commercial",
        "foreign": ["informational"]
      },
      "monthly_searches": [
        {"month": 3, "year": 2026, "volume": 2400},
        {"month": 2, "year": 2026, "volume": 2200}
      ],
      "serp_info": {
        "serp_count": 245000000,
        "features": ["featured_snippet", "people_also_ask", "sitelinks"]
      }
    },
    {
      "keyword": "smtp provider",
      "search_volume": 880,
      "cpc": 5.12,
      "competition": 0.65,
      "competition_level": "MEDIUM",
      "keyword_difficulty": 52,
      "search_intent": {
        "main": "commercial",
        "foreign": ["transactional"]
      },
      "monthly_searches": [...],
      "serp_info": null
    }
  ],
  "cost": 0.0105,
  "timestamp": "2026-03-06T14:30:00Z"
}
```

**Output table:**

```
$ dfseo keywords volume "email hosting" "smtp provider" -l Italy -o table

  Location: Italy | Language: Italian | Keywords: 2

  Keyword         │ Volume │ CPC   │ Comp  │ KD │ Intent
  ────────────────┼────────┼───────┼───────┼────┼────────────
  email hosting   │  2,400 │ $3.45 │ HIGH  │ 67 │ commercial
  smtp provider   │    880 │ $5.12 │ MED   │ 52 │ commercial

  Cost: $0.0105
```

-----

### `dfseo keywords suggestions`

Trova keyword suggerite che **contengono** la seed keyword (long-tail). Usa DataForSEO Labs Keyword Suggestions.

```bash
# Base
dfseo keywords suggestions "email hosting"

# Con limiti e filtri
dfseo keywords suggestions "email hosting" \
  --location "Italy" \
  --language "Italian" \
  --limit 50 \
  --min-volume 100 \
  --max-difficulty 40 \
  --include-seed

# Ordina per volume
dfseo keywords suggestions "email hosting" --sort volume --order desc
```

**Parametri:**

|Flag               |Default    |Descrizione                               |
|-------------------|-----------|------------------------------------------|
|`--location` / `-l`|da config  |Location name                             |
|`--language` / `-L`|da config  |Language name                             |
|`--limit` / `-n`   |`50`       |Max risultati (max 1000)                  |
|`--min-volume`     |-          |Filtra per volume minimo                  |
|`--max-volume`     |-          |Filtra per volume massimo                 |
|`--min-difficulty` |-          |Filtra per KD minimo                      |
|`--max-difficulty` |-          |Filtra per KD massimo                     |
|`--include-seed`   |`false`    |Include la seed keyword nei risultati     |
|`--sort`           |`relevance`|`relevance`, `volume`, `cpc`, `difficulty`|
|`--order`          |`desc`     |`asc`, `desc`                             |
|`--output` / `-o`  |`json`     |`json`, `table`, `csv`                    |

**Endpoint API:**

```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live
```

**Request body:**

```json
[{
  "keyword": "email hosting",
  "location_name": "Italy",
  "language_name": "Italian",
  "include_seed_keyword": true,
  "include_serp_info": true,
  "limit": 50,
  "filters": [
    ["keyword_info.search_volume", ">=", 100],
    "and",
    ["keyword_properties.keyword_difficulty", "<=", 40]
  ],
  "order_by": ["keyword_info.search_volume,desc"]
}]
```

**Output JSON:**

```json
{
  "seed_keyword": "email hosting",
  "location": "Italy",
  "language": "Italian",
  "total_count": 1245,
  "returned_count": 50,
  "results": [
    {
      "keyword": "best email hosting for small business",
      "search_volume": 1200,
      "cpc": 4.20,
      "competition": 0.71,
      "keyword_difficulty": 38,
      "search_intent": "commercial",
      "monthly_searches": [...]
    }
  ],
  "cost": 0.021,
  "timestamp": "2026-03-06T14:30:00Z"
}
```

**Output table:**

```
$ dfseo keywords suggestions "email hosting" -l Italy --min-volume 100 --max-difficulty 40 -n 10 -o table

  Seed: email hosting | Location: Italy | Showing: 10 of 1,245

  Keyword                                  │ Volume │ CPC   │ KD │ Intent
  ─────────────────────────────────────────┼────────┼───────┼────┼────────────
  best email hosting for small business    │  1,200 │ $4.20 │ 38 │ commercial
  cheap email hosting                      │    950 │ $2.80 │ 31 │ transactional
  free email hosting                       │    720 │ $1.90 │ 25 │ transactional
  email hosting for business               │    580 │ $3.60 │ 35 │ commercial
  ...

  Cost: $0.021
```

-----

### `dfseo keywords ideas`

Trova keyword **semanticamente correlate** (non necessariamente contengono la seed). Usa DataForSEO Labs Keyword Ideas — algoritmo basato sulle categorie Google Ads.

```bash
# Base (accetta fino a 20 seed keywords)
dfseo keywords ideas "email hosting" "smtp service"

# Con filtri
dfseo keywords ideas "email hosting" \
  --location "Italy" \
  --language "Italian" \
  --limit 100 \
  --min-volume 50
```

**Parametri:** stessi di `keywords suggestions`.

**Endpoint API:**

```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live
```

**Request body:**

```json
[{
  "keywords": ["email hosting", "smtp service"],
  "location_name": "Italy",
  "language_name": "Italian",
  "include_serp_info": true,
  "limit": 100,
  "closely_variants": false
}]
```

**Differenza chiave vs suggestions:**

- `suggestions` → trova keyword che **contengono** la seed (long-tail expansion)
- `ideas` → trova keyword nella **stessa categoria** (non-obvious, semantically related)

Esempio pratico: seed “email hosting” → `suggestions` restituisce “best email hosting for business”, `ideas` restituisce “DKIM setup”, “mail server configuration”, “MX record”

-----

### `dfseo keywords difficulty`

Calcola la Keyword Difficulty per fino a 1000 keyword in un singolo request. Metrica proprietaria DataForSEO (0-100).

```bash
# Multiple keywords inline
dfseo keywords difficulty "email hosting" "smtp provider" "webmail"

# Da file
dfseo keywords difficulty --from-file keywords.txt

# Con location specifica
dfseo keywords difficulty "email hosting" --location "Italy" --language "Italian"
```

**Parametri:**

|Flag                |Default  |Descrizione                                   |
|--------------------|---------|----------------------------------------------|
|`--location` / `-l` |da config|Location name                                 |
|`--language` / `-L` |da config|Language name                                 |
|`--from-file` / `-f`|-        |Legge keyword da file (una per riga, max 1000)|
|`--output` / `-o`   |`json`   |`json`, `table`, `csv`                        |

**Endpoint API:**

```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live
```

**Request body:**

```json
[{
  "keywords": ["email hosting", "smtp provider", "webmail"],
  "location_name": "Italy",
  "language_name": "Italian"
}]
```

**Output JSON:**

```json
{
  "keywords_count": 3,
  "location": "Italy",
  "language": "Italian",
  "results": [
    {"keyword": "email hosting", "keyword_difficulty": 67},
    {"keyword": "smtp provider", "keyword_difficulty": 52},
    {"keyword": "webmail", "keyword_difficulty": 45}
  ],
  "cost": 0.0103,
  "timestamp": "2026-03-06T14:30:00Z"
}
```

**Output table:**

```
$ dfseo keywords difficulty "email hosting" "smtp provider" "webmail" -l Italy -o table

  Location: Italy | Keywords: 3

  Keyword         │ KD  │ Level
  ────────────────┼─────┼───────────
  email hosting   │  67 │ ██████▋  Hard
  smtp provider   │  52 │ █████▏   Medium
  webmail         │  45 │ ████▌    Medium

  Cost: $0.0103
```

La colonna `Level` è un visual indicator calcolato dal CLI:

- 0-29: Easy (verde)
- 30-49: Medium (giallo)
- 50-69: Hard (arancione)
- 70-100: Very Hard (rosso)

-----

### `dfseo keywords search-intent`

Classifica il search intent di fino a 1000 keyword.

```bash
# Inline
dfseo keywords search-intent "buy email hosting" "what is DKIM" "smtp server setup guide"

# Da file
dfseo keywords search-intent --from-file keywords.txt --location "Italy"
```

**Parametri:**

|Flag                |Default  |Descrizione                |
|--------------------|---------|---------------------------|
|`--location` / `-l` |da config|Location name              |
|`--language` / `-L` |da config|Language name              |
|`--from-file` / `-f`|-        |File con keyword (max 1000)|
|`--output` / `-o`   |`json`   |`json`, `table`, `csv`     |

**Endpoint API:**

```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/search_intent/live
```

**Request body:**

```json
[{
  "keywords": ["buy email hosting", "what is DKIM", "smtp server setup guide"],
  "location_name": "Italy",
  "language_name": "Italian"
}]
```

**Output JSON:**

```json
{
  "keywords_count": 3,
  "location": "Italy",
  "language": "Italian",
  "results": [
    {
      "keyword": "buy email hosting",
      "main_intent": "transactional",
      "foreign_intents": ["commercial"],
      "probability": 0.92
    },
    {
      "keyword": "what is DKIM",
      "main_intent": "informational",
      "foreign_intents": [],
      "probability": 0.98
    },
    {
      "keyword": "smtp server setup guide",
      "main_intent": "informational",
      "foreign_intents": ["navigational"],
      "probability": 0.85
    }
  ],
  "cost": 0.012,
  "timestamp": "2026-03-06T14:30:00Z"
}
```

-----

### `dfseo keywords for-site`

Trova le keyword per cui un dominio si posiziona o che sono rilevanti per esso.

```bash
# Keyword rilevanti per un dominio
dfseo keywords for-site "qboxmail.it" \
  --location "Italy" \
  --language "Italian" \
  --limit 100 \
  --min-volume 50
```

**Parametri:**

|Flag               |Default    |Descrizione                               |
|-------------------|-----------|------------------------------------------|
|`--location` / `-l`|da config  |Location name                             |
|`--language` / `-L`|da config  |Language name                             |
|`--limit` / `-n`   |`100`      |Max risultati                             |
|`--min-volume`     |-          |Volume minimo                             |
|`--max-volume`     |-          |Volume massimo                            |
|`--sort`           |`relevance`|`relevance`, `volume`, `cpc`, `difficulty`|
|`--output` / `-o`  |`json`     |`json`, `table`, `csv`                    |

**Endpoint API:**

```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/keywords_for_site/live
```

**Request body:**

```json
[{
  "target": "qboxmail.it",
  "location_name": "Italy",
  "language_name": "Italian",
  "include_serp_info": true,
  "limit": 100,
  "filters": [
    ["keyword_info.search_volume", ">=", 50]
  ],
  "order_by": ["keyword_info.search_volume,desc"]
}]
```

**Output JSON:**

```json
{
  "target": "qboxmail.it",
  "location": "Italy",
  "language": "Italian",
  "total_count": 342,
  "returned_count": 100,
  "results": [
    {
      "keyword": "email hosting professionale",
      "search_volume": 480,
      "cpc": 2.90,
      "competition": 0.55,
      "keyword_difficulty": 41,
      "search_intent": "commercial",
      "serp_info": {
        "serp_count": 12400000,
        "features": ["people_also_ask"]
      }
    }
  ],
  "cost": 0.035,
  "timestamp": "2026-03-06T14:30:00Z"
}
```

-----

### `dfseo keywords ads-volume`

Accede direttamente ai dati **Google Ads** (volume, CPC, competition) senza le metriche proprietarie DataForSEO. Utile quando serve il dato “puro” da Google Ads.

```bash
# Fino a 20 keyword per request (limite Google Ads)
dfseo keywords ads-volume "email hosting" "smtp provider"

# Con date range
dfseo keywords ads-volume "email hosting" \
  --location "Italy" \
  --language "Italian" \
  --date-from 2025-01 \
  --date-to 2026-03
```

**Parametri:**

|Flag                |Default  |Descrizione                   |
|--------------------|---------|------------------------------|
|`--location` / `-l` |da config|Location name                 |
|`--language` / `-L` |da config|Language name                 |
|`--date-from`       |-        |Inizio range storico (YYYY-MM)|
|`--date-to`         |-        |Fine range storico (YYYY-MM)  |
|`--from-file` / `-f`|-        |File con keyword (max 20)     |
|`--output` / `-o`   |`json`   |`json`, `table`, `csv`        |

**Endpoint API:**

```
POST https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live
```

**Nota rate limit:** max 12 request/minuto per Google Ads endpoints. Il client deve gestirlo.

-----

### `dfseo keywords ads-suggestions`

Suggerimenti keyword direttamente da Google Ads (max 20 seed keywords).

```bash
dfseo keywords ads-suggestions "email hosting" "smtp" \
  --location "Italy" \
  --language "Italian" \
  --limit 100
```

**Endpoint API:**

```
POST https://api.dataforseo.com/v3/keywords_data/google_ads/keywords_for_keywords/live
```

**Nota:** restituisce fino a 20.000 suggerimenti per request, ma con il rate limit di 12/min.

-----

## Endpoint Mappings v1.1

|Comando CLI                     |Fonte     |Endpoint API                                                  |
|--------------------------------|----------|--------------------------------------------------------------|
|`dfseo keywords volume`         |Labs      |`POST /v3/dataforseo_labs/google/keyword_overview/live`       |
|`dfseo keywords suggestions`    |Labs      |`POST /v3/dataforseo_labs/google/keyword_suggestions/live`    |
|`dfseo keywords ideas`          |Labs      |`POST /v3/dataforseo_labs/google/keyword_ideas/live`          |
|`dfseo keywords difficulty`     |Labs      |`POST /v3/dataforseo_labs/google/bulk_keyword_difficulty/live`|
|`dfseo keywords search-intent`  |Labs      |`POST /v3/dataforseo_labs/google/search_intent/live`          |
|`dfseo keywords for-site`       |Labs      |`POST /v3/dataforseo_labs/google/keywords_for_site/live`      |
|`dfseo keywords ads-volume`     |Google Ads|`POST /v3/keywords_data/google_ads/search_volume/live`        |
|`dfseo keywords ads-suggestions`|Google Ads|`POST /v3/keywords_data/google_ads/keywords_for_keywords/live`|

-----

## Filtri DataForSEO Labs

Gli endpoint Labs supportano un sistema di filtri potente. Il CLI deve tradurre i flag `--min-volume`, `--max-difficulty` ecc. nella sintassi filtri dell’API:

```json
"filters": [
  ["keyword_info.search_volume", ">=", 100],
  "and",
  ["keyword_properties.keyword_difficulty", "<=", 40]
]
```

**Operatori supportati:** `=`, `<>`, `>`, `<`, `>=`, `<=`, `contains`, `not_contains`, `in`, `not_in`

**Campi filtrabili principali:**

- `keyword_info.search_volume` — volume di ricerca
- `keyword_info.cpc` — cost per click
- `keyword_info.competition` — competition (0-1)
- `keyword_properties.keyword_difficulty` — difficulty score (0-100)
- `search_intent_info.main_intent` — tipo di intent

Il CLI deve costruire automaticamente il filtro combinando i vari flag con `"and"`.

-----

## Gestione `--from-file`

Pattern condiviso da `volume`, `difficulty`, `search-intent`:

```python
def load_keywords(keywords: list[str], from_file: Optional[str]) -> list[str]:
    """Carica keyword da argomenti CLI o file."""
    if from_file:
        with open(from_file) as f:
            file_keywords = [line.strip() for line in f if line.strip()]
        return file_keywords
    return keywords
```

Il file deve supportare:

- Una keyword per riga
- Righe vuote ignorate
- Righe che iniziano con `#` ignorate (commenti)
- Encoding UTF-8

-----

## Istruzioni per Claude Code — v1.1

### Cosa fare

1. **Crea `src/dfseo/commands/keywords.py`** — nuovo Typer sub-app con tutti i comandi
1. **Registra il sub-command** in `cli.py`: `app.add_typer(keywords.app, name="keywords")`
1. **Implementa `keywords volume` per primo** — è il comando più usato, testa il flusso Labs API
1. **Aggiungi logica filtri** — traduzione da flag CLI a sintassi filtri DataForSEO
1. **Implementa `keywords difficulty`** — semplice, bulk fino a 1000 keyword
1. **Implementa `keywords suggestions` e `keywords ideas`** — stessa struttura, endpoint diversi
1. **Implementa `keywords search-intent` e `keywords for-site`**
1. **Implementa `keywords ads-volume` e `keywords ads-suggestions`** — attenzione al rate limit 12/min
1. **Aggiungi utility `load_keywords()`** — condivisa tra i comandi che accettano `--from-file`
1. **Aggiorna SKILL.md** con i nuovi comandi

### Dettagli implementativi

- I comandi Labs possono usare lo stesso `client.py` della v1.0, cambia solo il base path
- Il rate limiting per Google Ads (12/min) deve essere separato da quello generale
- L’output formatter della v1.0 deve funzionare senza modifiche — stessi flag `--output`
- I filtri vanno costruiti programmaticamente: ogni flag `--min-*` / `--max-*` aggiunge un elemento all’array filtri
- Il campo `order_by` accetta stringhe tipo `"keyword_info.search_volume,desc"`
- Nella tabella per `difficulty`, aggiungere una barra visuale con rich (tipo progress bar) e un label colorato

### Cosa NON fare

- Non mischiare endpoint Labs e Google Ads nello stesso comando — sono fonti diverse
- Non superare i 700 keyword per `volume` e i 1000 per `difficulty`
- Non ignorare il rate limit di 12/min per Google Ads — mettere un throttle esplicito
- Non duplicare la logica di output — riusare il formatter della v1.0

-----

## Aggiornamento SKILL.md

Aggiungere alla skill existente:

```markdown
### Keyword Volume
\`\`\`bash
dfseo keywords volume "keyword1" "keyword2" --location "Country" --language "Language"
\`\`\`

### Keyword Suggestions (long-tail)
\`\`\`bash
dfseo keywords suggestions "seed keyword" --min-volume 100 --max-difficulty 40 --limit 50
\`\`\`

### Keyword Ideas (semantically related)
\`\`\`bash
dfseo keywords ideas "seed1" "seed2" --limit 100
\`\`\`

### Keyword Difficulty (bulk, up to 1000)
\`\`\`bash
dfseo keywords difficulty "kw1" "kw2" "kw3" --location "Country"
# Or from file:
dfseo keywords difficulty --from-file keywords.txt
\`\`\`

### Keywords for a Domain
\`\`\`bash
dfseo keywords for-site "domain.com" --min-volume 50 --sort volume
\`\`\`

### Search Intent Classification
\`\`\`bash
dfseo keywords search-intent "buy hosting" "what is smtp" "gmail login"
\`\`\`
```

-----

## Riferimenti v1.1

- Keywords Data API Overview: https://docs.dataforseo.com/v3/keywords-data-overview/
- DataForSEO Labs Google Overview: https://docs.dataforseo.com/v3/dataforseo_labs-google-overview/
- Keyword Overview endpoint: https://dataforseo.com/help-center/getting-keyword-data-with-keyword-overview-and-historical-keyword-data-endpoints
- Bulk Keyword Difficulty: https://docs.dataforseo.com/v3/dataforseo_labs-google-bulk_keyword_difficulty-live/
- Keyword Suggestions: https://docs.dataforseo.com/v3/dataforseo_labs-google-keyword_suggestions-live/
- Keyword Ideas: https://docs.dataforseo.com/v3/dataforseo_labs-keyword_ideas-live/
- Google Ads Keywords for Keywords: https://docs.dataforseo.com/v3/keywords_data-google_ads-keywords_for_keywords-live/
