# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""Fine-tuning JSONL read/write utilities.

System prompts are referenced by MEMORY.md hash,
with the actual content stored in a __system_prompts__ entry at the top of the JSONL.
This prevents the same MEMORY.md content from being duplicated across hundreds of rows.

JSONL structure:
  Row 0:   {"__system_prompts__": {"<hash>": "<content>", ...}}
  Row 1-N: {"messages": [...], "metadata": {...}, "system_hash": "<hash>"}
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
    """Return the path to MEMORY.jsonl (same directory as MEMORY.md)."""
    return get_memory_path().parent / JSONL_FILE


def _content_hash(text: str) -> str:
    """Return a truncated SHA-256 hash of a system prompt."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


# ------------------------------------------------------------------ #
# Internal: system prompt store
# ------------------------------------------------------------------ #

def _load_raw_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [line for line in f if line.strip()]


def _load_system_store(path: Path) -> dict[str, str]:
    """Read the __system_prompts__ map from the first line."""
    lines = _load_raw_lines(path)
    if not lines:
        return {}
    first = json.loads(lines[0])
    if "__system_prompts__" in first:
        return first["__system_prompts__"]
    return {}


def _save_system_store(path: Path, store: dict[str, str]) -> None:
    """Overwrite the first line with __system_prompts__ (preserve other lines)."""
    lines = _load_raw_lines(path)
    header = json.dumps({"__system_prompts__": store}, ensure_ascii=False) + "\n"
    # Replace existing header or prepend if none exists
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
    """Register a system prompt in the store and return its hash."""
    h = _content_hash(system)
    store = _load_system_store(path)
    if h not in store:
        store[h] = system
        _save_system_store(path, store)
    return h


# ------------------------------------------------------------------ #
# Public API
# ------------------------------------------------------------------ #

def append_entry(
    system: str,
    user: str,
    assistant: str,
    source: Source,
) -> None:
    """Append one entry to MEMORY.jsonl."""
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
    """Append a train session Q&A pair.

    user      = AI trainer's question
    assistant = user's answer (the ground truth for the clone)
    """
    system = get_train_finetune_system().format(memory_content=memory_content)
    append_entry(system, question, answer, source="train")


def append_talk(
    memory_content: str,
    user_message: str,
    tamago_response: str,
) -> None:
    """Append one talk session exchange.

    user      = conversation partner's message
    assistant = tamago's response (the clone's behavior)
    """
    system = get_talk_system().format(memory_content=memory_content)
    append_entry(system, user_message, tamago_response, source="talk")


def read_all() -> list[dict]:
    """Return all entries from MEMORY.jsonl (excluding __system_prompts__ row)."""
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
    """Return entry count statistics."""
    entries = read_all()
    total = len(entries)
    by_source: dict[str, int] = {}
    for e in entries:
        src = e.get("metadata", {}).get("source", "unknown")
        by_source[src] = by_source.get(src, 0) + 1
    return {"total": total, **by_source}
