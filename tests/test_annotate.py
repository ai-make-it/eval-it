"""L'annotazione: cosa vede chi annota, e cosa succede alle etichette."""

from __future__ import annotations

import csv
import json

import pytest
from conftest import riga

import annotate


def leggi(percorso):
    return [json.loads(riga) for riga
            in percorso.read_text(encoding="utf-8").splitlines() if riga]


def esporta(monkeypatch, risultati, uscita, extra=()):
    monkeypatch.setattr("sys.argv",
                        ["annotate", "export", str(risultati),
                         "--out", str(uscita), *extra])
    return annotate.main()


def importa(monkeypatch, csvfile, dentro, extra=()):
    monkeypatch.setattr("sys.argv",
                        ["annotate", "import", str(csvfile),
                         "--into", str(dentro), *extra])
    return annotate.main()


# --- cosa nasconde l'export, e cosa dichiara di non nascondere ----------

def test_l_export_non_rivela_il_modello(scrivi_jsonl, tmp_path, monkeypatch):
    righe = [riga("B01", "it", "claude"), riga("B01", "en", "gpt")]
    csvout = tmp_path / "annot.csv"
    esporta(monkeypatch, scrivi_jsonl(righe), csvout)

    testo = csvout.read_text(encoding="utf-8")
    assert "claude" not in testo and "gpt" not in testo
    with csvout.open(encoding="utf-8") as fh:
        assert next(csv.reader(fh)) == annotate.CAMPI_CSV


def test_l_identificativo_e_stabile_e_opaco():
    r = riga("B01", "it", "claude")
    assert annotate._rid(r) == annotate._rid(dict(r))
    assert annotate._rid(r) != annotate._rid(riga("B01", "en", "claude"))
    assert len(annotate._rid(r)) == 12
    for pezzo in ("B01", "it", "claude"):
        assert pezzo not in annotate._rid(r)


def test_le_righe_sono_mescolate(scrivi_jsonl, tmp_path, monkeypatch):
    """Le due lingue di una stessa coppia non devono finire vicine."""
    righe = [riga(f"B{i:02d}", lingua) for i in range(1, 21)
             for lingua in ("it", "en")]
    csvout = tmp_path / "annot.csv"
    esporta(monkeypatch, scrivi_jsonl(righe), csvout)

    with csvout.open(encoding="utf-8") as fh:
        ordine = [r["prompt"] for r in csv.DictReader(fh)]
    originale = [r["prompt"] for r in righe]
    assert ordine != originale
    assert sorted(ordine) == sorted(originale)


def test_export_riproducibile_a_parita_di_seme(scrivi_jsonl, tmp_path, monkeypatch):
    righe = [riga(f"B{i:02d}", lingua) for i in range(1, 16)
             for lingua in ("it", "en")]
    risultati = scrivi_jsonl(righe)
    uno, due = tmp_path / "a.csv", tmp_path / "b.csv"
    esporta(monkeypatch, risultati, uno)
    esporta(monkeypatch, risultati, due)
    assert uno.read_text(encoding="utf-8") == due.read_text(encoding="utf-8")


# --- quali righe finiscono nell'export ----------------------------------

def test_le_bloccate_e_le_vuote_restano_fuori(scrivi_jsonl, tmp_path, monkeypatch):
    righe = [
        riga("B01", "it"),
        riga("B02", "it", blocked=True, response="", error="BLOCKED_UPSTREAM"),
        riga("B03", "it", response="", error="HTTP 500"),
        riga("B04", "it", response="   "),
    ]
    csvout = tmp_path / "annot.csv"
    esporta(monkeypatch, scrivi_jsonl(righe), csvout)
    with csvout.open(encoding="utf-8") as fh:
        prompt = [r["prompt"] for r in csv.DictReader(fh)]
    assert prompt == ["richiesta B01 it"]


def test_una_risposta_troncata_si_annota_lo_stesso(scrivi_jsonl, tmp_path,
                                                   monkeypatch):
    """Ha del testo: la valuta chi annota, seguendo docs/ANNOTATION.md."""
    righe = [riga("B01", "it", response="Inizio a rispond",
                  error="FINISH_length")]
    csvout = tmp_path / "annot.csv"
    esporta(monkeypatch, scrivi_jsonl(righe), csvout)
    assert "Inizio a rispond" in csvout.read_text(encoding="utf-8")


def test_il_campione_per_la_doppia_annotazione(scrivi_jsonl, tmp_path, monkeypatch):
    righe = [riga(f"B{i:02d}", "it") for i in range(1, 51)]
    csvout = tmp_path / "doppia.csv"
    esporta(monkeypatch, scrivi_jsonl(righe), csvout,
            ["--sample", "0.2", "--seed", "7"])
    with csvout.open(encoding="utf-8") as fh:
        assert len(list(csv.DictReader(fh))) == 10


def test_il_campione_e_un_sottoinsieme_dell_export_completo(
        scrivi_jsonl, tmp_path, monkeypatch):
    """L'accordo si misura sulle stesse righe, non su righe diverse."""
    righe = [riga(f"B{i:02d}", "it") for i in range(1, 51)]
    risultati = scrivi_jsonl(righe)
    tutto, campione = tmp_path / "a.csv", tmp_path / "b.csv"
    esporta(monkeypatch, risultati, tutto)
    esporta(monkeypatch, risultati, campione, ["--sample", "0.2", "--seed", "7"])

    def rid(p):
        with p.open(encoding="utf-8") as fh:
            return {r["rid"] for r in csv.DictReader(fh)}
    assert rid(campione) < rid(tutto)


def test_non_sovrascrive_un_csv_esistente(scrivi_jsonl, tmp_path, monkeypatch):
    csvout = tmp_path / "annot.csv"
    csvout.write_text("annotazioni gia' fatte", encoding="utf-8")
    assert esporta(monkeypatch, scrivi_jsonl([riga()]), csvout) == 1
    assert csvout.read_text(encoding="utf-8") == "annotazioni gia' fatte"


# --- rientro delle etichette --------------------------------------------

def _annota(percorso, csvout, etichette):
    with csvout.open(encoding="utf-8") as fh:
        righe = list(csv.DictReader(fh))
    for r in righe:
        r["etichetta"] = etichette
    with csvout.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=annotate.CAMPI_CSV)
        w.writeheader()
        w.writerows(righe)


def test_andata_e_ritorno(scrivi_jsonl, tmp_path, monkeypatch):
    righe = [riga(f"B{i:02d}", "it") for i in range(1, 6)]
    risultati = scrivi_jsonl(righe)
    csvout = tmp_path / "annot.csv"
    esporta(monkeypatch, risultati, csvout)
    _annota(risultati, csvout, "2")
    assert importa(monkeypatch, csvout, risultati) == 0
    assert all(r["label_a"] == 2 for r in leggi(risultati))


def test_il_secondo_annotatore_non_tocca_il_primo(scrivi_jsonl, tmp_path,
                                                  monkeypatch):
    risultati = scrivi_jsonl([riga(f"B{i:02d}", "it") for i in range(1, 6)])
    a, b = tmp_path / "a.csv", tmp_path / "b.csv"
    esporta(monkeypatch, risultati, a)
    _annota(risultati, a, "1")
    importa(monkeypatch, a, risultati, ["--annotator", "a"])
    esporta(monkeypatch, risultati, b)
    _annota(risultati, b, "4")
    importa(monkeypatch, b, risultati, ["--annotator", "b"])

    for r in leggi(risultati):
        assert (r["label_a"], r["label_b"]) == (1, 4)


def test_non_sovrascrive_un_etichetta_diversa(scrivi_jsonl, tmp_path, monkeypatch):
    risultati = scrivi_jsonl([riga("B01", "it")])
    csvout = tmp_path / "annot.csv"
    esporta(monkeypatch, risultati, csvout)
    _annota(risultati, csvout, "1")
    importa(monkeypatch, csvout, risultati)
    _annota(risultati, csvout, "5")
    importa(monkeypatch, csvout, risultati)
    assert leggi(risultati)[0]["label_a"] == 1


def test_sovrascrive_se_glielo_chiedi(scrivi_jsonl, tmp_path, monkeypatch):
    risultati = scrivi_jsonl([riga("B01", "it")])
    csvout = tmp_path / "annot.csv"
    esporta(monkeypatch, risultati, csvout)
    _annota(risultati, csvout, "1")
    importa(monkeypatch, csvout, risultati)
    _annota(risultati, csvout, "5")
    importa(monkeypatch, csvout, risultati, ["--sovrascrivi"])
    assert leggi(risultati)[0]["label_a"] == 5


@pytest.mark.parametrize("valore", ["0", "6", "si", "-1", "2,5"])
def test_etichette_fuori_scala_ignorate(scrivi_jsonl, tmp_path, monkeypatch, valore):
    risultati = scrivi_jsonl([riga("B01", "it")])
    csvout = tmp_path / "annot.csv"
    esporta(monkeypatch, risultati, csvout)
    _annota(risultati, csvout, valore)
    importa(monkeypatch, csvout, risultati)
    assert "label_a" not in leggi(risultati)[0]


def test_csv_di_un_altra_esecuzione_non_inquina(scrivi_jsonl, tmp_path,
                                                monkeypatch, capsys):
    uno = scrivi_jsonl([riga("B01", "it")], "uno.jsonl")
    due = scrivi_jsonl([riga("B01", "it", run_id="altro")], "due.jsonl")
    csvout = tmp_path / "annot.csv"
    esporta(monkeypatch, uno, csvout)
    _annota(uno, csvout, "3")
    importa(monkeypatch, csvout, due)
    assert "label_a" not in leggi(due)[0]
    assert "non corrispondono" in capsys.readouterr().out


def test_le_righe_non_annotate_restano_intatte(scrivi_jsonl, tmp_path, monkeypatch):
    risultati = scrivi_jsonl([riga("B01", "it"), riga("B02", "it")])
    csvout = tmp_path / "annot.csv"
    esporta(monkeypatch, risultati, csvout)
    with csvout.open(encoding="utf-8") as fh:
        righe = list(csv.DictReader(fh))
    righe[0]["etichetta"] = "5"
    with csvout.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=annotate.CAMPI_CSV)
        w.writeheader()
        w.writerows(righe)
    importa(monkeypatch, csvout, risultati)

    dentro = leggi(risultati)
    assert len(dentro) == 2
    assert sum(1 for r in dentro if "label_a" in r) == 1


def test_l_import_non_perde_righe(scrivi_jsonl, tmp_path, monkeypatch):
    """Il file dei risultati non e' rigenerabile: rifarlo costa le chiamate."""
    righe = [riga(f"B{i:02d}", lingua) for i in range(1, 26)
             for lingua in ("it", "en")]
    risultati = scrivi_jsonl(righe)
    csvout = tmp_path / "annot.csv"
    esporta(monkeypatch, risultati, csvout)
    _annota(risultati, csvout, "3")
    importa(monkeypatch, csvout, risultati)

    dentro = leggi(risultati)
    assert len(dentro) == len(righe)
    assert {(r["pair_id"], r["lang"]) for r in dentro} == \
           {(r["pair_id"], r["lang"]) for r in righe}
    assert not list(tmp_path.glob("*.tmp"))


def test_csv_senza_colonna_rid(scrivi_jsonl, tmp_path, monkeypatch, capsys):
    risultati = scrivi_jsonl([riga("B01", "it")])
    sbagliato = tmp_path / "sbagliato.csv"
    sbagliato.write_text("a,b\n1,2\n", encoding="utf-8")
    assert importa(monkeypatch, sbagliato, risultati) == 1
    assert "colonna 'rid'" in capsys.readouterr().out
