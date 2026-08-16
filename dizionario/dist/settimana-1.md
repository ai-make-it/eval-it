# Settimana 1 · Le fondamenta

10 voci.

---

<a id="token"></a>

## Token

**Cos'è.** L'unità in cui un modello spezza il testo prima di elaborarlo. Non è una parola e non è una lettera, sta in mezzo.

**Perché conta.** Si paga a token, si misura a token, e tutti i limiti sono espressi in token. L'italiano ne consuma dal 15 al 30% in più dell'inglese per dire la stessa cosa, quindi lavorare nella propria lingua costa di più e porta prima al limite.

**L'errore comune.** Contare le parole. "Cinquemila parole" non dice se si sta dentro il limite.

*Inglese: token*

Vedi anche: [Finestra di contesto](dizionario.md#finestra-di-contesto), [Campionamento](dizionario.md#campionamento).

---

<a id="finestra-di-contesto"></a>

## Finestra di contesto

**Cos'è.** Quanto testo il modello riesce a tenere davanti agli occhi in una volta sola. Ci sta dentro tutto: le istruzioni, i documenti forniti, la conversazione fino a quel punto e la risposta che deve ancora scrivere.

**Perché conta.** Quando la si supera qualcosa viene tagliato, e non è chi usa il sistema a decidere cosa. È la causa più frequente dei comportamenti che gli utenti descrivono come "si è dimenticato quello che gli avevo detto".

**L'errore comune.** Pensare che una finestra grande significhi che il modello usa bene tutto quello che c'è dentro. Le informazioni che stanno in mezzo a un contesto lungo vengono usate peggio di quelle all'inizio e alla fine.

*Inglese: context window*

Vedi anche: [Token](dizionario.md#token), [RAG](dizionario.md#rag), [Prompt di sistema](dizionario.md#prompt-di-sistema).

---

<a id="temperatura"></a>

## Temperatura

**Cos'è.** Il parametro che decide quanto il modello si allontana dalla scelta più probabile a ogni passo. Vicino a zero prende quasi sempre la continuazione più probabile, alzandola diventa più vario e più imprevedibile.

**Perché conta.** È la ragione per cui la stessa domanda dà risposte diverse. Valutare un sistema senza aver fissato la temperatura significa misurare anche il rumore.

**L'errore comune.** Credere che a temperatura zero il modello diventi deterministico. La variabilità crolla, non sparisce: restano differenze dovute a come il calcolo viene eseguito sull'hardware.

*Inglese: temperature*

Vedi anche: [Campionamento](dizionario.md#campionamento), [Set di prova](dizionario.md#set-di-prova).

---

<a id="allucinazione"></a>

## Allucinazione

**Cos'è.** Quando il modello produce un'affermazione falsa con la stessa sicurezza con cui ne produce una vera. Non sta mentendo e non si è rotto: sta facendo quello che fa sempre, cioè generare la continuazione più plausibile.

**Perché conta.** È una proprietà di come funziona, non un difetto in via di correzione. I sistemi migliorano nel ridurne la frequenza, non nell'eliminarla, e questo cambia il modo in cui vanno progettati i controlli attorno.

**L'errore comune.** Trattarla come un bug da segnalare. Se il piano è "quando allucina lo segnaliamo", non è un piano.

*Inglese: hallucination*

Vedi anche: [RAG](dizionario.md#rag), [Ground truth](dizionario.md#ground-truth), [Osservabilità](dizionario.md#osservabilita).

---

<a id="valutazione"></a>

## Valutazione

**Cos'è.** Il processo con cui si misura se un sistema fa quello che deve, su un insieme di casi scelti apposta e sempre gli stessi. Non è provarlo qualche volta e vedere se sembra andare.

**Perché conta.** È l'unica cosa che separa "abbiamo comprato l'AI" da "sappiamo cosa fa". Senza, ogni modifica al sistema è una scommessa e ogni miglioramento è un'impressione.

**L'errore comune.** Costruirla dopo. Una valutazione scritta a valle tende a misurare proprio le cose che il sistema già fa bene, perché è da quelle che si è partiti per scriverla.

*Inglese: eval, evaluation*

Vedi anche: [Set di prova](dizionario.md#set-di-prova), [Metrica](dizionario.md#metrica), [Benchmark](dizionario.md#benchmark).

---

<a id="ground-truth"></a>

## Ground truth

**Cos'è.** La risposta corretta contro cui si confronta l'output del sistema. In italiano si dice a volte "verità di riferimento", ma quasi nessuno lo dice.

**Perché conta.** Senza, non si sta valutando: si stanno raccogliendo impressioni. Stabilirla è di solito la parte più costosa del lavoro, ed è quella che viene saltata per prima.

**L'errore comune.** Darla per ovvia. Su molti compiti reali due esperti competenti non sono d'accordo tra loro, e chi non se ne accorge prima lo scopre leggendo risultati che non stanno in piedi.

*Inglese: ground truth*

Vedi anche: [Annotazione](dizionario.md#annotazione), [Accordo tra annotatori](dizionario.md#accordo-tra-annotatori), [Set di prova](dizionario.md#set-di-prova).

---

<a id="benchmark"></a>

## Benchmark

**Cos'è.** Un insieme standard di prove usato per confrontare modelli diversi sulla stessa base. Sono le tabelle che compaiono a ogni annuncio di un modello nuovo.

**Perché conta.** Servono a confrontare i modelli tra loro. Non servono a dire se un modello va bene per un caso specifico.

**L'errore comune.** Scegliere il modello guardando la classifica. Il primo può essere peggiore del terzo sul caso concreto, e capita spesso.

*Inglese: benchmark*

Vedi anche: [Valutazione](dizionario.md#valutazione), [Set di prova](dizionario.md#set-di-prova), [Overfitting](dizionario.md#overfitting).

---

<a id="drift"></a>

## Drift

**Cos'è.** Il peggioramento graduale di un sistema che nessuno ha toccato, perché è cambiato il mondo intorno. Cambiano i dati in ingresso, cambiano le abitudini di chi lo usa, cambia il modello sotto quando il fornitore lo aggiorna.

**Perché conta.** È il fallimento che non fa rumore. Il sistema non si rompe, si sposta piano, e chi lo usa se ne accorge molto tempo dopo.

**L'errore comune.** Misurare una volta sola, al collaudo. Una valutazione senza una cadenza è la fotografia di un giorno.

*Inglese: drift, model drift, data drift*

Vedi anche: [Regressione](dizionario.md#regressione), [Osservabilità](dizionario.md#osservabilita), [Valutazione](dizionario.md#valutazione).

---

<a id="regressione"></a>

## Regressione

**Cos'è.** Quando una modifica migliora una cosa e ne peggiora un'altra senza che nessuno se ne accorga. Un prompt riscritto, un aggiornamento del modello, un parametro spostato.

**Perché conta.** Nei sistemi AI succede più spesso e si vede molto meno che nel software tradizionale, perché non compare un errore. Compare un output leggermente peggiore, e leggermente peggiore non fa scattare niente.

**L'errore comune.** Verificare la modifica solo sui casi che si volevano sistemare. Quelli funzioneranno, sono appena stati sistemati. Il problema è tutto il resto.

*Inglese: regression*

Vedi anche: [Drift](dizionario.md#drift), [Set di prova](dizionario.md#set-di-prova), [Soglia di accettazione](dizionario.md#soglia-di-accettazione).

---

<a id="prompt-injection"></a>

## Prompt injection

**Cos'è.** Quando un'istruzione nascosta dentro il materiale che il sistema legge, una pagina web, un documento, una mail, viene eseguita come se fosse un comando dell'utente.

**Perché conta.** È il problema di sicurezza strutturale di qualunque sistema che legga contenuto esterno o usi strumenti per conto di qualcuno, e a oggi non ha una soluzione completa. Si mitiga, non si chiude.

**L'errore comune.** Confonderla con il jailbreak. Nel jailbreak è l'utente che prova ad aggirare le regole. Nella prompt injection l'utente è la vittima.

*Inglese: prompt injection*

Vedi anche: [Jailbreak](dizionario.md#jailbreak), [Prompt di sistema](dizionario.md#prompt-di-sistema), [Uso di strumenti](dizionario.md#uso-di-strumenti).

---
