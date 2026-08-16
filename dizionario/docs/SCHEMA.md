# Schema del dataset

Una voce è un file YAML in `voci/`, chiamato `NNN-slug.yaml`. Nove campi obbligatori, tre facoltativi.

Le regole qui sotto sono tutte verificate da `src/validate.py`. Se una regola non è verificabile automaticamente è scritto perché.

---

## Campi obbligatori

### `id`

Stringa di tre cifre, tra virgolette. **Le virgolette servono**: senza, YAML legge `001` come il numero 1 e la numerazione si rompe.

Progressivo, senza buchi. Un id assegnato non si riusa: se una voce viene ritirata, il suo numero resta vuoto e la cosa si documenta.

```yaml
id: "001"
```

### `slug`

Identificatore stabile, in minuscolo, senza accenti, con i trattini al posto degli spazi. Deve derivare meccanicamente da `termine`: il validatore ricalcola e confronta.

È la cosa che gli altri citano. Cambiarlo rompe i collegamenti esterni, e non si cambia dopo la pubblicazione.

```yaml
slug: finestra-di-contesto
```

### `termine`

Il termine come si legge nel dizionario. Maiuscola iniziale, il resto in minuscolo salvo i nomi propri (*Constitutional AI*, *RLHF*).

Unico su tutto il dataset, confronto senza distinzione di maiuscole.

### `settimana` e `gruppo`

Numero da 1 a 6 e nome del gruppo corrispondente. I due devono essere coerenti, la tabella è nel validatore.

| | Gruppo |
|---|---|
| 1 | Le fondamenta |
| 2 | Come si usa |
| 3 | Architettura e agenti |
| 4 | Come sbaglia |
| 5 | Come si verifica |
| 6 | Sicurezza |

Il numero è un raggruppamento tematico che coincide con il calendario di pubblicazione. Non è un livello di difficoltà.

### `inglese`

Lista di stringhe. Il termine inglese corrispondente, più eventuali sinonimi ed acronimi in uso.

L'ordine conta: il primo è quello più usato. Serve a costruire `dist/indice-inglese.md`, che è il modo in cui la maggior parte delle persone arriva a una voce, perché il termine lo ha incontrato in inglese.

```yaml
inglese:
  - "chain of thought"
  - "CoT"
```

### `cos_e`

La definizione. Due frasi, tre al massimo: oltre le tre il validatore avvisa.

Si entra nel merito alla prima parola. Le aperture che girano intorno all'argomento vengono segnalate.

### `perche_conta`

La conseguenza pratica. Cosa cambia nel lavoro di chi legge.

Non è il posto dove si spiega che il concetto è importante: è il posto dove si dice **cosa succede a chi non lo sa**.

### `errore_comune`

Cosa si sbaglia intorno a questo termine. Un comportamento concreto.

**È il campo che tiene in piedi il dizionario.** Il validatore misura quanto lessico condivide con `cos_e`: sopra il 25% avvisa, perché quasi sempre significa che sta riformulando la definizione invece di dire cosa la gente fa di sbagliato.

La misura è una spia, non un giudizio. Può sbagliarsi in entrambe le direzioni, e per questo avvisa senza bloccare.

---

## Campi facoltativi

### `vedi_anche`

Lista di slug di altre voci. Curata a mano, non calcolata.

Il validatore controlla che ogni slug esista e che nessuna voce rimandi a se stessa. Non richiede reciprocità: *jailbreak* rimanda a *prompt injection* perché è lì che si capisce la differenza, ma non vale necessariamente il contrario.

Due o tre rimandi. Una voce che ne ha otto sta facendo l'indice.

### `revisione`

Intero, parte da 1. Si incrementa quando cambia la sostanza di un campo, non per un refuso.

### `nota`

Testo libero, per il redattore. Non viene pubblicato. Serve a lasciare traccia di una decisione discutibile, così la prossima persona non la ridiscute da zero.

---

## Vincoli su tutti i campi di testo

**Caratteri vietati**, bloccanti: trattino lungo, trattino medio, puntini di sospensione in un carattere solo, virgolette curve, apostrofo curvo.

Sono una scelta di stile della pubblicazione, ed è anche il controllo più rapido per distinguere il testo scritto qui da quello incollato da altrove.

**Lunghezza**: minimo 60 caratteri, bloccante. Oltre 700, avviso.

**Punteggiatura finale**: il campo termina con un punto, un punto interrogativo o una virgoletta di chiusura. Avviso.

---

## Formato dei file

Testo lungo nei blocchi piegati (`>-`), a capo attorno ai 74 caratteri.

Non è estetica: un campo scritto su una riga sola produce diff illeggibili, e una correzione di tre parole appare come la riscrittura dell'intero paragrafo. Con il testo mandato a capo, la revisione di una pull request si legge.

---

## Cosa non è nello schema, di proposito

**Nessuna data.** Le voci non hanno data di pubblicazione né di aggiornamento: quelle stanno in git, che le tiene meglio e non si può falsificare a mano.

**Nessun autore nel file.** Sta nella cronologia di git, per la stessa ragione.

**Nessuna categoria oltre `settimana`.** Un secondo asse di classificazione sembra sempre una buona idea e diventa sempre incoerente, perché nessuno lo mantiene su tutte le voci quando il dataset cresce.
