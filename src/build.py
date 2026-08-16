"""
Rende il dataset nei formati che servono a chi lo usa.

    python src/build.py

Scrive in dist/:
    dizionario.json        tutte le voci, per chi programma
    dizionario.csv         tutte le voci, per chi apre un foglio di calcolo
    dizionario.md          il dizionario intero, in ordine alfabetico
    settimana-N.md         i sei gruppi di pubblicazione, uno per file
    indice-inglese.md      dall'inglese all'italiano

dist/ e' rigenerabile: non si modifica a mano, si modifica voci/ e si
rilancia. Se qualcuno corregge un refuso in dist/ la correzione sparisce
alla prima build, ed e' il comportamento voluto.
"""

from __future__ import annotations

import csv
import json
import pathlib
import unicodedata

import yaml

RADICE = pathlib.Path(__file__).resolve().parent.parent
VOCI = RADICE / "voci"
DIST = RADICE / "dist"

GRUPPI = {
    1: "Le fondamenta",
    2: "Come si usa",
    3: "Architettura e agenti",
    4: "Come sbaglia",
    5: "Come si verifica",
    6: "Sicurezza",
}

NOMI: dict[str, str] = {}

INTESTAZIONE = (
    "Dizionario ragionato dell'AI in italiano. Ogni voce ha quattro campi "
    "fissi: cos'e', perche' conta, l'errore comune, il termine inglese. "
    "Dati CC BY 4.0."
)


def chiave_ordinamento(t: str) -> str:
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def carica() -> list[dict]:
    voci = [yaml.safe_load(f.read_text(encoding="utf-8"))
            for f in sorted(VOCI.glob("*.yaml"))]
    return sorted(voci, key=lambda v: v["id"])


def blocco_md(v: dict, base: str = "") -> str:
    """Un'ancora esplicita: gli slug sono senza accenti, i titoli no, e
    l'ancora automatica di GitHub li terrebbe (osservabilita' / osservabilita)."""
    ing = ", ".join(v["inglese"])
    righe = [
        f'<a id="{v["slug"]}"></a>',
        "",
        f"## {v['termine']}",
        "",
        f"**Cos'è.** {v['cos_e']}",
        "",
        f"**Perché conta.** {v['perche_conta']}",
        "",
        f"**L'errore comune.** {v['errore_comune']}",
        "",
        f"*Inglese: {ing}*",
    ]
    if v.get("vedi_anche"):
        voci = ", ".join(f"[{NOMI.get(s, s)}]({base}#{s})"
                         for s in v["vedi_anche"])
        righe += ["", f"Vedi anche: {voci}."]
    return "\n".join(righe)


def main() -> int:
    voci = carica()
    DIST.mkdir(exist_ok=True)
    NOMI.update({v["slug"]: v["termine"] for v in voci})

    # JSON
    payload = {
        "nome": "Dizionario ragionato dell'AI in italiano",
        "licenza": "CC BY 4.0",
        "voci": voci,
    }
    (DIST / "dizionario.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")

    # CSV
    campi = ["id", "slug", "termine", "settimana", "gruppo", "inglese",
             "cos_e", "perche_conta", "errore_comune", "vedi_anche"]
    with (DIST / "dizionario.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campi)
        w.writeheader()
        for v in voci:
            r = {c: v.get(c, "") for c in campi}
            r["inglese"] = "; ".join(v["inglese"])
            r["vedi_anche"] = "; ".join(v.get("vedi_anche") or [])
            w.writerow(r)

    # Markdown completo, ordine alfabetico
    alfa = sorted(voci, key=lambda v: chiave_ordinamento(v["termine"]))
    testo = ["# Dizionario ragionato dell'AI in italiano", "",
             INTESTAZIONE, "",
             f"{len(voci)} voci, in ordine alfabetico. "
             f"Generato da `voci/`, non modificare a mano.", "", "---", ""]
    for v in alfa:
        testo += [blocco_md(v), "", "---", ""]
    (DIST / "dizionario.md").write_text("\n".join(testo), encoding="utf-8")

    # un file per gruppo di pubblicazione
    for s, nome in GRUPPI.items():
        gruppo = [v for v in voci if v["settimana"] == s]
        if not gruppo:
            continue
        t = [f"# Settimana {s} · {nome}", "",
             f"{len(gruppo)} voci.", "", "---", ""]
        for v in gruppo:
            t += [blocco_md(v, base="dizionario.md"), "", "---", ""]
        (DIST / f"settimana-{s}.md").write_text("\n".join(t), encoding="utf-8")

    # indice inglese -> italiano
    coppie = sorted(
        ((ing, v["termine"], v["slug"]) for v in voci for ing in v["inglese"]),
        key=lambda x: chiave_ordinamento(x[0]))
    t = ["# Dall'inglese all'italiano", "",
         "| Inglese | Italiano |", "|---|---|"]
    t += [f"| {ing} | [{it}](dizionario.md#{sl}) |" for ing, it, sl in coppie]
    (DIST / "indice-inglese.md").write_text("\n".join(t) + "\n",
                                            encoding="utf-8")

    print(f"[ok] {len(voci)} voci · {len(coppie)} termini inglesi")
    for f in sorted(DIST.iterdir()):
        print(f"     {f.name:<24} {f.stat().st_size:>7} byte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
