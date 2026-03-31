"""LLM 操作のユーティリティ（バックエンド非依存）"""

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

# バックエンド設定が変わらない限り同じインスタンスを使い回す
_cached_backend: LLMBackend | None = None
_cached_backend_name: str | None = None


def _backend() -> LLMBackend:
    """アクティブバックエンドのシングルトンを返す"""
    global _cached_backend, _cached_backend_name
    from tamago.config import get_active_backend

    current_name = get_active_backend()
    if _cached_backend is None or _cached_backend_name != current_name:
        _cached_backend = get_backend(current_name)
        _cached_backend_name = current_name
    return _cached_backend


def train_question(memory_content: str, conversation: list[dict[str, str]]) -> str:
    """trainモードでの質問を生成する"""
    system = get_train_question_system().format(memory_content=memory_content)
    return _backend().chat(system, conversation)


def train_update(memory_content: str, question: str, answer: str) -> str:
    """ユーザーの回答からMEMORY.mdの更新内容を生成する

    更新されたMEMORY.md全文を返す。
    """
    system = get_train_update_system().format(memory_content=memory_content)
    messages = [
        {"role": "user", "content": get_train_update_user(question, answer)},
    ]
    return _backend().chat(system, messages, max_tokens=4096)


def talk_response(memory_content: str, messages: list[dict[str, str]]) -> str:
    """talkモードでユーザーの分身として応答する"""
    system = get_talk_system().format(memory_content=memory_content)
    return _backend().chat(system, messages)
