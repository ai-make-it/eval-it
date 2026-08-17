# Dizionario ragionato dell'AI in italiano

**Sessanta voci del vocabolario tecnico dell'intelligenza artificiale, scritte in italiano da chi lavora con questi sistemi, non tradotte da un glossario inglese.**

Dati aperti, CC BY 4.0. Si contribuisce con una pull request.

*Sixty entries of the technical AI vocabulary, written in Italian rather than translated from English glossaries. Open data, CC BY 4.0. English summary at the bottom.*

---

## Perché esiste

Chi in Italia deve decidere se e come usare questi sistemi si trova davanti un vocabolario che esiste solo in inglese. Non è un problema di traduzione: è che i termini arrivano senza il contesto operativo, e chi li incontra impara la parola senza imparare cosa ci si sbaglia intorno.

Un glossario tradotto dice cosa significa *drift*. Non dice che la ragione per cui i sistemi in produzione peggiorano senza che nessuno li abbia toccati è quasi sempre quella, e che il piano di misura va scritto prima, non dopo.

Questo dizionario prova a dire la seconda cosa.

---

## La disciplina dei quattro campi

Ogni voce ha esattamente quattro campi, sempre gli stessi:

| Campo | Cosa contiene |
|---|---|
| **Cos'è** | La definizione, in due frasi. Tre al massimo |
| **Perché conta** | La conseguenza pratica. Cosa cambia nel lavoro di chi legge |
| **L'errore comune** | Cosa si sbaglia intorno a questo termine |
| **Inglese** | Il termine o i termini inglesi corrispondenti |

**Il terzo campo è il controllo di qualità.** Se su una voce non si riesce a scrivere l'errore comune, la voce non è pronta: significa che chi la scrive conosce la definizione ma non ha visto il termine usato male. Un dizionario di definizioni corrette lo si trova già tradotto ovunque.

Il vincolo è deliberatamente stretto. Un dizionario che si concede eccezioni al formato diventa un'enciclopedia in due anni, e un'enciclopedia in italiano su questo argomento è un lavoro che nessuna persona sola porta a termine.

---

## Struttura

```
voci/                  la fonte: un file YAML per voce
dist/                  generato, non si modifica a mano
  dizionario.json      tutte le voci, per chi programma
  dizionario.csv       tutte le voci, per un foglio di calcolo
  dizionario.md        il dizionario intero, in ordine alfabetico
  settimana-N.md       i sei gruppi di pubblicazione
  indice-inglese.md    dall'inglese all'italiano
sito/                  generato, il sito statico da pubblicare
  index.html           l'indice, con la ricerca
  voce/<slug>/         una pagina per voce
  gruppo/<n>-<nome>/   una pagina per gruppo
  inglese/             dall'inglese all'italiano
  dati/                json, csv, markdown, scaricabili
src/validate.py        controlla il dataset, gira in CI
src/build.py           rigenera dist/
src/sito.py            rigenera sito/
src/collegamenti.py    controlla il sito generato, gira in CI
deploy.sh              carica sito/ sull'hosting, via SSH
docs/SCHEMA.md         i campi, uno per uno
CONTRIBUTING.md        come si propone una voce
```

**La fonte è `voci/`.** Un file per voce, così due proposte diverse non entrano mai in conflitto sulla stessa riga. `dist/` e `sito/` sono rigenerabili: una correzione fatta lì sparisce alla prima build.

```bash
pip install pyyaml
python src/validate.py       # controlla il dataset
python src/build.py          # rigenera dist/
python src/sito.py           # rigenera sito/
python src/collegamenti.py   # controlla il sito generato
```

---

## Il sito

Il dizionario si pubblica su **[ai-make.it/dizionario/](https://ai-make.it/dizionario/)**, come sito statico in una sottocartella del dominio.

Statico, e non una sezione del CMS, per la stessa ragione per cui la fonte è `voci/`: le pagine sono un prodotto del dataset, e un contenuto ricopiato dentro un CMS si stacca dal sorgente alla prima correzione. Qui una voce si corregge nel suo YAML, si rigenera, si carica.

`src/sito.py` produce 69 pagine: l'indice, le 60 voci, i sei gruppi, l'indice inglese, la pagina dei dati. Ogni voce ha un indirizzo stabile, `/dizionario/voce/<slug>/`, che coincide con lo slug del dataset: gli indirizzi non si rompono finché non si rompe il dataset, e lo slug non si cambia dopo la pubblicazione.

Il sito non chiama nessuna CDN e non carica nessuna libreria. La ricerca filtra il documento leggendo chiavi già presenti nel markup, quindi funziona anche se non parte niente altro. Ogni pagina porta canonical, Open Graph e JSON-LD (`DefinedTermSet` sull'indice, `DefinedTerm` su ogni voce, `BreadcrumbList` sul percorso), che è il modo in cui una definizione viene ripresa da un motore di ricerca invece che riscritta.

L'indirizzo di base non è cablato nel codice:

```bash
DIZIONARIO_BASE=https://esempio.it/glossario python src/sito.py
```

### Pubblicazione

```bash
./deploy.sh              # prova a vuoto: dice cosa cambierebbe
./deploy.sh --conferma   # carica
```

La prova a vuoto è il comportamento predefinito perché `rsync` gira con `--delete`, e su un hosting condiviso un percorso remoto sbagliato cancella un sito. Lo script si rifiuta di partire se la destinazione è la radice del dominio invece di una sottocartella dedicata.

Le credenziali stanno in `deploy.conf`, che non entra in git: si parte da `deploy.conf.esempio`. Servono l'utente SSH e una chiave, che si importa in SiteGround da Site Tools, Devs, SSH Keys Manager.

Chi non ha una macchina con `ssh` e `rsync` a portata usa il workflow **dizionario, pubblica**, da Actions: gira sullo stesso `deploy.sh` su un runner GitHub, e parte anche lui in prova a vuoto salvo che si scelga `carica`. Vuole due segreti, `SG_CHIAVE` (la chiave privata) e `SG_UTENTE`. Il trigger è solo manuale, di proposito: su un repo pubblico un trigger su pull request esporrebbe i segreti a una pull request da un fork.

Due cose vanno fatte a mano, una volta sola, perché stanno fuori da questa cartella: dichiarare `https://ai-make.it/dizionario/sitemap.xml` nel `robots.txt` alla radice del dominio, e inviare la sitemap in Search Console. Un `robots.txt` dentro una sottocartella non lo legge nessuno, e per questo non lo generiamo.

---

## Le regole sono nel validatore, non nel README

`src/validate.py` è il posto dove vive la disciplina editoriale, e gira su ogni pull request. Blocca i campi mancanti, gli slug che non corrispondono al termine, i numeri duplicati, i rimandi rotti, e la punteggiatura fuori standard.

Avvisa, senza bloccare, quando una definizione supera le tre frasi, quando una voce apre con un giro di parole invece di entrare nel merito, e quando l'errore comune riusa troppo lessico della definizione, che è il modo in cui una voce smette di dire qualcosa e comincia a ripetersi.

Quest'ultimo controllo è una spia statistica, non un giudizio: misura la sovrapposizione delle parole di contenuto tra i due campi. Sulle sessanta voci iniziali il massimo osservato è 0,13; la soglia è a 0,25.

---

## I sei gruppi

Le voci sono organizzate in sei gruppi, pensati per essere letti in qualsiasi ordine ma pubblicati in questa sequenza.

| | Gruppo | Cosa copre |
|---|---|---|
| 1 | Le fondamenta | I termini che servono per leggere tutti gli altri |
| 2 | Come si usa | Il vocabolario di chi lavora con i modelli |
| 3 | Architettura e agenti | Il vocabolario di chi costruisce |
| 4 | Come sbaglia | I modi in cui questi sistemi falliscono |
| 5 | Come si verifica | Il vocabolario della valutazione |
| 6 | Sicurezza | Il vocabolario della sicurezza tecnica |

Dieci voci per gruppo.

---

## Cosa questo dizionario non è

**Non è una traduzione.** Diversi termini restano in inglese perché in italiano non si dicono, e dove è così è scritto. *Token*, *embedding*, *fine-tuning* e *reward hacking* si usano così: inventare un calco italiano che nessuno userà rende il dizionario inservibile proprio a chi ne ha bisogno.

**Non è neutrale sull'uso.** Il campo *errore comune* contiene giudizi su cosa si sbaglia. Sono discutibili, ed è per questo che si aprono issue.

**Non è completo.** Sessanta voci coprono il vocabolario che serve per leggere una documentazione tecnica e per capire una discussione sulla valutazione. Non coprono la visione artificiale, il parlato, la robotica, né la parte normativa.

---

## Come contribuire

Le voci nuove e le correzioni si propongono con una pull request. `CONTRIBUTING.md` spiega il formato; `docs/SCHEMA.md` descrive i campi.

Il criterio con cui si accetta una voce nuova è uno solo: **si riesce a scrivere l'errore comune?** Se sì, la voce ha qualcosa da dire. Se no, è una definizione, e le definizioni ci sono già.

---

## Il progetto collegato, nella cartella accanto

**[eval-it](../)** misura quello che qui viene definito: un modello rifiuta in italiano una richiesta che accetta in inglese, e di quanto? Prompt appaiati, annotazione cieca, intervalli di confidenza.

Le voci *rifiuto eccessivo*, *accordo tra annotatori*, *set di prova* e *soglia di accettazione* descrivono esattamente gli oggetti che quel repo maneggia.

---

## Licenza

**Testo e dati: CC BY 4.0.** Si può riusare, anche commercialmente, citando la fonte.

**Codice (`src/`): MIT.**

Se lo usi, citalo. Se lo estendi in un'altra lingua, scrivilo: la struttura a quattro campi è pensata per essere riusata.

---
---

## English summary

**A reasoned dictionary of AI terminology in Italian.** Sixty entries covering the vocabulary needed to read technical documentation and follow a discussion about model evaluation.

Every entry has exactly four fields: what it is (two sentences), why it matters in practice, **the common mistake**, and the English term. The third field is the quality gate: if you cannot write the common mistake, the entry is not ready. It is what separates this from a translated glossary.

The source of truth is `voci/`, one YAML file per entry, so contributions never conflict on the same line. `dist/` is generated. `src/validate.py` enforces the editorial discipline in CI: required fields, slug consistency, unique ids, resolvable cross-references, and a lexical-overlap check that flags entries whose "common mistake" is merely restating the definition.

Terms that Italian practitioners genuinely use in English stay in English. Inventing Italian calques nobody uses would make the dictionary useless to the people who need it.

Text and data CC BY 4.0, code MIT. Designed to be reused for other languages.
