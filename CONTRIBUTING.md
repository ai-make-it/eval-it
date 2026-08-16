# Come si contribuisce

Tre modi, in ordine di quanto sono utili.

---

## 1. Segnalare un errore

Apri una issue. Se è un refuso basta indicarlo; se è un errore di merito, scrivi anche perché, così la discussione parte già dal punto giusto.

Le voci sono opinabili per costruzione: il campo *errore comune* dice cosa la gente sbaglia, ed è un giudizio. Contestarlo è un contributo, non un fastidio.

---

## 2. Migliorare una voce esistente

Modifica il file in `voci/`, lancia `python src/validate.py`, apri una pull request.

Nella descrizione della PR scrivi **cosa cambia e perché**, in due righe. Una riscrittura senza motivazione è difficile da valutare anche quando è migliore dell'originale.

Non toccare `dist/`: viene rigenerato e la modifica andrebbe persa.

---

## 3. Proporre una voce nuova

**Prima di scriverla, prova a scrivere l'errore comune.**

È il criterio, e non è una formalità. Se riesci a dire cosa la gente sbaglia intorno a quel termine, la voce ha una ragione di esistere. Se riesci solo a definirlo, la definizione si trova già in inglese tradotta ovunque, e aggiungerla qui rende il dizionario più lungo senza renderlo più utile.

### Il formato

Un file per voce, in `voci/`, chiamato `NNN-slug.yaml`.

```yaml
id: "061"
slug: nome-della-voce
termine: "Nome della voce"
settimana: 4
gruppo: "Come sbaglia"
inglese:
  - "english term"
  - "sinonimo inglese"
cos_e: >-
  La definizione, in due frasi. Tre al massimo. Si entra nel merito alla
  prima parola.
perche_conta: >-
  La conseguenza pratica. Cosa cambia nel lavoro di chi legge, non perché
  il concetto è interessante.
errore_comune: >-
  Cosa si sbaglia. Un comportamento concreto, non una riformulazione
  della definizione.
vedi_anche:
  - altra-voce
  - terza-voce
revisione: 1
```

`docs/SCHEMA.md` descrive ogni campo per esteso.

### Le regole di scrittura

**Due frasi per la definizione.** Tre se serve. Oltre, non è più un dizionario.

**Si entra nel merito alla prima parola.** *"Il token è l'unità in cui..."*, non *"Nel campo dell'intelligenza artificiale, il token rappresenta..."*.

**Niente trattini lunghi**, niente virgolette curve, niente apostrofi tipografici. Il validatore li blocca. È una scelta di stile della pubblicazione, ed è anche il modo più rapido per distinguere il testo scritto qui da quello incollato da altrove.

**Il termine inglese resta inglese quando è così che si dice.** *Token*, *embedding*, *fine-tuning* non si traducono, perché nessuno li traduce lavorando. Inventare un calco italiano che nessuno userà rende la voce inutile a chi ne ha bisogno. Dove esiste un termine italiano in uso reale, si usa quello e si mette l'inglese nel campo apposito.

**Il campo *perché conta* parla al lettore, non del concetto.** *"Si paga a token e tutti i limiti sono espressi in token"* è una conseguenza. *"È un concetto centrale dell'elaborazione del linguaggio"* non lo è.

### Prima di aprire la PR

```bash
pip install pyyaml
python src/validate.py     # deve uscire con 0
python src/build.py        # rigenera dist/
```

Includi anche `dist/` rigenerato nella PR: così la differenza si legge sia nel sorgente sia nel testo pubblicato.

---

## Cosa viene rifiutato

**Voci senza errore comune.** Il criterio è quello, e non si fanno eccezioni: la prima eccezione apre la strada a tutte le altre.

**Voci fuori perimetro.** Il dizionario copre il vocabolario dei modelli linguistici, della loro valutazione e della loro sicurezza. Visione artificiale, parlato, robotica e materia normativa sono fuori, non perché contino meno ma perché un dizionario che copre tutto non lo mantiene nessuno.

**Riscritture di massa.** Una PR che tocca venti voci non è valutabile. Se il problema è sistematico, apri prima una issue.

**Termini di marca.** I nomi commerciali dei prodotti cambiano ogni sei mesi e il dizionario invecchierebbe con loro.

---

## Licenza dei contributi

Proponendo una modifica accetti che il testo sia pubblicato con **CC BY 4.0** e il codice con **MIT**, come il resto del repo. I contributi vengono attribuiti nella cronologia di git, che è il registro di chi ha scritto cosa.
