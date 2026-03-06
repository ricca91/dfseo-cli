# dfseo-cli — DataForSEO CLI for AI Agents

> Spec document v1.0 — Brief per Claude Code
> Autore: Ricc | Data: Marzo 2026

-----

## Vision

`dfseo` è un CLI che dà ad agenti AI (OpenClaw, Claude Code, Gemini CLI, qualsiasi agent framework) accesso diretto ai dati SEO di DataForSEO — senza dover scrivere script custom o integrare SDK.

Ispirazione diretta: **gogcli** (Google Workspace CLI di steipete) e **gws** (Google Workspace CLI ufficiale). Stessa filosofia: un binario, output JSON, pensato per le macchine ma usabile dagli umani.

-----

## Stack Tecnologico

|Componente       |Scelta                         |Motivazione                                   |
|-----------------|-------------------------------|----------------------------------------------|
|Linguaggio       |**Python 3.11+**               |Ecosistema maturo, iterazione veloce          |
|CLI framework    |**Typer**                      |Auto-genera help, type hints, shell completion|
|HTTP client      |**httpx**                      |Async-ready, timeout handling, HTTP/2         |
|Output formatting|**rich** (opzionale)           |Pretty tables per modalità human              |
|Packaging        |**PyPI** (`pip install dfseo`) |Distribuzione standard                        |
|Config           |**~/.config/dfseo/config.toml**|XDG-compliant                                 |

-----

## Architettura

```
dfseo/
├── pyproject.toml          # Build config (setuptools/hatch)
├── README.md
├── LICENSE                  # MIT
├── src/
│   └── dfseo/
│       ├── __init__.py
│       ├── cli.py           # Entry point Typer app
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── serp.py      # Comandi SERP API
│       │   ├── auth.py      # Setup credenziali
│       │   └── config.py    # Gestione configurazione
│       ├── client.py        # DataForSEO API client wrapper
│       ├── config.py        # Config loader (TOML)
│       ├── output.py        # Output formatter (JSON/table/csv)
│       └── models.py        # Pydantic models per response
├── tests/
│   ├── test_serp.py
│   ├── test_client.py
│   └── fixtures/            # Mock API responses
└── SKILL.md                 # Agent skill file (per OpenClaw/Claude Code)
```

-----

## Autenticazione

DataForSEO usa HTTP Basic Auth (login + password da https://app.dataforseo.com/api-access).

### Setup

```bash
# Metodo 1: comando interattivo
dfseo auth setup
# → Chiede login e password, salva in ~/.config/dfseo/config.toml

# Metodo 2: environment variables (preferito per agenti)
export DATAFORSEO_LOGIN="your@email.com"
export DATAFORSEO_PASSWORD="your_api_password"

# Metodo 3: flag inline (per testing)
dfseo serp google "keyword" --login user --password pass
```

### Priorità di risoluzione credenziali

1. Flag `--login` / `--password` (inline)
1. Env vars `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD`
1. File `~/.config/dfseo/config.toml`

### Config file format

```toml
# ~/.config/dfseo/config.toml

[auth]
login = "your@email.com"
password = "your_api_password"

[defaults]
location_name = "Italy"
language_name = "Italian"
device = "desktop"
output = "json"             # json | table | csv
```

### Verifica credenziali

```bash
dfseo auth status
# Output: ✓ Authenticated as your@email.com (balance: $42.50)
```

-----

## Comandi v1 — SERP API

La v1 copre esclusivamente la SERP API, usando il metodo **Live** (risultati real-time, niente task asincroni).

### Struttura comandi

```
dfseo <resource> <action> [args] [options]
```

Pattern coerente con gogcli:

- `gog gmail search "query"` → `dfseo serp google "keyword"`
- `gog calendar events` → `dfseo serp bing "keyword"`

-----

### `dfseo serp google`

Ricerca SERP organica su Google.

```bash
# Ricerca base
dfseo serp google "email hosting provider"

# Con parametri
dfseo serp google "email hosting provider" \
  --location "Italy" \
  --language "Italian" \
  --device desktop \
  --depth 100 \
  --output json

# Ricerca mobile
dfseo serp google "email hosting" --device mobile --os android

# Solo featured snippets e PAA
dfseo serp google "what is DKIM" --features-only
```

**Parametri:**

|Flag               |Default  |Descrizione                                    |
|-------------------|---------|-----------------------------------------------|
|`--location` / `-l`|da config|Nome location (es. “Italy”, “United States”)   |
|`--language` / `-L`|da config|Nome lingua (es. “Italian”, “English”)         |
|`--device` / `-d`  |`desktop`|`desktop` o `mobile`                           |
|`--os`             |`null`   |`windows`, `macos`, `ios`, `android`           |
|`--depth` / `-n`   |`100`    |Numero risultati (max 700)                     |
|`--output` / `-o`  |`json`   |`json`, `table`, `csv`                         |
|`--raw`            |`false`  |Output API response completa senza parsing     |
|`--features-only`  |`false`  |Filtra solo SERP features (PAA, snippets, ecc.)|

**Output JSON (default, per agenti):**

```json
{
  "keyword": "email hosting provider",
  "location": "Italy",
  "language": "Italian",
  "device": "desktop",
  "results_count": 100,
  "serp_features": ["featured_snippet", "people_also_ask", "local_pack"],
  "organic_results": [
    {
      "rank": 1,
      "rank_group": 1,
      "domain": "example.com",
      "url": "https://example.com/email-hosting",
      "title": "Best Email Hosting Provider 2026",
      "description": "Compare the top email hosting...",
      "breadcrumb": "example.com › email › hosting"
    }
  ],
  "featured_snippet": {
    "text": "...",
    "source_url": "...",
    "source_domain": "..."
  },
  "people_also_ask": [
    {
      "question": "What is the best email hosting for business?",
      "expanded_text": "..."
    }
  ],
  "cost": 0.002,
  "timestamp": "2026-03-06T14:30:00Z"
}
```

**Output table (per umani):**

```
$ dfseo serp google "email hosting" --output table

  Keyword: email hosting | Location: Italy | Device: desktop | Results: 100

  # │ Domain            │ Title                              │ URL
  ──┼───────────────────┼────────────────────────────────────┼──────────────
  1 │ example.com       │ Best Email Hosting 2026            │ /email-host…
  2 │ provider.com      │ Email Hosting for Business          │ /business…
  3 │ hosting.it        │ Hosting Email Professionale         │ /email…

  SERP Features: featured_snippet, people_also_ask, local_pack
  Cost: $0.002
```

-----

### `dfseo serp bing`

Stessa interfaccia di `dfseo serp google`, endpoint Bing.

```bash
dfseo serp bing "email hosting provider" --location "Italy"
```

-----

### `dfseo serp youtube`

Ricerca SERP su YouTube.

```bash
dfseo serp youtube "email marketing tutorial" --depth 20
```

-----

### `dfseo serp compare`

Comando helper: confronta risultati SERP tra due search engine.

```bash
dfseo serp compare "email hosting" --engines google,bing --location "Italy"
```

Output: tabella che mostra overlap di domini, posizioni diverse, domini unici per engine.

-----

### `dfseo serp locations`

Lista le location disponibili per DataForSEO.

```bash
# Cerca location
dfseo serp locations --search "italy"

# Output: lista di location_name e location_code
```

-----

### `dfseo serp languages`

Lista le lingue disponibili.

```bash
dfseo serp languages --search "ital"
```

-----

### `dfseo auth setup`

Setup interattivo delle credenziali.

```bash
dfseo auth setup
# → Login: your@email.com
# → Password: ********
# → Saved to ~/.config/dfseo/config.toml
```

-----

### `dfseo auth status`

Verifica credenziali e saldo account.

```bash
dfseo auth status
# → ✓ Authenticated as user@email.com
# → Balance: $42.50
# → Rate limit: 2000 req/min
```

-----

### `dfseo config set`

Imposta defaults.

```bash
dfseo config set location "Italy"
dfseo config set language "Italian"
dfseo config set output json
dfseo config set device desktop
```

### `dfseo config show`

Mostra configurazione corrente.

```bash
dfseo config show
# → location: Italy
# → language: Italian
# → output: json
# → device: desktop
```

-----

## Convenzioni Output

Fondamentale per l’uso da parte degli agenti:

### 1. JSON come default

L’output predefinito è **JSON valido su stdout**. Niente testo decorativo, niente spinner, niente emoji in modalità JSON. Gli agenti parsano stdout direttamente.

### 2. Errori su stderr

Tutti i messaggi di errore, warning e log vanno su **stderr**. Questo permette:

```bash
# L'agente può parsare stdout anche in caso di warning
result=$(dfseo serp google "keyword" 2>/dev/null)
```

### 3. Exit codes

|Code|Significato          |
|----|---------------------|
|`0` |Successo             |
|`1` |Errore generico      |
|`2` |Errore autenticazione|
|`3` |Rate limit raggiunto |
|`4` |Parametri invalidi   |
|`5` |Saldo insufficiente  |

### 4. Flag `--output` / `-o`

- `json` — JSON compatto su una riga (default)
- `json-pretty` — JSON indentato (debug)
- `table` — Tabella formattata con rich (per umani)
- `csv` — CSV con header

### 5. Flag `--quiet` / `-q`

Sopprime tutto tranne il risultato. Utile per piping:

```bash
dfseo serp google "keyword" -q | jq '.organic_results[0].url'
```

### 6. Flag `--verbose` / `-v`

Mostra request/response details su stderr. Per debug:

```bash
dfseo serp google "keyword" -v 2>debug.log
```

-----

## SKILL.md — Agent Skill File

Incluso nel repo, permette a qualsiasi agente AI di scoprire e usare il tool.

```markdown
---
name: dfseo-cli
description: >
  SEO data CLI powered by DataForSEO APIs. Use when the user needs SERP data,
  keyword rankings, search engine results for any keyword/location/language.
  Triggers on: "SERP", "search results", "keyword ranking", "SEO data",
  "Google results for", "check ranking", "search position".
---

# dfseo-cli — SEO Data from your terminal

## Quick Start
Requires DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD env vars.

## Core Commands

### Google SERP
\`\`\`bash
dfseo serp google "keyword" --location "Country" --language "Language"
\`\`\`

### Bing SERP
\`\`\`bash
dfseo serp bing "keyword" --location "Country"
\`\`\`

### YouTube SERP
\`\`\`bash
dfseo serp youtube "keyword"
\`\`\`

### Available locations
\`\`\`bash
dfseo serp locations --search "country name"
\`\`\`

## Output
- Default: JSON on stdout (machine-readable)
- Errors: stderr only
- Add `--output table` for human-readable format

## Common Patterns
\`\`\`bash
# Top 10 results for a keyword in Italy
dfseo serp google "keyword" -l "Italy" -L "Italian" -n 10

# Compare Google vs Bing
dfseo serp compare "keyword" --engines google,bing

# Get SERP features only
dfseo serp google "keyword" --features-only
\`\`\`
```

-----

## API Client — Dettagli Implementativi

### Endpoint base

```
https://api.dataforseo.com/v3/
```

### Autenticazione

HTTP Basic Auth. Header:

```
Authorization: Basic base64(login:password)
```

### SERP Live Advanced (endpoint principale)

```
POST https://api.dataforseo.com/v3/serp/google/organic/live/advanced
```

**Request body:**

```json
[{
  "keyword": "email hosting provider",
  "location_name": "Italy",
  "language_name": "Italian",
  "device": "desktop",
  "os": "windows",
  "depth": 100
}]
```

**Response parsing:**
Il response è annidato: `tasks[0].result[0].items[]` contiene i risultati SERP.
Ogni item ha un `type` (organic, featured_snippet, people_also_ask, local_pack, ecc.).
Il client deve filtrare per tipo e strutturare l’output in modo pulito.

### Endpoint mappings

|Comando CLI           |Endpoint API                                 |
|----------------------|---------------------------------------------|
|`dfseo serp google`   |`POST /v3/serp/google/organic/live/advanced` |
|`dfseo serp bing`     |`POST /v3/serp/bing/organic/live/advanced`   |
|`dfseo serp youtube`  |`POST /v3/serp/youtube/organic/live/advanced`|
|`dfseo serp locations`|`GET /v3/serp/google/locations`              |
|`dfseo serp languages`|`GET /v3/serp/google/languages`              |
|`dfseo auth status`   |`GET /v3/appendix/user_data`                 |

### Rate limiting

- Max 2000 request/minuto
- Il client deve leggere gli header `X-RateLimit-Remaining` e rallentare automaticamente
- In caso di 429, retry con exponential backoff (max 3 tentativi)

### Error handling

- Controllare `status_code` nel response (20000 = OK)
- Ogni task ha il suo `status_code` e `status_message`
- Mappare gli errori DataForSEO sugli exit code del CLI

-----

## Roadmap Post-v1

Una volta validata la v1 con SERP, le espansioni naturali sono:

|Versione|Feature          |Comandi                                                               |
|--------|-----------------|----------------------------------------------------------------------|
|v1.0    |SERP API (Live)  |`serp google/bing/youtube`, `serp compare`, `serp locations/languages`|
|v1.1    |Keywords Data API|`keywords volume`, `keywords suggestions`, `keywords difficulty`      |
|v1.2    |On-Page API      |`site audit`, `site pages`, `site errors`                             |
|v1.3    |Backlinks API    |`backlinks summary`, `backlinks list`, `backlinks anchors`            |
|v2.0    |MCP Server mode  |`dfseo mcp` — espone tutti i comandi come tool MCP                    |

L’idea della v2.0 è cruciale: lo stesso codebase serve sia come CLI che come MCP server, esattamente come fa `gws mcp` di Google.

-----

## Istruzioni per Claude Code

### Cosa fare

1. **Inizializza il progetto** con `pyproject.toml` (usa hatch o setuptools), entry point `dfseo`
1. **Implementa prima `client.py`** — wrapper httpx con auth, error handling, retry logic
1. **Implementa `auth setup` e `auth status`** — per validare che le credenziali funzionano
1. **Implementa `serp google`** — comando core, usa endpoint Live Advanced
1. **Implementa output formatter** — JSON default, table con rich, csv
1. **Aggiungi `serp bing` e `serp youtube`** — stessa struttura, endpoint diverso
1. **Aggiungi `serp locations` e `serp languages`** — utility GET
1. **Aggiungi `serp compare`** — logica di diff tra due risultati
1. **Scrivi test** con mock responses (fixtures JSON da docs DataForSEO)
1. **Crea SKILL.md** nella root del progetto

### Principi di design

- **JSON su stdout, tutto il resto su stderr** — non mischiare mai
- **Niente dipendenze pesanti** — solo typer, httpx, rich (opzionale), tomli, pydantic
- **Fail fast** — se mancano credenziali, exit 2 subito con messaggio chiaro
- **Type hints ovunque** — il codice deve essere leggibile da un agente AI
- **Docstring su ogni funzione pubblica** — gli agenti li usano per capire il tool
- **Config XDG-compliant** — `~/.config/dfseo/config.toml`
- **Niente stato globale** — dependency injection per il client API

### Cosa NON fare

- Non usare il client Python ufficiale DataForSEO (`dataforseo_client`) — è over-engineered per un CLI. Usa httpx direttamente
- Non implementare il metodo Standard (task asincroni) nella v1 — solo Live
- Non aggiungere spinner o progress bar in modalità JSON
- Non usare `click` — usa Typer (è basato su click ma con type hints)
- Non hardcodare location/language — sempre configurabili

-----

## Riferimenti

- DataForSEO API Docs: https://docs.dataforseo.com/v3/
- DataForSEO SERP Overview: https://docs.dataforseo.com/v3/serp-overview/
- DataForSEO Python Client (riferimento, non da usare): https://github.com/dataforseo/PythonClient
- gogcli (ispirazione): https://github.com/steipete/gogcli
- gws Google Workspace CLI (ispirazione): https://github.com/googleworkspace/cli
- Typer docs: https://typer.tiangolo.com/
