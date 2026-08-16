# Note per chi lavora su questo repo

Vale per le persone e per gli assistenti. Questo repo misura il comportamento di prodotti commerciali: alcune di queste regole sono l'unica cosa che tiene il lavoro difendibile.

## Le tre regole che non si toccano

**Misurare, non aggirare.** Tutte le richieste del test set sono dirette: nessuna finzione, nessun role-play, nessuna tecnica di aggiramento. Se una modifica introducesse una tecnica di aggiramento, renderebbe false le notifiche già inviate ai fornitori, che è peggio di non averle mandate.

**Gli item ad alta severità si prelevano, non si inventano.** Le righe `A11`-`A15` si riempiono da benchmark pubblicati (DoNotAnswer, HarmBench) citando la fonte nella colonna `source`. Non scrivere prompt dannosi nuovi: i risultati non sarebbero confrontabili con nessuna letteratura, ed è anche peggiore pratica.

**Gemini via `ai.google.dev`, mai Vertex AI.** I Service Specific Terms di Google Cloud contengono una clausola *Benchmarking* che pone condizioni alla pubblicazione. Il vincolo è scritto in `src/providers.py` e in `config.example.yaml` perché non venga perso in una modifica distratta.

## Cosa non deve finire nel repo

`config.yaml`, `results/*.jsonl` e i CSV di annotazione sono in `.gitignore`. Contengono chiavi API e output dei modelli. Non toglierli da lì e non aggiungere eccezioni.

**Nessun output dannoso trascritto**, mai, nemmeno come esempio in un file di documentazione. Si categorizza, non si riporta.

Se emerge un aggiramento funzionante, **non si pubblica**: si segnala al fornitore attraverso il suo canale di disclosure e si pubblica solo il fatto statistico.

## Definizioni che vivono in un posto solo

`RIFIUTO = {1, 2}` sta in `src/analyze.py`, riga sola, ed è dichiarato nel README. Cambiarla cambia tutti i numeri pubblicati: se la si cambia, va cambiata anche la dichiarazione e vanno rifatte le tabelle.

La scala di annotazione sta in `docs/ANNOTATION.md`. Non riscriverla a metà di una campagna di annotazione.

## Etichette: campi separati

`label_a` e `label_b` sono umane. Qualsiasi etichettatura automatica va in un campo distinto, mai sovrascrivendo le due precedenti. Nel momento in cui si mescolano, il kappa pubblicato non significa più niente.

## Prima di eseguire

Snapshot datati fissati dall'endpoint dei modelli, non nomi di famiglia. Tier a pagamento. Account dedicato. Notifiche ai fornitori inviate e registrate.

## Regole di scrittura

Niente trattini lunghi, virgolette curve, apostrofi tipografici. Niente emoji. Verbi di misura, mai verbi di giudizio: *"il tasso rilevato è del 40%, IC 95% 34-46%"*, non *"il modello X è pericoloso"*.

## Il dizionario sta in `dizionario/`

`dizionario/` definisce in italiano i termini che qui vengono misurati. E' un progetto a se': sorgente in `dizionario/voci/`, sue regole in `dizionario/CLAUDE.md`, sua CI. Le due cartelle non condividono codice e non devono cominciare a farlo.

Una regola sola le attraversa: `dizionario/sito/` e' generato e finisce su ai-make.it, quindi si rigenera con `python src/sito.py`, non si ritocca a mano.
