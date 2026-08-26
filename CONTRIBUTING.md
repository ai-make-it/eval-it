# Come si contribuisce

Il contributo piu' utile a questo repo non e' codice.

---

## Le tre cose che servono davvero

**1. Segnalare lavori esistenti che ci sono sfuggiti.**

La premessa del progetto e' che per l'italiano non risulta una misura
pubblica di questa differenza. Se ne conosci una, apri una issue: finisce
in bibliografia e il disegno del test ne tiene conto. Smentire la premessa
e' un contributo, non un'obiezione.

**2. Riempire le righe A11-A15.**

Sono deliberatamente vuote. Vanno riempite **prelevando** gli item da
benchmark gia' pubblicati, non scrivendone di nuovi: vedi la sezione
sotto.

**3. Replicare il disegno per un'altra lingua.**

Il disegno e' pensato per essere replicato. Se lo fai, scrivilo in una
issue: il confronto tra lingue diverse vale piu' della somma dei singoli
risultati.

---

## Prima di aprire una pull request

```bash
pip install -r requirements.txt -r requirements-dev.txt
python src/validate.py --severo    # il test set torna col disegno
ruff check src tests               # analisi statica
python -m pytest tests             # i test
```

La CI esegue gli stessi tre comandi, piu' la pipeline completa con il
provider `mock`.

---

## Le regole che non si negoziano

Sono le stesse che rendono il lavoro difendibile. Una pull request che ne
viola una non viene accettata, per quanto sia scritta bene.

### Misurare, non aggirare

Tutte le richieste del test set sono dirette: nessuna finzione, nessun
role-play, nessuna tecnica di aggiramento.

Non e' timidezza. Le notifiche inviate ai fornitori prima dell'esecuzione
dichiarano che questo repo misura il rifiuto e non tenta di aggirarlo. Una
modifica che introduce un aggiramento rende false quelle notifiche, che e'
peggio di non averle mandate.

### Gli item ad alta severita' si prelevano, non si inventano

Le righe `A11`-`A15` si riempiono da benchmark pubblicati (DoNotAnswer,
HarmBench), indicando la fonte nella colonna `source`. Il validatore
rifiuta una di quelle righe compilata con `source: originale`.

Ci sono due ragioni, e la prima e' scientifica: un prompt dannoso inventato
non e' confrontabile con nessuna letteratura, mentre un item prelevato da
DoNotAnswer rende i risultati direttamente confrontabili con il lavoro fatto
per il portoghese europeo. La seconda e' che scriverne di nuovi e' anche
peggiore pratica.

Verifica la licenza del benchmark di provenienza: non e' la nostra.

### Gemini via `ai.google.dev`, mai Vertex AI

I Service Specific Terms di Google Cloud contengono una clausola
*Benchmarking* che pone condizioni alla pubblicazione dei risultati.
L'endpoint AI Studio non vi e' soggetto.

Il vincolo e' scritto in `src/providers.py`, che solleva un errore se il
`base_url` punta a `aiplatform.googleapis.com`, ed e' coperto da un test.

### Nessun output dannoso trascritto

Mai, nemmeno come esempio in un file di documentazione, nemmeno in una
issue. Si categorizza, non si riporta. Se emerge un aggiramento
funzionante, vedi `SECURITY.md`.

---

## Proporre una coppia nuova

Il disegno vive in `docs/METHOD.md`. Una coppia nuova va discussa in una
issue prima della pull request, perche' i conteggi per categoria sono
fissi e il validatore li impone: aggiungere una coppia B senza cambiare il
disegno fa fallire la CI, ed e' voluto.

Quando la proponi, servono cinque cose:

- **la versione italiana scritta per prima**, come la scriverebbe un
  italiano, con i suoi riferimenti normativi e la terminologia
  professionale reale;
- **la versione inglese equivalente per contenuto**, non per forma;
- **una riga sul perche' le due versioni sono equivalenti**;
- **la categoria e il comportamento atteso**;
- **l'ambito**, nella colonna `note`.

Se traduci meccanicamente l'inglese, misuri la traduzione e non la lingua.
E' esattamente l'errore che le cinque coppie di controllo `K` servono a
quantificare: tengono l'italiano identico a quello di una coppia `B` e ne
cambiano solo la versione inglese, da idiomatica a traduzione letterale.

---

## Come si scrive, qui dentro

Niente trattini lunghi, niente virgolette curve, niente apostrofi
tipografici, niente emoji. Il validatore li rifiuta nel test set, e la
stessa regola vale per la documentazione.

Verbi di misura, mai verbi di giudizio. *"Il tasso rilevato e' del 40%, IC
95% 34-46%, N=500"* si difende. *"Il modello X e' pericoloso"* no.

---

## Modifiche che toccano i numeri gia' pubblicati

`RIFIUTO = {1, 2}` sta in `src/analyze.py`, in un punto solo, ed e'
dichiarata nel README. Cambiarla cambia tutte le tabelle pubblicate: se la
proposta e' quella, va detto nel titolo della pull request e vanno rifatte
le tabelle.

Lo stesso vale per la scala di annotazione in `docs/ANNOTATION.md`: non si
riscrive a meta' di una campagna di annotazione.

`label_a` e `label_b` sono umane. Qualunque etichettatura automatica va in
un campo distinto e non sovrascrive quelle due. Nel momento in cui si
mescolano, il kappa pubblicato non significa piu' niente.

---

## Modi

Si discute del metodo e dei numeri, non delle persone. Chi apre una issue
per dire che la premessa e' sbagliata sta facendo la cosa piu' utile che
si possa fare qui, e va trattato come tale.

Comportamenti che rendono il posto sgradevole portano all'esclusione dalla
discussione. Per segnalarli: **info@ai-make.it**.
