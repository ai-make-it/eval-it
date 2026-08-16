"""
Esecuzione dell'esperimento.

Legge le coppie da prompts/pairs.csv, la configurazione da config.yaml,
e scrive un JSONL in results/. E' ripartibile: se il file esiste gia',
salta le combinazioni gia' eseguite.

    python src/run.py --config config.yaml
    python src/run.py --config config.yaml --models mock --dry-run
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import pathlib
import sys
from typing import Any, Iterator

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import providers  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent


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


def done_keys(out: pathlib.Path) -> set[tuple]:
    if not out.exists():
        return set()
    seen = set()
    with out.open(encoding="utf-8") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            seen.add((r["pair_id"], r["lang"], r["model_key"], r["repetition"]))
    return seen


def jobs(pairs, models, reps) -> Iterator[dict[str, Any]]:
    for pair in pairs:
        for lang in ("it", "en"):
            for mkey, mcfg in models.items():
                for rep in range(1, reps + 1):
                    yield {
                        "pair": pair,
                        "lang": lang,
                        "model_key": mkey,
                        "model_cfg": mcfg,
                        "repetition": rep,
                    }


def main() -> int:
    ap = argparse.ArgumentParser()
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

    cfg = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8"))
    params = cfg["params"]
    models = cfg["models"]
    if args.models:
        models = {k: v for k, v in models.items() if k in args.models}
        if not models:
            print("[!] Nessun modello corrisponde a --models")
            return 1

    pairs = load_pairs(ROOT / cfg["pairs_file"])
    if args.pairs:
        pairs = [p for p in pairs if p["id"] in args.pairs]

    out = pathlib.Path(args.out) if args.out else (
        ROOT / "results" / f"run-{dt.date.today().isoformat()}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)

    already = done_keys(out)
    todo = [j for j in jobs(pairs, models, params["repetitions"])
            if (j["pair"]["id"], j["lang"], j["model_key"],
                j["repetition"]) not in already]

    total = len(pairs) * 2 * len(models) * params["repetitions"]
    print(f"[i] coppie {len(pairs)} · modelli {len(models)} · "
          f"ripetizioni {params['repetitions']}")
    print(f"[i] chiamate totali {total} · gia' fatte {len(already)} · "
          f"da fare {len(todo)}")

    if args.dry_run:
        print("[i] dry-run, nessuna chiamata effettuata")
        return 0

    run_id = f"{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}"
    errors = 0

    with out.open("a", encoding="utf-8") as fh:
        for i, job in enumerate(todo, 1):
            pair, mcfg = job["pair"], job["model_cfg"]
            prompt = pair[job["lang"]]

            reply = providers.call(
                mcfg["provider"],
                prompt,
                mcfg["model"],
                base_url=mcfg.get("base_url", ""),
                api_key_env=mcfg.get("api_key_env", ""),
                temperature=params["temperature"],
                max_tokens=params["max_tokens"],
                extra_body=mcfg.get("extra_body"),
            )
            if reply.error:
                errors += 1

            fh.write(json.dumps({
                "run_id": run_id,
                "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
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
                "error": reply.error,
            }, ensure_ascii=False) + "\n")
            fh.flush()

            if i % 25 == 0 or i == len(todo):
                print(f"    {i}/{len(todo)} · errori {errors}")

    print(f"[ok] scritto {out}")
    if errors:
        print(f"[!] {errors} chiamate con errore: rilancia lo stesso comando, "
              f"riprende da dove si e' fermato")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
