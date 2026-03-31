# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""LLM utilities (backend-agnostic)"""

from __future__ import annotations

from dotenv import load_dotenv

from tamago.backends import LLMBackend, get_backend
from tamago.prompts import (
    get_train_question_system,
    get_train_update_system,
    get_train_update_user,
    get_talk_system,
)

load_dotenv()

# Reuse the same backend instance unless the config changes
_cached_backend: LLMBackend | None = None
_cached_backend_name: str | None = None


def _backend() -> LLMBackend:
    """Return a singleton for the active backend."""
    global _cached_backend, _cached_backend_name
    from tamago.config import get_active_backend

    current_name = get_active_backend()
    if _cached_backend is None or _cached_backend_name != current_name:
        _cached_backend = get_backend(current_name)
        _cached_backend_name = current_name
    return _cached_backend


def train_question(memory_content: str, conversation: list[dict[str, str]]) -> str:
    """Generate a question for train mode."""
    system = get_train_question_system().format(memory_content=memory_content)
    return _backend().chat(system, conversation)


def train_update(memory_content: str, question: str, answer: str) -> str:
    """Generate updated MEMORY.md content from the user's answer.

    Returns the full updated MEMORY.md text.
    """
    system = get_train_update_system().format(memory_content=memory_content)
    messages = [
        {"role": "user", "content": get_train_update_user(question, answer)},
    ]
    return _backend().chat(system, messages, max_tokens=4096)


def talk_response(memory_content: str, messages: list[dict[str, str]]) -> str:
    """Respond as the user's AI clone in talk mode."""
    system = get_talk_system().format(memory_content=memory_content)
    return _backend().chat(system, messages)
