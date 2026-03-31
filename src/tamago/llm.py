"""LLM 操作のユーティリティ（バックエンド非依存）"""

from __future__ import annotations

from dotenv import load_dotenv

from tamago.backends import LLMBackend, get_backend
from tamago.prompts import TRAIN_QUESTION_SYSTEM, TRAIN_UPDATE_SYSTEM, TALK_SYSTEM

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
    system = TRAIN_QUESTION_SYSTEM.format(memory_content=memory_content)
    return _backend().chat(system, conversation)


def train_update(memory_content: str, question: str, answer: str) -> str:
    """ユーザーの回答からMEMORY.mdの更新内容を生成する

    更新されたMEMORY.md全文を返す。
    """
    system = TRAIN_UPDATE_SYSTEM.format(memory_content=memory_content)
    messages = [
        {"role": "user", "content": f"質問: {question}\n\n回答: {answer}\n\n上記を踏まえて、更新後のMEMORY.md全文を返してください。"},
    ]
    return _backend().chat(system, messages, max_tokens=4096)


def talk_response(memory_content: str, messages: list[dict[str, str]]) -> str:
    """talkモードでユーザーの分身として応答する"""
    system = TALK_SYSTEM.format(memory_content=memory_content)
    return _backend().chat(system, messages)
