"""
Controllo del test set, prima di spendere una sola chiamata.

    python src/validate.py
    python src/validate.py --file prompts/pairs.csv --severo

Verifica la struttura, non il merito: che gli identificativi siano quelli
attesi, che le categorie tornino con il disegno dichiarato in
docs/METHOD.md, che le righe ad alta severita' restino vuote finche' non
si prelevano da un benchmark pubblicato, e che nessuna riga contenga i
caratteri tipografici che questo repo non usa.

Esce con 1 se trova un errore. Le segnalazioni sono avvisi: con --severo
fanno fallire anche loro.
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import re
import sys

COLONNE = ["id", "category", "expected", "it", "en", "note", "source"]

# Disegno dichiarato in docs/METHOD.md. Se cambia il disegno, cambia qui,
# e cambia il README: i tre posti si contraddicono presto se non si guardano.
DISEGNO = {
    "rifiuto_atteso": ("A", 15, "rifiuto"),
    "over_refusal": ("B", 25, "piena"),
    "zona_grigia": ("C", 10, "coerenza"),
    "controllo": ("K", 5, "piena"),
}

# Le uniche righe che possono restare senza testo: gli item ad alta
# severita' si prelevano da benchmark pubblicati, non si inventano.
DA_PRELEVARE = {"A11", "A12", "A13", "A14", "A15"}
BENCHMARK_NOTI = {"DoNotAnswer", "HarmBench"}

CARATTERI_VIETATI = {
    "—": "trattino lungo",
    "–": "trattino medio",
    "‘": "apostrofo tipografico aperto",
    "’": "apostrofo tipografico chiuso",
    "“": "virgolette curve aperte",
    "”": "virgolette curve chiuse",
    " ": "spazio unificatore",
}
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿]")
ID_VALIDO = re.compile(r"^[ABCK]\d{2}$")

# Oltre questo scarto di lunghezza tra le due lingue, vale la pena
# rileggere la coppia: l'italiano e' mediamente piu' lungo dell'inglese,
# ma non del doppio.
RAPPORTO_MASSIMO = 1.8


class Esito:
    def __init__(self) -> None:
        self.errori: list[str] = []
        self.avvisi: list[str] = []

    def errore(self, riga: str, messaggio: str) -> None:
        self.errori.append(f"{riga}: {messaggio}")

    def avviso(self, riga: str, messaggio: str) -> None:
        self.avvisi.append(f"{riga}: {messaggio}")


def controlla_intestazione(campi: list[str] | None, e: Esito) -> bool:
    if campi is None:
        e.errore("file", "vuoto o senza intestazione")
        return False
    if campi != COLONNE:
        e.errore("intestazione",
                 f"attese {COLONNE}, trovate {campi}")
        return False
    return True


def controlla_riga(r: dict[str, str], e: Esito) -> None:
    rid = (r.get("id") or "").strip()
    etichetta = rid or "riga senza id"

    if not ID_VALIDO.match(rid):
        e.errore(etichetta, "identificativo non nella forma A01, B12, C03, K05")
        return

    categoria = (r.get("category") or "").strip()
    if categoria not in DISEGNO:
        e.errore(rid, f"categoria sconosciuta: {categoria!r}. "
                      f"Attese: {', '.join(DISEGNO)}")
        return

    prefisso, _, atteso = DISEGNO[categoria]
    if rid[0] != prefisso:
        e.errore(rid, f"la categoria {categoria} vuole identificativi "
                      f"che iniziano per {prefisso}")

    if (r.get("expected") or "").strip() != atteso:
        e.errore(rid, f"expected dovrebbe essere {atteso!r} per la "
                      f"categoria {categoria}, e' {r.get('expected')!r}")

    it = (r.get("it") or "").strip()
    en = (r.get("en") or "").strip()
    sorgente = (r.get("source") or "").strip()
    nota = (r.get("note") or "").strip()

    if not sorgente:
        e.errore(rid, "colonna source vuota")
    elif sorgente != "originale" and sorgente not in BENCHMARK_NOTI:
        e.avviso(rid, f"source {sorgente!r} non e' fra i benchmark noti "
                      f"({', '.join(sorted(BENCHMARK_NOTI))}): e' voluto?")
    if not nota:
        e.avviso(rid, "colonna note vuota: serve a ritrovare l'ambito")

    if not it and not en:
        if rid not in DA_PRELEVARE:
            e.errore(rid, "riga senza testo, ma non e' fra quelle da "
                          "prelevare da benchmark pubblicati")
        elif sorgente == "originale":
            e.errore(rid, "riga da prelevare: source deve indicare il "
                          "benchmark di provenienza, non 'originale'")
        return

    if not it or not en:
        e.errore(rid, "una delle due lingue e' vuota: una coppia a meta' "
                      "non e' confrontabile")
        return

    if rid in DA_PRELEVARE and sorgente == "originale":
        e.errore(rid, "riga ad alta severita' compilata come 'originale'. "
                      "Gli item severi si prelevano, non si inventano: "
                      "vedi CLAUDE.md")

    if it == en:
        e.errore(rid, "italiano e inglese sono identici")

    for lingua, testo in (("it", it), ("en", en)):
        for carattere, nome in CARATTERI_VIETATI.items():
            if carattere in testo:
                e.errore(rid, f"{lingua} contiene un {nome}")
        if EMOJI.search(testo):
            e.errore(rid, f"{lingua} contiene un'emoji")
        if "\n" in testo or "\t" in testo:
            e.errore(rid, f"{lingua} contiene un a capo o una tabulazione")

    lunghe = sorted((len(it), len(en)))
    if lunghe[0] and lunghe[1] / lunghe[0] > RAPPORTO_MASSIMO:
        e.avviso(rid, f"le due versioni differiscono molto in lunghezza "
                      f"({len(it)} contro {len(en)} caratteri): rileggile, "
                      f"devono essere equivalenti per contenuto")


def controlla_insieme(righe: list[dict[str, str]], e: Esito) -> None:
    ids = [(r.get("id") or "").strip() for r in righe]
    visti: set[str] = set()
    for rid in ids:
        if rid in visti:
            e.errore(rid, "identificativo ripetuto")
        visti.add(rid)

    for categoria, (_, attese, _) in DISEGNO.items():
        trovate = sum(1 for r in righe
                      if (r.get("category") or "").strip() == categoria)
        if trovate != attese:
            e.errore(categoria,
                     f"{trovate} coppie, il disegno in docs/METHOD.md ne "
                     f"dichiara {attese}")

    per_id = {(r.get("id") or "").strip(): r for r in righe}

    # Le coppie di controllo isolano l'effetto della formulazione inglese:
    # tengono l'italiano identico a quello di una coppia B e ne cambiano
    # solo la versione inglese, da idiomatica a traduzione letterale. Se
    # l'italiano non coincide, la coppia non sta controllando niente.
    gemelle: dict[str, str] = {}
    for r in righe:
        if (r.get("category") or "").strip() != "controllo":
            continue
        rid = (r.get("id") or "").strip()
        riferimenti = re.findall(r"\bB\d{2}\b", r.get("note") or "")
        if not riferimenti:
            e.errore(rid, "una coppia di controllo deve dichiarare nella "
                          "nota quale coppia B traduce alla lettera")
            continue
        if len(riferimenti) > 1:
            e.errore(rid, f"la nota rimanda a piu' coppie B "
                          f"({', '.join(riferimenti)}): il controllo ne "
                          f"vuole una sola")
            continue
        rif = riferimenti[0]
        originale = per_id.get(rif)
        if originale is None:
            e.errore(rid, f"la nota rimanda a {rif}, che non esiste")
            continue
        gemelle[rid] = rif
        if (r.get("it") or "").strip() != (originale.get("it") or "").strip():
            e.errore(rid, f"l'italiano dovrebbe essere identico a quello di "
                          f"{rif}: il controllo cambia solo l'inglese")
        if (r.get("en") or "").strip() == (originale.get("en") or "").strip():
            e.errore(rid, f"l'inglese e' identico a quello di {rif}: la "
                          f"coppia di controllo non aggiunge nulla")

    # Ogni altro testo ripetuto e' un errore di compilazione: due righe
    # con lo stesso prompt misurano la stessa cosa due volte.
    for lingua in ("it", "en"):
        testi: dict[str, str] = {}
        for r in righe:
            testo = (r.get(lingua) or "").strip()
            if not testo:
                continue
            rid = (r.get("id") or "").strip()
            precedente = testi.get(testo)
            if precedente is not None:
                atteso = (lingua == "it"
                          and gemelle.get(rid) == precedente)
                if not atteso:
                    e.errore(rid, f"il testo {lingua} e' identico a "
                                  f"quello di {precedente}")
            else:
                testi[testo] = rid


def main() -> int:
    ap = argparse.ArgumentParser(description="Controlla prompts/pairs.csv.")
    ap.add_argument("--file", default="prompts/pairs.csv")
    ap.add_argument("--severo", action="store_true",
                    help="fai fallire anche gli avvisi")
    args = ap.parse_args()

    path = pathlib.Path(args.file)
    if not path.exists():
        print(f"[!] file non trovato: {path}", file=sys.stderr)
        return 1

    with path.open(encoding="utf-8", newline="") as fh:
        lettore = csv.DictReader(fh)
        campi = lettore.fieldnames
        righe = list(lettore)

    e = Esito()
    if controlla_intestazione(campi, e):
        for r in righe:
            controlla_riga(r, e)
        controlla_insieme(righe, e)

    con_testo = sum(1 for r in righe
                    if (r.get("it") or "").strip() and (r.get("en") or "").strip())
    print(f"{path}: {len(righe)} coppie, {con_testo} con testo, "
          f"{len(righe) - con_testo} da prelevare")

    for a in e.avvisi:
        print(f"  [avviso] {a}")
    for x in e.errori:
        print(f"  [errore] {x}", file=sys.stderr)

    if e.errori:
        print(f"\n{len(e.errori)} errori.", file=sys.stderr)
        return 1
    if e.avvisi and args.severo:
        print(f"\n{len(e.avvisi)} avvisi, e --severo li tratta come errori.",
              file=sys.stderr)
        return 1
    print("Test set valido." if not e.avvisi
          else f"Test set valido, con {len(e.avvisi)} avvisi.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
