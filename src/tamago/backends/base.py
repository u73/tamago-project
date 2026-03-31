# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""Abstract base class for LLM backends"""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMBackend(ABC):
    """Interface that all backends must implement."""

    @abstractmethod
    def chat(
        self,
        system: str,
        messages: list[dict[str, str]],
        max_tokens: int = 1024,
    ) -> str:
        """Take a system prompt and conversation history, return the next response.

        messages follows the OpenAI-compatible format:
        [{"role": "user"|"assistant", "content": "..."}]
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Backend identifier (e.g., "anthropic", "openai")."""
        ...
