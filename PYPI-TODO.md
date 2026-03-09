# PyPI Publishing — Checklist manuale

> Cose che richiedono le tue credenziali, il tuo account o decisioni personali.

## 1. Email autore in pyproject.toml

- [ ] Sostituisci `riccardo@example.com` con la tua email reale in `pyproject.toml` (riga `authors`)

## 2. Verifica nome pacchetto su PyPI

```bash
pip index versions dfseo
```

- [ ] Se il nome `dfseo` è già preso, rinomina `name = "dfseo-cli"` in `pyproject.toml` (l'entry point CLI resta `dfseo`)

## 3. Account PyPI

- [ ] Crea account su https://pypi.org/account/register/ (se non ce l'hai)
- [ ] Abilita 2FA (obbligatorio)
- [ ] Crea un API token: https://pypi.org/manage/account/token/ (scope: "Entire account" per la prima volta)

## 4. Configura credenziali locali

```bash
# Opzione A: file
cat > ~/.pypirc << 'EOF'
[pypi]
username = __token__
password = pypi-YOUR_API_TOKEN_HERE
EOF
chmod 600 ~/.pypirc

# Opzione B: variabili d'ambiente
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_API_TOKEN_HERE
```

- [ ] Credenziali configurate

## 5. Build e verifica locale

```bash
pip install build twine
python -m build
twine check dist/*
```

- [ ] `twine check` dice "PASSED" per tutti i file

## 6. Test installazione pulita

```bash
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

- [ ] Tutti i comandi funzionano correttamente

## 7. Pubblica su TestPyPI

```bash
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dfseo
dfseo --help
```

- [ ] Installazione da TestPyPI funziona

## 8. Pubblica su PyPI (produzione)

```bash
twine upload dist/*
```

- [ ] `pip install dfseo` funziona

## 9. Tag e Release GitHub

```bash
git tag v1.0.0
git push origin v1.0.0
```

- [ ] Tag pushato
- [ ] GitHub Release creata (GitHub → Releases → "Create a new release", tag `v1.0.0`)

## 10. Configura Trusted Publishers (per release automatiche future)

La GitHub Action `.github/workflows/publish.yml` è già nel repo. Per attivarla:

1. Vai su https://pypi.org/manage/project/dfseo/settings/publishing/
2. Aggiungi GitHub come trusted publisher:
   - Repository: `ricca91/dfseo-cli`
   - Workflow: `publish.yml`
   - Environment: `pypi`

- [ ] Trusted publisher configurato su PyPI
- [ ] Crea environment `pypi` su GitHub (Settings → Environments → New environment)
