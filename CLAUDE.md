# Note per chi lavora su questo repo

Vale per le persone e per gli assistenti. Questo repo misura il comportamento di prodotti commerciali: alcune di queste regole sono l'unica cosa che tiene il lavoro difendibile.

## Le tre regole che non si toccano

**Misurare, non aggirare.** Tutte le richieste del test set sono dirette: nessuna finzione, nessun role-play, nessuna tecnica di aggiramento. Se una modifica introducesse una tecnica di aggiramento, renderebbe false le notifiche già inviate ai fornitori, che è peggio di non averle mandate.

**Gli item ad alta severità si prelevano, non si inventano.** Le righe `A11`-`A15` si riempiono da benchmark pubblicati (DoNotAnswer, HarmBench) citando la fonte nella colonna `source`. Non scrivere prompt dannosi nuovi: i risultati non sarebbero confrontabili con nessuna letteratura, ed è anche peggiore pratica.

**Gemini via `ai.google.dev`, mai Vertex AI.** I Service Specific Terms di Google Cloud contengono una clausola *Benchmarking* che pone condizioni alla pubblicazione. Il vincolo è scritto in `src/providers.py`, che solleva un errore se il `base_url` punta a `aiplatform.googleapis.com`, ed è coperto da un test.

## Prima di aprire una pull request

```bash
python src/validate.py --severo
ruff check src tests
python -m pytest tests
```

Sono gli stessi tre comandi che gira la CI, più la pipeline completa col provider `mock`. Il resto delle regole per chi contribuisce sta in `CONTRIBUTING.md`.

## Cosa non deve finire nel repo

`config.yaml`, `results/*.jsonl` e i CSV di annotazione sono in `.gitignore`. Contengono chiavi API e output dei modelli. Non toglierli da lì e non aggiungere eccezioni.

**Nessun output dannoso trascritto**, mai, nemmeno come esempio in un file di documentazione. Si categorizza, non si riporta.

Se emerge un aggiramento funzionante, **non si pubblica**: si segnala al fornitore attraverso il suo canale di disclosure e si pubblica solo il fatto statistico.

## Definizioni che vivono in un posto solo

`RIFIUTO = {1, 2}` sta in `src/analyze.py`, riga sola, ed è dichiarato nel README. Cambiarla cambia tutti i numeri pubblicati: se la si cambia, va cambiata anche la dichiarazione e vanno rifatte le tabelle.

La scala di annotazione sta in `docs/ANNOTATION.md`. Non riscriverla a metà di una campagna di annotazione.

I conteggi per categoria stanno in `DISEGNO`, in `src/validate.py`, e sono gli stessi dichiarati in `docs/METHOD.md` e nel README. Il validatore li impone: aggiungere una coppia senza toccare le tre dichiarazioni fa fallire la CI, ed è voluto.

## L'unità di analisi è la coppia, non la chiamata

Le ripetizioni sullo stesso prompt non sono osservazioni indipendenti, e la stessa coppia compare in entrambe le lingue. L'intervallo di confidenza in `analyze.py` è un bootstrap a grappoli sulle coppie proprio per questo.

Non sostituirlo con un intervallo binomiale sul numero di chiamate: restringerebbe gli intervalli di circa la radice del numero di ripetizioni e farebbe sembrare significativi dei delta che non lo sono. È il difetto che un revisore ostile cerca per primo, subito dopo il kappa.

## Cieco sul modello, non sulla lingua

L'export di `annotate.py` nasconde quale modello ha risposto e mescola le righe. Non nasconde la lingua, e non può: la richiesta va letta. Non scrivere da nessuna parte che l'annotazione è cieca sulla lingua: è falso, ed è la prima cosa che un revisore contesta.

## Le chiamate bloccate sono un dato

Una chiamata fermata dal fornitore per il contenuto ha `blocked: true` e nessun testo. Non è un guasto: è il rifiuto più netto che esista, e `analyze.py` la conta come tale. Non rimetterla fra gli errori tecnici: escluderla abbasserebbe i tassi proprio sui modelli che bloccano di più.

## Etichette: campi separati

`label_a` e `label_b` sono umane. Qualsiasi etichettatura automatica va in un campo distinto, mai sovrascrivendo le due precedenti. Nel momento in cui si mescolano, il kappa pubblicato non significa più niente.

## Prima di eseguire

Snapshot datati fissati dall'endpoint dei modelli, non nomi di famiglia. Tier a pagamento. Account dedicato. Notifiche ai fornitori inviate e registrate.

## Regole di scrittura

Niente trattini lunghi, virgolette curve, apostrofi tipografici. Niente emoji. Verbi di misura, mai verbi di giudizio: *"il tasso rilevato è del 40%, IC 95% 34-46%"*, non *"il modello X è pericoloso"*.

## Il dizionario sta altrove

[`ai-make-it/dizionario`](https://github.com/ai-make-it/dizionario) definisce in italiano i termini che qui vengono misurati. Ha vissuto per un po' in questo repo, in una cartella accanto, e la convivenza non aggiungeva niente: nessun codice condiviso, due build, due CI, due licenze.

Non riportarlo dentro. Quello che i due progetti condividono e' il vocabolario, e si tiene vivo con i rimandi nei README.
