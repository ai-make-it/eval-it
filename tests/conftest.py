"""Percorsi e materiale condiviso dai test."""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))


@pytest.fixture
def root() -> pathlib.Path:
    return ROOT


def riga(pair_id="B01", lang="it", model="m1", rep=1, label=None, **extra):
    """Una riga di risultati, con i campi che il resto della pipeline usa."""
    r = {
        "run_id": "20260826T101500Z",
        "timestamp": "2026-08-26T10:15:00+00:00",
        "pair_id": pair_id,
        "category": "over_refusal",
        "expected": "piena",
        "lang": lang,
        "model_key": model,
        "provider": "mock",
        "model_requested": "mock",
        "model_returned": "mock",
        "temperature": 0,
        "max_tokens": 1024,
        "system_prompt": None,
        "repetition": rep,
        "prompt": f"richiesta {pair_id} {lang}",
        "response": f"risposta {pair_id} {lang} {rep}",
        "latency_ms": 5,
        "attempts": 1,
        "blocked": False,
        "error": None,
    }
    if label is not None:
        r["label_a"] = label
    r.update(extra)
    return r


@pytest.fixture
def scrivi_jsonl(tmp_path):
    def _scrivi(righe, nome="run.jsonl"):
        p = tmp_path / nome
        p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                             for r in righe), encoding="utf-8")
        return p
    return _scrivi
