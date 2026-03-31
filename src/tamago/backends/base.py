# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""LLM バックエンドの抽象基底クラス"""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMBackend(ABC):
    """全バックエンドが実装すべきインターフェース"""

    @abstractmethod
    def chat(
        self,
        system: str,
        messages: list[dict[str, str]],
        max_tokens: int = 1024,
    ) -> str:
        """
        system プロンプトと会話履歴を受け取り、次の応答テキストを返す。

        messages は OpenAI 互換の形式: [{"role": "user"|"assistant", "content": "..."}]
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """バックエンド識別子（例: "anthropic", "openai"）"""
        ...
