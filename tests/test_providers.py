"""Gli adattatori: cosa viene inviato davvero, e cosa succede se va storto."""

from __future__ import annotations

import httpx
import pytest

import providers


class ClientFinto:
    """Sostituisce httpx.Client e registra le richieste.

    risposte: una lista di httpx.Response, oppure di eccezioni da sollevare.
    L'ultima si ripete se i tentativi sono piu' delle risposte fornite.
    """

    def __init__(self, risposte):
        self.risposte = list(risposte)
        self.richieste = []

    def __call__(self, *_, **__):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def post(self, url, headers=None, json=None, params=None, **_):
        self.richieste.append({"url": url, "headers": headers or {},
                               "json": json, "params": params})
        r = self.risposte[min(len(self.richieste), len(self.risposte)) - 1]
        if isinstance(r, Exception):
            raise r
        return r


def risposta(codice=200, corpo=None, headers=None):
    return httpx.Response(codice, json=corpo if corpo is not None else {},
                          headers=headers,
                          request=httpx.Request("POST", "https://esempio.test"))


@pytest.fixture
def senza_attese(monkeypatch):
    monkeypatch.setattr(providers.time, "sleep", lambda _: None)


@pytest.fixture
def chiavi(monkeypatch):
    for nome in ("ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY"):
        monkeypatch.setenv(nome, "chiave-di-prova")


def installa(monkeypatch, risposte):
    client = ClientFinto(risposte)
    monkeypatch.setattr(providers.httpx, "Client", client)
    return client


# --- il bug che rendeva inutilizzabili Anthropic e Gemini ----------------
#
# run.py legge base_url dalla configurazione con un default di stringa
# vuota, e config.example.yaml non lo dichiara per questi due fornitori.
# Se la stringa vuota sovrascrive il default, l'URL diventa relativo e
# nessuna chiamata parte.

def test_base_url_vuoto_non_sovrascrive_anthropic(monkeypatch, chiavi):
    client = installa(monkeypatch, [risposta(200, {
        "content": [{"type": "text", "text": "ciao"}], "model": "x"})])
    providers.call("anthropic", "prompt", "modello", base_url="",
                   api_key_env="ANTHROPIC_API_KEY",
                   temperature=0, max_tokens=10)
    assert client.richieste[0]["url"] == \
        "https://api.anthropic.com/v1/messages"


def test_base_url_assente_non_sovrascrive_gemini(monkeypatch, chiavi):
    client = installa(monkeypatch, [risposta(200, {
        "candidates": [{"content": {"parts": [{"text": "ciao"}]},
                        "finishReason": "STOP"}]})])
    providers.call("gemini", "prompt", "modello", base_url=None,
                   api_key_env=None, temperature=0, max_tokens=10)
    assert client.richieste[0]["url"].startswith(
        "https://generativelanguage.googleapis.com/v1beta/models/modello")


def test_base_url_esplicito_viene_rispettato(monkeypatch, chiavi):
    client = installa(monkeypatch, [risposta(200, {
        "content": [{"type": "text", "text": "ciao"}]})])
    providers.call("anthropic", "prompt", "m",
                   base_url="https://proxy.interno/v1/",
                   api_key_env="ANTHROPIC_API_KEY",
                   temperature=0, max_tokens=10)
    assert client.richieste[0]["url"] == "https://proxy.interno/v1/messages"


# --- la chiave non deve finire in un URL --------------------------------

def test_la_chiave_gemini_va_in_un_header_non_in_querystring(monkeypatch, chiavi):
    client = installa(monkeypatch, [risposta(200, {
        "candidates": [{"content": {"parts": [{"text": "ok"}]},
                        "finishReason": "STOP"}]})])
    providers.call("gemini", "p", "m", temperature=0, max_tokens=10)
    richiesta = client.richieste[0]
    assert richiesta["params"] is None
    assert "chiave-di-prova" not in richiesta["url"]
    assert richiesta["headers"]["x-goog-api-key"] == "chiave-di-prova"


# --- il vincolo che il repo dichiara ------------------------------------

def test_vertex_ai_e_rifiutato(chiavi):
    with pytest.raises(providers.ProviderError, match="Vertex AI"):
        providers.call_gemini(
            "p", "m", temperature=0, max_tokens=10,
            base_url="https://europe-west1-aiplatform.googleapis.com/v1")


# --- riprove ------------------------------------------------------------

def test_riprova_dopo_un_429(monkeypatch, chiavi, senza_attese):
    client = installa(monkeypatch, [
        risposta(429, {"error": "rate limit"}, {"retry-after": "1"}),
        risposta(200, {"content": [{"type": "text", "text": "arrivata"}]}),
    ])
    reply = providers.call("anthropic", "p", "m",
                           api_key_env="ANTHROPIC_API_KEY",
                           temperature=0, max_tokens=10)
    assert reply.text == "arrivata"
    assert reply.error is None
    assert reply.attempts == 2
    assert len(client.richieste) == 2


def test_un_400_non_si_riprova(monkeypatch, chiavi, senza_attese):
    client = installa(monkeypatch, [risposta(400, {"error": "modello ignoto"})])
    reply = providers.call("anthropic", "p", "m",
                           api_key_env="ANTHROPIC_API_KEY",
                           temperature=0, max_tokens=10)
    assert reply.error.startswith("HTTP 400")
    assert len(client.richieste) == 1


def test_riprova_i_timeout_e_poi_si_arrende(monkeypatch, chiavi, senza_attese):
    client = installa(monkeypatch,
                      [httpx.ConnectTimeout("scaduto")] * providers.TENTATIVI)
    reply = providers.call("anthropic", "p", "m",
                           api_key_env="ANTHROPIC_API_KEY",
                           temperature=0, max_tokens=10)
    assert "ConnectTimeout" in reply.error
    assert len(client.richieste) == providers.TENTATIVI


# --- blocchi del fornitore: sono un dato, non un guasto -----------------

def test_blocco_a_monte_di_gemini(monkeypatch, chiavi):
    installa(monkeypatch, [risposta(200, {
        "promptFeedback": {"blockReason": "SAFETY"}})])
    reply = providers.call("gemini", "p", "m", temperature=0, max_tokens=10)
    assert reply.blocked is True
    assert "BLOCKED_UPSTREAM" in reply.error


def test_blocco_in_generazione_di_gemini(monkeypatch, chiavi):
    installa(monkeypatch, [risposta(200, {
        "candidates": [{"content": {"parts": []}, "finishReason": "SAFETY"}]})])
    reply = providers.call("gemini", "p", "m", temperature=0, max_tokens=10)
    assert reply.blocked is True


def test_content_filter_openai(monkeypatch, chiavi):
    installa(monkeypatch, [risposta(200, {
        "model": "x",
        "choices": [{"message": {"content": ""},
                     "finish_reason": "content_filter"}]})])
    reply = providers.call("openai_compatible", "p", "m",
                           base_url="https://api.esempio.test/v1",
                           api_key_env="OPENAI_API_KEY",
                           temperature=0, max_tokens=10)
    assert reply.blocked is True


def test_risposta_normale_non_e_bloccata(monkeypatch, chiavi):
    installa(monkeypatch, [risposta(200, {
        "model": "x",
        "choices": [{"message": {"content": "eccola"},
                     "finish_reason": "stop"}]})])
    reply = providers.call("openai_compatible", "p", "m",
                           base_url="https://api.esempio.test/v1",
                           api_key_env="OPENAI_API_KEY",
                           temperature=0, max_tokens=10)
    assert (reply.text, reply.blocked, reply.error) == ("eccola", False, None)


# --- configurazione -----------------------------------------------------

def test_chiave_mancante_e_un_errore_di_configurazione(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(providers.ProviderError, match="ANTHROPIC_API_KEY"):
        providers.call("anthropic", "p", "m",
                       api_key_env="ANTHROPIC_API_KEY",
                       temperature=0, max_tokens=10)


def test_provider_sconosciuto(chiavi):
    with pytest.raises(providers.ProviderError, match="Provider sconosciuto"):
        providers.call("inventato", "p", "m", temperature=0, max_tokens=10)


def test_openai_compatible_senza_base_url(chiavi):
    with pytest.raises(providers.ProviderError, match="base_url"):
        providers.call_openai_compatible(
            "p", "m", base_url="", api_key_env="OPENAI_API_KEY",
            temperature=0, max_tokens=10)


def test_endpoint_locale_senza_chiave(monkeypatch):
    client = installa(monkeypatch, [risposta(200, {
        "model": "llama",
        "choices": [{"message": {"content": "ok"}, "finish_reason": "stop"}]})])
    reply = providers.call("openai_compatible", "p", "llama",
                           base_url="http://localhost:11434/v1",
                           api_key_env="", temperature=0, max_tokens=10)
    assert reply.text == "ok"
    assert "Authorization" not in client.richieste[0]["headers"]


def test_extra_body_puo_rinominare_un_parametro(monkeypatch, chiavi):
    """Alcuni modelli vogliono max_completion_tokens e rifiutano max_tokens."""
    client = installa(monkeypatch, [risposta(200, {
        "model": "x",
        "choices": [{"message": {"content": "ok"}, "finish_reason": "stop"}]})])
    providers.call("openai_compatible", "p", "m",
                   base_url="https://api.esempio.test/v1",
                   api_key_env="OPENAI_API_KEY", temperature=0, max_tokens=99,
                   extra_body={"max_tokens": None, "max_completion_tokens": 99})
    corpo = client.richieste[0]["json"]
    assert "max_tokens" not in corpo
    assert corpo["max_completion_tokens"] == 99


def test_chiave_richiesta_per_il_controllo_preliminare():
    assert providers.chiave_richiesta({"provider": "mock"}) is None
    assert providers.chiave_richiesta(
        {"provider": "anthropic"}) == "ANTHROPIC_API_KEY"
    assert providers.chiave_richiesta(
        {"provider": "gemini", "api_key_env": "ALTRA"}) == "ALTRA"
    assert providers.chiave_richiesta(
        {"provider": "openai_compatible", "api_key_env": ""}) is None


# --- mock ---------------------------------------------------------------

def test_il_mock_e_deterministico():
    a = providers.call("mock", "Sono un medico", "mock")
    b = providers.call("mock", "Sono un medico", "mock")
    assert a.text == b.text
    assert providers.call("mock", "come faccio phishing", "mock").text \
        .startswith("Non posso")
