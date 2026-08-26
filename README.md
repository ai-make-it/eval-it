# eval-it

[![eval-it](https://github.com/ai-make-it/eval-it/actions/workflows/eval-it.yml/badge.svg)](https://github.com/ai-make-it/eval-it/actions/workflows/eval-it.yml)

**Un modello di intelligenza artificiale non si comporta allo stesso modo in tutte le lingue. Per l'italiano, quanto sia grande la differenza non risulta misurato pubblicamente.**

Questo repo contiene il test set, il codice e il metodo per verificarlo.

*An AI model does not behave the same way in every language. For Italian, we have not found a public measurement of how large that difference is. This repo contains the test set, the code and the method. English summary at the bottom.*

Se trovi un lavoro che ci è sfuggito, apri una issue: finisce in bibliografia e il disegno del test ne tiene conto.

---

## Cosa misura

Ogni voce del test set è una **coppia**: la stessa richiesta in italiano e in inglese.

Il risultato non è *quanto rifiuta il modello X*. È **la differenza tra le due lingue sullo stesso contenuto**. Tutto il resto del disegno serve a rendere quella differenza credibile.

Tre categorie:

| | Cosa | Coppie | Perché |
|---|---|---|---|
| **A** | Richieste che il modello **deve** rifiutare | 15 | Linea di base. Se sbaglia qui, il resto va riletto |
| **B** | Richieste legittime che il modello **non deve** rifiutare | 25 | **È qui che sta il risultato** |
| **C** | Richieste genuinamente ambigue | 10 | Non conta il verdetto, conta la coerenza tra lingue |
| **K** | Controllo per traduzione letterale | 5 | Risponde a *la differenza dipende dalla lingua o da come hai scritto i prompt?* |

**La categoria B è la più grande perché è la più utile.** Un modello che rifiuta tutto è sicurissimo e inservibile. Se in italiano un medico, un avvocato o un insegnante si vede negare più spesso una risposta legittima, il risultato è che **i professionisti italiani ricevono un servizio peggiore a parità di richiesta**. È verificabile, e non accusa nessuno di essere pericoloso.

---

## Come si usa

```bash
git clone https://github.com/ai-make-it/eval-it
cd eval-it
pip install -r requirements.txt
cp config.example.yaml config.yaml

python src/validate.py     # il test set torna con il disegno dichiarato
```

**Provalo senza chiavi e senza spendere**, il provider `mock` esegue l'intera pipeline:

```bash
python src/run.py --config config.yaml --models mock --dry-run
python src/run.py --config config.yaml --models mock
```

**Esecuzione reale.** Apri `config.yaml`, scommenta i modelli, e **sostituisci i segnaposto con gli snapshot datati** presi dall'endpoint dei modelli di ogni fornitore.

```bash
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GOOGLE_API_KEY=...

python src/run.py --config config.yaml
```

L'esecuzione è **ripartibile**: se si interrompe, rilancia lo stesso comando e riprende da dove si era fermata.

**Annotazione.** L'export non mostra quale modello ha risposto e mescola le righe, così le due versioni di una stessa coppia non finiscono mai vicine. La lingua invece si vede, e non può essere altrimenti: la richiesta è scritta in italiano o in inglese, e chi annota deve leggerla per valutare la risposta. È un limite del disegno, dichiarato qui e in [`docs/ANNOTATION.md`](docs/ANNOTATION.md), non un difetto dello strumento.

```bash
python src/annotate.py export results/run-<data>.jsonl --out annotazione.csv
# compila la colonna 'etichetta' con 1-5, vedi docs/ANNOTATION.md
python src/annotate.py import annotazione.csv --into results/run-<data>.jsonl --annotator a

# doppia annotazione sul 20%, con un secondo annotatore
python src/annotate.py export results/run-<data>.jsonl --sample 0.2 --out doppia.csv
python src/annotate.py import doppia.csv --into results/run-<data>.jsonl --annotator b
```

**Analisi.**

```bash
python src/analyze.py results/run-<data>.jsonl --csv tabella.csv
```

---

## L'accordo tra annotatori non è opzionale

È mezza giornata di lavoro e determina se tutto il resto ha senso.

Se due persone competenti classificano lo stesso output allo stesso modo solo nel 70% dei casi, **nessuna differenza inferiore al 30% tra italiano e inglese è reale**. Meglio saperlo prima di pubblicarla.

`analyze.py` calcola l'accordo grezzo e il kappa di Cohen, e **avvisa esplicitamente quando il kappa scende sotto 0,6**. È il primo controllo che un revisore ostile cerca, ed è l'unico che non si può recuperare dopo.

Ne riporta tre versioni, perché misurano cose diverse. Il **kappa pesato** tiene conto del fatto che la scala 1-5 è ordinale: un disaccordo fra 4 e 5 non è un disaccordo fra 1 e 5. Il **kappa binario**, calcolato sulla sola dicotomia rifiuto sì o no, è quello che conta per i numeri pubblicati, perché è la stessa dicotomia che definisce `RIFIUTO`. Due annotatori possono litigare su tutta la scala e concordare perfettamente su quello che finisce in tabella.

---

## L'unità di analisi è la coppia, non la chiamata

Ogni coppia viene interrogata più volte, e nelle due lingue. Le righe che
ne risultano **non sono osservazioni indipendenti**: tre ripetizioni dello
stesso prompt sullo stesso modello dicono quasi la stessa cosa tre volte.

Contarle come tre osservazioni separate restringerebbe gli intervalli di
confidenza di circa la radice del numero di ripetizioni. In pratica: un
delta non significativo comincerebbe a sembrare significativo, e sarebbe
un artefatto del conteggio.

L'intervallo che `analyze.py` riporta è un **bootstrap a grappoli sulle
coppie**: ricampiona le coppie, non le singole chiamate. Rispetta le
ripetizioni e l'appaiamento italiano/inglese, che è l'altra dipendenza del
disegno, visto che la stessa coppia compare in entrambe le lingue.

Lo strumento segnala con `!` le righe calcolate su meno di dieci coppie:
lì il bootstrap è indicativo e non va citato come misura. Riguarda sempre
la categoria K, che di coppie ne ha cinque per costruzione.

**Le chiamate fermate dal fornitore** prima o durante la generazione non
hanno testo da annotare, ma non sono guasti: sono il rifiuto più netto che
esista. Vengono registrate a parte e contate come rifiuto. Escluderle
sposterebbe i tassi verso il basso proprio sui modelli che bloccano di
più. `--bloccati escludi` mostra quanto cambia la tabella con l'altra
scelta, e la differenza va dichiarata.

---

## Le tre regole di questo repo

**Misurare, non aggirare.** Tutte le richieste sono dirette: nessuna finzione, nessun role-play, nessuna tecnica di aggiramento. Si chiede la cosa e si registra se il modello dice no. Questo tiene il lavoro fuori dalle clausole contrattuali che vietano di *aggirare* i guardrail, e produce comunque il dato.

**Gli item ad alta severità si prelevano, non si inventano.** Cinque righe del test set (`A11`-`A15`) sono deliberatamente vuote, con l'indicazione della fonte da cui prenderle. Inventare prompt dannosi nuovi è **peggiore scienza**, perché i risultati non sarebbero confrontabili con nessuna letteratura, oltre che peggiore pratica. La fonte consigliata per tre di esse è **DoNotAnswer**, lo stesso dataset usato da CLARIN-PT-LDB per il portoghese europeo: prelevando da lì, i risultati diventano direttamente confrontabili.

**Gemini via AI Studio, non Vertex AI.** I Service Specific Terms di Google Cloud contengono una clausola *Benchmarking* (§ 7) che pone condizioni alla pubblicazione dei risultati. L'endpoint `ai.google.dev` non vi è soggetto. È scritto nel codice e nella configurazione perché non venga dimenticato.

---

## Prima di eseguire

La sequenza completa, con l'ordine dei passi e i controlli che impediscono di andare avanti, sta in **[`docs/RUNBOOK.md`](docs/RUNBOOK.md)**. In breve:

- **Notifica preventiva a OpenAI e Anthropic.** Cinque righe: chi sei, cosa misuri, su quali modelli, in che date, che pubblicherai metodo e dati. Non serve una risposta, serve la prova dell'invio. Le Usage Policy dei due fornitori contengono clausole su *unsolicited safety testing* e *prior authorization* che una notifica disattiva.
- **Account dedicato**, separato da qualsiasi cosa operativa.
- **Tier a pagamento**, sempre. Sul tier gratuito di alcuni fornitori i prompt alimentano l'addestramento, e il benchmark si contamina da solo.
- **Diritto di replica**: manda i risultati ai fornitori 7-14 giorni prima della pubblicazione, offrendo di pubblicare la loro risposta accanto ai dati. Non lo impone nessuna norma. È la cautela che converte un potenziale conflitto in una correzione tecnica.

---

## Come si scrive quello che esce

**Verbi di misura, mai verbi di giudizio.** *"Il tasso rilevato è del 40%, IC 95% 34-46%, N=500, il 12/09/2026 su `<snapshot>`"* è inattaccabile. *"Il modello X è pericoloso"* no. Il rischio non è mai nella tabella, è nel titolo.

**Nessuna estrapolazione.** *Su questo test set, su questi prompt, in queste date.* Mai *il modello X è meno sicuro in italiano* come affermazione generale. È la differenza tra un risultato e una diagnosi.

**Nessun output dannoso trascritto.** Si categorizza, non si riporta. E se emerge un aggiramento funzionante, non si pubblica: si segnala al fornitore e si pubblica solo il fatto statistico.

---

## Struttura

```
prompts/pairs.csv      il test set: 55 coppie, 50 con testo
src/validate.py        controlla che il test set torni con il disegno
src/run.py             esecuzione, ripartibile
src/providers.py       adattatori, httpx e corpi espliciti, senza SDK
src/annotate.py        export cieco sul modello e rientro delle etichette
src/analyze.py         tabella, intervalli di confidenza, accordo
tests/                 98 test, gli stessi che gira la CI
config.example.yaml    parametri e modelli
docs/METHOD.md         il disegno per esteso
docs/ANNOTATION.md     istruzioni per chi annota
docs/RUNBOOK.md        la sequenza operativa di una campagna
CONTRIBUTING.md        come si contribuisce, e cosa non si accetta
SECURITY.md            chiavi, segnalazioni, cosa non finisce nel repo
```

Gli adattatori sono scritti con `httpx` e corpi di richiesta espliciti, **senza SDK**, di proposito: chi legge deve poter vedere esattamente cosa viene inviato. È il punto di un repo la cui credibilità sta nel metodo.

---

## Limiti dichiarati

- **Nessun system prompt** in questa versione. Quasi tutti i deployment reali ne hanno uno, e cambia il comportamento più di quanto si creda. È la v2.
- **La cornice professionale è dichiarata dentro il prompt** nelle coppie B. È deliberato: misura se il modello riconosce una cornice italiana quanto ne riconosce una anglofona. Un giro senza cornice sarebbe un secondo esperimento.
- **Temperatura 0 non è determinismo.** La variabilità cala, non sparisce. Le tre ripetizioni servono a misurarla, non a eliminarla.
- **Non è una classifica, è una mappa.** Confrontare un modello accademico da 7 miliardi di parametri con i modelli di frontiera non è un confronto alla pari, e va scritto a chiare lettere.
- **L'annotazione non è cieca sulla lingua**, e non può esserlo. Quello che la contiene è altro: chi annota non sa quale modello ha risposto, le righe sono mescolate, la scala misura un comportamento osservabile e non un giudizio, e l'accordo fra due annotatori indipendenti dice quanto margine di interpretazione resta.
- **Cinque coppie su cinquantacinque sono vuote.** Sono gli item ad alta severità, che si prelevano da benchmark pubblicati invece di inventarli. Finché restano vuote, la categoria A ne ha dieci invece di quindici, e va scritto.

---

## Il dizionario, in `dizionario/`

**[Dizionario ragionato dell'AI in italiano](dizionario/)** spiega in italiano i termini che qui vengono misurati: *rifiuto eccessivo*, *accordo tra annotatori*, *benchmark*, *red teaming*. Sessanta voci, dati aperti.

Sono lo stesso lavoro visto da due lati: uno definisce il vocabolario, l'altro lo mette alla prova. Per questo stanno nello stesso repo, in due cartelle che non si toccano: `dizionario/` ha il suo sorgente (`voci/`), la sua build e la sua CI.

Da `voci/` si generano i dati aperti (`dizionario/dist/`) e il sito statico (`dizionario/sito/`) pubblicato su **[ai-make.it/dizionario/](https://ai-make.it/dizionario/)**.

```bash
cd dizionario
python src/validate.py && python src/build.py && python src/sito.py
./deploy.sh              # prova a vuoto, carica con --conferma
```

Dettagli in [`dizionario/README.md`](dizionario/README.md).

---

## Licenza

Codice: **MIT**. Test set, documentazione e risultati: **CC BY 4.0**. Il testo di entrambe è in [`LICENSE`](LICENSE).

Gli item che riempiranno le righe `A11`-`A15` restano sotto la licenza del benchmark da cui vengono prelevati, che non è questa.

Se lo usi, citalo. Se lo usi per un'altra lingua, scrivilo: il disegno è pensato per essere replicabile, ed è esattamente quello che gli autori del dataset giapponese *AnswerCarefully* hanno chiesto quando hanno pubblicato le traduzioni inglesi dei propri item.

---
---

## English summary

**An AI model does not behave the same way in every language.** Safety guardrails that hold in English can fail in another language, or conversely block perfectly legitimate professional requests because the model does not recognise the local framing.

This has been measured for Japanese, Chinese, Korean, Hindi, Portuguese, French, German and Spanish. **For Italian, we have not found a public measurement.**

This repo contains a paired test set (same request in Italian and English), a small multi-provider runner, a blind annotation workflow, and an analysis script that reports refusal rates per language with confidence intervals and inter-annotator agreement.

**Design principles:** measure refusal, never circumvent guardrails. High-severity items are drawn from published benchmarks rather than invented, so results stay comparable with existing literature. Google is accessed via AI Studio, not Vertex AI, whose terms place conditions on publishing benchmark results.

The 25 over-refusal pairs are the core of the set: if Italian doctors, lawyers and teachers are denied legitimate answers more often than their English-speaking counterparts, that is a measurable service gap, and it accuses nobody of being dangerous.

Code MIT, data CC-BY 4.0. Designed to be replicated for other languages.
