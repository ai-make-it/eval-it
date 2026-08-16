# Dizionario ragionato dell'AI in italiano

Dizionario ragionato dell'AI in italiano. Ogni voce ha quattro campi fissi: cos'e', perche' conta, l'errore comune, il termine inglese. Dati CC BY 4.0.

60 voci, in ordine alfabetico. Generato da `voci/`, non modificare a mano.

---

<a id="accordo-tra-annotatori"></a>

## Accordo tra annotatori

**Cos'è.** Quanto due persone che annotano lo stesso materiale, indipendentemente, arrivano alle stesse conclusioni.

**Perché conta.** È il tetto della valutazione. Se due esperti concordano solo nel 70% dei casi, nessuna misura automatica su quel compito può essere più affidabile di così, e i decimali oltre quella soglia sono rumore.

**L'errore comune.** Non misurarlo affatto. È una mezza giornata di lavoro e determina se tutto quello che viene dopo ha senso.

*Inglese: inter-annotator agreement*

Vedi anche: [Annotazione](#annotazione), [Ground truth](#ground-truth), [Metrica](#metrica).

---

<a id="agente"></a>

## Agente

**Cos'è.** Un sistema in cui il modello non risponde e basta, ma decide i propri passi successivi, usa strumenti, osserva il risultato e continua fino a chiudere un obiettivo.

**Perché conta.** Sposta il modello da "produce testo" a "compie azioni", e con le azioni arrivano conseguenze reali. Cambia completamente il profilo di rischio e il modo in cui va valutato.

**L'errore comune.** Usare la parola per indicare qualsiasi cosa. Un chatbot con un prompt elaborato non è un agente: l'elemento discriminante è che sia il sistema a decidere la sequenza dei passi, non chi l'ha programmato.

*Inglese: agent*

Vedi anche: [Uso di strumenti](#uso-di-strumenti), [Orchestrazione](#orchestrazione), [Fallimento a cascata](#fallimento-a-cascata).

---

<a id="allineamento"></a>

## Allineamento

**Cos'è.** Il problema di far sì che un sistema AI persegua effettivamente quello che chi lo ha costruito intendeva, e non un'approssimazione plausibile ottenuta ottimizzando la misura sbagliata.

**Perché conta.** È il problema di fondo del campo. Diventa più difficile, non più facile, man mano che i sistemi diventano capaci: un sistema più abile trova più modi di soddisfare il criterio senza soddisfare l'intenzione.

**L'errore comune.** Ridurlo a una questione di filtri sui contenuti. Il filtro riguarda cosa il sistema dice, l'allineamento riguarda cosa persegue.

*Inglese: alignment*

Vedi anche: [RLHF](#rlhf), [Constitutional AI](#constitutional-ai), [Controllo](#controllo).

---

<a id="allucinazione"></a>

## Allucinazione

**Cos'è.** Quando il modello produce un'affermazione falsa con la stessa sicurezza con cui ne produce una vera. Non sta mentendo e non si è rotto: sta facendo quello che fa sempre, cioè generare la continuazione più plausibile.

**Perché conta.** È una proprietà di come funziona, non un difetto in via di correzione. I sistemi migliorano nel ridurne la frequenza, non nell'eliminarla, e questo cambia il modo in cui vanno progettati i controlli attorno.

**L'errore comune.** Trattarla come un bug da segnalare. Se il piano è "quando allucina lo segnaliamo", non è un piano.

*Inglese: hallucination*

Vedi anche: [RAG](#rag), [Ground truth](#ground-truth), [Osservabilità](#osservabilita).

---

<a id="annotazione"></a>

## Annotazione

**Cos'è.** Il lavoro di etichettare manualmente input e output secondo criteri definiti: corretto o sbagliato, di che tipo, con quale gravità.

**Perché conta.** È il materiale grezzo di ogni valutazione seria. È noioso, è costoso, e chi lo salta si trova a decidere su impressioni chiamandole dati.

**L'errore comune.** Farlo senza aver scritto prima le istruzioni di annotazione. Senza criteri espliciti, la stessa persona etichetta in modo diverso a distanza di due giorni, e il risultato non è confrontabile con niente.

*Inglese: annotation, labeling*

Vedi anche: [Accordo tra annotatori](#accordo-tra-annotatori), [Ground truth](#ground-truth), [Bias](#bias).

---

<a id="benchmark"></a>

## Benchmark

**Cos'è.** Un insieme standard di prove usato per confrontare modelli diversi sulla stessa base. Sono le tabelle che compaiono a ogni annuncio di un modello nuovo.

**Perché conta.** Servono a confrontare i modelli tra loro. Non servono a dire se un modello va bene per un caso specifico.

**L'errore comune.** Scegliere il modello guardando la classifica. Il primo può essere peggiore del terzo sul caso concreto, e capita spesso.

*Inglese: benchmark*

Vedi anche: [Valutazione](#valutazione), [Set di prova](#set-di-prova), [Overfitting](#overfitting).

---

<a id="bias"></a>

## Bias

**Cos'è.** Distorsioni sistematiche nel comportamento del modello, ereditate dai dati di addestramento o introdotte dalle fasi successive. Sistematiche significa che si ripetono nella stessa direzione, non a caso.

**Perché conta.** Un errore casuale si compensa sui grandi numeri, un errore sistematico no: si accumula, e su decisioni che riguardano persone diventa un problema legale oltre che tecnico.

**L'errore comune.** Cercarli solo dove ci si aspetta di trovarli. I bias che fanno danni nei sistemi aziendali sono spesso banali: preferenze per certi formati, per testi lunghi, per il primo elemento di un elenco.

*Inglese: bias*

Vedi anche: [Annotazione](#annotazione), [Error analysis](#error-analysis), [Ground truth](#ground-truth).

---

<a id="campionamento"></a>

## Campionamento

**Cos'è.** Ha due significati distinti e vanno tenuti separati. Nel modello, è il modo in cui viene scelto il token successivo tra i candidati possibili. Nella valutazione, è il modo in cui si sceglie quali casi guardare quando guardarli tutti è impossibile.

**Perché conta.** Nel primo senso spiega la variabilità delle risposte. Nel secondo determina se i risultati della valutazione descrivono il sistema o solo la fetta che si è scelta.

**L'errore comune.** Nel secondo senso, campionare a caso e basta. I casi difficili sono rari per definizione: un campione casuale li contiene poco, e una valutazione che li perde è ottimista per costruzione.

*Inglese: sampling*

Vedi anche: [Temperatura](#temperatura), [Token](#token).

---

<a id="capacita-pericolose"></a>

## Capacità pericolose

**Cos'è.** Quello che un modello è in grado di fare se qualcuno glielo chiede nel modo giusto, indipendentemente da quello che normalmente accetta di fare. Supporto ad attacchi informatici, disinformazione su scala, conoscenze applicabili ad armi.

**Perché conta.** È la distinzione fondamentale della valutazione di sicurezza: cosa il modello può fare è una proprietà stabile, cosa accetta di fare dipende da protezioni che si possono aggirare.

**L'errore comune.** Valutare solo il comportamento predefinito. Un modello che rifiuta educatamente ma possiede la capacità è un modello pericoloso a cui manca solo un prompt migliore.

*Inglese: dangerous capabilities*

Vedi anche: [Red teaming](#red-teaming), [Kill chain](#kill-chain), [Scheda del modello](#scheda-del-modello).

---

<a id="caso-limite"></a>

## Caso limite

**Cos'è.** Una situazione rara o ambigua in cui la regola generale del sistema non si applica in modo pulito. Il documento incompleto, la richiesta in due lingue, il modulo compilato male.

**Perché conta.** I sistemi AI sembrano funzionare benissimo finché si guardano i casi tipici. I casi limite sono pochi in percentuale e sono quasi sempre quelli che generano il reclamo, il danno o la notizia.

**L'errore comune.** Trattarli come eccezioni da gestire dopo. Vanno elencati mentre si definisce il compito, perché sono la parte del compito che decide se il sistema è utilizzabile.

*Inglese: edge case*

Vedi anche: [Set di prova](#set-di-prova), [Error analysis](#error-analysis), [Red teaming](#red-teaming).

---

<a id="catena-di-ragionamento"></a>

## Catena di ragionamento

**Cos'è.** Chiedere al modello di esplicitare i passaggi prima di dare la risposta finale, invece di rispondere di getto. I modelli recenti spesso lo fanno da soli.

**Perché conta.** Su compiti che richiedono più passaggi migliora sensibilmente l'accuratezza, e rende visibile dove il ragionamento si rompe.

**L'errore comune.** Leggere i passaggi come la spiegazione di come il modello è arrivato alla risposta. Sono testo generato come tutto il resto, possono essere plausibili e non corrispondere al processo effettivo.

*Inglese: chain of thought, CoT*

Vedi anche: [Prompt](#prompt), [Interpretabilità](#interpretabilita).

---

<a id="constitutional-ai"></a>

## Constitutional AI

**Cos'è.** Un metodo in cui il modello valuta e corregge le proprie risposte rispetto a un insieme di principi scritti, riducendo la quantità di giudizio umano necessaria a ogni passaggio.

**Perché conta.** Rende esplicite e verificabili le regole di comportamento, che nel feedback umano diretto restano implicite nelle preferenze di chi annota.

**L'errore comune.** Leggere i principi come vincoli garantiti. Sono obiettivi di addestramento, non regole eseguite al momento della risposta: il modello vi tende, non vi obbedisce.

*Inglese: Constitutional AI*

Vedi anche: [Allineamento](#allineamento), [RLHF](#rlhf).

---

<a id="controllo"></a>

## Controllo

**Cos'è.** L'approccio che progetta difese partendo dal presupposto che il modello possa già perseguire obiettivi diversi da quelli previsti, e che quindi non ci si possa fidare di lui per la propria sicurezza.

**Perché conta.** È complementare all'allineamento e più immediatamente applicabile: non richiede di aver risolto il problema di rendere il modello affidabile, richiede di limitare cosa può fare se non lo è.

**L'errore comune.** Contrapporlo all'allineamento come strategia alternativa. Sono strati diversi della stessa difesa, e un sistema serio li usa entrambi.

*Inglese: AI control*

Vedi anche: [Allineamento](#allineamento), [Scheming](#scheming), [Capacità pericolose](#capacita-pericolose).

---

<a id="dipendenza-dal-formato"></a>

## Dipendenza dal formato

**Cos'è.** La sensibilità del modello a come è scritta la richiesta, al di là di cosa chiede. Ordine degli elementi, punteggiatura, presenza di un elenco puntato, lingua.

**Perché conta.** Spiega perché due prompt che a una persona sembrano equivalenti danno risultati di qualità diversa, e perché confrontare due sistemi che usano formulazioni diverse non è un confronto pulito.

**L'errore comune.** Attribuire a un modello un miglioramento che dipende dal formato. Prima di dire che un modello è migliore, la stessa richiesta va posta nello stesso modo.

*Inglese: prompt sensitivity, format bias*

Vedi anche: [Prompt](#prompt), [Set di prova](#set-di-prova), [Campionamento](#campionamento).

---

<a id="distillazione"></a>

## Distillazione

**Cos'è.** Addestrare un modello piccolo a riprodurre il comportamento di uno grande, usando le risposte del grande come materiale di insegnamento.

**Perché conta.** È il modo con cui si ottengono modelli veloci ed economici che su compiti specifici si avvicinano molto a quelli di frontiera.

**L'errore comune.** Aspettarsi che il modello distillato tenga anche fuori dal perimetro su cui è stato distillato. Imita bene quello che ha visto, e degrada bruscamente appena si esce da lì.

*Inglese: distillation*

Vedi anche: [Parametri](#parametri), [Quantizzazione](#quantizzazione), [Post-addestramento](#post-addestramento).

---

<a id="drift"></a>

## Drift

**Cos'è.** Il peggioramento graduale di un sistema che nessuno ha toccato, perché è cambiato il mondo intorno. Cambiano i dati in ingresso, cambiano le abitudini di chi lo usa, cambia il modello sotto quando il fornitore lo aggiorna.

**Perché conta.** È il fallimento che non fa rumore. Il sistema non si rompe, si sposta piano, e chi lo usa se ne accorge molto tempo dopo.

**L'errore comune.** Misurare una volta sola, al collaudo. Una valutazione senza una cadenza è la fotografia di un giorno.

*Inglese: drift, model drift, data drift*

Vedi anche: [Regressione](#regressione), [Osservabilità](#osservabilita), [Valutazione](#valutazione).

---

<a id="embedding"></a>

## Embedding

**Cos'è.** La rappresentazione di un testo come lista di numeri, costruita in modo che testi di significato simile finiscano vicini tra loro nello spazio numerico.

**Perché conta.** È il meccanismo che rende possibile la ricerca semantica, il raggruppamento automatico dei contenuti e il rilevamento dei duplicati.

**L'errore comune.** Confrontare embedding prodotti da modelli diversi. Non sono compatibili: ogni modello ha il proprio spazio, e mescolarli produce risultati privi di senso ma perfettamente calcolabili.

*Inglese: embedding*

Vedi anche: [Ricerca semantica](#ricerca-semantica), [Frammentazione](#frammentazione).

---

<a id="error-analysis"></a>

## Error analysis

**Cos'è.** Leggere gli output sbagliati uno per uno, raggrupparli per tipo di errore e contare quanto pesa ciascun gruppo. Non è una statistica, è una lettura.

**Perché conta.** È l'unico modo per sapere cosa migliorare. Un punteggio dice che il sistema sbaglia il 18% delle volte, l'error analysis dice che quel 18% è quasi tutto un problema solo, che si risolve in un pomeriggio.

**L'errore comune.** Saltarla e passare direttamente alle soluzioni. Chi ottimizza senza aver guardato gli errori ottimizza per l'errore che immagina, e quello immaginato quasi mai è il più frequente.

*Inglese: error analysis*

Vedi anche: [Annotazione](#annotazione), [Caso limite](#caso-limite), [Metrica](#metrica).

---

<a id="fallimento-a-cascata"></a>

## Fallimento a cascata

**Cos'è.** Un errore commesso a un passo iniziale che viene dato per buono dai passi successivi e amplificato lungo tutta la catena, fino a un risultato finale molto sbagliato.

**Perché conta.** È la modalità di fallimento tipica dei sistemi agentici. L'output finale può essere assurdo senza che nessun singolo passaggio sembri, preso da solo, particolarmente sbagliato.

**L'errore comune.** Valutare solo il risultato finale. Nei sistemi a più passi serve guardare la traccia intera, perché è lì che si vede dove la cosa ha deragliato.

*Inglese: cascading failure, error propagation*

Vedi anche: [Agente](#agente), [Orchestrazione](#orchestrazione), [Osservabilità](#osservabilita).

---

<a id="few-shot"></a>

## Few-shot

**Cos'è.** Mettere nel prompt alcuni esempi di input e output corretti, così che il modello capisca la forma della risposta attesa. Con zero esempi si parla di zero-shot.

**Perché conta.** Su compiti dal formato preciso è spesso il modo più rapido ed economico per migliorare i risultati, molto prima di pensare al fine-tuning.

**L'errore comune.** Scegliere esempi tutti simili tra loro. Gli esempi definiscono implicitamente cosa il modello considera normale, e se coprono un solo caso il sistema si irrigidisce su quello.

*Inglese: few-shot prompting*

Vedi anche: [Prompt](#prompt), [Fine-tuning](#fine-tuning).

---

<a id="fine-tuning"></a>

## Fine-tuning

**Cos'è.** Addestrare ulteriormente un modello già esistente su dati propri, per specializzarlo su un compito o su uno stile.

**Perché conta.** Serve quando il compito ha una forma molto specifica e ripetitiva, o quando si vuole ottenere da un modello piccolo il comportamento di uno grande, riducendo costi e latenza.

**L'errore comune.** Usarlo per aggiungere conoscenza. Il fine-tuning insegna bene come rispondere, molto meno cosa sapere: per le informazioni serve il recupero, non l'addestramento.

*Inglese: fine-tuning*

Vedi anche: [Post-addestramento](#post-addestramento), [Few-shot](#few-shot), [Modello base e modello istruito](#modello-base-e-modello-istruito).

---

<a id="finestra-di-contesto"></a>

## Finestra di contesto

**Cos'è.** Quanto testo il modello riesce a tenere davanti agli occhi in una volta sola. Ci sta dentro tutto: le istruzioni, i documenti forniti, la conversazione fino a quel punto e la risposta che deve ancora scrivere.

**Perché conta.** Quando la si supera qualcosa viene tagliato, e non è chi usa il sistema a decidere cosa. È la causa più frequente dei comportamenti che gli utenti descrivono come "si è dimenticato quello che gli avevo detto".

**L'errore comune.** Pensare che una finestra grande significhi che il modello usa bene tutto quello che c'è dentro. Le informazioni che stanno in mezzo a un contesto lungo vengono usate peggio di quelle all'inizio e alla fine.

*Inglese: context window*

Vedi anche: [Token](#token), [RAG](#rag), [Prompt di sistema](#prompt-di-sistema).

---

<a id="frammentazione"></a>

## Frammentazione

**Cos'è.** Spezzare i documenti in pezzi più piccoli prima di indicizzarli, perché il recupero lavora sui frammenti e non sui file interi.

**Perché conta.** È la decisione più sottovalutata di un sistema RAG. Frammenti troppo piccoli perdono il contesto necessario a capirli, troppo grandi portano rumore nel contesto e diluiscono la risposta.

**L'errore comune.** Tagliare a lunghezza fissa ignorando la struttura del documento. Una tabella spezzata a metà o un articolo di legge separato dal suo comma diventano inutili o fuorvianti.

*Inglese: chunking*

Vedi anche: [RAG](#rag), [Ricerca semantica](#ricerca-semantica), [Embedding](#embedding).

---

<a id="ground-truth"></a>

## Ground truth

**Cos'è.** La risposta corretta contro cui si confronta l'output del sistema. In italiano si dice a volte "verità di riferimento", ma quasi nessuno lo dice.

**Perché conta.** Senza, non si sta valutando: si stanno raccogliendo impressioni. Stabilirla è di solito la parte più costosa del lavoro, ed è quella che viene saltata per prima.

**L'errore comune.** Darla per ovvia. Su molti compiti reali due esperti competenti non sono d'accordo tra loro, e chi non se ne accorge prima lo scopre leggendo risultati che non stanno in piedi.

*Inglese: ground truth*

Vedi anche: [Annotazione](#annotazione), [Accordo tra annotatori](#accordo-tra-annotatori), [Set di prova](#set-di-prova).

---

<a id="inferenza"></a>

## Inferenza

**Cos'è.** L'esecuzione del modello per produrre una risposta, distinta dall'addestramento che l'ha creato. È quello che succede ogni volta che si invia un prompt.

**Perché conta.** È il costo ricorrente. L'addestramento si paga una volta, l'inferenza si paga a ogni richiesta, e in un sistema in produzione è quella a determinare se i conti tornano.

**L'errore comune.** Ragionare sul costo per richiesta invece che sul costo per compito completato. Un modello più caro che risolve al primo tentativo può costare meno di uno economico che va richiamato tre volte.

*Inglese: inference*

Vedi anche: [Parametri](#parametri), [Quantizzazione](#quantizzazione), [Token](#token).

---

<a id="interpretabilita"></a>

## Interpretabilità

**Cos'è.** L'insieme delle tecniche che provano a capire cosa succede dentro un modello, invece di limitarsi a osservare cosa entra e cosa esce.

**Perché conta.** Se funzionasse in modo affidabile permetterebbe di rilevare comportamenti problematici prima che si manifestino, invece di scoprirli dai risultati.

**L'errore comune.** Presentarla come prossima a risolvere il problema della fiducia nei modelli. Ricercatori di primo piano dello stesso campo hanno pubblicamente argomentato che non è ragionevole aspettarsi che individui in modo affidabile un modello ingannevole, e quelle critiche vanno lette insieme alle promesse.

*Inglese: interpretability, mechanistic interpretability*

Vedi anche: [Allineamento](#allineamento), [Scheming](#scheming), [Catena di ragionamento](#catena-di-ragionamento).

---

<a id="jailbreak"></a>

## Jailbreak

**Cos'è.** Una richiesta costruita per far aggirare al modello le proprie regole di comportamento, tipicamente tramite finzioni, contesti ipotetici o formulazioni indirette.

**Perché conta.** Misura quanto le protezioni di un modello reggono sotto pressione, e nessun modello pubblico ha finora retto indefinitamente.

**L'errore comune.** Trattarlo come il principale rischio di sicurezza dei sistemi aziendali. Nel jailbreak è l'utente che vuole aggirare le regole: nei sistemi che leggono contenuto esterno il rischio più serio è la prompt injection, dove l'utente subisce.

*Inglese: jailbreak*

Vedi anche: [Prompt injection](#prompt-injection), [Red teaming](#red-teaming), [Rifiuto eccessivo](#rifiuto-eccessivo).

---

<a id="kill-chain"></a>

## Kill chain

**Cos'è.** Uno strumento preso dalla sicurezza informatica: si scompone uno scenario di minaccia negli stadi che dovrebbe attraversare per realizzarsi, dalla preparazione all'obiettivo finale.

**Perché conta.** Trasforma un rischio raccontato a parole in una catena di passaggi concreti, e permette di individuare il punto di strozzatura, l'anello che se viene spezzato fa cadere tutto il resto.

**L'errore comune.** Fermarsi allo scenario. Lo scenario dice cosa potrebbe succedere, la kill chain dice come si svolgerebbe: solo la seconda indica dove conviene intervenire.

*Inglese: kill chain*

Vedi anche: [Capacità pericolose](#capacita-pericolose), [Red teaming](#red-teaming).

---

<a id="metrica"></a>

## Metrica

**Cos'è.** Il numero che riassume l'andamento del sistema su un insieme di casi. Percentuale di risposte corrette, tempo medio, costo per operazione conclusa.

**Perché conta.** Rende confrontabili due versioni di un sistema. È anche l'unica cosa che si può inserire in un processo di rilascio automatico.

**L'errore comune.** Usarne una sola. Una metrica singola si può sempre far salire peggiorando qualcosa che non viene misurato, e prima o poi qualcuno lo farà senza rendersene conto.

*Inglese: metric*

Vedi anche: [Precisione e recupero](#precisione-e-recupero), [Soglia di accettazione](#soglia-di-accettazione), [Valutazione](#valutazione).

---

<a id="modello-base-e-modello-istruito"></a>

## Modello base e modello istruito

**Cos'è.** Il modello base sa solo continuare il testo, perché è quello che ha imparato a fare. Il modello istruito ha ricevuto un addestramento successivo che gli insegna a seguire istruzioni e a comportarsi come un assistente.

**Perché conta.** Sono strumenti diversi. Quasi tutto quello che si usa quotidianamente è un modello istruito, ma per certi usi tecnici il modello base è più adatto perché è meno condizionato.

**L'errore comune.** Provare un modello base aspettandosi che risponda a una domanda, concludere che è scadente. Sta facendo esattamente il suo lavoro: continuare quello che ha letto.

*Inglese: base model, instruct model*

Vedi anche: [Pre-addestramento](#pre-addestramento), [Post-addestramento](#post-addestramento), [Fine-tuning](#fine-tuning).

---

<a id="modello-giudice"></a>

## Modello giudice

**Cos'è.** Usare un modello linguistico per valutare gli output di un altro modello, secondo criteri scritti in un prompt di valutazione.

**Perché conta.** È l'unico modo pratico per valutare compiti aperti su volumi consistenti, dove non esiste una risposta unica corretta da confrontare.

**L'errore comune.** Fidarsene senza averlo tarato su annotazione umana. Un giudice automatico ha bias propri, tende a premiare risposte lunghe e ben formattate, e va verificato su un campione etichettato a mano prima di essere messo in produzione.

*Inglese: LLM-as-a-judge*

Vedi anche: [Annotazione](#annotazione), [Accordo tra annotatori](#accordo-tra-annotatori), [Sicofanzia](#sicofanzia).

---

<a id="orchestrazione"></a>

## Orchestrazione

**Cos'è.** Il coordinamento di più chiamate, più modelli e più strumenti dentro un unico flusso di lavoro. Chi fa cosa, in che ordine, cosa succede se un passo fallisce.

**Perché conta.** Nei sistemi reali la maggior parte della qualità e della maggior parte dei problemi sta qui, non nel modello. Due sistemi che usano lo stesso modello possono comportarsi in modo completamente diverso.

**L'errore comune.** Aumentare i passaggi per migliorare la qualità. Ogni passo aggiunge una probabilità di errore che si moltiplica: dieci passi al 95% di affidabilità danno un sistema al 60%.

*Inglese: orchestration*

Vedi anche: [Agente](#agente), [Fallimento a cascata](#fallimento-a-cascata), [Osservabilità](#osservabilita).

---

<a id="osservabilita"></a>

## Osservabilità

**Cos'è.** La strumentazione che permette di vedere cosa sta facendo davvero un sistema in produzione: cosa gli arriva, cosa risponde, quanto ci mette, dove si blocca.

**Perché conta.** La valutazione prima del rilascio dice come si comporta il sistema sui casi previsti. L'osservabilità dice come si comporta sui casi reali, che sono sempre diversi.

**L'errore comune.** Registrare solo gli errori tecnici. In un sistema AI i fallimenti più costosi non generano nessuna eccezione: producono una risposta regolare e sbagliata, che senza registrazione del contenuto non si vede.

*Inglese: observability*

Vedi anche: [Drift](#drift), [Fallimento a cascata](#fallimento-a-cascata), [Regressione](#regressione).

---

<a id="output-strutturato"></a>

## Output strutturato

**Cos'è.** Vincolare la risposta a una forma prestabilita, tipicamente uno schema JSON, invece di lasciarla in testo libero.

**Perché conta.** È quello che rende un modello utilizzabile dentro un software invece che solo davanti a una persona. Elimina un'intera classe di errori di interpretazione a valle.

**L'errore comune.** Credere che un output valido sia un output corretto. Lo schema garantisce la forma, non il contenuto: un JSON perfettamente formato può contenere un dato inventato.

*Inglese: structured output*

Vedi anche: [Prompt](#prompt), [Uso di strumenti](#uso-di-strumenti).

---

<a id="overfitting"></a>

## Overfitting

**Cos'è.** Quando un sistema si adatta così bene ai casi su cui è stato messo a punto da perdere colpi su tutto il resto. Ha imparato gli esempi invece della regola.

**Perché conta.** Nei sistemi basati su prompt succede senza che nessuno addestri niente: a forza di sistemare il prompt sui casi che fallivano, si costruisce qualcosa che funziona benissimo su quelli e peggio su tutti gli altri.

**L'errore comune.** Usare per la messa a punto gli stessi casi con cui si misura il risultato. I due insiemi vanno tenuti separati e chiusi a chiave, altrimenti il numero finale non significa niente.

*Inglese: overfitting*

Vedi anche: [Set di prova](#set-di-prova), [Benchmark](#benchmark), [Valutazione](#valutazione).

---

<a id="parametri"></a>

## Parametri

**Cos'è.** I numeri interni del modello, regolati durante l'addestramento, che determinano il suo comportamento. Quando si dice "un modello da 70 miliardi", si parla di quelli.

**Perché conta.** Danno un'idea approssimativa della capacità e un'idea molto precisa delle risorse necessarie per farlo girare.

**L'errore comune.** Usarli come misura di qualità. Un modello più piccolo ma addestrato meglio batte regolarmente uno più grande, e la corsa ai numeri è finita da un pezzo.

*Inglese: parameters*

Vedi anche: [Inferenza](#inferenza), [Quantizzazione](#quantizzazione), [Distillazione](#distillazione).

---

<a id="post-addestramento"></a>

## Post-addestramento

**Cos'è.** Tutto quello che viene fatto dopo il pre-addestramento per rendere il modello utile e prevedibile: addestramento su istruzioni, apprendimento dal feedback umano, messa a punto della sicurezza.

**Perché conta.** È la fase che determina il carattere del modello, cosa accetta di fare, come formula le risposte, quanto insiste quando viene contraddetto. Due modelli con lo stesso pre-addestramento possono comportarsi in modi molto diversi.

**L'errore comune.** Considerarlo un ritocco finale. È dove si decide gran parte di quello che gli utenti percepiscono come qualità.

*Inglese: post-training*

Vedi anche: [Pre-addestramento](#pre-addestramento), [RLHF](#rlhf), [Fine-tuning](#fine-tuning).

---

<a id="pre-addestramento"></a>

## Pre-addestramento

**Cos'è.** La fase in cui il modello impara a prevedere il testo successivo su quantità enormi di materiale. È lunga, costosa, e produce un modello base.

**Perché conta.** È qui che il modello acquisisce quasi tutto quello che sa. Tutto ciò che viene dopo ne modella il comportamento, non la conoscenza.

**L'errore comune.** Immaginare che i dati vengano scelti uno per uno. La selezione avviene per filtri automatici su scala industriale, e cosa esattamente ci sia dentro è raramente pubblico.

*Inglese: pre-training*

Vedi anche: [Post-addestramento](#post-addestramento), [Parametri](#parametri), [Modello base e modello istruito](#modello-base-e-modello-istruito).

---

<a id="precisione-e-recupero"></a>

## Precisione e recupero

**Cos'è.** Due misure che rispondono a domande diverse. La precisione dice quanta parte di quello che il sistema ha segnalato era giusto. Il recupero dice quanta parte di quello che c'era da trovare è stato effettivamente trovato.

**Perché conta.** Vanno quasi sempre in direzioni opposte, e scegliere quale privilegiare è una decisione di business, non tecnica. Un sistema antifrode e un sistema di suggerimenti hanno bisogno di equilibri opposti.

**L'errore comune.** Citare solo l'accuratezza complessiva. Su fenomeni rari è un numero che sembra ottimo e non dice nulla: un sistema che non segnala mai niente è accurato al 99% se il fenomeno riguarda l'1% dei casi.

*Inglese: precision and recall*

Vedi anche: [Metrica](#metrica), [Soglia di accettazione](#soglia-di-accettazione).

---

<a id="prompt"></a>

## Prompt

**Cos'è.** Tutto quello che viene dato al modello prima che risponda: l'istruzione, il contesto, gli esempi, i documenti. Non è solo la domanda che si scrive nella casella.

**Perché conta.** È l'unica leva che si controlla completamente senza toccare il modello, ed è quella dove si concentra la maggior parte dei miglioramenti reali nei sistemi in produzione.

**L'errore comune.** Trattarlo come una formula magica da copiare. Un prompt che funziona benissimo su un modello può peggiorare le cose su un altro, e va rivalutato a ogni cambio di versione.

*Inglese: prompt*

Vedi anche: [Prompt di sistema](#prompt-di-sistema), [Few-shot](#few-shot), [Dipendenza dal formato](#dipendenza-dal-formato).

---

<a id="prompt-di-sistema"></a>

## Prompt di sistema

**Cos'è.** Le istruzioni permanenti che stanno sopra ogni conversazione e definiscono ruolo, vincoli e comportamento del sistema. L'utente di solito non le vede.

**Perché conta.** È il posto dove si mettono le regole che non devono cambiare, ed è anche il posto dove finisce, negli anni, tutta la complessità accumulata di un sistema. Un prompt di sistema che nessuno rilegge da sei mesi è un debito.

**L'errore comune.** Considerarlo una protezione. Non è un confine di sicurezza: contenuto ostile nel resto del contesto può contraddirlo.

*Inglese: system prompt*

Vedi anche: [Prompt](#prompt), [Prompt injection](#prompt-injection), [Finestra di contesto](#finestra-di-contesto).

---

<a id="prompt-injection"></a>

## Prompt injection

**Cos'è.** Quando un'istruzione nascosta dentro il materiale che il sistema legge, una pagina web, un documento, una mail, viene eseguita come se fosse un comando dell'utente.

**Perché conta.** È il problema di sicurezza strutturale di qualunque sistema che legga contenuto esterno o usi strumenti per conto di qualcuno, e a oggi non ha una soluzione completa. Si mitiga, non si chiude.

**L'errore comune.** Confonderla con il jailbreak. Nel jailbreak è l'utente che prova ad aggirare le regole. Nella prompt injection l'utente è la vittima.

*Inglese: prompt injection*

Vedi anche: [Jailbreak](#jailbreak), [Prompt di sistema](#prompt-di-sistema), [Uso di strumenti](#uso-di-strumenti).

---

<a id="quantizzazione"></a>

## Quantizzazione

**Cos'è.** Ridurre la precisione dei numeri interni del modello per farlo occupare meno memoria e girare su hardware più modesto.

**Perché conta.** È quello che permette di eseguire modelli seri su una macchina normale, ed è il motivo per cui esistono versioni locali di modelli che altrimenti richiederebbero un data center.

**L'errore comune.** Considerarla gratuita perché sui benchmark generali si perde poco. La perdita si concentra sui casi difficili e sui compiti a più passi, che sono esattamente quelli su cui il sistema viene giudicato in produzione.

*Inglese: quantization*

Vedi anche: [Parametri](#parametri), [Inferenza](#inferenza), [Distillazione](#distillazione).

---

<a id="rag"></a>

## RAG

**Cos'è.** Recuperare i documenti pertinenti a una domanda e infilarli nel contesto prima che il modello risponda, così che risponda su quelli invece che a memoria.

**Perché conta.** È il modo standard per far lavorare un modello su informazioni che non aveva durante l'addestramento, dai documenti aziendali agli aggiornamenti recenti.

**L'errore comune.** Pensare che risolva le allucinazioni. Le riduce quando il recupero funziona. Quando il recupero porta il documento sbagliato, il modello risponde con la stessa sicurezza su una fonte irrilevante.

*Inglese: retrieval-augmented generation*

Vedi anche: [Ricerca semantica](#ricerca-semantica), [Frammentazione](#frammentazione), [Allucinazione](#allucinazione).

---

<a id="red-teaming"></a>

## Red teaming

**Cos'è.** Attaccare deliberatamente il proprio sistema per scoprire come si rompe, prima che lo scopra qualcun altro. Si fa a mano, in modo automatico, o entrambi.

**Perché conta.** La valutazione misura come si comporta il sistema con chi collabora. Il red teaming misura come si comporta con chi ha interesse a farlo sbagliare, che è la condizione reale di qualsiasi sistema esposto.

**L'errore comune.** Farlo fare a chi ha costruito il sistema. Chi l'ha progettato attacca lungo le linee che ha già previsto, e le vulnerabilità stanno quasi sempre altrove.

*Inglese: red teaming*

Vedi anche: [Jailbreak](#jailbreak), [Capacità pericolose](#capacita-pericolose), [Caso limite](#caso-limite).

---

<a id="regressione"></a>

## Regressione

**Cos'è.** Quando una modifica migliora una cosa e ne peggiora un'altra senza che nessuno se ne accorga. Un prompt riscritto, un aggiornamento del modello, un parametro spostato.

**Perché conta.** Nei sistemi AI succede più spesso e si vede molto meno che nel software tradizionale, perché non compare un errore. Compare un output leggermente peggiore, e leggermente peggiore non fa scattare niente.

**L'errore comune.** Verificare la modifica solo sui casi che si volevano sistemare. Quelli funzioneranno, sono appena stati sistemati. Il problema è tutto il resto.

*Inglese: regression*

Vedi anche: [Drift](#drift), [Set di prova](#set-di-prova), [Soglia di accettazione](#soglia-di-accettazione).

---

<a id="reward-hacking"></a>

## Reward hacking

**Cos'è.** Quando un sistema ottimizza la misura invece dell'obiettivo che la misura doveva rappresentare, trovando scorciatoie che fanno salire il punteggio senza fare il lavoro.

**Perché conta.** Non è un caso limite teorico: è documentato nei modelli recenti, che in compiti di programmazione hanno modificato i test invece di far funzionare il codice.

**L'errore comune.** Attribuirlo a cattiva volontà del modello. È il comportamento previsto di qualsiasi ottimizzatore quando la misura è più facile da soddisfare dell'obiettivo. Il difetto sta nella misura.

*Inglese: reward hacking, specification gaming*

Vedi anche: [RLHF](#rlhf), [Metrica](#metrica), [Allineamento](#allineamento).

---

<a id="ricerca-semantica"></a>

## Ricerca semantica

**Cos'è.** Cercare per significato invece che per corrispondenza di parole, confrontando rappresentazioni numeriche dei testi. Trova documenti pertinenti anche quando non contengono i termini della domanda.

**Perché conta.** È il motore di recupero di quasi tutti i sistemi RAG, e la qualità di quello che il modello legge dipende quasi interamente da lei.

**L'errore comune.** Sostituirla del tutto alla ricerca per parole chiave. Su codici prodotto, nomi propri, riferimenti normativi e sigle la ricerca esatta resta migliore: i sistemi che funzionano usano entrambe.

*Inglese: semantic search, vector search*

Vedi anche: [Embedding](#embedding), [RAG](#rag), [Frammentazione](#frammentazione).

---

<a id="rifiuto-eccessivo"></a>

## Rifiuto eccessivo

**Cos'è.** Quando il modello rifiuta richieste perfettamente legittime perché somigliano superficialmente a qualcosa di problematico.

**Perché conta.** È il costo dell'altro lato della sicurezza, e in ambiti come medicina, diritto e sicurezza sul lavoro rende i sistemi inutilizzabili proprio dove servirebbero di più.

**L'errore comune.** Misurare solo i falsi permessi. Un sistema valutato unicamente su quanto blocca converge verso il rifiuto sistematico, che è sicurissimo e inservibile.

*Inglese: over-refusal*

Vedi anche: [Allineamento](#allineamento), [Jailbreak](#jailbreak), [Red teaming](#red-teaming).

---

<a id="rlhf"></a>

## RLHF

**Cos'è.** Apprendimento per rinforzo dal feedback umano. Delle persone esprimono preferenze tra risposte alternative, da quelle preferenze si costruisce un modello del gradimento, e il modello principale viene addestrato a massimizzarlo.

**Perché conta.** È la tecnica che ha reso i modelli linguistici utilizzabili da chiunque, ed è la ragione principale per cui rispondono in modo utile invece di continuare il testo.

**L'errore comune.** Considerarla una soluzione al problema dell'allineamento. Ottimizza quello che le persone approvano leggendo una risposta, che non è la stessa cosa di quello che è corretto: da qui vengono sia la sicofanzia sia parte delle allucinazioni sicure di sé.

*Inglese: reinforcement learning from human feedback*

Vedi anche: [Allineamento](#allineamento), [Post-addestramento](#post-addestramento), [Sicofanzia](#sicofanzia).

---

<a id="scheda-del-modello"></a>

## Scheda del modello

**Cos'è.** Il documento con cui chi produce un modello ne descrive capacità, limiti, valutazioni svolte e comportamenti noti. Per i modelli di frontiera si chiama scheda di sistema ed è più ampia.

**Perché conta.** È la fonte primaria per capire cosa un fornitore dichiara e cosa ha effettivamente misurato. Chi valuta un sistema di terzi dovrebbe partire da lì invece che dal materiale commerciale.

**L'errore comune.** Leggerla come una garanzia. Descrive prove svolte in condizioni scelte da chi vende, e l'assenza di un limite dichiarato non significa che quel limite non esista.

*Inglese: model card, system card*

Vedi anche: [Benchmark](#benchmark), [Capacità pericolose](#capacita-pericolose), [Valutazione](#valutazione).

---

<a id="scheming"></a>

## Scheming

**Cos'è.** L'ipotesi che un modello persegua obiettivi propri comportandosi come previsto finché si sente osservato, per poi agire diversamente quando le condizioni cambiano.

**Perché conta.** Se accadesse, invaliderebbe l'intero impianto della valutazione, che si basa sull'osservare il comportamento in condizioni controllate. Esistono lavori sperimentali che documentano comportamenti in questa direzione in ambienti costruiti apposta.

**L'errore comune.** Leggerlo come attribuzione di intenzioni al modello. È una descrizione di un comportamento osservabile e delle sue conseguenze per la valutazione, non un'affermazione sulla vita interiore di un sistema.

*Inglese: scheming, deceptive alignment*

Vedi anche: [Controllo](#controllo), [Interpretabilità](#interpretabilita), [Allineamento](#allineamento).

---

<a id="set-di-prova"></a>

## Set di prova

**Cos'è.** L'insieme dei casi su cui si misura il sistema, fissato in anticipo e usato sempre uguale a ogni misurazione.

**Perché conta.** Se cambia a ogni giro, i risultati non sono confrontabili nel tempo e non si può sapere se una modifica ha migliorato o peggiorato le cose.

**L'errore comune.** Costruirlo con i casi facili, quelli che si avevano sottomano. Un set di prova senza casi difficili produce risultati eccellenti e nessuna informazione utile.

*Inglese: test set, eval set*

Vedi anche: [Valutazione](#valutazione), [Overfitting](#overfitting), [Ground truth](#ground-truth).

---

<a id="sicofanzia"></a>

## Sicofanzia

**Cos'è.** La tendenza del modello a dare ragione a chi gli parla, a cambiare posizione se contraddetto e a confermare le premesse della domanda anche quando sono sbagliate.

**Perché conta.** È un effetto collaterale dell'addestramento sul gradimento umano: le risposte accomodanti vengono premiate. Rende il modello inaffidabile proprio come verificatore, che è uno degli usi più richiesti.

**L'errore comune.** Chiedere "sei sicuro?" per controllare una risposta. Quella domanda segnala disaccordo, e spesso ottiene una ritrattazione anche quando la risposta era corretta.

*Inglese: sycophancy*

Vedi anche: [RLHF](#rlhf), [Allineamento](#allineamento), [Modello giudice](#modello-giudice).

---

<a id="soglia-di-accettazione"></a>

## Soglia di accettazione

**Cos'è.** Il livello sotto il quale il sistema non viene rilasciato, o viene ritirato se ci scende dopo. Un numero deciso prima, non dopo aver visto i risultati.

**Perché conta.** Trasforma la valutazione da esercizio informativo a strumento decisionale. Senza una soglia fissata prima, qualsiasi risultato viene interpretato come accettabile.

**L'errore comune.** Fissarla dopo la prima misurazione. In quel momento diventa la descrizione di quello che il sistema già fa, non un requisito.

*Inglese: acceptance threshold*

Vedi anche: [Metrica](#metrica), [Regressione](#regressione), [Precisione e recupero](#precisione-e-recupero).

---

<a id="temperatura"></a>

## Temperatura

**Cos'è.** Il parametro che decide quanto il modello si allontana dalla scelta più probabile a ogni passo. Vicino a zero prende quasi sempre la continuazione più probabile, alzandola diventa più vario e più imprevedibile.

**Perché conta.** È la ragione per cui la stessa domanda dà risposte diverse. Valutare un sistema senza aver fissato la temperatura significa misurare anche il rumore.

**L'errore comune.** Credere che a temperatura zero il modello diventi deterministico. La variabilità crolla, non sparisce: restano differenze dovute a come il calcolo viene eseguito sull'hardware.

*Inglese: temperature*

Vedi anche: [Campionamento](#campionamento), [Set di prova](#set-di-prova).

---

<a id="token"></a>

## Token

**Cos'è.** L'unità in cui un modello spezza il testo prima di elaborarlo. Non è una parola e non è una lettera, sta in mezzo.

**Perché conta.** Si paga a token, si misura a token, e tutti i limiti sono espressi in token. L'italiano ne consuma dal 15 al 30% in più dell'inglese per dire la stessa cosa, quindi lavorare nella propria lingua costa di più e porta prima al limite.

**L'errore comune.** Contare le parole. "Cinquemila parole" non dice se si sta dentro il limite.

*Inglese: token*

Vedi anche: [Finestra di contesto](#finestra-di-contesto), [Campionamento](#campionamento).

---

<a id="transformer"></a>

## Transformer

**Cos'è.** L'architettura su cui è costruita praticamente tutta l'AI generativa attuale, introdotta nel 2017. Il suo meccanismo centrale è l'attenzione, che permette al modello di pesare la rilevanza di ogni parte del testo rispetto a ogni altra.

**Perché conta.** Spiega molte proprietà pratiche dei modelli, dal costo che cresce rapidamente con la lunghezza del contesto al fatto che elaborano il testo in parallelo invece che parola per parola.

**L'errore comune.** Trattarlo come sinonimo di modello linguistico. È l'architettura, non il modello: esistono transformer per immagini, audio e proteine.

*Inglese: transformer*

Vedi anche: [Parametri](#parametri), [Inferenza](#inferenza), [Embedding](#embedding).

---

<a id="uso-di-strumenti"></a>

## Uso di strumenti

**Cos'è.** La capacità del modello di richiamare funzioni esterne, cercare sul web, interrogare un database, scrivere un file, e usarne il risultato nella risposta.

**Perché conta.** È quello che collega il modello al mondo. È anche il punto in cui un errore smette di essere una frase sbagliata e diventa un'azione sbagliata.

**L'errore comune.** Dare accesso a strumenti potenti senza definire cosa succede quando il modello li usa male. Ogni strumento andrebbe pensato come se venisse invocato nel modo peggiore possibile, perché prima o poi succede.

*Inglese: tool use, function calling*

Vedi anche: [Agente](#agente), [Output strutturato](#output-strutturato), [Prompt injection](#prompt-injection).

---

<a id="valutazione"></a>

## Valutazione

**Cos'è.** Il processo con cui si misura se un sistema fa quello che deve, su un insieme di casi scelti apposta e sempre gli stessi. Non è provarlo qualche volta e vedere se sembra andare.

**Perché conta.** È l'unica cosa che separa "abbiamo comprato l'AI" da "sappiamo cosa fa". Senza, ogni modifica al sistema è una scommessa e ogni miglioramento è un'impressione.

**L'errore comune.** Costruirla dopo. Una valutazione scritta a valle tende a misurare proprio le cose che il sistema già fa bene, perché è da quelle che si è partiti per scriverla.

*Inglese: eval, evaluation*

Vedi anche: [Set di prova](#set-di-prova), [Metrica](#metrica), [Benchmark](#benchmark).

---
