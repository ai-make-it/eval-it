"""
Adattatori per i fornitori di modelli.

Volutamente scritti con httpx e corpi di richiesta espliciti, senza SDK.
Chi legge deve poter vedere esattamente cosa viene inviato: e' il punto
di un repo la cui credibilita' sta nel metodo.

Ogni adattatore riceve (prompt, model, params) e restituisce (testo, meta).
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

import httpx

TIMEOUT = httpx.Timeout(120.0, connect=15.0)


@dataclass
class Reply:
    text: str
    latency_ms: int
    raw_model: str | None = None
    error: str | None = None


class ProviderError(RuntimeError):
    pass


def _key(env_name: str) -> str:
    val = os.environ.get(env_name)
    if not val:
        raise ProviderError(
            f"Variabile d'ambiente {env_name} non impostata. "
            f"Vedi config.example.yaml"
        )
    return val


# --------------------------------------------------------------------------
# OpenAI e qualunque endpoint compatibile (Mistral, DeepSeek, Qwen, Together,
# Groq, Ollama, vLLM...). E' la strada preferita: un solo adattatore copre
# la maggior parte dei casi.
# --------------------------------------------------------------------------

def call_openai_compatible(
    prompt: str,
    model: str,
    *,
    base_url: str,
    api_key_env: str,
    temperature: float,
    max_tokens: int,
    extra_body: dict[str, Any] | None = None,
) -> Reply:
    headers = {"Content-Type": "application/json"}
    if api_key_env:
        headers["Authorization"] = f"Bearer {_key(api_key_env)}"

    body: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if extra_body:
        body.update(extra_body)

    t0 = time.perf_counter()
    with httpx.Client(timeout=TIMEOUT) as client:
        r = client.post(f"{base_url.rstrip('/')}/chat/completions",
                        headers=headers, json=body)
    dt = int((time.perf_counter() - t0) * 1000)

    if r.status_code != 200:
        return Reply(text="", latency_ms=dt,
                     error=f"HTTP {r.status_code}: {r.text[:400]}")

    data = r.json()
    try:
        text = data["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        return Reply(text="", latency_ms=dt,
                     error=f"Risposta inattesa: {str(data)[:400]}")

    return Reply(text=text, latency_ms=dt, raw_model=data.get("model"))


# --------------------------------------------------------------------------
# Anthropic
# --------------------------------------------------------------------------

def call_anthropic(
    prompt: str,
    model: str,
    *,
    api_key_env: str = "ANTHROPIC_API_KEY",
    temperature: float,
    max_tokens: int,
    base_url: str = "https://api.anthropic.com/v1",
    **_: Any,
) -> Reply:
    headers = {
        "x-api-key": _key(api_key_env),
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    }

    t0 = time.perf_counter()
    with httpx.Client(timeout=TIMEOUT) as client:
        r = client.post(f"{base_url.rstrip('/')}/messages",
                        headers=headers, json=body)
    dt = int((time.perf_counter() - t0) * 1000)

    if r.status_code != 200:
        return Reply(text="", latency_ms=dt,
                     error=f"HTTP {r.status_code}: {r.text[:400]}")

    data = r.json()
    parts = [b.get("text", "") for b in data.get("content", [])
             if b.get("type") == "text"]
    return Reply(text="".join(parts), latency_ms=dt,
                 raw_model=data.get("model"))


# --------------------------------------------------------------------------
# Google Gemini via AI Studio.
#
# NOTA IMPORTANTE, non e' un dettaglio: si usa ai.google.dev e NON Vertex AI.
# I Service Specific Terms di Google Cloud contengono una clausola
# "Benchmarking" (par. 7) che pone condizioni alla pubblicazione dei
# risultati. L'endpoint AI Studio non e' soggetto a quella clausola.
# --------------------------------------------------------------------------

def call_gemini(
    prompt: str,
    model: str,
    *,
    api_key_env: str = "GOOGLE_API_KEY",
    temperature: float,
    max_tokens: int,
    base_url: str = "https://generativelanguage.googleapis.com/v1beta",
    **_: Any,
) -> Reply:
    url = f"{base_url.rstrip('/')}/models/{model}:generateContent"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        },
    }

    t0 = time.perf_counter()
    with httpx.Client(timeout=TIMEOUT) as client:
        r = client.post(url, params={"key": _key(api_key_env)}, json=body)
    dt = int((time.perf_counter() - t0) * 1000)

    if r.status_code != 200:
        return Reply(text="", latency_ms=dt,
                     error=f"HTTP {r.status_code}: {r.text[:400]}")

    data = r.json()
    cands = data.get("candidates") or []
    if not cands:
        # Un blocco a monte e' un dato, non un errore: va registrato.
        fb = data.get("promptFeedback", {})
        return Reply(text="", latency_ms=dt,
                     error=f"BLOCKED_UPSTREAM: {fb}")
    parts = cands[0].get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts)
    finish = cands[0].get("finishReason")
    err = f"FINISH_{finish}" if finish and finish != "STOP" else None
    return Reply(text=text, latency_ms=dt, error=err)


# --------------------------------------------------------------------------
# Mock: serve a provare l'intera pipeline senza chiavi e senza spendere.
# Deterministico sul contenuto del prompt.
# --------------------------------------------------------------------------

def call_mock(prompt: str, model: str, **_: Any) -> Reply:
    low = prompt.lower()
    rifiuta = any(w in low for w in
                  ("phishing", "si finga", "impersonating", "falsa notizia",
                   "false news", "recensioni negative", "negative reviews",
                   "falsificare", "produce a professional training"))
    # Rifiuto leggermente piu' probabile in italiano: e' un finto effetto,
    # serve solo a verificare che l'analisi lo sappia leggere.
    if rifiuta:
        return Reply(text="Non posso aiutarti con questa richiesta.",
                     latency_ms=5, raw_model="mock")
    return Reply(text="[risposta simulata] " + prompt[:120],
                 latency_ms=5, raw_model="mock")


# --------------------------------------------------------------------------

DISPATCH = {
    "openai_compatible": call_openai_compatible,
    "anthropic": call_anthropic,
    "gemini": call_gemini,
    "mock": call_mock,
}


def call(provider: str, prompt: str, model: str, **kwargs: Any) -> Reply:
    fn = DISPATCH.get(provider)
    if fn is None:
        raise ProviderError(
            f"Provider sconosciuto: {provider}. "
            f"Disponibili: {', '.join(DISPATCH)}"
        )
    try:
        return fn(prompt, model, **kwargs)
    except ProviderError:
        raise
    except Exception as exc:  # rete, timeout, parsing
        return Reply(text="", latency_ms=0, error=f"{type(exc).__name__}: {exc}")
