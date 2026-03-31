# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""OpenAI バックエンド"""

from __future__ import annotations

from tamago.backends.base import LLMBackend

DEFAULT_MODEL = "gpt-4o"


class OpenAIBackend(LLMBackend):
    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        **_kwargs: object,
    ) -> None:
        try:
            from openai import OpenAI  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError("openai パッケージが必要です: uv add openai")
        self._model = model or DEFAULT_MODEL
        self._client = OpenAI(base_url=base_url) if base_url else OpenAI()

    @property
    def name(self) -> str:
        return "openai"

    def chat(
        self,
        system: str,
        messages: list[dict[str, str]],
        max_tokens: int = 1024,
    ) -> str:
        full_messages = [{"role": "system", "content": system}, *messages]
        response = self._client.chat.completions.create(
            model=self._model,
            max_tokens=max_tokens,
            messages=full_messages,
        )
        return response.choices[0].message.content or ""
