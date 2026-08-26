"""
Esecuzione dell'esperimento.

Legge le coppie da prompts/pairs.csv, la configurazione da config.yaml,
e scrive un JSONL in results/. E' ripartibile: se il file esiste gia',
salta le combinazioni gia' eseguite.

    python src/run.py --config config.yaml
    python src/run.py --config config.yaml --models mock --dry-run

Accanto al JSONL scrive un file .meta.json con l'impronta del test set,
i parametri e i modelli richiesti. Serve a poter dire, mesi dopo, contro
quale versione esatta del test set sono stati prodotti quei numeri.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import pathlib
import platform
import sys
from collections.abc import Iterator
from typing import Any

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import providers  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINGUE = ("it", "en")


def _risolvi(percorso: str) -> pathlib.Path:
    """Percorsi relativi letti rispetto alla radice del repo, non alla cwd."""
    p = pathlib.Path(percorso)
    return p if p.is_absolute() else ROOT / p


def load_pairs(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    usable, skipped = [], []
    for r in rows:
        if r.get("it", "").strip() and r.get("en", "").strip():
            usable.append(r)
        else:
            skipped.append(r["id"])
    if skipped:
        print(f"[i] {len(skipped)} coppie senza testo, saltate: "
              f"{', '.join(skipped)}")
        print("    (sono gli item ad alta severita' da prelevare da "
              "benchmark pubblicati, vedi docs/METHOD.md)")
    return usable


def impronta(path: pathlib.Path) -> str:
    """SHA-256 del test set, per legare i risultati alla loro versione."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def done_keys(out: pathlib.Path) -> set[tuple]:
    if not out.exists():
        return set()
    seen = set()
    with out.open(encoding="utf-8") as fh:
        for numero, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                print(f"[!] riga {numero} di {out.name} illeggibile, ignorata")
                continue
            try:
                seen.add((r["pair_id"], r["lang"], r["model_key"], r["repetition"]))
            except KeyError:
                print(f"[!] riga {numero} di {out.name} senza chiavi attese")
    return seen


def controlla_chiavi(models: dict[str, dict]) -> list[str]:
    """Quali variabili d'ambiente mancano, per i modelli richiesti.

    Si controlla prima di spendere: una chiave mancante scoperta alla
    chiamata numero settecento lascia un file a meta'.
    """
    import os
    mancanti = []
    for key, cfg in models.items():
        env = providers.chiave_richiesta(cfg)
        if env and not os.environ.get(env):
            mancanti.append(f"{key}: {env}")
    return mancanti


def jobs(pairs, models, reps) -> Iterator[dict[str, Any]]:
    for pair in pairs:
        for lang in LINGUE:
            for mkey, mcfg in models.items():
                for rep in range(1, reps + 1):
                    yield {
                        "pair": pair,
                        "lang": lang,
                        "model_key": mkey,
                        "model_cfg": mcfg,
                        "repetition": rep,
                    }


def scrivi_meta(out: pathlib.Path, cfg: dict, models: dict,
                pairs_path: pathlib.Path, n_pairs: int, run_id: str) -> None:
    meta = {
        "run_id": run_id,
        "generato": dt.datetime.now(dt.UTC).isoformat(),
        "pairs_file": str(pairs_path.relative_to(ROOT)),
        "pairs_sha256": impronta(pairs_path),
        "pairs_usate": n_pairs,
        "params": cfg["params"],
        # Solo il nome della variabile d'ambiente, mai il suo valore.
        "models": {
            k: {kk: vv for kk, vv in v.items() if kk != "extra_body"}
            for k, v in models.items()
        },
        "python": platform.python_version(),
    }
    path = out.with_suffix(out.suffix + ".meta.json")
    path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    print(f"[i] manifesto in {path}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Esegue il test set su uno o piu' modelli.")
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--out", default=None,
                    help="file JSONL di output (default: results/run-<data>.jsonl)")
    ap.add_argument("--models", nargs="*", default=None,
                    help="esegui solo questi model_key")
    ap.add_argument("--pairs", nargs="*", default=None,
                    help="esegui solo questi pair_id")
    ap.add_argument("--dry-run", action="store_true",
                    help="stampa quante chiamate farebbe e si ferma")
    args = ap.parse_args()

    config_path = _risolvi(args.config)
    if not config_path.exists():
        print(f"[!] configurazione non trovata: {config_path}")
        print("    Copia config.example.yaml in config.yaml e adattalo.")
        return 1

    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    for campo in ("pairs_file", "params", "models"):
        if campo not in cfg:
            print(f"[!] manca '{campo}' in {config_path.name}")
            return 1
    params = cfg["params"]
    models = cfg["models"]

    if args.models:
        ignoti = [m for m in args.models if m not in models]
        if ignoti:
            print(f"[!] model_key non in configurazione: {', '.join(ignoti)}")
            print(f"    disponibili: {', '.join(models)}")
            return 1
        models = {k: v for k, v in models.items() if k in args.models}

    pairs_path = _risolvi(cfg["pairs_file"])
    pairs = load_pairs(pairs_path)
    if args.pairs:
        noti = {p["id"] for p in pairs}
        ignoti = [p for p in args.pairs if p not in noti]
        if ignoti:
            print(f"[!] pair_id assenti o senza testo: {', '.join(ignoti)}")
            return 1
        pairs = [p for p in pairs if p["id"] in args.pairs]
    if not pairs:
        print("[!] nessuna coppia da eseguire")
        return 1

    out = _risolvi(args.out) if args.out else (
        ROOT / "results" / f"run-{dt.date.today().isoformat()}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)

    already = done_keys(out)
    todo = [j for j in jobs(pairs, models, params["repetitions"])
            if (j["pair"]["id"], j["lang"], j["model_key"],
                j["repetition"]) not in already]

    total = len(pairs) * len(LINGUE) * len(models) * params["repetitions"]
    print(f"[i] coppie {len(pairs)} · modelli {len(models)} · "
          f"ripetizioni {params['repetitions']}")
    print(f"[i] chiamate totali {total} · gia' fatte {len(already)} · "
          f"da fare {len(todo)}")

    mancanti = controlla_chiavi(models)
    if mancanti:
        print("[!] chiavi mancanti nell'ambiente, niente viene eseguito:")
        for m in mancanti:
            print(f"      {m}")
        return 1

    if args.dry_run:
        print("[i] dry-run, nessuna chiamata effettuata")
        return 0

    if not todo:
        print("[ok] niente da fare, il file e' gia' completo")
        return 0

    run_id = f"{dt.datetime.now(dt.UTC):%Y%m%dT%H%M%SZ}"
    scrivi_meta(out, cfg, models, pairs_path, len(pairs), run_id)
    errors = blocked = 0

    with out.open("a", encoding="utf-8") as fh:
        for i, job in enumerate(todo, 1):
            pair, mcfg = job["pair"], job["model_cfg"]
            prompt = pair[job["lang"]]

            reply = providers.call(
                mcfg["provider"],
                prompt,
                mcfg["model"],
                base_url=mcfg.get("base_url"),
                api_key_env=mcfg.get("api_key_env"),
                temperature=params["temperature"],
                max_tokens=params["max_tokens"],
                extra_body=mcfg.get("extra_body"),
            )
            if reply.error and not reply.blocked:
                errors += 1
            if reply.blocked:
                blocked += 1

            fh.write(json.dumps({
                "run_id": run_id,
                "timestamp": dt.datetime.now(dt.UTC).isoformat(),
                "pair_id": pair["id"],
                "category": pair["category"],
                "expected": pair["expected"],
                "lang": job["lang"],
                "model_key": job["model_key"],
                "provider": mcfg["provider"],
                "model_requested": mcfg["model"],
                "model_returned": reply.raw_model,
                "temperature": params["temperature"],
                "max_tokens": params["max_tokens"],
                "system_prompt": None,
                "repetition": job["repetition"],
                "prompt": prompt,
                "response": reply.text,
                "latency_ms": reply.latency_ms,
                "attempts": reply.attempts,
                "blocked": reply.blocked,
                "error": reply.error,
            }, ensure_ascii=False) + "\n")
            fh.flush()

            if i % 25 == 0 or i == len(todo):
                print(f"    {i}/{len(todo)} · errori {errors} · "
                      f"bloccati a monte {blocked}")

    print(f"[ok] scritto {out}")
    if blocked:
        print(f"[i] {blocked} chiamate fermate dal fornitore per il contenuto.")
        print("    Non sono errori: l'analisi le conta come rifiuto a monte.")
    if errors:
        print(f"[!] {errors} chiamate con errore: rilancia lo stesso comando, "
              f"riprende da dove si e' fermato")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
