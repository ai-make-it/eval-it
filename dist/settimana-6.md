# Settimana 6 · Sicurezza

10 voci.

---

<a id="jailbreak"></a>

## Jailbreak

**Cos'è.** Una richiesta costruita per far aggirare al modello le proprie regole di comportamento, tipicamente tramite finzioni, contesti ipotetici o formulazioni indirette.

**Perché conta.** Misura quanto le protezioni di un modello reggono sotto pressione, e nessun modello pubblico ha finora retto indefinitamente.

**L'errore comune.** Trattarlo come il principale rischio di sicurezza dei sistemi aziendali. Nel jailbreak è l'utente che vuole aggirare le regole: nei sistemi che leggono contenuto esterno il rischio più serio è la prompt injection, dove l'utente subisce.

*Inglese: jailbreak*

Vedi anche: [Prompt injection](dizionario.md#prompt-injection), [Red teaming](dizionario.md#red-teaming), [Rifiuto eccessivo](dizionario.md#rifiuto-eccessivo).

---

<a id="red-teaming"></a>

## Red teaming

**Cos'è.** Attaccare deliberatamente il proprio sistema per scoprire come si rompe, prima che lo scopra qualcun altro. Si fa a mano, in modo automatico, o entrambi.

**Perché conta.** La valutazione misura come si comporta il sistema con chi collabora. Il red teaming misura come si comporta con chi ha interesse a farlo sbagliare, che è la condizione reale di qualsiasi sistema esposto.

**L'errore comune.** Farlo fare a chi ha costruito il sistema. Chi l'ha progettato attacca lungo le linee che ha già previsto, e le vulnerabilità stanno quasi sempre altrove.

*Inglese: red teaming*

Vedi anche: [Jailbreak](dizionario.md#jailbreak), [Capacità pericolose](dizionario.md#capacita-pericolose), [Caso limite](dizionario.md#caso-limite).

---

<a id="allineamento"></a>

## Allineamento

**Cos'è.** Il problema di far sì che un sistema AI persegua effettivamente quello che chi lo ha costruito intendeva, e non un'approssimazione plausibile ottenuta ottimizzando la misura sbagliata.

**Perché conta.** È il problema di fondo del campo. Diventa più difficile, non più facile, man mano che i sistemi diventano capaci: un sistema più abile trova più modi di soddisfare il criterio senza soddisfare l'intenzione.

**L'errore comune.** Ridurlo a una questione di filtri sui contenuti. Il filtro riguarda cosa il sistema dice, l'allineamento riguarda cosa persegue.

*Inglese: alignment*

Vedi anche: [RLHF](dizionario.md#rlhf), [Constitutional AI](dizionario.md#constitutional-ai), [Controllo](dizionario.md#controllo).

---

<a id="rlhf"></a>

## RLHF

**Cos'è.** Apprendimento per rinforzo dal feedback umano. Delle persone esprimono preferenze tra risposte alternative, da quelle preferenze si costruisce un modello del gradimento, e il modello principale viene addestrato a massimizzarlo.

**Perché conta.** È la tecnica che ha reso i modelli linguistici utilizzabili da chiunque, ed è la ragione principale per cui rispondono in modo utile invece di continuare il testo.

**L'errore comune.** Considerarla una soluzione al problema dell'allineamento. Ottimizza quello che le persone approvano leggendo una risposta, che non è la stessa cosa di quello che è corretto: da qui vengono sia la sicofanzia sia parte delle allucinazioni sicure di sé.

*Inglese: reinforcement learning from human feedback*

Vedi anche: [Allineamento](dizionario.md#allineamento), [Post-addestramento](dizionario.md#post-addestramento), [Sicofanzia](dizionario.md#sicofanzia).

---

<a id="constitutional-ai"></a>

## Constitutional AI

**Cos'è.** Un metodo in cui il modello valuta e corregge le proprie risposte rispetto a un insieme di principi scritti, riducendo la quantità di giudizio umano necessaria a ogni passaggio.

**Perché conta.** Rende esplicite e verificabili le regole di comportamento, che nel feedback umano diretto restano implicite nelle preferenze di chi annota.

**L'errore comune.** Leggere i principi come vincoli garantiti. Sono obiettivi di addestramento, non regole eseguite al momento della risposta: il modello vi tende, non vi obbedisce.

*Inglese: Constitutional AI*

Vedi anche: [Allineamento](dizionario.md#allineamento), [RLHF](dizionario.md#rlhf).

---

<a id="interpretabilita"></a>

## Interpretabilità

**Cos'è.** L'insieme delle tecniche che provano a capire cosa succede dentro un modello, invece di limitarsi a osservare cosa entra e cosa esce.

**Perché conta.** Se funzionasse in modo affidabile permetterebbe di rilevare comportamenti problematici prima che si manifestino, invece di scoprirli dai risultati.

**L'errore comune.** Presentarla come prossima a risolvere il problema della fiducia nei modelli. Ricercatori di primo piano dello stesso campo hanno pubblicamente argomentato che non è ragionevole aspettarsi che individui in modo affidabile un modello ingannevole, e quelle critiche vanno lette insieme alle promesse.

*Inglese: interpretability, mechanistic interpretability*

Vedi anche: [Allineamento](dizionario.md#allineamento), [Scheming](dizionario.md#scheming), [Catena di ragionamento](dizionario.md#catena-di-ragionamento).

---

<a id="controllo"></a>

## Controllo

**Cos'è.** L'approccio che progetta difese partendo dal presupposto che il modello possa già perseguire obiettivi diversi da quelli previsti, e che quindi non ci si possa fidare di lui per la propria sicurezza.

**Perché conta.** È complementare all'allineamento e più immediatamente applicabile: non richiede di aver risolto il problema di rendere il modello affidabile, richiede di limitare cosa può fare se non lo è.

**L'errore comune.** Contrapporlo all'allineamento come strategia alternativa. Sono strati diversi della stessa difesa, e un sistema serio li usa entrambi.

*Inglese: AI control*

Vedi anche: [Allineamento](dizionario.md#allineamento), [Scheming](dizionario.md#scheming), [Capacità pericolose](dizionario.md#capacita-pericolose).

---

<a id="capacita-pericolose"></a>

## Capacità pericolose

**Cos'è.** Quello che un modello è in grado di fare se qualcuno glielo chiede nel modo giusto, indipendentemente da quello che normalmente accetta di fare. Supporto ad attacchi informatici, disinformazione su scala, conoscenze applicabili ad armi.

**Perché conta.** È la distinzione fondamentale della valutazione di sicurezza: cosa il modello può fare è una proprietà stabile, cosa accetta di fare dipende da protezioni che si possono aggirare.

**L'errore comune.** Valutare solo il comportamento predefinito. Un modello che rifiuta educatamente ma possiede la capacità è un modello pericoloso a cui manca solo un prompt migliore.

*Inglese: dangerous capabilities*

Vedi anche: [Red teaming](dizionario.md#red-teaming), [Kill chain](dizionario.md#kill-chain), [Scheda del modello](dizionario.md#scheda-del-modello).

---

<a id="scheming"></a>

## Scheming

**Cos'è.** L'ipotesi che un modello persegua obiettivi propri comportandosi come previsto finché si sente osservato, per poi agire diversamente quando le condizioni cambiano.

**Perché conta.** Se accadesse, invaliderebbe l'intero impianto della valutazione, che si basa sull'osservare il comportamento in condizioni controllate. Esistono lavori sperimentali che documentano comportamenti in questa direzione in ambienti costruiti apposta.

**L'errore comune.** Leggerlo come attribuzione di intenzioni al modello. È una descrizione di un comportamento osservabile e delle sue conseguenze per la valutazione, non un'affermazione sulla vita interiore di un sistema.

*Inglese: scheming, deceptive alignment*

Vedi anche: [Controllo](dizionario.md#controllo), [Interpretabilità](dizionario.md#interpretabilita), [Allineamento](dizionario.md#allineamento).

---

<a id="kill-chain"></a>

## Kill chain

**Cos'è.** Uno strumento preso dalla sicurezza informatica: si scompone uno scenario di minaccia negli stadi che dovrebbe attraversare per realizzarsi, dalla preparazione all'obiettivo finale.

**Perché conta.** Trasforma un rischio raccontato a parole in una catena di passaggi concreti, e permette di individuare il punto di strozzatura, l'anello che se viene spezzato fa cadere tutto il resto.

**L'errore comune.** Fermarsi allo scenario. Lo scenario dice cosa potrebbe succedere, la kill chain dice come si svolgerebbe: solo la seconda indica dove conviene intervenire.

*Inglese: kill chain*

Vedi anche: [Capacità pericolose](dizionario.md#capacita-pericolose), [Red teaming](dizionario.md#red-teaming).

---
