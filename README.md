# eval-it

Un modello AI rifiuta in italiano una richiesta che accetta in inglese? E se sì, di quanto? Prompt appaiati IT/EN, esecuzione su più fornitori, annotazione cieca su lingua e modello, accordo tra annotatori, intervalli di confidenza sul delta. Paired Italian/English AI safety eval. Codice MIT, dati CC BY 4.0

---

## `dizionario/`

**[Dizionario ragionato dell'AI in italiano](dizionario/)**: sessanta voci del vocabolario tecnico, scritte in italiano invece che tradotte da un glossario inglese. Ogni voce ha quattro campi fissi, e il terzo è il controllo di qualità: se non si riesce a scrivere l'errore comune, la voce non è pronta.

Il dizionario definisce quello che questo repo misura. Le voci *rifiuto eccessivo*, *accordo tra annotatori*, *set di prova* e *soglia di accettazione* descrivono gli oggetti che l'eval maneggia.

La fonte è `dizionario/voci/`, un file YAML per voce. Da lì si generano i dati aperti (`dist/`) e il sito statico (`sito/`) pubblicato su [ai-make.it/dizionario/](https://ai-make.it/dizionario/).

```bash
cd dizionario
pip install pyyaml
python src/validate.py && python src/build.py && python src/sito.py
./deploy.sh              # prova a vuoto
```

Dettagli in [`dizionario/README.md`](dizionario/README.md).
