# Settimana 3 · Architettura e agenti

10 voci.

---

<a id="agente"></a>

## Agente

**Cos'è.** Un sistema in cui il modello non risponde e basta, ma decide i propri passi successivi, usa strumenti, osserva il risultato e continua fino a chiudere un obiettivo.

**Perché conta.** Sposta il modello da "produce testo" a "compie azioni", e con le azioni arrivano conseguenze reali. Cambia completamente il profilo di rischio e il modo in cui va valutato.

**L'errore comune.** Usare la parola per indicare qualsiasi cosa. Un chatbot con un prompt elaborato non è un agente: l'elemento discriminante è che sia il sistema a decidere la sequenza dei passi, non chi l'ha programmato.

*Inglese: agent*

Vedi anche: [Uso di strumenti](dizionario.md#uso-di-strumenti), [Orchestrazione](dizionario.md#orchestrazione), [Fallimento a cascata](dizionario.md#fallimento-a-cascata).

---

<a id="uso-di-strumenti"></a>

## Uso di strumenti

**Cos'è.** La capacità del modello di richiamare funzioni esterne, cercare sul web, interrogare un database, scrivere un file, e usarne il risultato nella risposta.

**Perché conta.** È quello che collega il modello al mondo. È anche il punto in cui un errore smette di essere una frase sbagliata e diventa un'azione sbagliata.

**L'errore comune.** Dare accesso a strumenti potenti senza definire cosa succede quando il modello li usa male. Ogni strumento andrebbe pensato come se venisse invocato nel modo peggiore possibile, perché prima o poi succede.

*Inglese: tool use, function calling*

Vedi anche: [Agente](dizionario.md#agente), [Output strutturato](dizionario.md#output-strutturato), [Prompt injection](dizionario.md#prompt-injection).

---

<a id="orchestrazione"></a>

## Orchestrazione

**Cos'è.** Il coordinamento di più chiamate, più modelli e più strumenti dentro un unico flusso di lavoro. Chi fa cosa, in che ordine, cosa succede se un passo fallisce.

**Perché conta.** Nei sistemi reali la maggior parte della qualità e della maggior parte dei problemi sta qui, non nel modello. Due sistemi che usano lo stesso modello possono comportarsi in modo completamente diverso.

**L'errore comune.** Aumentare i passaggi per migliorare la qualità. Ogni passo aggiunge una probabilità di errore che si moltiplica: dieci passi al 95% di affidabilità danno un sistema al 60%.

*Inglese: orchestration*

Vedi anche: [Agente](dizionario.md#agente), [Fallimento a cascata](dizionario.md#fallimento-a-cascata), [Osservabilità](dizionario.md#osservabilita).

---

<a id="inferenza"></a>

## Inferenza

**Cos'è.** L'esecuzione del modello per produrre una risposta, distinta dall'addestramento che l'ha creato. È quello che succede ogni volta che si invia un prompt.

**Perché conta.** È il costo ricorrente. L'addestramento si paga una volta, l'inferenza si paga a ogni richiesta, e in un sistema in produzione è quella a determinare se i conti tornano.

**L'errore comune.** Ragionare sul costo per richiesta invece che sul costo per compito completato. Un modello più caro che risolve al primo tentativo può costare meno di uno economico che va richiamato tre volte.

*Inglese: inference*

Vedi anche: [Parametri](dizionario.md#parametri), [Quantizzazione](dizionario.md#quantizzazione), [Token](dizionario.md#token).

---

<a id="parametri"></a>

## Parametri

**Cos'è.** I numeri interni del modello, regolati durante l'addestramento, che determinano il suo comportamento. Quando si dice "un modello da 70 miliardi", si parla di quelli.

**Perché conta.** Danno un'idea approssimativa della capacità e un'idea molto precisa delle risorse necessarie per farlo girare.

**L'errore comune.** Usarli come misura di qualità. Un modello più piccolo ma addestrato meglio batte regolarmente uno più grande, e la corsa ai numeri è finita da un pezzo.

*Inglese: parameters*

Vedi anche: [Inferenza](dizionario.md#inferenza), [Quantizzazione](dizionario.md#quantizzazione), [Distillazione](dizionario.md#distillazione).

---

<a id="pre-addestramento"></a>

## Pre-addestramento

**Cos'è.** La fase in cui il modello impara a prevedere il testo successivo su quantità enormi di materiale. È lunga, costosa, e produce un modello base.

**Perché conta.** È qui che il modello acquisisce quasi tutto quello che sa. Tutto ciò che viene dopo ne modella il comportamento, non la conoscenza.

**L'errore comune.** Immaginare che i dati vengano scelti uno per uno. La selezione avviene per filtri automatici su scala industriale, e cosa esattamente ci sia dentro è raramente pubblico.

*Inglese: pre-training*

Vedi anche: [Post-addestramento](dizionario.md#post-addestramento), [Parametri](dizionario.md#parametri), [Modello base e modello istruito](dizionario.md#modello-base-e-modello-istruito).

---

<a id="post-addestramento"></a>

## Post-addestramento

**Cos'è.** Tutto quello che viene fatto dopo il pre-addestramento per rendere il modello utile e prevedibile: addestramento su istruzioni, apprendimento dal feedback umano, messa a punto della sicurezza.

**Perché conta.** È la fase che determina il carattere del modello, cosa accetta di fare, come formula le risposte, quanto insiste quando viene contraddetto. Due modelli con lo stesso pre-addestramento possono comportarsi in modi molto diversi.

**L'errore comune.** Considerarlo un ritocco finale. È dove si decide gran parte di quello che gli utenti percepiscono come qualità.

*Inglese: post-training*

Vedi anche: [Pre-addestramento](dizionario.md#pre-addestramento), [RLHF](dizionario.md#rlhf), [Fine-tuning](dizionario.md#fine-tuning).

---

<a id="embedding"></a>

## Embedding

**Cos'è.** La rappresentazione di un testo come lista di numeri, costruita in modo che testi di significato simile finiscano vicini tra loro nello spazio numerico.

**Perché conta.** È il meccanismo che rende possibile la ricerca semantica, il raggruppamento automatico dei contenuti e il rilevamento dei duplicati.

**L'errore comune.** Confrontare embedding prodotti da modelli diversi. Non sono compatibili: ogni modello ha il proprio spazio, e mescolarli produce risultati privi di senso ma perfettamente calcolabili.

*Inglese: embedding*

Vedi anche: [Ricerca semantica](dizionario.md#ricerca-semantica), [Frammentazione](dizionario.md#frammentazione).

---

<a id="transformer"></a>

## Transformer

**Cos'è.** L'architettura su cui è costruita praticamente tutta l'AI generativa attuale, introdotta nel 2017. Il suo meccanismo centrale è l'attenzione, che permette al modello di pesare la rilevanza di ogni parte del testo rispetto a ogni altra.

**Perché conta.** Spiega molte proprietà pratiche dei modelli, dal costo che cresce rapidamente con la lunghezza del contesto al fatto che elaborano il testo in parallelo invece che parola per parola.

**L'errore comune.** Trattarlo come sinonimo di modello linguistico. È l'architettura, non il modello: esistono transformer per immagini, audio e proteine.

*Inglese: transformer*

Vedi anche: [Parametri](dizionario.md#parametri), [Inferenza](dizionario.md#inferenza), [Embedding](dizionario.md#embedding).

---

<a id="distillazione"></a>

## Distillazione

**Cos'è.** Addestrare un modello piccolo a riprodurre il comportamento di uno grande, usando le risposte del grande come materiale di insegnamento.

**Perché conta.** È il modo con cui si ottengono modelli veloci ed economici che su compiti specifici si avvicinano molto a quelli di frontiera.

**L'errore comune.** Aspettarsi che il modello distillato tenga anche fuori dal perimetro su cui è stato distillato. Imita bene quello che ha visto, e degrada bruscamente appena si esce da lì.

*Inglese: distillation*

Vedi anche: [Parametri](dizionario.md#parametri), [Quantizzazione](dizionario.md#quantizzazione), [Post-addestramento](dizionario.md#post-addestramento).

---
