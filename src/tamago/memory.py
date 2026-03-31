# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""MEMORY.md read/write/parse utilities"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from tamago.i18n import t, SECTION_KEYS

MEMORY_FILE = "MEMORY.md"


def _section_names() -> list[str]:
    """Return section names in the current language."""
    return [t(f"section.{k}") for k in SECTION_KEYS]


def _history_section_names() -> set[str]:
    """Return the history section name in all languages (for cross-language compat)."""
    return {"更新履歴", "History"}


def get_memory_path() -> Path:
    return Path.cwd() / MEMORY_FILE


def memory_exists() -> bool:
    return get_memory_path().exists()


def create_memory() -> Path:
    """Generate MEMORY.md from the template."""
    dest = get_memory_path()
    template = t("template.memory")
    dest.write_text(template, encoding="utf-8")
    return dest


def read_memory() -> str:
    """Read the full contents of MEMORY.md."""
    path = get_memory_path()
    if not path.exists():
        raise FileNotFoundError(t("memory.not_found", file=MEMORY_FILE))
    return path.read_text(encoding="utf-8")


def write_memory(content: str) -> None:
    """Overwrite MEMORY.md."""
    get_memory_path().write_text(content, encoding="utf-8")


def parse_sections(content: str) -> dict[str, str]:
    """Parse MEMORY.md into sections keyed by header name."""
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
    """Replace the content of a specific section."""
    lines = content.splitlines()
    result: list[str] = []
    in_target = False
    replaced = False

    for line in lines:
        match = re.match(r"^## (.+)$", line)
        if match:
            if in_target:
                # End of the target section
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

    # Handle case where target was the last section
    if in_target and not replaced:
        result.append("")

    return "\n".join(result)


def add_history_entry(content: str, entry: str) -> str:
    """Add an entry to the history section."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    history_entry = f"- [{timestamp}] {entry}"

    sections = parse_sections(content)

    # Find the history section regardless of language
    history_name = None
    for name in _history_section_names():
        if name in sections:
            history_name = name
            break

    if history_name is None:
        # Fall back to the current language's section name
        history_name = t("section.history")

    current_history = sections.get(history_name, "")

    if current_history:
        new_history = f"{history_entry}\n{current_history}"
    else:
        new_history = history_entry

    return update_section(content, history_name, new_history)


def section_stats(content: str) -> dict[str, dict[str, int]]:
    """Return per-section statistics (chars, lines)."""
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
