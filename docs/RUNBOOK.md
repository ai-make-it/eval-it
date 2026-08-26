# Come si esegue una campagna

Il metodo sta in `docs/METHOD.md`. Qui c'e' la sequenza operativa: cosa
si fa, in che ordine, e cosa impedisce di andare avanti.

L'ordine non e' un suggerimento. Tre passi non si possono recuperare dopo:
le notifiche ai fornitori, gli snapshot datati, e la doppia annotazione.

---

## Prima di spendere un euro

### 1. Il test set deve essere chiuso

```bash
python src/validate.py --severo
```

Chiuso vuol dire anche le righe `A11`-`A15`, che sono vuote per
costruzione e vanno riempite prelevando gli item da benchmark pubblicati.
Finche' sono vuote, `run.py` le salta e lo dichiara: si puo' eseguire, ma
la categoria A resta a dieci coppie invece di quindici, e va scritto in
pubblicazione.

**Perche' prima di tutto il resto.** Le notifiche ai fornitori dichiarano
cosa si misura. Se il test set cambia dopo, la notifica descrive un'altra
cosa.

### 2. Notifica preventiva ai fornitori

Cinque righe a ciascun fornitore i cui modelli entrano nella campagna:
chi sei, cosa misuri, su quali modelli, in che date, che pubblicherai
metodo e dati.

Non serve una risposta, serve **la prova dell'invio**: le Usage Policy di
alcuni fornitori contengono clausole su *unsolicited safety testing* e
*prior authorization* che una notifica disattiva. Conserva le copie
inviate insieme al resto del materiale della campagna.

### 3. Account e chiavi

- **Account dedicato**, separato da qualsiasi cosa operativa. Se viene
  sospeso non blocca altro.
- **Tier a pagamento, sempre.** Su alcuni fornitori i prompt del tier
  gratuito alimentano l'addestramento, e il benchmark si contamina da
  solo.
- Chiavi con la portata minima che il fornitore permette.
- Chiavi solo in variabili d'ambiente. Vedi `SECURITY.md`.

### 4. Gli snapshot datati

```bash
cp config.example.yaml config.yaml
```

Poi, per ogni modello, **interroga l'endpoint dei modelli del fornitore e
scrivi in `config.yaml` l'identificativo datato che ti restituisce**.

`gpt-5` non e' un modello, e' una famiglia. I modelli cambiano dietro lo
stesso nome commerciale, e senza identificativo datato il risultato
diventa incontestabile solo perche' diventa irripetibile. E' il primo
punto su cui un fornitore puo' rispondere che stai misurando un'altra
cosa.

`config.yaml` non entra in git.

### 5. Il conto a vuoto

```bash
python src/run.py --config config.yaml --dry-run
```

Stampa quante chiamate farebbe. Confrontalo con il volume atteso in
`docs/METHOD.md` prima di lanciare.

Il controllo delle chiavi gira anche in `--dry-run`: se ne manca una, si
ferma qui e non dopo trecento chiamate.

---

## L'esecuzione

```bash
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GOOGLE_API_KEY=...

python src/run.py --config config.yaml
```

**E' ripartibile.** Se si interrompe, rilancia lo stesso comando: rilegge
il file dei risultati e riprende da dove si era fermato. Gli errori
transitori (429, 5xx, timeout) sono gia' riprovati dentro, con attesa
crescente.

**Se al termine restano errori**, rilancia: colma i buchi senza rifare le
chiamate riuscite. Sopra il 5% di errori, `analyze.py` avvisa e chiede di
rilanciare prima di analizzare.

**Accanto ai risultati compare un `.meta.json`.** Contiene l'impronta
SHA-256 del test set, i parametri e i modelli richiesti. Serve a poter
dire, mesi dopo, contro quale versione esatta del test set sono stati
prodotti quei numeri. Conservalo insieme al JSONL: senza, i risultati non
sono legati a niente.

**Le chiamate fermate dal fornitore per il contenuto** non sono errori.
Vengono registrate con `blocked: true` e contate a parte: sono il rifiuto
piu' netto che esista, ed escluderle abbasserebbe i tassi proprio sui
modelli che bloccano di piu'.

---

## L'annotazione

```bash
python src/annotate.py export results/run-<data>.jsonl --out annotazione.csv
```

Chi annota **legge prima `docs/ANNOTATION.md` per intero**, poi guarda il
primo output. Non il contrario: se si definiscono i criteri strada
facendo, la stessa persona classifica diversamente a due giorni di
distanza.

L'export non mostra quale modello ha risposto e mescola le righe. La
lingua si vede, perche' la richiesta va letta: e' un limite del disegno,
ed e' dichiarato.

```bash
python src/annotate.py import annotazione.csv \
  --into results/run-<data>.jsonl --annotator a
```

### La doppia annotazione non e' opzionale

```bash
python src/annotate.py export results/run-<data>.jsonl \
  --sample 0.2 --seed 7 --out doppia.csv
python src/annotate.py import doppia.csv \
  --into results/run-<data>.jsonl --annotator b
```

Un secondo annotatore rifa' il 20% delle righe, indipendentemente e senza
vedere le etichette del primo.

E' mezza giornata e determina se tutto il resto ha senso. Se due persone
competenti concordano solo nel 70% dei casi, nessuna differenza inferiore
al 30% fra le lingue e' reale. **E' l'unico passo che non si recupera
dopo**: rifarlo a valle, sapendo cosa si spera di trovare, non e' la
stessa cosa.

---

## L'analisi

```bash
python src/analyze.py results/run-<data>.jsonl --csv tabella.csv
```

Tre numeri vanno guardati prima della tabella.

**Il kappa binario.** Sotto 0,6 lo strumento avvisa. Se succede, la cosa
da fare non e' pubblicare comunque: e' tornare su `docs/ANNOTATION.md`,
capire su quali confini gli annotatori sono in disaccordo, riscrivere le
definizioni e riannotare.

**L'incoerenza tra ripetizioni.** Quanta parte delle terne (coppia,
lingua, modello) non da' sempre lo stesso esito. Temperatura zero riduce
la variabilita', non la elimina. Un valore alto e' un limite da
dichiarare.

**La quota di errori tecnici.** Sopra il 5%, rilancia `run.py`.

Poi confronta le due letture delle chiamate bloccate:

```bash
python src/analyze.py results/run-<data>.jsonl --bloccati escludi
```

Se i due conti danno tabelle diverse, va detto in pubblicazione quale si
sta riportando e quanto cambia l'altra.

---

## Il controllo sulle app

Dopo l'analisi preliminare, non prima: le dieci coppie da rifare a mano
nelle app consumer si scelgono guardando dove l'API ha dato il delta piu'
marcato.

Sessioni nuove, nessuna cronologia. Va dichiarato che il controllo e'
manuale, non cieco, e su campione piccolo: e' un'indicazione, non una
misura.

---

## Prima di pubblicare

**Diritto di replica.** I risultati ai fornitori 7-14 giorni prima, con
l'offerta di pubblicare la loro risposta accanto ai dati. Non lo impone
nessuna norma. E' la cautela che converte un potenziale conflitto in una
correzione tecnica.

**Accanto a ogni numero**: N, intervallo di confidenza, accordo tra
annotatori, data di esecuzione, identificativo datato del modello.

**Verbi di misura, mai verbi di giudizio.** Il rischio non e' mai nella
tabella, e' nel titolo.

**Nessuna estrapolazione.** Su questo test set, su questi prompt, in
queste date.

**Nessun output dannoso trascritto.** Si categorizza, non si riporta.

---

## Chiusura

- Ruota le chiavi usate nella campagna.
- Archivia insieme: il JSONL, il suo `.meta.json`, i CSV di annotazione,
  le copie delle notifiche inviate, la tabella.
- Nessuno di questi file entra nel repo: contengono output dei modelli.
  Quello che si pubblica e' la tabella, insieme agli output grezzi
  ripuliti, se e quando si decide di pubblicarli.

---

## Sull'esecuzione in cloud

L'intera campagna e' qualche migliaio di chiamate HTTP: gira su un
portatile in qualche ora, e finche' e' cosi' un'infrastruttura in piu' e'
solo superficie in piu' da proteggere.

Se e quando servira' (piu' modelli, ripetizioni piu' numerose, esecuzioni
periodiche), la direzione decisa e' **Google Cloud**: un Cloud Run Job che
esegue il container, le chiavi in Secret Manager, i risultati su un bucket
in regione europea. Vale la pena farlo quando il test set e' chiuso, non
prima: un'infrastruttura costruita attorno a un test set che cambia ancora
va rifatta.

Resta il vincolo di sempre, che riguarda l'endpoint dei modelli e non
l'infrastruttura: **Gemini via `ai.google.dev`, mai Vertex AI**. Far
girare il container su Google Cloud non lo intacca, perche' i modelli si
continuano a chiamare da AI Studio.
