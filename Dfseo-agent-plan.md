# SEO Agent — Business Plan

> Da dfseo-cli a “Autonomous SEO Agent as a Service”
> Modello: Ibrido (agency first → productize)
> Target: Startup e indie maker globali
> Timeline: Full time, 6 mesi al primo revenue milestone

-----

## La Vision in Una Frase

**Un agente SEO autonomo che costa meno di un freelancer, lavora 24/7, e produce risultati che un indie maker può agire direttamente.**

Non un altro tool SEO. Non un altro dashboard. Un collega digitale che fa il lavoro e ti manda un report con cosa fare.

-----

## Perché Funziona Adesso

Tre trend si stanno incrociando in questo momento:

1. **Le API SEO sono diventate commodity.** DataForSEO, SEMrush API, Ahrefs API — i dati costano centesimi. Il valore non è più nell’accesso ai dati ma nel sapere cosa farne.
1. **Gli LLM sanno ragionare sui dati.** Un Claude o GPT-4 può guardare un report keyword e dire “questa keyword ha volume alto, difficulty bassa, intent commerciale — scrivi un articolo su questo topic.” Un anno fa non poteva.
1. **Indie maker e startup non hanno budget per un SEO specialist** (~$3-5K/mese) ma hanno bisogno di SEO per crescere organicamente. C’è un gap enorme tra “faccio tutto da solo con Ubersuggest” e “assumo un’agenzia”.

Tu ti infili esattamente in quel gap.

-----

## Il Personal System: “The SEO Autopilot”

Il sistema ha un nome. Lo chiameremo **SEO Autopilot** (o un nome migliore che trovi tu — deve essere memorabile e autoesplicativo).

**Cosa fa:**

- Ogni settimana analizza il tuo sito, i competitor, e il mercato keyword
- Produce un report con azioni concrete, ordinate per impatto
- Monitora i ranking e avvisa quando qualcosa cambia
- Trova opportunità di link building automaticamente
- Genera brief per content writer basati su keyword gap reali

**Cosa NON fa (per ora):**

- Non scrive contenuti (suggerisce cosa scrivere)
- Non fa outreach automatico (trova i target, tu mandi l’email)
- Non modifica il sito (dice cosa fixare, tu o il dev lo fate)

Questo è cruciale: l’agente è un **analyst e strategist**, non un executor. L’umano approva e agisce. Questo riduce il rischio, costruisce fiducia, e rende il servizio vendibile.

-----

## Fase 1: Agency Mode (Mesi 1-3)

### Obiettivo: 5-10 clienti paying, €200-400/mese ciascuno

Non vendi un prodotto. Vendi un servizio che dietro le quinte è un agente. Il cliente riceve un report settimanale fatto bene e azioni concrete. Non sa (e non gli importa) se lo fa un umano o un bot.

### Come Funziona

**Il workflow settimanale per ogni cliente:**

```
1. L'agente (tu + dfseo-cli + LLM) analizza:
   - Ranking attuali per keyword target
   - Nuove opportunità keyword (volume/difficulty)
   - Salute tecnica del sito (audit on-page)
   - Profilo backlink (nuovi, persi, opportunità)
   - Cosa fanno i competitor

2. L'agente produce un report Markdown/PDF con:
   - Executive summary (3 righe: cosa va bene, cosa va male, cosa fare)
   - Keyword opportunities (tabella con volume, KD, intent)
   - Technical issues (errori trovati, priorità)
   - Backlink opportunities (link gap vs competitor)
   - Content suggestions (topic, keyword target, search intent)
   - Week-over-week ranking changes

3. Tu rivedi il report (5-10 min), aggiungi note personali, e lo mandi al cliente

4. Il cliente agisce sulle raccomandazioni (o ti chiede di farlo per extra fee)
```

### Stack Tecnico Fase 1

```
dfseo-cli          → dati SEO (già pronto)
Python script      → orchestrazione workflow (cron settimanale)
Claude API         → analisi dati e generazione report
Markdown → PDF     → report professionale
Email / Notion     → delivery al cliente
Stripe             → pagamento ricorrente
```

Non serve niente di più. Niente dashboard, niente webapp, niente login. Un cron job, un report, un’email.

### Come Trovare i Primi 5 Clienti

**Target: indie maker con un prodotto live e zero SEO strategy.**

Dove trovarli:

- **Indie Hackers** — gente che posta “how do I get organic traffic?”
- **Twitter/X** — founder che lamentano “SEO is hard” o “should I invest in SEO?”
- **Product Hunt** — prodotti lanciati di recente senza SEO evidente
- **Reddit r/SaaS, r/startups, r/SEO** — gente che chiede consigli SEO

**L’approccio di vendita:**

Non mandi un DM freddo. Fai un **free audit non richiesto**.

```
1. Trova un indie maker con un sito live
2. Esegui:
   dfseo site audit "loro-sito.com" --max-pages 50 --wait
   dfseo keywords for-site "loro-sito.com" --location "United States" --min-volume 50
   dfseo backlinks summary "loro-sito.com"
3. Scrivi un mini-report (10 righe) con 3 quick win
4. Manda come reply/DM: "Hey, ho fatto un audit veloce del tuo sito. Ho trovato 3 cose che puoi fixare subito per migliorare il ranking. Ecco il report — gratis, nessun obbligo."
5. Se rispondono: "Ti interessa ricevere questo tipo di analisi ogni settimana? €300/mese."
```

Questo funziona perché:

- Dimostri competenza PRIMA di chiedere soldi
- Il report è reale, non un template
- L’effort per te è 5 minuti (dfseo + Claude API)
- Per loro, quel report vale ore di lavoro manuale

### Pricing Fase 1

|Piano      |Prezzo    |Cosa include                                                                     |
|-----------|----------|---------------------------------------------------------------------------------|
|**Starter**|€200/mese |Report settimanale, 1 sito, keyword monitoring                                   |
|**Growth** |€400/mese |Report settimanale, 1 sito + 3 competitor, content briefs, backlink opportunities|
|**Custom** |€600+/mese|Tutto + implementazione fix tecnici, content strategy call mensile               |

Il costo per te per cliente: ~€10-20/mese in API calls. Margine: 90%+.

### Metriche Fase 1

- **Target revenue:** €1.500-3.000/mese entro mese 3
- **Clienti target:** 5-10
- **Tempo per cliente:** 30 min/settimana (5 min agente + 10 min review + 15 min supporto)
- **Validazione:** almeno 3 clienti che rinnovano al mese 2

-----

## Fase 2: Automazione (Mesi 3-5)

### Obiettivo: Ridurre il tempo per cliente a < 5 min, scalare a 20-30 clienti

Ora che hai 5-10 clienti e capisci cosa vogliono davvero (non quello che pensi tu), automatizzi.

### Cosa Costruire

**1. Agente OpenClaw “SEO Autopilot”**

Un agente con SOUL.md configurato come SEO specialist:

```
L'agente ha:
- SOUL.md → personalità, tono, framework decisionale
- IDENTITY.md → "Sono un SEO analyst per startup e indie maker"
- dfseo skill → accesso a tutti i dati SEO
- Report generation skill → produce report strutturati
- Competitor tracking skill → confronta settimana su settimana
```

L’agente gira su cron (settimanale), per ogni cliente:

1. Legge la configurazione cliente (sito, competitor, keyword target)
1. Esegue la batteria di analisi via dfseo-cli
1. Passa i dati a Claude API per l’analisi
1. Genera il report in Markdown
1. Lo converte in PDF
1. Lo manda via email (o lo posta su Notion/Slack del cliente)

**2. Client configuration file**

```toml
# clients/acme-startup.toml

[client]
name = "Acme Startup"
domain = "acme.io"
email = "founder@acme.io"

[seo]
location = "United States"
language = "English"
target_keywords = ["project management tool", "task manager for teams"]
competitors = ["linear.app", "height.app", "shortcut.com"]

[report]
frequency = "weekly"
format = "pdf"
delivery = "email"
include_content_briefs = true
include_backlink_opportunities = true

[alerts]
ranking_drop_threshold = 5    # alert se una keyword perde 5+ posizioni
new_competitor_alert = true
```

**3. Dashboard semplice (opzionale)**

Se i clienti lo richiedono: una pagina web minimale dove vedono i report passati e lo stato attuale. Next.js + Vercel + Supabase. Ma solo se necessario — molti indie maker preferiscono email/Slack.

### Stack Tecnico Fase 2

```
OpenClaw agent      → orchestrazione autonoma
dfseo-cli           → dati SEO
Claude API          → analisi e report generation
n8n o cron          → scheduling
TOML configs        → configurazione per cliente
Resend / Postmark   → email delivery
Supabase            → storage report (opzionale)
Stripe              → billing ricorrente
```

### Metriche Fase 2

- **Target revenue:** €5.000-8.000/mese
- **Clienti:** 20-30
- **Tempo per cliente:** < 5 min/settimana (solo review outlier)
- **Tempo totale:** ~10 ore/settimana su delivery, resto su growth

-----

## Fase 3: Productize (Mesi 5-8)

### Obiettivo: Self-serve signup, €10K+/mese

Ora che l’agente è stabile e i clienti sono soddisfatti, apri il self-serve.

### Cosa Costruire

**1. Landing page con signup**

Il cliente si registra, inserisce il suo dominio e i competitor, paga, e riceve il primo report in 24 ore. No call, no onboarding manuale.

**2. Onboarding automatico**

```
1. Cliente inserisce dominio + 3 competitor + keyword target
2. Il sistema lancia un audit iniziale (dfseo site audit + keywords + backlinks)
3. Genera un "Baseline Report" con lo stato attuale
4. Configura il cron settimanale
5. Manda il primo report via email
```

**3. Client portal (light)**

Una pagina dove il cliente vede:

- Report corrente e storico
- Ranking trend (grafico settimanale)
- Action items aperti / completati
- Settings (competitor, keyword, frequenza)

### Pricing Fase 3

|Piano     |Prezzo   |Target                                                      |
|----------|---------|------------------------------------------------------------|
|**Solo**  |$99/mese |1 sito, 2 competitor, report settimanale                    |
|**Growth**|$249/mese|1 sito, 5 competitor, content briefs, backlink opportunities|
|**Agency**|$499/mese|3 siti, 10 competitor, white-label reports, API access      |

### Metriche Fase 3

- **Target revenue:** €10.000-15.000/mese
- **Clienti:** 50-100
- **Churn target:** < 10%/mese
- **CAC target:** < €50 (content marketing + free audit funnel)

-----

## Fase 4: Scale (Mesi 8-12)

### Opzioni di crescita

**A. Vertical expansion:** aggiungi più capability all’agente

- Content writing (genera bozze articoli, non solo brief)
- Technical SEO implementation (genera fix code per dev)
- Local SEO (Google Business Profile optimization)
- E-commerce SEO (product page optimization)

**B. Horizontal expansion:** altri tipi di agente

- PPC Agent (gestione campagne Google Ads)
- Content Agent (piano editoriale + bozze)
- Social Media Agent (analisi e scheduling)
- Ogni agente è un add-on al piano base

**C. Platform play:** diventa il luogo dove si comprano agenti marketing

- Marketplace di agenti specializzati
- Altri builder creano agenti sulla tua infrastruttura
- Tu prendi una % per ogni agente venduto
- Questo è il long-game ma richiede traction prima

-----

## Funnel di Acquisizione

### Il Flywheel

```
1. Free audit (dfseo-cli in 5 minuti)
   ↓
2. Share on Twitter/LinkedIn ("Ho fatto un audit di X, ecco cosa ho trovato")
   ↓
3. Commenti e DM ("Puoi farlo anche per me?")
   ↓
4. Free audit per loro → "Vuoi questo ogni settimana?"
   ↓
5. Cliente paying
   ↓
6. Risultati → case study → content → torna al punto 2
```

### Content Strategy

Ogni settimana produci:

- **1 free audit pubblico** di un sito noto (indie maker, startup, open source project) → Twitter thread
- **1 post educativo** su un aspetto SEO (keyword research, link building, on-page) → Twitter
- **1 case study** di un cliente (con permesso) → LinkedIn + blog

Il free audit pubblico è il growth engine. Costa 5 minuti, produce un thread da 10+ tweet, e dimostra competenza a migliaia di persone.

-----

## Financial Model

### Costi Fissi Mensili

|Voce                   |Costo                        |
|-----------------------|-----------------------------|
|DataForSEO API         |~€100 (minimum commitment)   |
|Claude API (Anthropic) |~€50-100 (dipende dal volume)|
|Vercel / hosting       |€0-20                        |
|Email delivery (Resend)|€0-20                        |
|Dominio                |~€1                          |
|**Totale**             |**~€170-240/mese**           |

### Break-even

Con pricing a €200/mese:

- **Break-even: 1-2 clienti** (mese 1)

Con pricing a €300/mese medio:

- **5 clienti = €1.500/mese** (margine ~€1.300)
- **10 clienti = €3.000/mese** (margine ~€2.750)
- **30 clienti = €9.000/mese** (margine ~€8.500)

I costi API scalano sub-linearmente: il costo per cliente scende man mano che aggiungi clienti (batch queries, caching).

-----

## Timeline Mese per Mese

### Mese 1: Foundation + First Clients

**Settimana 1-2:**

- [x] dfseo-cli funzionante (fatto)
- [ ] Pubblica su PyPI
- [ ] Landing page live su Vercel
- [ ] OpenClaw skill pubblicata

**Settimana 3-4:**

- [ ] Crea il workflow di report generation (dfseo + Claude API → PDF)
- [ ] Fai 10 free audit pubblici su Twitter (1 al giorno per 10 giorni)
- [ ] Manda 20 DM personalizzati con mini-audit gratuiti
- [ ] Obiettivo: 2-3 clienti paying

### Mese 2: Refine + Grow

- [ ] Ottimizza il report in base al feedback dei primi clienti
- [ ] Automatizza il più possibile (cron job per data collection)
- [ ] Continua content marketing (2 audit pubblici/settimana)
- [ ] Obiettivo: 5-8 clienti paying, €1.500+/mese

### Mese 3: Automate

- [ ] Costruisci l’agente OpenClaw con SOUL.md configurato
- [ ] Client config files per ogni cliente
- [ ] Email delivery automatico dei report
- [ ] Obiettivo: 10+ clienti, <5 min per cliente, €3.000+/mese

### Mese 4: Stabilize + Document

- [ ] Documenta il processo end-to-end
- [ ] Crea 3 case study dai primi clienti
- [ ] Refine pricing (alza se la domanda c’è)
- [ ] Obiettivo: €4.000-5.000/mese stabile

### Mese 5: Productize

- [ ] Self-serve signup page
- [ ] Onboarding automatico
- [ ] Client portal base
- [ ] Obiettivo: primi clienti self-serve

### Mese 6: Scale

- [ ] Paid acquisition (se unit economics funzionano)
- [ ] Partnership con community indie maker
- [ ] Obiettivo: €8.000-10.000/mese, 30+ clienti

-----

## Rischi e Mitigazioni

|Rischio                            |Probabilità       |Mitigazione                                                                                 |
|-----------------------------------|------------------|--------------------------------------------------------------------------------------------|
|DataForSEO cambia pricing          |Media             |Il CLI è API-agnostic nella struttura; puoi wrappare altre API                              |
|LLM produce analisi sbagliate      |Alta (all’inizio) |Review umana obbligatoria in Fase 1; migliora prompt con dati reali                         |
|Clienti churn alto                 |Media             |Focus su actionable output, non vanity metrics. Se il cliente agisce e vede risultati, resta|
|Competitor lancia servizio simile  |Bassa (per ora)   |First mover advantage + relazione personale + content flywheel                              |
|SEO diventa irrilevante (AI search)|Bassa (short term)|Espandi a “AI visibility” — monitorare presenza in AI Overviews, ChatGPT, Perplexity        |

-----

## Il Nome

Hai bisogno di un nome per il servizio/prodotto. Opzioni:

- **SEO Autopilot** — chiaro, diretto, dice cosa fa
- **RankAgent** — agente + ranking, tech-oriented
- **SEO Copilot** — meno autonomo, più collaborativo
- **GrowthBot** — generico ma catchy
- **Rankly** — corto, .io probabilmente disponibile
- **AutoRank** — automatico + ranking

Il nome deve funzionare sia come servizio agency (“Subscribe to SEO Autopilot”) che come prodotto futuro. Pensaci, non serve decidere adesso.

-----

## Primo Step da Fare Domani

Non tutto questo piano. Solo questo:

1. **Scegli 5 siti di indie maker** che conosci o trovi su Twitter/Indie Hackers
1. **Esegui un audit con dfseo-cli** su ognuno
1. **Scrivi un mini-report** (5 bullet point, 3 quick win)
1. **Posta il primo come thread su Twitter** (“I audited @maker’s site for free. Here’s what I found:”)
1. **Manda gli altri 4 come DM**

Se anche solo 1 su 5 dice “quanto costa ricevere questo ogni settimana?”, hai validato il business.
