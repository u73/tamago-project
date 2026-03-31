# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""Fine-tuning 用 JSONL の読み書き

system プロンプトは MEMORY.md のハッシュで参照し、
実体は JSONL 先頭の __system_prompts__ エントリに格納する。
これにより同じ MEMORY.md 内容が何百行も重複することを防ぐ。

JSONL 構造:
  行0:   {"__system_prompts__": {"<hash>": "<content>", ...}}
  行1-N: {"messages": [...], "metadata": {...}, "system_hash": "<hash>"}
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Literal

from tamago.memory import get_memory_path
from tamago.prompts import get_talk_system, get_train_finetune_system

JSONL_FILE = "MEMORY.jsonl"

Source = Literal["train", "talk"]


def get_jsonl_path() -> Path:
    """MEMORY.jsonl のパスを返す（MEMORY.md と同じディレクトリ）"""
    return get_memory_path().parent / JSONL_FILE


def _content_hash(text: str) -> str:
    """system プロンプトの短縮ハッシュを返す"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


# ------------------------------------------------------------------ #
# 内部: system プロンプトストア
# ------------------------------------------------------------------ #

def _load_raw_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [line for line in f if line.strip()]


def _load_system_store(path: Path) -> dict[str, str]:
    """先頭行の __system_prompts__ マップを読み出す"""
    lines = _load_raw_lines(path)
    if not lines:
        return {}
    first = json.loads(lines[0])
    if "__system_prompts__" in first:
        return first["__system_prompts__"]
    return {}


def _save_system_store(path: Path, store: dict[str, str]) -> None:
    """先頭行を __system_prompts__ で上書き（他の行は維持）"""
    lines = _load_raw_lines(path)
    header = json.dumps({"__system_prompts__": store}, ensure_ascii=False) + "\n"
    # 既存ヘッダーがあれば差し替え、なければ先頭に追加
    if lines:
        first = json.loads(lines[0])
        if "__system_prompts__" in first:
            lines[0] = header
        else:
            lines.insert(0, header)
    else:
        lines = [header]
    with path.open("w", encoding="utf-8") as f:
        f.writelines(lines)


def _ensure_system(path: Path, system: str) -> str:
    """system プロンプトをストアに登録し、ハッシュを返す"""
    h = _content_hash(system)
    store = _load_system_store(path)
    if h not in store:
        store[h] = system
        _save_system_store(path, store)
    return h


# ------------------------------------------------------------------ #
# 公開 API
# ------------------------------------------------------------------ #

def append_entry(
    system: str,
    user: str,
    assistant: str,
    source: Source,
) -> None:
    """MEMORY.jsonl に 1件追記する"""
    path = get_jsonl_path()
    h = _ensure_system(path, system)
    entry = {
        "messages": [
            {"role": "system",    "content": system},
            {"role": "user",      "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "system_hash": h,
        "metadata": {
            "source":    source,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        },
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def append_train(
    memory_content: str,
    question: str,
    answer: str,
) -> None:
    """train セッションの Q&A を追記する

    user      = AI トレーナーの質問
    assistant = ユーザーの回答（= 分身が持つべき正解）
    """
    system = get_train_finetune_system().format(memory_content=memory_content)
    append_entry(system, question, answer, source="train")


def append_talk(
    memory_content: str,
    user_message: str,
    tamago_response: str,
) -> None:
    """talk セッションの 1往復を追記する

    user      = 会話相手の発言
    assistant = tamago の応答（= 分身の振る舞い）
    """
    system = get_talk_system().format(memory_content=memory_content)
    append_entry(system, user_message, tamago_response, source="talk")


def read_all() -> list[dict]:
    """MEMORY.jsonl の全エントリを返す（__system_prompts__ 行は除外）"""
    path = get_jsonl_path()
    if not path.exists():
        return []
    entries = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if "__system_prompts__" in obj:
                continue
            entries.append(obj)
    return entries


def stats() -> dict[str, int]:
    """エントリ数の統計を返す"""
    entries = read_all()
    total = len(entries)
    by_source: dict[str, int] = {}
    for e in entries:
        src = e.get("metadata", {}).get("source", "unknown")
        by_source[src] = by_source.get(src, 0) + 1
    return {"total": total, **by_source}
