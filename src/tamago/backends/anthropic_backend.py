# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""Anthropic Claude バックエンド"""

from __future__ import annotations

from tamago.backends.base import LLMBackend

DEFAULT_MODEL = "claude-sonnet-4-20250514"


class AnthropicBackend(LLMBackend):
    def __init__(self, model: str | None = None, **_kwargs: object) -> None:
        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic パッケージが必要です: uv add anthropic")
        self._model = model or DEFAULT_MODEL
        self._client = anthropic.Anthropic()

    @property
    def name(self) -> str:
        return "anthropic"

    def chat(
        self,
        system: str,
        messages: list[dict[str, str]],
        max_tokens: int = 1024,
    ) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        return response.content[0].text
