"""
Controlla il sito generato.

    python src/collegamenti.py

Esce con 1 se qualcosa non torna. Gira in CI dopo src/sito.py.

I controlli corrispondono ai modi in cui un sito statico generato si guasta
in silenzio: un rimando a una voce rinominata, un blocco JSON-LD rotto da
un apostrofo, un trattino lungo entrato dalla porta di servizio del
generatore invece che da quella delle voci, dove il validatore lo blocca.
"""

from __future__ import annotations

import html
import json
import pathlib
import re
import sys
import urllib.parse
from html.parser import HTMLParser

SITO = pathlib.Path(__file__).resolve().parent.parent / "sito"

VIETATI = {
    "—": "trattino lungo",
    "–": "trattino medio",
    "…": "puntini di sospensione in un solo carattere",
    "“": "virgolette curve",
    "”": "virgolette curve",
    "’": "apostrofo curvo",
}


class Struttura(HTMLParser):
    """Tag bilanciati e un solo h1. Un h1 in piu' e' quasi sempre un
    frammento incollato nel posto sbagliato."""

    VUOTI = {"meta", "link", "br", "img", "input", "hr", "source", "col"}

    def __init__(self) -> None:
        super().__init__()
        self.pila: list[str] = []
        self.errori: list[str] = []
        self.h1 = 0

    def handle_starttag(self, tag: str, _attrs) -> None:
        if tag in self.VUOTI:
            return
        self.pila.append(tag)
        if tag == "h1":
            self.h1 += 1

    def handle_endtag(self, tag: str) -> None:
        if not self.pila:
            self.errori.append(f"</{tag}> senza apertura")
        elif self.pila[-1] != tag:
            self.errori.append(f"</{tag}> chiude un <{self.pila[-1]}>")
        else:
            self.pila.pop()


def main() -> int:
    if not SITO.exists():
        print("[errore] sito/ non c'e'. Lancia prima python src/sito.py")
        return 1

    pagine = sorted(SITO.rglob("*.html"))
    guasti: list[str] = []
    collegamenti = 0
    blocchi = 0

    for f in pagine:
        dove = f.relative_to(SITO)
        testo = f.read_text(encoding="utf-8")

        for href in re.findall(r'(?:href|src)="([^"]+)"', testo):
            href = html.unescape(href)
            if href.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            collegamenti += 1
            meta = (f.parent / urllib.parse.urlparse(href).path).resolve()
            if meta.is_dir():
                meta = meta / "index.html"
            if not meta.exists():
                guasti.append(f"{dove}: collegamento rotto verso {href}")

        for blocco in re.findall(
                r'<script type="application/ld\+json">\n(.*?)\n</script>',
                testo, re.S):
            blocchi += 1
            try:
                json.loads(blocco)
            except json.JSONDecodeError as err:
                guasti.append(f"{dove}: JSON-LD non valido ({err})")

        s = Struttura()
        s.feed(testo)
        for err in s.errori:
            guasti.append(f"{dove}: {err}")
        if s.pila:
            guasti.append(f"{dove}: tag non chiusi, {', '.join(s.pila[:4])}")
        if s.h1 != 1:
            guasti.append(f"{dove}: {s.h1} elementi h1, ne serve esattamente 1")

        for carattere, nome in VIETATI.items():
            if carattere in testo:
                guasti.append(f"{dove}: {nome}")

        if "<title></title>" in testo or 'content=""' in testo:
            guasti.append(f"{dove}: titolo o meta vuoti")

    for g in guasti:
        print(f"  [x] {g}")

    if guasti:
        print(f"\n[errore] {len(guasti)} problemi su {len(pagine)} pagine.")
        return 1

    print(f"[ok] {len(pagine)} pagine · {collegamenti} collegamenti interni "
          f"· {blocchi} blocchi JSON-LD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
