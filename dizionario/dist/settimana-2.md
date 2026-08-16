# Settimana 2 · Come si usa

10 voci.

---

<a id="prompt"></a>

## Prompt

**Cos'è.** Tutto quello che viene dato al modello prima che risponda: l'istruzione, il contesto, gli esempi, i documenti. Non è solo la domanda che si scrive nella casella.

**Perché conta.** È l'unica leva che si controlla completamente senza toccare il modello, ed è quella dove si concentra la maggior parte dei miglioramenti reali nei sistemi in produzione.

**L'errore comune.** Trattarlo come una formula magica da copiare. Un prompt che funziona benissimo su un modello può peggiorare le cose su un altro, e va rivalutato a ogni cambio di versione.

*Inglese: prompt*

Vedi anche: [Prompt di sistema](dizionario.md#prompt-di-sistema), [Few-shot](dizionario.md#few-shot), [Dipendenza dal formato](dizionario.md#dipendenza-dal-formato).

---

<a id="prompt-di-sistema"></a>

## Prompt di sistema

**Cos'è.** Le istruzioni permanenti che stanno sopra ogni conversazione e definiscono ruolo, vincoli e comportamento del sistema. L'utente di solito non le vede.

**Perché conta.** È il posto dove si mettono le regole che non devono cambiare, ed è anche il posto dove finisce, negli anni, tutta la complessità accumulata di un sistema. Un prompt di sistema che nessuno rilegge da sei mesi è un debito.

**L'errore comune.** Considerarlo una protezione. Non è un confine di sicurezza: contenuto ostile nel resto del contesto può contraddirlo.

*Inglese: system prompt*

Vedi anche: [Prompt](dizionario.md#prompt), [Prompt injection](dizionario.md#prompt-injection), [Finestra di contesto](dizionario.md#finestra-di-contesto).

---

<a id="few-shot"></a>

## Few-shot

**Cos'è.** Mettere nel prompt alcuni esempi di input e output corretti, così che il modello capisca la forma della risposta attesa. Con zero esempi si parla di zero-shot.

**Perché conta.** Su compiti dal formato preciso è spesso il modo più rapido ed economico per migliorare i risultati, molto prima di pensare al fine-tuning.

**L'errore comune.** Scegliere esempi tutti simili tra loro. Gli esempi definiscono implicitamente cosa il modello considera normale, e se coprono un solo caso il sistema si irrigidisce su quello.

*Inglese: few-shot prompting*

Vedi anche: [Prompt](dizionario.md#prompt), [Fine-tuning](dizionario.md#fine-tuning).

---

<a id="catena-di-ragionamento"></a>

## Catena di ragionamento

**Cos'è.** Chiedere al modello di esplicitare i passaggi prima di dare la risposta finale, invece di rispondere di getto. I modelli recenti spesso lo fanno da soli.

**Perché conta.** Su compiti che richiedono più passaggi migliora sensibilmente l'accuratezza, e rende visibile dove il ragionamento si rompe.

**L'errore comune.** Leggere i passaggi come la spiegazione di come il modello è arrivato alla risposta. Sono testo generato come tutto il resto, possono essere plausibili e non corrispondere al processo effettivo.

*Inglese: chain of thought, CoT*

Vedi anche: [Prompt](dizionario.md#prompt), [Interpretabilità](dizionario.md#interpretabilita).

---

<a id="output-strutturato"></a>

## Output strutturato

**Cos'è.** Vincolare la risposta a una forma prestabilita, tipicamente uno schema JSON, invece di lasciarla in testo libero.

**Perché conta.** È quello che rende un modello utilizzabile dentro un software invece che solo davanti a una persona. Elimina un'intera classe di errori di interpretazione a valle.

**L'errore comune.** Credere che un output valido sia un output corretto. Lo schema garantisce la forma, non il contenuto: un JSON perfettamente formato può contenere un dato inventato.

*Inglese: structured output*

Vedi anche: [Prompt](dizionario.md#prompt), [Uso di strumenti](dizionario.md#uso-di-strumenti).

---

<a id="rag"></a>

## RAG

**Cos'è.** Recuperare i documenti pertinenti a una domanda e infilarli nel contesto prima che il modello risponda, così che risponda su quelli invece che a memoria.

**Perché conta.** È il modo standard per far lavorare un modello su informazioni che non aveva durante l'addestramento, dai documenti aziendali agli aggiornamenti recenti.

**L'errore comune.** Pensare che risolva le allucinazioni. Le riduce quando il recupero funziona. Quando il recupero porta il documento sbagliato, il modello risponde con la stessa sicurezza su una fonte irrilevante.

*Inglese: retrieval-augmented generation*

Vedi anche: [Ricerca semantica](dizionario.md#ricerca-semantica), [Frammentazione](dizionario.md#frammentazione), [Allucinazione](dizionario.md#allucinazione).

---

<a id="frammentazione"></a>

## Frammentazione

**Cos'è.** Spezzare i documenti in pezzi più piccoli prima di indicizzarli, perché il recupero lavora sui frammenti e non sui file interi.

**Perché conta.** È la decisione più sottovalutata di un sistema RAG. Frammenti troppo piccoli perdono il contesto necessario a capirli, troppo grandi portano rumore nel contesto e diluiscono la risposta.

**L'errore comune.** Tagliare a lunghezza fissa ignorando la struttura del documento. Una tabella spezzata a metà o un articolo di legge separato dal suo comma diventano inutili o fuorvianti.

*Inglese: chunking*

Vedi anche: [RAG](dizionario.md#rag), [Ricerca semantica](dizionario.md#ricerca-semantica), [Embedding](dizionario.md#embedding).

---

<a id="ricerca-semantica"></a>

## Ricerca semantica

**Cos'è.** Cercare per significato invece che per corrispondenza di parole, confrontando rappresentazioni numeriche dei testi. Trova documenti pertinenti anche quando non contengono i termini della domanda.

**Perché conta.** È il motore di recupero di quasi tutti i sistemi RAG, e la qualità di quello che il modello legge dipende quasi interamente da lei.

**L'errore comune.** Sostituirla del tutto alla ricerca per parole chiave. Su codici prodotto, nomi propri, riferimenti normativi e sigle la ricerca esatta resta migliore: i sistemi che funzionano usano entrambe.

*Inglese: semantic search, vector search*

Vedi anche: [Embedding](dizionario.md#embedding), [RAG](dizionario.md#rag), [Frammentazione](dizionario.md#frammentazione).

---

<a id="fine-tuning"></a>

## Fine-tuning

**Cos'è.** Addestrare ulteriormente un modello già esistente su dati propri, per specializzarlo su un compito o su uno stile.

**Perché conta.** Serve quando il compito ha una forma molto specifica e ripetitiva, o quando si vuole ottenere da un modello piccolo il comportamento di uno grande, riducendo costi e latenza.

**L'errore comune.** Usarlo per aggiungere conoscenza. Il fine-tuning insegna bene come rispondere, molto meno cosa sapere: per le informazioni serve il recupero, non l'addestramento.

*Inglese: fine-tuning*

Vedi anche: [Post-addestramento](dizionario.md#post-addestramento), [Few-shot](dizionario.md#few-shot), [Modello base e modello istruito](dizionario.md#modello-base-e-modello-istruito).

---

<a id="modello-base-e-modello-istruito"></a>

## Modello base e modello istruito

**Cos'è.** Il modello base sa solo continuare il testo, perché è quello che ha imparato a fare. Il modello istruito ha ricevuto un addestramento successivo che gli insegna a seguire istruzioni e a comportarsi come un assistente.

**Perché conta.** Sono strumenti diversi. Quasi tutto quello che si usa quotidianamente è un modello istruito, ma per certi usi tecnici il modello base è più adatto perché è meno condizionato.

**L'errore comune.** Provare un modello base aspettandosi che risponda a una domanda, concludere che è scadente. Sta facendo esattamente il suo lavoro: continuare quello che ha letto.

*Inglese: base model, instruct model*

Vedi anche: [Pre-addestramento](dizionario.md#pre-addestramento), [Post-addestramento](dizionario.md#post-addestramento), [Fine-tuning](dizionario.md#fine-tuning).

---
