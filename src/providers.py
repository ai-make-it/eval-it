"""
Adattatori per i fornitori di modelli.

Volutamente scritti con httpx e corpi di richiesta espliciti, senza SDK.
Chi legge deve poter vedere esattamente cosa viene inviato: e' il punto
di un repo la cui credibilita' sta nel metodo.

Ogni adattatore riceve (prompt, model, params) e restituisce un Reply.

Tre comportamenti valgono per tutti gli adattatori.

1. Un base_url vuoto o assente non sovrascrive il default: la
   configurazione lo omette per Anthropic e Gemini, e senza questa
   regola l'URL diventerebbe relativo.
2. Gli errori transitori (429, 5xx, timeout) si riprovano con attesa
   crescente. Con qualche migliaio di chiamate, un 429 non riprovato
   diventa un buco nei dati.
3. Un blocco del fornitore a monte della generazione non e' un errore di
   rete: e' un comportamento del prodotto, si registra come tale
   (blocked=True) e l'analisi lo conta invece di buttarlo via.
"""

from __future__ import annotations

import os
import random
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import httpx

TIMEOUT = httpx.Timeout(120.0, connect=15.0)

# Riprovabili: quote superata e guasti temporanei del fornitore.
RIPROVABILI = {408, 409, 425, 429, 500, 502, 503, 504}
TENTATIVI = 5
ATTESA_BASE = 2.0
ATTESA_MASSIMA = 60.0

ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1"
# ai.google.dev, non Vertex AI: vedi la nota su call_gemini.
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"


@dataclass
class Reply:
    text: str
    latency_ms: int
    raw_model: str | None = None
    error: str | None = None
    blocked: bool = False
    """True quando il fornitore ha fermato la richiesta o la risposta per
    ragioni di contenuto. E' un dato, non un guasto: l'analisi lo conta
    come rifiuto a monte e lo riporta separatamente."""
    attempts: int = 1


class ProviderError(RuntimeError):
    """Errore di configurazione: manca una chiave, il provider non esiste.

    Non si riprova e non si prosegue: e' un problema di chi lancia, non
    del fornitore.
    """


def _key(env_name: str) -> str:
    val = os.environ.get(env_name)
    if not val:
        raise ProviderError(
            f"Variabile d'ambiente {env_name} non impostata. "
            f"Vedi config.example.yaml"
        )
    return val


def _base(valore: str | None, default: str) -> str:
    """Un base_url vuoto vale come assente.

    La configurazione omette base_url per Anthropic e Gemini, e run.py lo
    legge con un default di stringa vuota: senza questo, la stringa vuota
    sovrascriverebbe l'indirizzo del fornitore.
    """
    return (valore or default).rstrip("/")


def _attesa(tentativo: int, retry_after: str | None = None) -> float:
    """Attesa crescente con jitter, o quanto chiede il fornitore."""
    if retry_after:
        try:
            return min(float(retry_after), ATTESA_MASSIMA)
        except ValueError:
            pass
    return min(ATTESA_BASE * (2 ** (tentativo - 1)), ATTESA_MASSIMA) + random.random()


def _con_riprove(esegui: Callable[[], httpx.Response]) -> tuple[httpx.Response | None, int, str | None]:
    """Esegue la chiamata riprovando gli errori transitori.

    Restituisce (risposta, tentativi_usati, errore). La risposta e' None
    solo se tutti i tentativi sono falliti.
    """
    ultimo_errore: str | None = None
    for tentativo in range(1, TENTATIVI + 1):
        try:
            r = esegui()
        except (httpx.TimeoutException, httpx.TransportError) as exc:
            ultimo_errore = f"{type(exc).__name__}: {exc}"
            if tentativo == TENTATIVI:
                return None, tentativo, ultimo_errore
            time.sleep(_attesa(tentativo))
            continue

        if r.status_code in RIPROVABILI and tentativo < TENTATIVI:
            time.sleep(_attesa(tentativo, r.headers.get("retry-after")))
            continue
        return r, tentativo, None

    return None, TENTATIVI, ultimo_errore


# --------------------------------------------------------------------------
# OpenAI e qualunque endpoint compatibile (Mistral, DeepSeek, Qwen, Together,
# Groq, Ollama, vLLM...). E' la strada preferita: un solo adattatore copre
# la maggior parte dei casi.
#
# Nota sui parametri: alcuni modelli recenti di OpenAI rifiutano max_tokens
# e vogliono max_completion_tokens, e non accettano temperature diversa dal
# default. Si sistema per singolo modello con extra_body in config.yaml,
# senza toccare questo file: vedi config.example.yaml.
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
    **_: Any,
) -> Reply:
    if not base_url:
        raise ProviderError(
            "provider openai_compatible richiede base_url in config.yaml"
        )

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
        # Consente di rimuovere una chiave scrivendo null in config.yaml.
        body.update(extra_body)
        body = {k: v for k, v in body.items() if v is not None}

    t0 = time.perf_counter()
    with httpx.Client(timeout=TIMEOUT) as client:
        r, tentativi, errore = _con_riprove(lambda: client.post(
            f"{_base(base_url, '')}/chat/completions", headers=headers, json=body))
    dt = int((time.perf_counter() - t0) * 1000)

    if r is None:
        return Reply(text="", latency_ms=dt, error=errore, attempts=tentativi)
    if r.status_code != 200:
        return Reply(text="", latency_ms=dt, attempts=tentativi,
                     error=f"HTTP {r.status_code}: {r.text[:400]}")

    data = r.json()
    try:
        scelta = data["choices"][0]
        text = scelta["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        return Reply(text="", latency_ms=dt, attempts=tentativi,
                     error=f"Risposta inattesa: {str(data)[:400]}")

    # content_filter: il fornitore ha fermato la generazione. E' un dato.
    finish = scelta.get("finish_reason")
    blocked = finish == "content_filter"
    err = f"FINISH_{finish}" if finish in ("content_filter", "length") else None

    return Reply(text=text, latency_ms=dt, raw_model=data.get("model"),
                 error=err, blocked=blocked, attempts=tentativi)


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
    base_url: str | None = None,
    extra_body: dict[str, Any] | None = None,
    **_: Any,
) -> Reply:
    headers = {
        "x-api-key": _key(api_key_env or "ANTHROPIC_API_KEY"),
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    }
    if extra_body:
        body.update(extra_body)
        body = {k: v for k, v in body.items() if v is not None}

    t0 = time.perf_counter()
    with httpx.Client(timeout=TIMEOUT) as client:
        r, tentativi, errore = _con_riprove(lambda: client.post(
            f"{_base(base_url, ANTHROPIC_BASE_URL)}/messages",
            headers=headers, json=body))
    dt = int((time.perf_counter() - t0) * 1000)

    if r is None:
        return Reply(text="", latency_ms=dt, error=errore, attempts=tentativi)
    if r.status_code != 200:
        return Reply(text="", latency_ms=dt, attempts=tentativi,
                     error=f"HTTP {r.status_code}: {r.text[:400]}")

    data = r.json()
    parts = [b.get("text", "") for b in data.get("content", [])
             if b.get("type") == "text"]
    stop = data.get("stop_reason")
    err = f"STOP_{stop}" if stop not in (None, "end_turn", "stop_sequence") else None
    return Reply(text="".join(parts), latency_ms=dt, attempts=tentativi,
                 raw_model=data.get("model"), error=err)


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
    base_url: str | None = None,
    extra_body: dict[str, Any] | None = None,
    **_: Any,
) -> Reply:
    base = _base(base_url, GEMINI_BASE_URL)
    if "aiplatform.googleapis.com" in base:
        raise ProviderError(
            "Vertex AI non e' ammesso da questo repo: i Service Specific "
            "Terms di Google Cloud pongono condizioni alla pubblicazione "
            "dei risultati di benchmark. Usa generativelanguage.googleapis.com."
        )

    url = f"{base}/models/{model}:generateContent"
    body: dict[str, Any] = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        },
    }
    if extra_body:
        body.update(extra_body)

    # La chiave va in un header, non in querystring: gli URL finiscono nei
    # log dei proxy, gli header no.
    headers = {"x-goog-api-key": _key(api_key_env or "GOOGLE_API_KEY"),
               "Content-Type": "application/json"}

    t0 = time.perf_counter()
    with httpx.Client(timeout=TIMEOUT) as client:
        r, tentativi, errore = _con_riprove(
            lambda: client.post(url, headers=headers, json=body))
    dt = int((time.perf_counter() - t0) * 1000)

    if r is None:
        return Reply(text="", latency_ms=dt, error=errore, attempts=tentativi)
    if r.status_code != 200:
        return Reply(text="", latency_ms=dt, attempts=tentativi,
                     error=f"HTTP {r.status_code}: {r.text[:400]}")

    data = r.json()
    cands = data.get("candidates") or []
    if not cands:
        # Blocco a monte della generazione: comportamento del prodotto.
        fb = data.get("promptFeedback", {})
        return Reply(text="", latency_ms=dt, blocked=True, attempts=tentativi,
                     error=f"BLOCKED_UPSTREAM: {str(fb)[:300]}")

    parts = cands[0].get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts)
    finish = cands[0].get("finishReason")
    blocked = finish in ("SAFETY", "BLOCKLIST", "PROHIBITED_CONTENT", "SPII")
    err = f"FINISH_{finish}" if finish and finish != "STOP" else None
    return Reply(text=text, latency_ms=dt, error=err, blocked=blocked,
                 raw_model=model, attempts=tentativi)


# --------------------------------------------------------------------------
# Mock: serve a provare l'intera pipeline senza chiavi e senza spendere.
# Deterministico sul contenuto del prompt.
#
# Il finto effetto e' voluto: il mock rifiuta un po' piu' spesso in
# italiano, cosi' chi prova la pipeline vede che l'analisi sa leggere un
# delta. Non e' un dato su nessun modello reale.
# --------------------------------------------------------------------------

_MOCK_RIFIUTA = (
    "phishing", "si finga", "impersonating", "falsa notizia", "false news",
    "recensioni negative", "negative reviews", "falsificare",
    "produce a professional training",
)


def call_mock(prompt: str, model: str, **_: Any) -> Reply:
    low = prompt.lower()
    if any(w in low for w in _MOCK_RIFIUTA):
        return Reply(text="Non posso aiutarti con questa richiesta.",
                     latency_ms=5, raw_model="mock")
    return Reply(text="[risposta simulata] " + prompt[:120],
                 latency_ms=5, raw_model="mock")


# --------------------------------------------------------------------------

DISPATCH: dict[str, Callable[..., Reply]] = {
    "openai_compatible": call_openai_compatible,
    "anthropic": call_anthropic,
    "gemini": call_gemini,
    "mock": call_mock,
}

# Chiave predefinita per i provider che non la dichiarano in config.yaml.
CHIAVE_PREDEFINITA = {
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GOOGLE_API_KEY",
}


def chiave_richiesta(cfg: dict[str, Any]) -> str | None:
    """Nome della variabile d'ambiente che serve a questo modello, se serve.

    Usata dal controllo preliminare di run.py: meglio scoprire che manca
    una chiave prima di aver speso qualche centinaio di chiamate.
    """
    provider = cfg.get("provider", "")
    if provider == "mock":
        return None
    if "api_key_env" in cfg:
        # Stringa vuota dichiarata apposta: endpoint locale senza chiave.
        return cfg["api_key_env"] or None
    return CHIAVE_PREDEFINITA.get(provider)


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
    except Exception as exc:  # rete, parsing, imprevisti
        return Reply(text="", latency_ms=0, error=f"{type(exc).__name__}: {exc}")
