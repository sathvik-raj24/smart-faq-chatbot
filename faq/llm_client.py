"""Multi-provider LLM client (requirement #2: "send the question to an LLM").

Supported backends - choose with the LLM_PROVIDER env var or --provider flag:

    openai       https://api.openai.com/v1          needs OPENAI_API_KEY
    huggingface  https://router.huggingface.co/v1   needs HF_TOKEN (free tier)
    ollama       http://localhost:11434/v1          local & free (ollama serve)
    demo         offline answers from data/syllabus.md (no key, no internet)
    auto         first available: openai -> huggingface -> ollama -> demo

All chat providers use the OpenAI-compatible interface via the `openai` SDK,
so one code path talks to every provider.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()  # read .env if present

try:  # the openai SDK is optional - demo mode works without it
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None

from faq.demo_engine import DemoBackend

PROVIDER_SPECS: dict[str, dict] = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "key_env": "OPENAI_API_KEY",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-4o-mini",
    },
    "huggingface": {
        "base_url": "https://router.huggingface.co/v1",
        "key_env": "HF_TOKEN",
        "model_env": "HUGGINGFACE_MODEL",
        "default_model": "meta-llama/Llama-3.1-8B-Instruct",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "key_env": None,
        "model_env": "OLLAMA_MODEL",
        "default_model": "llama3.2",
    },
}


class LLMClient:
    """Generates answers using the configured provider, with demo fallback."""

    def __init__(self, provider: str | None = None) -> None:
        requested = (provider or os.getenv("LLM_PROVIDER", "auto")).strip().lower()
        self.provider_name = self._resolve(requested)

        if self.provider_name == "demo" or OpenAI is None:
            self.provider_name = "demo" if OpenAI is None else self.provider_name
            self._backend = DemoBackend()
            self._client = None
            self.model = None
            return

        spec = PROVIDER_SPECS[self.provider_name]
        api_key = os.getenv(spec["key_env"]) or "not-needed"
        self._client = OpenAI(base_url=spec["base_url"], api_key=api_key)
        self.model = os.getenv(spec["model_env"], spec["default_model"])
        self._backend = None  # created lazily only if a call fails

    # ------------------------------------------------------------------ #
    def _resolve(self, requested: str) -> str:
        if requested == "demo":
            return "demo"
        if requested in PROVIDER_SPECS:
            return requested
        # auto: prefer providers that have a key, then local ollama, then demo
        for name in ("openai", "huggingface"):
            if os.getenv(PROVIDER_SPECS[name]["key_env"]):
                return name
        if self._ollama_alive():
            return "ollama"
        return "demo"

    @staticmethod
    def _ollama_alive() -> bool:
        try:
            import httpx  # installed together with the openai SDK

            httpx.get("http://localhost:11434/v1/models", timeout=0.8)
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------ #
    def describe(self) -> str:
        if self.provider_name == "demo":
            return "demo mode (offline answers from data/syllabus.md - no API key)"
        return f"{self.provider_name} (model: {self.model})"

    def generate(self, messages: list[dict]) -> str:
        """Send the chat messages to the LLM and return the reply text."""
        if self.provider_name == "demo":
            return self._backend.chat(messages)

        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=500,
            )
            return (response.choices[0].message.content or "").strip()
        except Exception as exc:  # never crash the app - degrade gracefully
            warning = (
                f"[Warning] {self.provider_name} call failed "
                f"({exc.__class__.__name__}: {exc}). Falling back to offline demo mode.\n\n"
            )
            if self._backend is None:
                self._backend = DemoBackend()
            return warning + self._backend.chat(messages)
