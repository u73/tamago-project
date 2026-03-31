# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""MEMORY.md の読み書き・パース"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from tamago.i18n import t, SECTION_KEYS

MEMORY_FILE = "MEMORY.md"


def _section_names() -> list[str]:
    """現在の言語でのセクション名リストを返す"""
    return [t(f"section.{k}") for k in SECTION_KEYS]


def _history_section_names() -> set[str]:
    """全言語の「更新履歴」セクション名を返す（言語切替対応）"""
    return {"更新履歴", "History"}


def get_memory_path() -> Path:
    return Path.cwd() / MEMORY_FILE


def memory_exists() -> bool:
    return get_memory_path().exists()


def create_memory() -> Path:
    """MEMORY.md を雛形から生成する"""
    dest = get_memory_path()
    template = t("template.memory")
    dest.write_text(template, encoding="utf-8")
    return dest


def read_memory() -> str:
    """MEMORY.md の全文を読み込む"""
    path = get_memory_path()
    if not path.exists():
        raise FileNotFoundError(t("memory.not_found", file=MEMORY_FILE))
    return path.read_text(encoding="utf-8")


def write_memory(content: str) -> None:
    """MEMORY.md を上書き保存する"""
    get_memory_path().write_text(content, encoding="utf-8")


def parse_sections(content: str) -> dict[str, str]:
    """MEMORY.md をセクションごとにパースする"""
    sections: dict[str, str] = {}
    current_section: str | None = None
    current_lines: list[str] = []

    for line in content.splitlines():
        match = re.match(r"^## (.+)$", line)
        if match:
            if current_section is not None:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = match.group(1)
            current_lines = []
        elif current_section is not None:
            current_lines.append(line)

    if current_section is not None:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections


def update_section(content: str, section_name: str, new_content: str) -> str:
    """指定セクションの内容を置換する"""
    lines = content.splitlines()
    result: list[str] = []
    in_target = False
    replaced = False

    for line in lines:
        match = re.match(r"^## (.+)$", line)
        if match:
            if in_target:
                # 前のセクションの終わり
                result.append("")
                result.append(line)
                in_target = False
                replaced = True
                continue
            if match.group(1) == section_name:
                result.append(line)
                result.append("")
                result.append(new_content)
                in_target = True
                continue
        if not in_target:
            result.append(line)

    # 最後のセクションだった場合
    if in_target and not replaced:
        result.append("")

    return "\n".join(result)


def add_history_entry(content: str, entry: str) -> str:
    """更新履歴セクションにエントリを追加する"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    history_entry = f"- [{timestamp}] {entry}"

    sections = parse_sections(content)

    # 言語に関係なく更新履歴セクションを探す
    history_name = None
    for name in _history_section_names():
        if name in sections:
            history_name = name
            break

    if history_name is None:
        # 見つからなければ現在の言語のセクション名を使う
        history_name = t("section.history")

    current_history = sections.get(history_name, "")

    if current_history:
        new_history = f"{history_entry}\n{current_history}"
    else:
        new_history = history_entry

    return update_section(content, history_name, new_history)


def section_stats(content: str) -> dict[str, dict[str, int]]:
    """各セクションの統計情報を返す"""
    sections = parse_sections(content)
    history_names = _history_section_names()
    stats: dict[str, dict[str, int]] = {}
    for name, text in sections.items():
        if name in history_names:
            continue
        chars = len(text)
        lines = len([l for l in text.splitlines() if l.strip()]) if text else 0
        stats[name] = {"chars": chars, "lines": lines}
    return stats
