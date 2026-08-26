# Note per chi lavora su questo repo

Vale per le persone e per gli assistenti. Le regole non sono preferenze estetiche: ognuna corrisponde a un modo in cui questo repo si guasta.

## La fonte è `voci/`, `dist/` e `sito/` sono generati

Non modificare mai i file in `dist/` né in `sito/`. Si modifica `voci/*.yaml` e si rilancia la catena. Una correzione fatta a valle sparisce alla build successiva, e la CI fallisce se `dist/` o `sito/` non sono allineati al sorgente.

Ogni modifica al dataset chiude con questi quattro comandi, in quest'ordine:

```bash
python src/validate.py       # deve uscire con 0
python src/build.py          # rigenera dist/
python src/sito.py           # rigenera sito/
python src/collegamenti.py   # deve uscire con 0
```

Tutti i risultati vanno inclusi nel commit.

## Il sito si rigenera, non si ritocca

`src/sito.py` produce `sito/`, che è quello che finisce su ai-make.it. Le stringhe che compaiono nelle pagine stanno nel generatore, e vanno scritte con gli accenti veri (`cos'è`, `perché`), non con l'apostrofo di ripiego che si usa nei commenti Python. I caratteri vietati alle voci lo sono anche qui, e `src/collegamenti.py` li blocca sul generato.

`sito/` deve restare riproducibile: due build di fila devono dare file identici. Niente date di build, niente numeri casuali, niente ordinamenti che dipendono dal filesystem. Una build che cambia da sola fa fallire la CI ogni giorno per una differenza che non significa nulla.

La pubblicazione è un'azione esplicita: `./deploy.sh` senza argomenti è una prova a vuoto, si carica solo con `--conferma`.

## Regole di scrittura, non negoziabili

**Niente trattini lunghi.** Niente trattini medi, virgolette curve, apostrofi tipografici, puntini di sospensione in un carattere solo. Il validatore li blocca. Al loro posto: virgole, due punti, punto e virgola.

**Niente frasi che suonano generate.** Nessun "è importante notare che", "in un mondo sempre più", "non solo... ma anche". Si entra nel merito alla prima parola.

**Niente emoji, niente hashtag decorativi.**

## La disciplina delle voci

Quattro campi, sempre gli stessi. Il criterio per accettare una voce nuova è uno solo: **si riesce a scrivere l'errore comune?** Se no, è una definizione, e le definizioni esistono già tradotte ovunque. Non si fanno eccezioni: la prima apre la strada a tutte le altre.

`docs/SCHEMA.md` descrive ogni campo. `CONTRIBUTING.md` spiega il formato di una proposta.

## Cosa non aggiungere

Date e autori nei file YAML: stanno in git, che li tiene meglio. Un secondo asse di classificazione oltre `settimana`: sembra sempre una buona idea e diventa sempre incoerente. Termini di marca: invecchiano in sei mesi.

## Il progetto collegato

[`eval-it`](https://github.com/ai-make-it/eval-it) misura quello che qui viene definito. Le due cose si citano a vicenda nei README e i rimandi vanno tenuti vivi.

Sono due repo separati. Hanno vissuto per un po' nello stesso repo, in due cartelle, e la convivenza non aggiungeva niente: nessun codice condiviso, due build, due CI, due licenze. Non ricominciare a mescolarli.
