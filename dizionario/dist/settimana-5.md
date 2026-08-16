# Settimana 5 · Come si verifica

10 voci.

---

<a id="error-analysis"></a>

## Error analysis

**Cos'è.** Leggere gli output sbagliati uno per uno, raggrupparli per tipo di errore e contare quanto pesa ciascun gruppo. Non è una statistica, è una lettura.

**Perché conta.** È l'unico modo per sapere cosa migliorare. Un punteggio dice che il sistema sbaglia il 18% delle volte, l'error analysis dice che quel 18% è quasi tutto un problema solo, che si risolve in un pomeriggio.

**L'errore comune.** Saltarla e passare direttamente alle soluzioni. Chi ottimizza senza aver guardato gli errori ottimizza per l'errore che immagina, e quello immaginato quasi mai è il più frequente.

*Inglese: error analysis*

Vedi anche: [Annotazione](dizionario.md#annotazione), [Caso limite](dizionario.md#caso-limite), [Metrica](dizionario.md#metrica).

---

<a id="annotazione"></a>

## Annotazione

**Cos'è.** Il lavoro di etichettare manualmente input e output secondo criteri definiti: corretto o sbagliato, di che tipo, con quale gravità.

**Perché conta.** È il materiale grezzo di ogni valutazione seria. È noioso, è costoso, e chi lo salta si trova a decidere su impressioni chiamandole dati.

**L'errore comune.** Farlo senza aver scritto prima le istruzioni di annotazione. Senza criteri espliciti, la stessa persona etichetta in modo diverso a distanza di due giorni, e il risultato non è confrontabile con niente.

*Inglese: annotation, labeling*

Vedi anche: [Accordo tra annotatori](dizionario.md#accordo-tra-annotatori), [Ground truth](dizionario.md#ground-truth), [Bias](dizionario.md#bias).

---

<a id="accordo-tra-annotatori"></a>

## Accordo tra annotatori

**Cos'è.** Quanto due persone che annotano lo stesso materiale, indipendentemente, arrivano alle stesse conclusioni.

**Perché conta.** È il tetto della valutazione. Se due esperti concordano solo nel 70% dei casi, nessuna misura automatica su quel compito può essere più affidabile di così, e i decimali oltre quella soglia sono rumore.

**L'errore comune.** Non misurarlo affatto. È una mezza giornata di lavoro e determina se tutto quello che viene dopo ha senso.

*Inglese: inter-annotator agreement*

Vedi anche: [Annotazione](dizionario.md#annotazione), [Ground truth](dizionario.md#ground-truth), [Metrica](dizionario.md#metrica).

---

<a id="metrica"></a>

## Metrica

**Cos'è.** Il numero che riassume l'andamento del sistema su un insieme di casi. Percentuale di risposte corrette, tempo medio, costo per operazione conclusa.

**Perché conta.** Rende confrontabili due versioni di un sistema. È anche l'unica cosa che si può inserire in un processo di rilascio automatico.

**L'errore comune.** Usarne una sola. Una metrica singola si può sempre far salire peggiorando qualcosa che non viene misurato, e prima o poi qualcuno lo farà senza rendersene conto.

*Inglese: metric*

Vedi anche: [Precisione e recupero](dizionario.md#precisione-e-recupero), [Soglia di accettazione](dizionario.md#soglia-di-accettazione), [Valutazione](dizionario.md#valutazione).

---

<a id="precisione-e-recupero"></a>

## Precisione e recupero

**Cos'è.** Due misure che rispondono a domande diverse. La precisione dice quanta parte di quello che il sistema ha segnalato era giusto. Il recupero dice quanta parte di quello che c'era da trovare è stato effettivamente trovato.

**Perché conta.** Vanno quasi sempre in direzioni opposte, e scegliere quale privilegiare è una decisione di business, non tecnica. Un sistema antifrode e un sistema di suggerimenti hanno bisogno di equilibri opposti.

**L'errore comune.** Citare solo l'accuratezza complessiva. Su fenomeni rari è un numero che sembra ottimo e non dice nulla: un sistema che non segnala mai niente è accurato al 99% se il fenomeno riguarda l'1% dei casi.

*Inglese: precision and recall*

Vedi anche: [Metrica](dizionario.md#metrica), [Soglia di accettazione](dizionario.md#soglia-di-accettazione).

---

<a id="modello-giudice"></a>

## Modello giudice

**Cos'è.** Usare un modello linguistico per valutare gli output di un altro modello, secondo criteri scritti in un prompt di valutazione.

**Perché conta.** È l'unico modo pratico per valutare compiti aperti su volumi consistenti, dove non esiste una risposta unica corretta da confrontare.

**L'errore comune.** Fidarsene senza averlo tarato su annotazione umana. Un giudice automatico ha bias propri, tende a premiare risposte lunghe e ben formattate, e va verificato su un campione etichettato a mano prima di essere messo in produzione.

*Inglese: LLM-as-a-judge*

Vedi anche: [Annotazione](dizionario.md#annotazione), [Accordo tra annotatori](dizionario.md#accordo-tra-annotatori), [Sicofanzia](dizionario.md#sicofanzia).

---

<a id="set-di-prova"></a>

## Set di prova

**Cos'è.** L'insieme dei casi su cui si misura il sistema, fissato in anticipo e usato sempre uguale a ogni misurazione.

**Perché conta.** Se cambia a ogni giro, i risultati non sono confrontabili nel tempo e non si può sapere se una modifica ha migliorato o peggiorato le cose.

**L'errore comune.** Costruirlo con i casi facili, quelli che si avevano sottomano. Un set di prova senza casi difficili produce risultati eccellenti e nessuna informazione utile.

*Inglese: test set, eval set*

Vedi anche: [Valutazione](dizionario.md#valutazione), [Overfitting](dizionario.md#overfitting), [Ground truth](dizionario.md#ground-truth).

---

<a id="soglia-di-accettazione"></a>

## Soglia di accettazione

**Cos'è.** Il livello sotto il quale il sistema non viene rilasciato, o viene ritirato se ci scende dopo. Un numero deciso prima, non dopo aver visto i risultati.

**Perché conta.** Trasforma la valutazione da esercizio informativo a strumento decisionale. Senza una soglia fissata prima, qualsiasi risultato viene interpretato come accettabile.

**L'errore comune.** Fissarla dopo la prima misurazione. In quel momento diventa la descrizione di quello che il sistema già fa, non un requisito.

*Inglese: acceptance threshold*

Vedi anche: [Metrica](dizionario.md#metrica), [Regressione](dizionario.md#regressione), [Precisione e recupero](dizionario.md#precisione-e-recupero).

---

<a id="osservabilita"></a>

## Osservabilità

**Cos'è.** La strumentazione che permette di vedere cosa sta facendo davvero un sistema in produzione: cosa gli arriva, cosa risponde, quanto ci mette, dove si blocca.

**Perché conta.** La valutazione prima del rilascio dice come si comporta il sistema sui casi previsti. L'osservabilità dice come si comporta sui casi reali, che sono sempre diversi.

**L'errore comune.** Registrare solo gli errori tecnici. In un sistema AI i fallimenti più costosi non generano nessuna eccezione: producono una risposta regolare e sbagliata, che senza registrazione del contenuto non si vede.

*Inglese: observability*

Vedi anche: [Drift](dizionario.md#drift), [Fallimento a cascata](dizionario.md#fallimento-a-cascata), [Regressione](dizionario.md#regressione).

---

<a id="scheda-del-modello"></a>

## Scheda del modello

**Cos'è.** Il documento con cui chi produce un modello ne descrive capacità, limiti, valutazioni svolte e comportamenti noti. Per i modelli di frontiera si chiama scheda di sistema ed è più ampia.

**Perché conta.** È la fonte primaria per capire cosa un fornitore dichiara e cosa ha effettivamente misurato. Chi valuta un sistema di terzi dovrebbe partire da lì invece che dal materiale commerciale.

**L'errore comune.** Leggerla come una garanzia. Descrive prove svolte in condizioni scelte da chi vende, e l'assenza di un limite dichiarato non significa che quel limite non esista.

*Inglese: model card, system card*

Vedi anche: [Benchmark](dizionario.md#benchmark), [Capacità pericolose](dizionario.md#capacita-pericolose), [Valutazione](dizionario.md#valutazione).

---
