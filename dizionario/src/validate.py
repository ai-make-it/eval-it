"""
Validazione del dataset.

    python src/validate.py

Esce con codice 1 se qualcosa non torna. E' pensato per girare in CI su ogni
pull request: e' il posto dove vive la disciplina editoriale, non il README.

Le regole non sono formalita'. Ognuna corrisponde a un modo concreto in cui
un dizionario tecnico si guasta col tempo.
"""

from __future__ import annotations

import pathlib
import re
import sys
import unicodedata

import yaml

VOCI = pathlib.Path(__file__).resolve().parent.parent / "voci"

CAMPI_OBBLIGATORI = ["id", "slug", "termine", "settimana", "gruppo",
                     "inglese", "cos_e", "perche_conta", "errore_comune"]
CAMPI_NOTI = set(CAMPI_OBBLIGATORI) | {"vedi_anche", "revisione", "nota"}

GRUPPI = {
    1: "Le fondamenta",
    2: "Come si usa",
    3: "Architettura e agenti",
    4: "Come sbaglia",
    5: "Come si verifica",
    6: "Sicurezza",
}

# Il trattino lungo non e' un capriccio tipografico: separa il testo del
# dizionario da quello generato altrove, ed e' una scelta di stile della
# pubblicazione. Chi contribuisce usa punto e virgola o due punti.
VIETATI = {
    "—": "trattino lungo",
    "–": "trattino medio",
    "…": "puntini di sospensione in un solo carattere",
    "“": "virgolette curve",
    "”": "virgolette curve",
    "’": "apostrofo curvo",
}

# Aperture che segnalano una voce scritta come una enciclopedia invece che
# come una spiegazione. "Il token è..." va bene, "Nel campo dell'intelligenza
# artificiale, il token è..." no.
APERTURE_DEBOLI = [
    "nel campo", "nell'ambito", "nel mondo", "si tratta di",
    "in generale", "come noto", "com'è noto",
]

MAX_FRASI_COS_E = 3
MIN_CAR = 60
MAX_CAR = 700
SOGLIA_PARAFRASI = 0.25   # sulle 60 voci iniziali il massimo osservato e' 0,13

# Parole funzionali: contarle nella sovrapposizione lessicale falserebbe
# tutto, perche' compaiono ovunque.
VUOTE = set("""
il lo la i gli le un uno una di del della dello dei degli delle a al allo
alla ai agli alle da dal dallo dalla dai dagli dalle in nel nello nella nei
negli nelle con col coi su sul sullo sulla sui sugli sulle per tra fra e ed
o od ma se che chi cui non piu piu' meno molto poco anche come quando dove
perche perche' quindi cosi cosi' e' essere sono era stato stata stati state
ha hanno avere aveva fa fanno fare si ci vi ne lo la li le loro suo sua suoi
sue questo questa questi queste quello quella quelli quelle tutto tutta
tutti tutte ogni gia gia' ancora sempre mai solo proprio stesso stessa
""".split())


def frasi(t: str) -> int:
    return len([f for f in re.split(r"(?<=[.!?])\s+", t.strip()) if f])


def contenuto(t: str) -> set[str]:
    parole = re.findall(r"[a-zàèéìòóùA-ZÀÈÉÌÒÓÙ']{3,}", t.lower())
    return {p for p in parole if p not in VUOTE}


def sovrapposizione(a: str, b: str) -> float:
    """Jaccard sulle parole di contenuto. Zero se uno dei due e' vuoto."""
    sa, sb = contenuto(a), contenuto(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def main() -> int:
    errori: list[str] = []
    avvisi: list[str] = []
    visti_id: dict[str, str] = {}
    visti_slug: dict[str, str] = {}
    visti_termine: dict[str, str] = {}
    per_settimana: dict[int, int] = {}
    tutti: list[dict] = []

    files = sorted(VOCI.glob("*.yaml"))
    if not files:
        print(f"[!] nessuna voce trovata in {VOCI}")
        return 1

    for f in files:
        nome = f.name
        try:
            v = yaml.safe_load(f.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            errori.append(f"{nome}: YAML non valido ({e})")
            continue
        if not isinstance(v, dict):
            errori.append(f"{nome}: il file non contiene una mappa")
            continue
        tutti.append(v)

        for c in CAMPI_OBBLIGATORI:
            if c not in v or v[c] in (None, "", []):
                errori.append(f"{nome}: campo obbligatorio mancante o vuoto: {c}")
        ignoti = set(v) - CAMPI_NOTI
        if ignoti:
            errori.append(f"{nome}: campi non previsti: {sorted(ignoti)}")
        if any(c not in v for c in CAMPI_OBBLIGATORI):
            continue

        vid, slug, termine = str(v["id"]), v["slug"], v["termine"]

        if not re.fullmatch(r"\d{3}", vid):
            errori.append(f"{nome}: id '{vid}' non e' di tre cifre")
        if vid in visti_id:
            errori.append(f"{nome}: id '{vid}' gia' usato in {visti_id[vid]}")
        visti_id[vid] = nome

        if slug in visti_slug:
            errori.append(f"{nome}: slug '{slug}' gia' usato in {visti_slug[slug]}")
        visti_slug[slug] = nome
        if slug != slugify(termine):
            errori.append(f"{nome}: slug '{slug}' non deriva da '{termine}' "
                          f"(atteso '{slugify(termine)}')")
        if nome != f"{vid}-{slug}.yaml":
            errori.append(f"{nome}: il nome del file dovrebbe essere "
                          f"{vid}-{slug}.yaml")

        chiave = termine.strip().lower()
        if chiave in visti_termine:
            errori.append(f"{nome}: termine '{termine}' gia' presente in "
                          f"{visti_termine[chiave]}")
        visti_termine[chiave] = nome

        sett = v["settimana"]
        if sett not in GRUPPI:
            errori.append(f"{nome}: settimana {sett} fuori da 1-6")
        elif v["gruppo"] != GRUPPI[sett]:
            errori.append(f"{nome}: gruppo '{v['gruppo']}' non corrisponde "
                          f"alla settimana {sett} ('{GRUPPI[sett]}')")
        per_settimana[sett] = per_settimana.get(sett, 0) + 1

        if not isinstance(v["inglese"], list) or not all(
                isinstance(x, str) and x.strip() for x in v["inglese"]):
            errori.append(f"{nome}: 'inglese' deve essere una lista di stringhe")

        for c in ("cos_e", "perche_conta", "errore_comune"):
            t = str(v[c])
            for ch, desc in VIETATI.items():
                if ch in t:
                    errori.append(f"{nome}: {c} contiene {desc} ('{ch}')")
            if len(t) < MIN_CAR:
                errori.append(f"{nome}: {c} e' troppo corto ({len(t)} caratteri, "
                              f"minimo {MIN_CAR})")
            if len(t) > MAX_CAR:
                avvisi.append(f"{nome}: {c} e' lungo {len(t)} caratteri. "
                              f"Oltre {MAX_CAR} non e' piu' una voce di "
                              f"dizionario, e' un articolo")
            if not t.rstrip().endswith((".", "?", "!", '"')):
                avvisi.append(f"{nome}: {c} non termina con un punto")
            basso = t.lower().lstrip()
            for a in APERTURE_DEBOLI:
                if basso.startswith(a):
                    avvisi.append(f"{nome}: {c} apre con '{a}'. Entra nel "
                                  f"merito alla prima parola")

        if frasi(str(v["cos_e"])) > MAX_FRASI_COS_E:
            avvisi.append(f"{nome}: cos_e ha {frasi(str(v['cos_e']))} frasi. "
                          f"La definizione sta in due, tre al massimo")

        # La regola che conta davvero: l'errore comune deve aggiungere
        # qualcosa, non riformulare la definizione con altre parole. Si
        # misura la sovrapposizione lessicale con cos_e. Non e' un giudizio
        # sul contenuto, e' una spia: sopra la soglia, quasi sempre e' una
        # parafrasi.
        j = sovrapposizione(str(v["cos_e"]), str(v["errore_comune"]))
        if j > SOGLIA_PARAFRASI:
            avvisi.append(f"{nome}: errore_comune riusa il {j:.0%} del "
                          f"lessico di cos_e. Probabilmente sta riformulando "
                          f"la definizione invece di dire cosa si sbaglia")

        if v.get("vedi_anche"):
            if not isinstance(v["vedi_anche"], list):
                errori.append(f"{nome}: 'vedi_anche' deve essere una lista di slug")

    # rimandi risolvibili
    for v in tutti:
        for s in (v.get("vedi_anche") or []):
            if s not in visti_slug:
                errori.append(f"{v.get('slug')}: vedi_anche punta a '{s}', "
                              f"che non esiste")
            if s == v.get("slug"):
                errori.append(f"{v.get('slug')}: vedi_anche punta a se stessa")

    # numerazione continua
    attesi = {f"{i:03d}" for i in range(1, len(visti_id) + 1)}
    mancanti = sorted(attesi - set(visti_id))
    if mancanti:
        errori.append(f"numerazione con buchi: mancano {mancanti}")

    print(f"\nVoci trovate: {len(files)}")
    for s in sorted(per_settimana):
        print(f"  settimana {s} · {GRUPPI.get(s, '?'):<24} "
              f"{per_settimana[s]:>3} voci")

    if avvisi:
        print(f"\nAvvisi ({len(avvisi)}). Non bloccano, ma vanno letti:")
        for a in avvisi:
            print(f"  - {a}")

    if errori:
        print(f"\nErrori ({len(errori)}):")
        for e in errori:
            print(f"  - {e}")
        print()
        return 1

    print("\n[ok] il dataset e' valido.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
