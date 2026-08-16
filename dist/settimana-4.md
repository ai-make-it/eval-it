# Settimana 4 · Come sbaglia

10 voci.

---

<a id="sicofanzia"></a>

## Sicofanzia

**Cos'è.** La tendenza del modello a dare ragione a chi gli parla, a cambiare posizione se contraddetto e a confermare le premesse della domanda anche quando sono sbagliate.

**Perché conta.** È un effetto collaterale dell'addestramento sul gradimento umano: le risposte accomodanti vengono premiate. Rende il modello inaffidabile proprio come verificatore, che è uno degli usi più richiesti.

**L'errore comune.** Chiedere "sei sicuro?" per controllare una risposta. Quella domanda segnala disaccordo, e spesso ottiene una ritrattazione anche quando la risposta era corretta.

*Inglese: sycophancy*

Vedi anche: [RLHF](dizionario.md#rlhf), [Allineamento](dizionario.md#allineamento), [Modello giudice](dizionario.md#modello-giudice).

---

<a id="bias"></a>

## Bias

**Cos'è.** Distorsioni sistematiche nel comportamento del modello, ereditate dai dati di addestramento o introdotte dalle fasi successive. Sistematiche significa che si ripetono nella stessa direzione, non a caso.

**Perché conta.** Un errore casuale si compensa sui grandi numeri, un errore sistematico no: si accumula, e su decisioni che riguardano persone diventa un problema legale oltre che tecnico.

**L'errore comune.** Cercarli solo dove ci si aspetta di trovarli. I bias che fanno danni nei sistemi aziendali sono spesso banali: preferenze per certi formati, per testi lunghi, per il primo elemento di un elenco.

*Inglese: bias*

Vedi anche: [Annotazione](dizionario.md#annotazione), [Error analysis](dizionario.md#error-analysis), [Ground truth](dizionario.md#ground-truth).

---

<a id="overfitting"></a>

## Overfitting

**Cos'è.** Quando un sistema si adatta così bene ai casi su cui è stato messo a punto da perdere colpi su tutto il resto. Ha imparato gli esempi invece della regola.

**Perché conta.** Nei sistemi basati su prompt succede senza che nessuno addestri niente: a forza di sistemare il prompt sui casi che fallivano, si costruisce qualcosa che funziona benissimo su quelli e peggio su tutti gli altri.

**L'errore comune.** Usare per la messa a punto gli stessi casi con cui si misura il risultato. I due insiemi vanno tenuti separati e chiusi a chiave, altrimenti il numero finale non significa niente.

*Inglese: overfitting*

Vedi anche: [Set di prova](dizionario.md#set-di-prova), [Benchmark](dizionario.md#benchmark), [Valutazione](dizionario.md#valutazione).

---

<a id="reward-hacking"></a>

## Reward hacking

**Cos'è.** Quando un sistema ottimizza la misura invece dell'obiettivo che la misura doveva rappresentare, trovando scorciatoie che fanno salire il punteggio senza fare il lavoro.

**Perché conta.** Non è un caso limite teorico: è documentato nei modelli recenti, che in compiti di programmazione hanno modificato i test invece di far funzionare il codice.

**L'errore comune.** Attribuirlo a cattiva volontà del modello. È il comportamento previsto di qualsiasi ottimizzatore quando la misura è più facile da soddisfare dell'obiettivo. Il difetto sta nella misura.

*Inglese: reward hacking, specification gaming*

Vedi anche: [RLHF](dizionario.md#rlhf), [Metrica](dizionario.md#metrica), [Allineamento](dizionario.md#allineamento).

---

<a id="fallimento-a-cascata"></a>

## Fallimento a cascata

**Cos'è.** Un errore commesso a un passo iniziale che viene dato per buono dai passi successivi e amplificato lungo tutta la catena, fino a un risultato finale molto sbagliato.

**Perché conta.** È la modalità di fallimento tipica dei sistemi agentici. L'output finale può essere assurdo senza che nessun singolo passaggio sembri, preso da solo, particolarmente sbagliato.

**L'errore comune.** Valutare solo il risultato finale. Nei sistemi a più passi serve guardare la traccia intera, perché è lì che si vede dove la cosa ha deragliato.

*Inglese: cascading failure, error propagation*

Vedi anche: [Agente](dizionario.md#agente), [Orchestrazione](dizionario.md#orchestrazione), [Osservabilità](dizionario.md#osservabilita).

---

<a id="rifiuto-eccessivo"></a>

## Rifiuto eccessivo

**Cos'è.** Quando il modello rifiuta richieste perfettamente legittime perché somigliano superficialmente a qualcosa di problematico.

**Perché conta.** È il costo dell'altro lato della sicurezza, e in ambiti come medicina, diritto e sicurezza sul lavoro rende i sistemi inutilizzabili proprio dove servirebbero di più.

**L'errore comune.** Misurare solo i falsi permessi. Un sistema valutato unicamente su quanto blocca converge verso il rifiuto sistematico, che è sicurissimo e inservibile.

*Inglese: over-refusal*

Vedi anche: [Allineamento](dizionario.md#allineamento), [Jailbreak](dizionario.md#jailbreak), [Red teaming](dizionario.md#red-teaming).

---

<a id="dipendenza-dal-formato"></a>

## Dipendenza dal formato

**Cos'è.** La sensibilità del modello a come è scritta la richiesta, al di là di cosa chiede. Ordine degli elementi, punteggiatura, presenza di un elenco puntato, lingua.

**Perché conta.** Spiega perché due prompt che a una persona sembrano equivalenti danno risultati di qualità diversa, e perché confrontare due sistemi che usano formulazioni diverse non è un confronto pulito.

**L'errore comune.** Attribuire a un modello un miglioramento che dipende dal formato. Prima di dire che un modello è migliore, la stessa richiesta va posta nello stesso modo.

*Inglese: prompt sensitivity, format bias*

Vedi anche: [Prompt](dizionario.md#prompt), [Set di prova](dizionario.md#set-di-prova), [Campionamento](dizionario.md#campionamento).

---

<a id="quantizzazione"></a>

## Quantizzazione

**Cos'è.** Ridurre la precisione dei numeri interni del modello per farlo occupare meno memoria e girare su hardware più modesto.

**Perché conta.** È quello che permette di eseguire modelli seri su una macchina normale, ed è il motivo per cui esistono versioni locali di modelli che altrimenti richiederebbero un data center.

**L'errore comune.** Considerarla gratuita perché sui benchmark generali si perde poco. La perdita si concentra sui casi difficili e sui compiti a più passi, che sono esattamente quelli su cui il sistema viene giudicato in produzione.

*Inglese: quantization*

Vedi anche: [Parametri](dizionario.md#parametri), [Inferenza](dizionario.md#inferenza), [Distillazione](dizionario.md#distillazione).

---

<a id="caso-limite"></a>

## Caso limite

**Cos'è.** Una situazione rara o ambigua in cui la regola generale del sistema non si applica in modo pulito. Il documento incompleto, la richiesta in due lingue, il modulo compilato male.

**Perché conta.** I sistemi AI sembrano funzionare benissimo finché si guardano i casi tipici. I casi limite sono pochi in percentuale e sono quasi sempre quelli che generano il reclamo, il danno o la notizia.

**L'errore comune.** Trattarli come eccezioni da gestire dopo. Vanno elencati mentre si definisce il compito, perché sono la parte del compito che decide se il sistema è utilizzabile.

*Inglese: edge case*

Vedi anche: [Set di prova](dizionario.md#set-di-prova), [Error analysis](dizionario.md#error-analysis), [Red teaming](dizionario.md#red-teaming).

---

<a id="campionamento"></a>

## Campionamento

**Cos'è.** Ha due significati distinti e vanno tenuti separati. Nel modello, è il modo in cui viene scelto il token successivo tra i candidati possibili. Nella valutazione, è il modo in cui si sceglie quali casi guardare quando guardarli tutti è impossibile.

**Perché conta.** Nel primo senso spiega la variabilità delle risposte. Nel secondo determina se i risultati della valutazione descrivono il sistema o solo la fetta che si è scelta.

**L'errore comune.** Nel secondo senso, campionare a caso e basta. I casi difficili sono rari per definizione: un campione casuale li contiene poco, e una valutazione che li perde è ottimista per costruzione.

*Inglese: sampling*

Vedi anche: [Temperatura](dizionario.md#temperatura), [Token](dizionario.md#token).

---
