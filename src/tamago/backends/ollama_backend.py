# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""Ollama backend"""

from __future__ import annotations

from tamago.backends.base import LLMBackend

DEFAULT_MODEL = "llama3.2"
DEFAULT_BASE_URL = "http://localhost:11434"


class OllamaBackend(LLMBackend):
    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        **_kwargs: object,
    ) -> None:
        try:
            from ollama import Client  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError("ollama package is required: uv add ollama")
        self._model = model or DEFAULT_MODEL
        self._client = Client(host=base_url or DEFAULT_BASE_URL)

    @property
    def name(self) -> str:
        return "ollama"

    def chat(
        self,
        system: str,
        messages: list[dict[str, str]],
        max_tokens: int = 1024,
    ) -> str:
        full_messages = [{"role": "system", "content": system}, *messages]
        response = self._client.chat(
            model=self._model,
            messages=full_messages,
            options={"num_predict": max_tokens},
        )
        return response.message.content or ""
