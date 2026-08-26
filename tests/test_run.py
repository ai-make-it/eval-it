"""L'esecuzione: ripartenza, controllo preliminare, manifesto."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest
import yaml

import run

CONFIG = {
    "pairs_file": "prompts/pairs.csv",
    "params": {"temperature": 0, "max_tokens": 64, "repetitions": 2},
    "models": {"mock": {"provider": "mock", "model": "mock"}},
}


@pytest.fixture
def config(tmp_path, root):
    percorso = tmp_path / "config.yaml"
    cfg = json.loads(json.dumps(CONFIG))
    cfg["pairs_file"] = str(root / "prompts" / "pairs.csv")
    percorso.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return percorso


def esegui(monkeypatch, config, out, extra=()):
    monkeypatch.setattr("sys.argv", ["run", "--config", str(config),
                                     "--out", str(out), *extra])
    return run.main()


def righe(percorso):
    return [json.loads(riga) for riga
            in percorso.read_text(encoding="utf-8").splitlines() if riga]


def test_dry_run_non_scrive_niente(monkeypatch, config, tmp_path):
    out = tmp_path / "run.jsonl"
    assert esegui(monkeypatch, config, out, ["--dry-run"]) == 0
    assert not out.exists()


def test_esecuzione_completa_col_mock(monkeypatch, config, tmp_path):
    out = tmp_path / "run.jsonl"
    assert esegui(monkeypatch, config, out, ["--pairs", "B01", "B02"]) == 0

    dati = righe(out)
    # 2 coppie x 2 lingue x 2 ripetizioni
    assert len(dati) == 8
    assert {r["lang"] for r in dati} == {"it", "en"}
    assert {r["repetition"] for r in dati} == {1, 2}
    assert all(r["error"] is None for r in dati)
    assert all(r["response"] for r in dati)


def test_le_coppie_senza_testo_sono_saltate(monkeypatch, config, tmp_path, capsys):
    out = tmp_path / "run.jsonl"
    esegui(monkeypatch, config, out, ["--dry-run"])
    uscita = capsys.readouterr().out
    assert "A11" in uscita and "saltate" in uscita
    # 50 coppie con testo x 2 lingue x 2 ripetizioni
    assert "chiamate totali 200" in uscita


def test_e_ripartibile(monkeypatch, config, tmp_path, capsys):
    """Se si interrompe, rilanciare non rifa' le chiamate gia' pagate."""
    out = tmp_path / "run.jsonl"
    esegui(monkeypatch, config, out, ["--pairs", "B01"])
    prima = righe(out)

    esegui(monkeypatch, config, out, ["--pairs", "B01"])
    assert righe(out) == prima
    assert "niente da fare" in capsys.readouterr().out


def test_riparte_da_dove_si_era_fermata(monkeypatch, config, tmp_path):
    out = tmp_path / "run.jsonl"
    esegui(monkeypatch, config, out, ["--pairs", "B01"])
    esegui(monkeypatch, config, out, ["--pairs", "B01", "B02"])

    dati = righe(out)
    assert len(dati) == 8
    chiavi = [(r["pair_id"], r["lang"], r["repetition"]) for r in dati]
    assert len(chiavi) == len(set(chiavi))


def test_una_riga_illeggibile_non_ferma_la_ripartenza(monkeypatch, config,
                                                      tmp_path, capsys):
    out = tmp_path / "run.jsonl"
    esegui(monkeypatch, config, out, ["--pairs", "B01"])
    with out.open("a", encoding="utf-8") as fh:
        fh.write("{ meta riga rotta\n")
    assert esegui(monkeypatch, config, out, ["--pairs", "B01"]) == 0
    assert "illeggibile" in capsys.readouterr().out


# --- il manifesto -------------------------------------------------------

def test_il_manifesto_lega_i_risultati_alla_versione_del_test_set(
        monkeypatch, config, tmp_path, root):
    out = tmp_path / "run.jsonl"
    esegui(monkeypatch, config, out, ["--pairs", "B01"])

    meta = json.loads((tmp_path / "run.jsonl.meta.json").read_text())
    assert meta["pairs_sha256"] == run.impronta(root / "prompts" / "pairs.csv")
    assert meta["params"]["repetitions"] == 2
    assert meta["pairs_usate"] == 1


def test_il_manifesto_non_contiene_chiavi(monkeypatch, tmp_path, root):
    cfg = json.loads(json.dumps(CONFIG))
    cfg["pairs_file"] = str(root / "prompts" / "pairs.csv")
    cfg["models"]["finto"] = {"provider": "mock", "model": "mock",
                              "api_key_env": "UNA_CHIAVE"}
    config = tmp_path / "config.yaml"
    config.write_text(yaml.safe_dump(cfg), encoding="utf-8")

    monkeypatch.setenv("UNA_CHIAVE", "valore-segretissimo")
    out = tmp_path / "run.jsonl"
    monkeypatch.setattr("sys.argv", ["run", "--config", str(config),
                                     "--out", str(out), "--pairs", "B01"])
    run.main()

    testo = (tmp_path / "run.jsonl.meta.json").read_text()
    assert "valore-segretissimo" not in testo
    assert "UNA_CHIAVE" in testo


# --- controlli preliminari ----------------------------------------------

def test_chiave_mancante_ferma_tutto_prima_di_spendere(monkeypatch, tmp_path, root):
    cfg = json.loads(json.dumps(CONFIG))
    cfg["pairs_file"] = str(root / "prompts" / "pairs.csv")
    cfg["models"] = {"vero": {"provider": "anthropic", "model": "x",
                              "api_key_env": "CHIAVE_ASSENTE"}}
    config = tmp_path / "config.yaml"
    config.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    monkeypatch.delenv("CHIAVE_ASSENTE", raising=False)

    out = tmp_path / "run.jsonl"
    assert esegui(monkeypatch, config, out) == 1
    assert not out.exists()


def test_configurazione_assente(monkeypatch, tmp_path, capsys):
    out = tmp_path / "run.jsonl"
    assert esegui(monkeypatch, tmp_path / "manca.yaml", out) == 1
    assert "non trovata" in capsys.readouterr().out


def test_modello_inesistente(monkeypatch, config, tmp_path, capsys):
    out = tmp_path / "run.jsonl"
    assert esegui(monkeypatch, config, out, ["--models", "inventato"]) == 1
    assert "non in configurazione" in capsys.readouterr().out


def test_coppia_inesistente(monkeypatch, config, tmp_path, capsys):
    out = tmp_path / "run.jsonl"
    assert esegui(monkeypatch, config, out, ["--pairs", "Z99"]) == 1
    assert "Z99" in capsys.readouterr().out


def test_coppia_senza_testo_rifiutata(monkeypatch, config, tmp_path):
    """A11 e' in pairs.csv ma non ha testo: non e' eseguibile."""
    out = tmp_path / "run.jsonl"
    assert esegui(monkeypatch, config, out, ["--pairs", "A11"]) == 1


# --- la pipeline intera, come la esegue chi legge il README --------------

def test_pipeline_completa_col_mock(root, tmp_path):
    """run, export, import, analyze: la sequenza del README, senza chiavi."""
    config = tmp_path / "config.yaml"
    config.write_text(yaml.safe_dump({
        "pairs_file": "prompts/pairs.csv",
        "params": {"temperature": 0, "max_tokens": 64, "repetitions": 2},
        "models": {"mock": {"provider": "mock", "model": "mock"}},
    }), encoding="utf-8")
    risultati = tmp_path / "run.jsonl"
    annot = tmp_path / "annot.csv"

    def py(*args):
        esito = subprocess.run([sys.executable, *args], cwd=root,
                               capture_output=True, text=True)
        assert esito.returncode == 0, esito.stdout + esito.stderr
        return esito.stdout

    py("src/run.py", "--config", str(config), "--out", str(risultati))
    py("src/annotate.py", "export", str(risultati), "--out", str(annot))

    import csv as _csv
    with annot.open(encoding="utf-8") as fh:
        righe_csv = list(_csv.DictReader(fh))
    # 50 coppie x 2 lingue x 2 ripetizioni
    assert len(righe_csv) == 200
    for i, r in enumerate(righe_csv):
        r["etichetta"] = "1" if i % 3 == 0 else "5"
    with annot.open("w", encoding="utf-8", newline="") as fh:
        w = _csv.DictWriter(fh, fieldnames=["rid", "prompt", "risposta",
                                            "etichetta", "note"])
        w.writeheader()
        w.writerows(righe_csv)

    py("src/annotate.py", "import", str(annot), "--into", str(risultati))
    uscita = py("src/analyze.py", str(risultati),
                "--csv", str(tmp_path / "tabella.csv"))

    assert "over_refusal" in uscita
    assert "IC 95% sul delta" in uscita
    assert (tmp_path / "tabella.csv").exists()
