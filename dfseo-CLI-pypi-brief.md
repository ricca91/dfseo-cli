# dfseo-cli — PyPI Publishing Brief

> Brief per Claude Code — Pubblicazione su PyPI
> Autore: Ricc | Data: Marzo 2026
> URGENTE: il comando `pip install dfseo` è già stato condiviso pubblicamente

-----

## Obiettivo

Pubblicare `dfseo` su PyPI in modo che `pip install dfseo` funzioni correttamente e installi il CLI con il comando `dfseo` disponibile globalmente.

-----

## Checklist Pre-Pubblicazione

### 1. Verifica nome pacchetto

```bash
# Controlla che "dfseo" sia disponibile su PyPI
pip index versions dfseo
# Se restituisce errore "No matching distribution" → il nome è libero
# Se qualcuno l'ha già preso → dobbiamo usare "dfseo-cli" come pacchetto
```

Se `dfseo` è occupato, usare `dfseo-cli` come nome pacchetto ma mantenere `dfseo` come entry point CLI:

```toml
[project.scripts]
dfseo = "dfseo.cli:app"
```

### 2. Verifica pyproject.toml

Il file deve contenere TUTTI questi campi:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "dfseo"
version = "1.0.0"
description = "DataForSEO CLI for AI agents — SERP, Keywords, Site Audit, Backlinks from your terminal"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.11"
authors = [
    {name = "Ricc", email = "TUA_EMAIL"}
]
keywords = [
    "seo", "cli", "dataforseo", "serp", "keywords", "backlinks",
    "site-audit", "ai-agents", "agent-native", "keyword-research"
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Typing :: Typed",
]
dependencies = [
    "typer>=0.9.0",
    "httpx>=0.25.0",
    "rich>=13.0.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-httpx>=0.30.0",
    "ruff>=0.1.0",
]

[project.scripts]
dfseo = "dfseo.cli:app"

[project.urls]
Homepage = "https://github.com/TUO_USERNAME/dfseo-cli"
Documentation = "https://github.com/TUO_USERNAME/dfseo-cli#readme"
Repository = "https://github.com/TUO_USERNAME/dfseo-cli"
Issues = "https://github.com/TUO_USERNAME/dfseo-cli/issues"
```

**Nota su tomli:** se usi `tomli` per il parsing config, aggiungilo alle dependencies solo per Python < 3.11 (3.11+ ha `tomllib` nella stdlib):

```toml
dependencies = [
    ...
    "tomli>=2.0.0; python_version < '3.11'",
]
```

### 3. Verifica struttura pacchetto

```
dfseo-cli/
├── pyproject.toml
├── README.md
├── LICENSE                    # MIT — deve esistere
├── SKILL.md
├── src/
│   └── dfseo/
│       ├── __init__.py        # DEVE contenere __version__
│       ├── cli.py
│       ├── client.py
│       ├── config.py
│       ├── output.py
│       ├── models.py
│       ├── polling.py
│       └── commands/
│           ├── __init__.py
│           ├── serp.py
│           ├── keywords.py
│           ├── site.py
│           ├── backlinks.py
│           ├── auth.py
│           └── config.py
└── tests/
```

**Verifica `__init__.py`:**

```python
# src/dfseo/__init__.py
"""DataForSEO CLI for AI agents."""
__version__ = "1.0.0"
```

**Verifica che hatch trovi il pacchetto** (se usi src layout):

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/dfseo"]
```

### 4. Verifica che il CLI funzioni dopo installazione pulita

```bash
# Crea un venv pulito e testa
python -m venv /tmp/test-dfseo
source /tmp/test-dfseo/bin/activate
pip install -e .
dfseo --help
dfseo --version
dfseo serp --help
dfseo keywords --help
dfseo site --help
dfseo backlinks --help
deactivate
rm -rf /tmp/test-dfseo
```

### 5. Verifica README.md

Il README è la long_description su PyPI. Deve renderizzare correttamente in Markdown. Verifica:

```bash
# Installa lo strumento di verifica
pip install build twine

# Build e controlla
python -m build
twine check dist/*
# Deve dire "PASSED" per tutti i file
```

-----

## Pubblicazione

### Step 1: Crea account PyPI

Se non hai già un account:

1. Vai su https://pypi.org/account/register/
1. Abilita 2FA (obbligatorio per nuovi account)
1. Crea un API token: https://pypi.org/manage/account/token/
- Scope: “Entire account” per la prima pubblicazione
- Dopo la prima pubblicazione, crea un token con scope limitato al progetto

### Step 2: Configura credenziali

```bash
# Opzione A: file di configurazione
cat > ~/.pypirc << 'EOF'
[pypi]
username = __token__
password = pypi-YOUR_API_TOKEN_HERE
EOF
chmod 600 ~/.pypirc

# Opzione B: variabili d'ambiente (preferito per CI)
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_API_TOKEN_HERE
```

### Step 3: Testa su TestPyPI PRIMA

```bash
# Build
python -m build

# Upload su TestPyPI
twine upload --repository testpypi dist/*

# Testa l'installazione da TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dfseo

# Verifica
dfseo --help
dfseo --version
```

### Step 4: Pubblica su PyPI (produzione)

```bash
# SOLO dopo aver verificato su TestPyPI
twine upload dist/*
```

### Step 5: Verifica

```bash
# Aspetta 1-2 minuti, poi:
pip install dfseo
dfseo --help

# Controlla la pagina PyPI
# https://pypi.org/project/dfseo/
```

-----

## Post-Pubblicazione

### Aggiorna GitHub

```bash
# Tag la release
git tag v1.0.0
git push origin v1.0.0
```

### Crea GitHub Release

1. Vai su GitHub → Releases → “Create a new release”
1. Tag: `v1.0.0`
1. Title: `v1.0.0 — First public release`
1. Description: copia le feature principali dal README
1. Attach: i file `.whl` e `.tar.gz` dalla cartella `dist/`

### Setup GitHub Actions per release automatiche (opzionale ma consigliato)

Crea `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

permissions:
  id-token: write

jobs:
  publish:
    runs-on: ubuntu-latest
    environment: pypi
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install build
      - run: python -m build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

Questo usa Trusted Publishers (niente token da gestire). Configura su PyPI:

1. Vai su https://pypi.org/manage/project/dfseo/settings/publishing/
1. Aggiungi GitHub come trusted publisher
1. Repository: `TUO_USERNAME/dfseo-cli`
1. Workflow: `publish.yml`
1. Environment: `pypi`

-----

## Troubleshooting Comuni

### “Package name already exists”

→ Usa `dfseo-cli` come nome pacchetto, mantieni `dfseo` come entry point CLI

### “Invalid metadata”

→ Verifica che README.md sia Markdown valido con `twine check dist/*`

### “dfseo: command not found” dopo pip install

→ Verifica che `[project.scripts]` punti al percorso corretto del Typer app
→ Verifica che `~/.local/bin` sia nel PATH

### Import errors dopo installazione

→ Verifica `[tool.hatch.build.targets.wheel] packages = ["src/dfseo"]`
→ Verifica che tutti i `__init__.py` esistano nelle sotto-cartelle

-----

## Sequenza comandi rapida (copia-incolla)

```bash
# 1. Verifica nome disponibile
pip index versions dfseo

# 2. Build
pip install build twine
python -m build
twine check dist/*

# 3. Test su TestPyPI
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dfseo
dfseo --help

# 4. Pubblica su PyPI
twine upload dist/*

# 5. Verifica
pip install dfseo
dfseo --help

# 6. Tag
git tag v1.0.0
git push origin v1.0.0
```
