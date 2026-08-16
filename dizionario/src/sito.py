"""
Genera il sito statico del dizionario, pronto da caricare su ai-make.it.

    python src/sito.py

Scrive in sito/:
    index.html                 l'indice, con la ricerca
    voce/<slug>/index.html     una pagina per voce
    gruppo/<n>-<slug>/         una pagina per gruppo di pubblicazione
    inglese/                   dall'inglese all'italiano
    dati/                      json, csv, markdown, scaricabili
    assets/                    un foglio di stile, uno script di ricerca
    sitemap.xml, llms.txt

Come dist/, sito/ e' rigenerabile: non si modifica a mano.

L'indirizzo di base si cambia senza toccare il codice:

    DIZIONARIO_BASE=https://esempio.it/dizionario python src/sito.py

Serve perche' canonical, Open Graph e sitemap vogliono indirizzi assoluti,
mentre i collegamenti fra le pagine restano relativi: il sito funziona
anche spostato in un'altra sottocartella.
"""

from __future__ import annotations

import html
import json
import os
import pathlib
import re
import shutil
import unicodedata

import yaml

RADICE = pathlib.Path(__file__).resolve().parent.parent
VOCI = RADICE / "voci"
DIST = RADICE / "dist"
SITO = RADICE / "sito"

BASE = os.environ.get("DIZIONARIO_BASE", "https://ai-make.it/dizionario").rstrip("/")
SITO_NOME = os.environ.get("DIZIONARIO_SITO", "ai-make.it")

TITOLO = "Dizionario ragionato dell'AI in italiano"
SOTTOTITOLO = (
    "Sessanta voci del vocabolario tecnico dell'intelligenza artificiale, "
    "scritte in italiano da chi lavora con questi sistemi, non tradotte "
    "da un glossario inglese."
)
DESCRIZIONE = (
    "Sessanta voci del vocabolario tecnico dell'AI in italiano. Ogni voce "
    "dice cos'è, perché conta e qual è l'errore comune. Dati aperti, "
    "CC BY 4.0."
)

GRUPPI = {
    1: "Le fondamenta",
    2: "Come si usa",
    3: "Architettura e agenti",
    4: "Come sbaglia",
    5: "Come si verifica",
    6: "Sicurezza",
}

# Serve nell'indice per dire cosa contiene un gruppo senza aprirlo.
GRUPPI_SOMMARIO = {
    1: "I termini che servono per leggere tutti gli altri.",
    2: "Il vocabolario di chi lavora con i modelli.",
    3: "Il vocabolario di chi costruisce.",
    4: "I modi in cui questi sistemi falliscono.",
    5: "Il vocabolario della valutazione.",
    6: "Il vocabolario della sicurezza tecnica.",
}

NOMI: dict[str, str] = {}


# ---------------------------------------------------------------- utilita'

def senza_accenti(t: str) -> str:
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def sgl(t: str) -> str:
    """Lo stesso slug del validatore, usato per gli indirizzi dei gruppi."""
    t = senza_accenti(t).replace("'", " ")
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")


def e(t: str) -> str:
    """Testo dentro un elemento."""
    return html.escape(str(t), quote=False)


def a(t: str) -> str:
    """Testo dentro un attributo."""
    return html.escape(str(t), quote=True)


def prima_frase(t: str, limite: int = 155) -> str:
    """La meta description: la prima frase, tagliata se non ci sta."""
    t = " ".join(t.split())
    taglio = t.find(". ")
    if 0 < taglio < limite:
        return t[:taglio + 1]
    if len(t) <= limite:
        return t
    return t[:limite].rsplit(" ", 1)[0] + "..."


def carica() -> list[dict]:
    voci = [yaml.safe_load(f.read_text(encoding="utf-8"))
            for f in sorted(VOCI.glob("*.yaml"))]
    return sorted(voci, key=lambda v: v["id"])


def via_gruppo(n: int) -> str:
    return f"gruppo/{n}-{sgl(GRUPPI[n])}/"


def scrivi(percorso: str, testo: str) -> None:
    f = SITO / percorso
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(testo, encoding="utf-8")


# ---------------------------------------------------------------- pagina

def pagina(*, corpo: str, titolo: str, descrizione: str, via: str,
           rel: str, jsonld: list[dict] | None = None,
           cerca: bool = True) -> str:
    """
    L'impalcatura comune. `via` e' il percorso della pagina rispetto alla
    radice del sito ("" per l'indice), `rel` il prefisso che riporta alla
    radice ("../../" da una voce). I collegamenti interni restano relativi
    perche' il sito deve funzionare anche in un'altra sottocartella;
    canonical e Open Graph no, perche' vogliono l'indirizzo assoluto.
    """
    canonico = f"{BASE}/{via}"
    blocchi = "\n".join(
        f'<script type="application/ld+json">\n'
        f'{json.dumps(d, ensure_ascii=False, indent=2)}\n</script>'
        for d in (jsonld or []))

    ricerca = ""
    if cerca:
        ricerca = f"""      <form class="cerca" action="{a(rel or './')}" method="get" role="search">
        <label class="via" for="q">Cerca una voce</label>
        <input id="q" name="q" type="search" autocomplete="off"
               placeholder="Cerca: token, drift, RAG..." value="">
      </form>"""

    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{a(titolo)}</title>
<meta name="description" content="{a(descrizione)}">
<link rel="canonical" href="{a(canonico)}">
<meta property="og:type" content="{'website' if via == '' else 'article'}">
<meta property="og:title" content="{a(titolo)}">
<meta property="og:description" content="{a(descrizione)}">
<meta property="og:url" content="{a(canonico)}">
<meta property="og:site_name" content="{a(SITO_NOME)}">
<meta property="og:locale" content="it_IT">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{a(rel)}assets/segno.svg" type="image/svg+xml">
<link rel="stylesheet" href="{a(rel)}assets/dizionario.css">
{blocchi}
</head>
<body data-radice="{a(rel)}">
<a class="salta" href="#contenuto">Salta al contenuto</a>

<header class="testata">
  <div class="riga">
    <a class="marchio" href="{a(rel or './')}">Dizionario ragionato dell'AI</a>
    <nav aria-label="Navigazione principale">
      <a href="{a(rel or './')}">Le voci</a>
      <a href="{a(rel)}inglese/">Dall'inglese</a>
      <a href="{a(rel)}dati/">I dati</a>
    </nav>
  </div>
{ricerca}
</header>

<main id="contenuto">
{corpo}
</main>

<footer class="chiusura">
  <p>Testo e dati <a href="https://creativecommons.org/licenses/by/4.0/deed.it"
     rel="license">CC BY 4.0</a>, codice MIT. Si riusa citando la fonte.</p>
  <p>Il dizionario si corregge e si estende con una pull request.
     Repo collegato: <a href="https://github.com/ai-make-it/eval-it">eval-it</a>,
     che misura quello che qui viene definito.</p>
</footer>

<script src="{a(rel)}assets/ricerca.js" defer></script>
</body>
</html>
"""


def briciole(rel: str, coppie: list[tuple[str, str]]) -> tuple[str, dict]:
    """Il percorso di navigazione, in HTML e in JSON-LD."""
    voci = []
    for i, (nome, via) in enumerate(coppie, start=1):
        voci.append({
            "@type": "ListItem",
            "position": i,
            "name": nome,
            "item": f"{BASE}/{via}",
        })
    pezzi = []
    for nome, via in coppie[:-1]:
        pezzi.append(f'<a href="{a(rel + via)}">{e(nome)}</a>')
    pezzi.append(f"<span aria-current=\"page\">{e(coppie[-1][0])}</span>")
    testo = ('<nav class="briciole" aria-label="Percorso">'
             + ' <span class="sep">/</span> '.join(pezzi) + "</nav>")
    return testo, {"@context": "https://schema.org",
                   "@type": "BreadcrumbList", "itemListElement": voci}


# ---------------------------------------------------------------- pezzi

def scheda(v: dict, rel: str, via: str) -> str:
    """La voce come appare in un elenco: termine, inglese, la definizione."""
    ing = ", ".join(v["inglese"])
    chiavi = senza_accenti(" ".join(
        [v["termine"], v["slug"], ing, v["gruppo"], v["cos_e"]]))
    return f"""<li class="scheda filtrabile" data-testo="{a(chiavi)}">
  <a class="termine" href="{a(rel + via)}">{e(v['termine'])}</a>
  <span class="ing">{e(ing)}</span>
  <p>{e(prima_frase(v['cos_e'], 120))}</p>
</li>"""


def campo(etichetta: str, testo: str, classe: str = "") -> str:
    return (f'<div class="campo {classe}">'
            f'<h2>{e(etichetta)}</h2><p>{e(testo)}</p></div>')


# ---------------------------------------------------------------- pagine

def fai_indice(voci: list[dict]) -> None:
    sezioni = []
    for n, nome in GRUPPI.items():
        gruppo = [v for v in voci if v["settimana"] == n]
        if not gruppo:
            continue
        schede = "\n".join(scheda(v, "", f"voce/{v['slug']}/") for v in gruppo)
        sezioni.append(f"""<section class="gruppo contenitore" id="gruppo-{n}">
  <div class="capo">
    <h2><a href="{a(via_gruppo(n))}">{e(nome)}</a></h2>
    <p>{e(GRUPPI_SOMMARIO[n])}</p>
  </div>
  <ul class="elenco">
{schede}
  </ul>
</section>""")

    corpo = f"""<div class="apertura">
  <h1>{e(TITOLO)}</h1>
  <p class="occhiello">{e(SOTTOTITOLO)}</p>
  <p>Ogni voce ha quattro campi, sempre gli stessi: cos'è, perché conta,
     l'errore comune, il termine inglese. Il terzo campo è il controllo di
     qualità: se su una voce non si riesce a scrivere l'errore comune, la
     voce non è pronta. Un dizionario di definizioni corrette lo si trova
     già tradotto ovunque.</p>
  <p class="conteggio">{len(voci)} voci in sei gruppi.
     <a href="inglese/">Se il termine lo hai incontrato in inglese, parti da qui.</a></p>
</div>

<p class="esito" role="status" hidden></p>

{chr(10).join(sezioni)}

<section class="dati">
  <h2>I dati sono aperti</h2>
  <p>Il dizionario si scarica intero, in tre formati.
     <a href="dati/dizionario.json">JSON</a> per chi programma,
     <a href="dati/dizionario.csv">CSV</a> per un foglio di calcolo,
     <a href="dati/dizionario.md">Markdown</a> per leggerlo tutto di seguito.</p>
</section>"""

    termini = [{
        "@type": "DefinedTerm",
        "name": v["termine"],
        "termCode": v["slug"],
        "url": f"{BASE}/voce/{v['slug']}/",
    } for v in voci]

    insieme = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "@id": f"{BASE}/#dizionario",
        "name": TITOLO,
        "description": DESCRIZIONE,
        "url": f"{BASE}/",
        "inLanguage": "it",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "hasDefinedTerm": termini,
    }

    scrivi("index.html", pagina(
        corpo=corpo, titolo=f"{TITOLO} | {SITO_NOME}",
        descrizione=DESCRIZIONE, via="", rel="", jsonld=[insieme]))


def fai_voce(v: dict, precedente: dict | None, seguente: dict | None) -> None:
    rel = "../../"
    n = v["settimana"]
    briciola, bl = briciole(rel, [
        ("Dizionario", ""),
        (GRUPPI[n], via_gruppo(n)),
        (v["termine"], f"voce/{v['slug']}/"),
    ])

    ing = ", ".join(v["inglese"])
    vedi = ""
    if v.get("vedi_anche"):
        voci = " ".join(
            f'<a href="{a(rel)}voce/{a(s)}/">{e(NOMI.get(s, s))}</a>'
            for s in v["vedi_anche"])
        vedi = f'<nav class="vedi"><h2>Vedi anche</h2>{voci}</nav>'

    scorri = []
    if precedente:
        scorri.append(f'<a class="prec" href="{a(rel)}voce/{a(precedente["slug"])}/">'
                      f'<span>Voce precedente</span>{e(precedente["termine"])}</a>')
    if seguente:
        scorri.append(f'<a class="segu" href="{a(rel)}voce/{a(seguente["slug"])}/">'
                      f'<span>Voce successiva</span>{e(seguente["termine"])}</a>')

    corpo = f"""{briciola}

<article class="voce">
  <header>
    <p class="etichetta"><a href="{a(rel)}{a(via_gruppo(n))}">{e(GRUPPI[n])}</a></p>
    <h1>{e(v['termine'])}</h1>
    <p class="inglese">In inglese: <b>{e(ing)}</b></p>
  </header>

  {campo("Cos'è", v["cos_e"])}
  {campo("Perché conta", v["perche_conta"])}
  {campo("L'errore comune", v["errore_comune"], "errore")}

  {vedi}
</article>

<nav class="scorri" aria-label="Altre voci">{"".join(scorri)}</nav>"""

    termine = {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": v["termine"],
        "alternateName": v["inglese"],
        "termCode": v["slug"],
        "description": " ".join(v["cos_e"].split()),
        "url": f"{BASE}/voce/{v['slug']}/",
        "inLanguage": "it",
        "inDefinedTermSet": {
            "@type": "DefinedTermSet",
            "@id": f"{BASE}/#dizionario",
            "name": TITOLO,
            "url": f"{BASE}/",
        },
    }

    scrivi(f"voce/{v['slug']}/index.html", pagina(
        corpo=corpo,
        titolo=f"{v['termine']} ({ing}): cosa significa | {TITOLO}",
        descrizione=prima_frase(v["cos_e"]),
        via=f"voce/{v['slug']}/", rel=rel, jsonld=[termine, bl]))


def fai_gruppo(n: int, gruppo: list[dict]) -> None:
    rel = "../../"
    nome = GRUPPI[n]
    briciola, bl = briciole(rel, [("Dizionario", ""), (nome, via_gruppo(n))])
    schede = "\n".join(scheda(v, rel, f"voce/{v['slug']}/") for v in gruppo)

    corpo = f"""{briciola}

<div class="apertura">
  <p class="etichetta">Gruppo {n} di 6</p>
  <h1>{e(nome)}</h1>
  <p class="occhiello">{e(GRUPPI_SOMMARIO[n])}</p>
  <p class="conteggio">{len(gruppo)} voci.
     <a href="{a(rel)}">Torna a tutte le voci.</a></p>
</div>

<p class="esito" role="status" hidden></p>

<section class="gruppo contenitore">
  <ul class="elenco">
{schede}
  </ul>
</section>"""

    scrivi(f"{via_gruppo(n)}index.html", pagina(
        corpo=corpo, titolo=f"{nome}: {len(gruppo)} voci | {TITOLO}",
        descrizione=f"{GRUPPI_SOMMARIO[n]} {len(gruppo)} voci del dizionario "
                    f"ragionato dell'AI in italiano.",
        via=via_gruppo(n), rel=rel, jsonld=[bl]))


def fai_inglese(voci: list[dict]) -> None:
    rel = "../"
    briciola, bl = briciole(rel, [("Dizionario", ""), ("Dall'inglese", "inglese/")])
    coppie = sorted(
        ((ing, v["termine"], v["slug"]) for v in voci for ing in v["inglese"]),
        key=lambda x: senza_accenti(x[0]))

    righe = "\n".join(
        f'<tr class="filtrabile" data-testo="{a(senza_accenti(ing + " " + it))}">'
        f"<td>{e(ing)}</td>"
        f'<td><a href="{a(rel)}voce/{a(sl)}/">{e(it)}</a></td></tr>'
        for ing, it, sl in coppie)

    corpo = f"""{briciola}

<div class="apertura">
  <h1>Dall'inglese all'italiano</h1>
  <p class="occhiello">La maggior parte delle persone arriva a una voce
     perché il termine lo ha incontrato in inglese. Questa è la porta
     d'ingresso da quella parte.</p>
  <p class="conteggio">{len(coppie)} termini inglesi verso {len(voci)} voci.</p>
</div>

<p class="esito" role="status" hidden></p>

<table class="tavola contenitore">
  <thead><tr><th scope="col">Inglese</th><th scope="col">Italiano</th></tr></thead>
  <tbody>
{righe}
  </tbody>
</table>

<p class="nota">Diversi termini restano in inglese anche in italiano, e dove
   è così la voce lo dice. <i>Token</i>, <i>embedding</i>, <i>fine-tuning</i>
   e <i>reward hacking</i> si usano così: inventare un calco che nessuno
   userebbe rende il dizionario inservibile proprio a chi ne ha bisogno.</p>"""

    scrivi("inglese/index.html", pagina(
        corpo=corpo, titolo=f"Dall'inglese all'italiano | {TITOLO}",
        descrizione=f"{len(coppie)} termini inglesi dell'AI con la voce "
                    f"italiana corrispondente. Da token a reward hacking.",
        via="inglese/", rel=rel, jsonld=[bl]))


def fai_dati(voci: list[dict]) -> None:
    rel = "../"
    briciola, bl = briciole(rel, [("Dizionario", ""), ("I dati", "dati/")])
    for f in ("dizionario.json", "dizionario.csv", "dizionario.md",
              "indice-inglese.md"):
        shutil.copyfile(DIST / f, SITO / "dati" / f)

    misure = {f.name: f.stat().st_size for f in (SITO / "dati").iterdir()}

    def riga(nome: str, cosa: str) -> str:
        kb = round(misure.get(nome, 0) / 1024)
        return (f'<li><a href="{a(nome)}">{e(nome)}</a> '
                f'<span class="peso">{kb} kB</span><p>{e(cosa)}</p></li>')

    corpo = f"""{briciola}

<div class="apertura">
  <h1>I dati</h1>
  <p class="occhiello">Il dizionario intero si scarica e si riusa, anche
     commercialmente, citando la fonte. Licenza CC BY 4.0.</p>
</div>

<ul class="elenco dritto contenitore">
{riga("dizionario.json", "Tutte le " + str(len(voci)) + " voci con tutti i campi. Il formato da usare se ci si costruisce sopra qualcosa.")}
{riga("dizionario.csv", "Le stesse voci in tabella, per chi le apre in un foglio di calcolo.")}
{riga("dizionario.md", "Il dizionario in ordine alfabetico, in un file solo.")}
{riga("indice-inglese.md", "Dall'inglese all'italiano, in tabella.")}
</ul>

<section class="dati">
  <h2>Come si cita</h2>
  <p><i>Dizionario ragionato dell'AI in italiano</i>, {e(SITO_NOME)},
     CC BY 4.0, {e(BASE)}/</p>
  <h2>Come si corregge</h2>
  <p>Il campo <i>errore comune</i> contiene giudizi su cosa si sbaglia, e sono
     discutibili: è per questo che si aprono issue. Le voci nuove e le
     correzioni si propongono con una pull request. Il criterio di
     accettazione è uno solo: si riesce a scrivere l'errore comune?</p>
</section>"""

    scrivi("dati/index.html", pagina(
        corpo=corpo, titolo=f"I dati, aperti e scaricabili | {TITOLO}",
        descrizione="Il dizionario dell'AI in italiano in JSON, CSV e "
                    "Markdown. Dati aperti CC BY 4.0.",
        via="dati/", rel=rel, jsonld=[bl], cerca=False))


def fai_mappa(voci: list[dict]) -> None:
    """
    La sitemap va dichiarata nel robots.txt della radice del dominio: un
    robots.txt dentro una sottocartella non lo legge nessuno, e per questo
    qui non lo generiamo.

    Senza lastmod di proposito. Una data messa alla build cambia a ogni
    rigenerazione, e sito/ smetterebbe di essere confrontabile con il
    sorgente: la CI segnalerebbe una differenza ogni giorno, per un dato
    che nessun motore usa come dichiarato.
    """
    vie = ["", "inglese/", "dati/"]
    vie += [via_gruppo(n) for n in GRUPPI]
    vie += [f"voce/{v['slug']}/" for v in voci]
    corpo = "\n".join(f"  <url><loc>{BASE}/{v}</loc></url>" for v in vie)
    scrivi("sitemap.xml",
           '<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{corpo}\n</urlset>\n")


def fai_llms(voci: list[dict]) -> None:
    righe = [f"# {TITOLO}", "",
             f"> {' '.join(DESCRIZIONE.split())}", "",
             "Quattro campi per voce: cos'è, perché conta, l'errore "
             "comune, il termine inglese. Licenza CC BY 4.0.", ""]
    for n, nome in GRUPPI.items():
        gruppo = [v for v in voci if v["settimana"] == n]
        if not gruppo:
            continue
        righe += [f"## {nome}", ""]
        righe += [f"- [{v['termine']}]({BASE}/voce/{v['slug']}/): "
                  f"{prima_frase(v['cos_e'], 120)}" for v in gruppo]
        righe.append("")
    righe += ["## Dati", "",
              f"- [JSON]({BASE}/dati/dizionario.json): tutte le voci",
              f"- [CSV]({BASE}/dati/dizionario.csv): tutte le voci in tabella",
              f"- [Markdown]({BASE}/dati/dizionario.md): il dizionario intero",
              ""]
    scrivi("llms.txt", "\n".join(righe))


# ---------------------------------------------------------------- risorse

def fai_risorse() -> None:
    for f in ("dizionario.css", "ricerca.js", "segno.svg"):
        shutil.copyfile(RADICE / "src" / "risorse" / f, SITO / "assets" / f)


# ---------------------------------------------------------------- main

def main() -> int:
    voci = carica()
    NOMI.update({v["slug"]: v["termine"] for v in voci})

    if not (DIST / "dizionario.json").exists():
        print("[errore] manca dist/. Lancia prima python src/build.py")
        return 1

    if SITO.exists():
        shutil.rmtree(SITO)
    (SITO / "assets").mkdir(parents=True)
    (SITO / "dati").mkdir(parents=True)

    fai_indice(voci)
    for i, v in enumerate(voci):
        fai_voce(v, voci[i - 1] if i else None,
                 voci[i + 1] if i + 1 < len(voci) else None)
    for n in GRUPPI:
        gruppo = [v for v in voci if v["settimana"] == n]
        if gruppo:
            fai_gruppo(n, gruppo)
    fai_inglese(voci)
    fai_dati(voci)
    fai_mappa(voci)
    fai_llms(voci)
    fai_risorse()

    pagine = sorted(SITO.rglob("*.html"))
    peso = sum(f.stat().st_size for f in SITO.rglob("*") if f.is_file())
    print(f"[ok] {len(pagine)} pagine · {len(voci)} voci · "
          f"{round(peso / 1024)} kB in sito/")
    print(f"     base: {BASE}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
