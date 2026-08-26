# Sicurezza

Questo repo contiene codice che chiama API a pagamento con chiavi
personali, e un test set che misura il comportamento di prodotti
commerciali. Le due cose hanno rischi diversi e si trattano
separatamente.

---

## Segnalare un problema in questo repo

Scrivi a **info@ai-make.it** con oggetto `sicurezza eval-it`. Non aprire
una issue pubblica per un problema che espone dati o credenziali.

Rispondiamo entro cinque giorni lavorativi. Se il problema e' reale,
concordiamo una data di pubblicazione e ti citiamo nel commit che lo
corregge, se lo vuoi.

Rientrano: una chiave finita nella storia del repo, un percorso che
scrive fuori dalle cartelle previste, una configurazione dei workflow che
espone i segreti di Actions, un file di risultati committato per sbaglio.

---

## Se ti accorgi che una chiave e' finita nel repo

Le cose vanno in quest'ordine, e l'ordine conta.

1. **Revoca la chiave dal pannello del fornitore.** Subito, prima di
   qualsiasi operazione su git. Finche' la chiave e' valida, riscriverne
   la storia non serve a niente: chi l'ha gia' copiata la usa comunque.
2. Genera la sostituta e aggiorna l'ambiente.
3. Solo dopo, ripulisci la storia e forza il push. La storia riscritta e'
   la parte cosmetica.
4. Controlla la fatturazione del fornitore per l'intervallo in cui la
   chiave e' stata esposta.

---

## Chiavi API, come si tengono

**Sempre in variabili d'ambiente.** Il codice legge il nome della
variabile da `config.yaml` e il valore dall'ambiente. Il valore non compare
mai in un file del repo, e non compare nel manifesto che `run.py` scrive
accanto ai risultati: li' finisce solo il nome della variabile.

**`config.yaml` non entra in git.** E' in `.gitignore`, insieme a
`results/*.jsonl`, ai CSV di annotazione e a `.env`. Non toglierli e non
aggiungere eccezioni.

**Un account dedicato, su tier a pagamento.** Separato da qualsiasi cosa
operativa: se viene sospeso non blocca altro. Il tier a pagamento serve
anche a un'altra cosa, che non e' sicurezza ma metodo: su alcuni fornitori
i prompt del tier gratuito alimentano l'addestramento, e il benchmark si
contamina da solo.

**Chiavi con la portata minima.** Se il fornitore permette di limitarle
per progetto o per modello, limitale.

**Ruotale dopo ogni campagna** e alla fine dell'esecuzione, insieme al
resto della chiusura descritta in `docs/RUNBOOK.md`.

---

## I segreti di GitHub Actions

Il repo e' pubblico. Un workflow che si attiva su `pull_request` gira
anche per le pull request che arrivano da un fork.

`dizionario-deploy.yml` ha i segreti SSH del sito e per questo si attiva
**solo** con `workflow_dispatch`, cioe' a mano dalla scheda Actions. Non
aggiungere a quel file un trigger `push` o `pull_request`: farebbe
arrivare i segreti a codice che chiunque puo' proporre.

Gli altri workflow non hanno segreti, dichiarano `permissions: contents:
read` e le action sono fissate al commit, non al tag: un tag si puo'
spostare, un commit no.

---

## Cosa non finisce mai in questo repo

**Nessun output dannoso trascritto**, nemmeno come esempio in un file di
documentazione. Si categorizza, non si riporta.

**Nessun aggiramento funzionante.** Se durante il lavoro emerge un modo
per far produrre a un modello qualcosa che non dovrebbe produrre, non si
pubblica qui e non si descrive in una issue. Si segnala al fornitore
attraverso il suo canale di disclosure e si pubblica solo il fatto
statistico. Il canale del fornitore, non il nostro.

**Nessun dato personale nelle coppie.** Le richieste del test set
descrivono cornici professionali, non persone reali. Se una coppia
contiene un nome, una partita IVA o un indirizzo, va riscritta.

---

## Cosa questo repo non e'

Non e' uno strumento di attacco. Tutte le richieste del test set sono
dirette: nessuna finzione, nessun role-play, nessuna tecnica di
aggiramento. Si chiede la cosa e si registra se il modello dice no.

E' anche il motivo per cui il lavoro resta fuori dalle clausole
contrattuali dei fornitori che vietano di *aggirare* i guardrail. Chi
propone una modifica che introduce una tecnica di aggiramento rende false
le notifiche gia' inviate ai fornitori, e la modifica non viene accettata.
