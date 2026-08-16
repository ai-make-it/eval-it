"""
Script usato una volta sola, per convertire il manoscritto originale in
voci strutturate. Resta nel repo per trasparenza: chi vuole verificare che
il dataset corrisponda al testo pubblicato puo' rieseguirlo.

    python src/_import_once.py sorgente.md

Non serve per l'uso normale del dizionario.
"""

from __future__ import annotations

import pathlib
import re
import sys
import textwrap
import unicodedata

TRATTINO = "—"   # trattino lungo, usato solo come separatore nel manoscritto

GRUPPI = {}


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def esc(s: str) -> str:
    """Blocco YAML piegato, cosi' il testo resta leggibile e diffabile."""
    body = textwrap.fill(s, width=74, initial_indent="  ",
                         subsequent_indent="  ")
    return ">-\n" + body


def main() -> int:
    src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    out_dir = pathlib.Path("voci")
    out_dir.mkdir(exist_ok=True)

    settimana = 0
    gruppo = ""
    n = 0

    blocchi = re.split(r"^(# SETTIMANA .*|## .*)$", src, flags=re.M)
    i = 1
    while i < len(blocchi):
        head, body = blocchi[i].strip(), blocchi[i + 1]
        i += 2

        if head.startswith("# SETTIMANA"):
            m = re.match(r"# SETTIMANA (\d+)\s*·\s*(.+)", head)
            settimana, gruppo = int(m.group(1)), m.group(2).strip()
            GRUPPI[settimana] = gruppo
            continue

        termine = head.lstrip("# ").strip()

        def campo(etichetta: str) -> str:
            m = re.search(
                rf"\*\*{etichetta}\*\*\s*{TRATTINO}\s*(.+?)(?=\n\n|\Z)",
                body, flags=re.S)
            if not m:
                raise SystemExit(f"campo '{etichetta}' mancante in '{termine}'")
            return " ".join(m.group(1).split())

        m_ing = re.search(r"\*Inglese:\s*(.+?)\*", body)
        if not m_ing:
            raise SystemExit(f"termine inglese mancante in '{termine}'")
        inglese = [t.strip() for t in m_ing.group(1).split(",") if t.strip()]

        n += 1
        vid = f"{n:03d}"
        slug = slugify(termine)

        c_cos = esc(campo("Cos'è"))
        c_perche = esc(campo("Perché conta"))
        c_errore = esc(campo("L'errore comune"))

        testo = "\n".join([
            f'id: "{vid}"',
            f"slug: {slug}",
            f"termine: {termine!r}".replace("'", '"'),
            f"settimana: {settimana}",
            f'gruppo: "{gruppo}"',
            "inglese:",
            *[f'  - "{t}"' for t in inglese],
            f"cos_e: {c_cos}",
            f"perche_conta: {c_perche}",
            f"errore_comune: {c_errore}",
            "vedi_anche: []",
            "revisione: 1",
            "",
        ])
        (out_dir / f"{vid}-{slug}.yaml").write_text(testo, encoding="utf-8")

    print(f"[ok] {n} voci scritte in {out_dir}/")
    for k in sorted(GRUPPI):
        print(f"     settimana {k}: {GRUPPI[k]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
