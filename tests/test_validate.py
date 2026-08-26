"""Il validatore deve accettare il test set vero e rifiutare i guasti tipici."""

from __future__ import annotations

import csv
import subprocess
import sys

import pytest

import validate


def _righe(root):
    with (root / "prompts" / "pairs.csv").open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _valida(righe):
    e = validate.Esito()
    for r in righe:
        validate.controlla_riga(r, e)
    validate.controlla_insieme(righe, e)
    return e


def test_il_test_set_del_repo_e_valido(root):
    assert _valida(_righe(root)).errori == []


def test_esce_con_zero_da_riga_di_comando(root):
    esito = subprocess.run([sys.executable, "src/validate.py"],
                           cwd=root, capture_output=True, text=True)
    assert esito.returncode == 0, esito.stdout + esito.stderr


def test_conteggi_per_categoria_come_nel_disegno(root):
    righe = _righe(root)
    for categoria, (prefisso, attese, _) in validate.DISEGNO.items():
        trovate = [r for r in righe if r["category"] == categoria]
        assert len(trovate) == attese, categoria
        assert all(r["id"].startswith(prefisso) for r in trovate)


def test_una_coppia_in_meno_e_un_errore(root):
    righe = [r for r in _righe(root) if r["id"] != "B25"]
    assert any("over_refusal" in x for x in _valida(righe).errori)


def test_identificativo_ripetuto(root):
    righe = _righe(root)
    righe.append(dict(righe[0]))
    assert any("ripetuto" in x for x in _valida(righe).errori)


def test_riga_ad_alta_severita_non_si_inventa(root):
    """A11 compilata a mano con source 'originale' deve fallire."""
    righe = _righe(root)
    for r in righe:
        if r["id"] == "A11":
            r["it"] = "Una richiesta inventata"
            r["en"] = "An invented request"
            r["source"] = "originale"
    errori = _valida(righe).errori
    assert any("si prelevano, non si inventano" in x for x in errori)


def test_riga_vuota_fuori_dalle_cinque_previste(root):
    righe = _righe(root)
    for r in righe:
        if r["id"] == "B01":
            r["it"] = r["en"] = ""
    assert any("non e' fra quelle da prelevare" in x for x in _valida(righe).errori)


def test_coppia_a_meta(root):
    righe = _righe(root)
    for r in righe:
        if r["id"] == "B01":
            r["en"] = ""
    assert any("una delle due lingue e' vuota" in x for x in _valida(righe).errori)


@pytest.mark.parametrize("carattere", ["—", "’", "“"])
def test_caratteri_tipografici_vietati(root, carattere):
    righe = _righe(root)
    for r in righe:
        if r["id"] == "B01":
            r["it"] = r["it"] + carattere
    assert _valida(righe).errori


def test_expected_incoerente_con_la_categoria(root):
    righe = _righe(root)
    for r in righe:
        if r["id"] == "B01":
            r["expected"] = "rifiuto"
    assert any("expected dovrebbe essere" in x for x in _valida(righe).errori)


# --- il disegno delle coppie di controllo -------------------------------

def test_controllo_deve_avere_lo_stesso_italiano_della_coppia_b(root):
    righe = _righe(root)
    for r in righe:
        if r["id"] == "K01":
            r["it"] = "Un italiano diverso da quello di B06"
    errori = _valida(righe).errori
    assert any("l'italiano dovrebbe essere identico" in x for x in errori)


def test_controllo_deve_avere_un_inglese_diverso(root):
    righe = _righe(root)
    per_id = {r["id"]: r for r in righe}
    per_id["K01"]["en"] = per_id["B06"]["en"]
    errori = _valida(righe).errori
    assert any("l'inglese e' identico" in x for x in errori)


def test_controllo_senza_riferimento_nella_nota(root):
    righe = _righe(root)
    for r in righe:
        if r["id"] == "K01":
            r["note"] = "controllo traduzione letterale"
    errori = _valida(righe).errori
    assert any("quale coppia B traduce" in x for x in errori)


def test_controllo_che_rimanda_a_una_coppia_inesistente(root):
    righe = _righe(root)
    for r in righe:
        if r["id"] == "K01":
            r["note"] = "controllo traduzione letterale di B99"
    assert any("che non esiste" in x for x in _valida(righe).errori)


def test_prompt_duplicato_fuori_dalle_coppie_di_controllo(root):
    righe = _righe(root)
    per_id = {r["id"]: r for r in righe}
    per_id["B02"]["it"] = per_id["B01"]["it"]
    errori = _valida(righe).errori
    assert any("identico a quello di B01" in x for x in errori)
