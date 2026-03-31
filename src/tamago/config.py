# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""Configuration management for ~/.tamago/config.yaml"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path.home() / ".tamago"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

DEFAULT_CONFIG: dict[str, Any] = {
    "language": "ja",
    "backend": "anthropic",
    "backends": {
        "anthropic": {
            "model": "claude-sonnet-4-20250514",
        },
        "openai": {
            "model": "gpt-4o",
            "base_url": None,
        },
        "ollama": {
            "model": "llama3.2",
            "base_url": "http://localhost:11434",
        },
        "llamacpp": {
            "model_path": None,       # Path to GGUF file (required)
            "chat_format": "chatml",  # chatml / llama-2 / mistral-instruct etc.
            "n_ctx": 4096,            # Context length
            "n_gpu_layers": 0,        # 0=CPU only / -1=all layers on GPU
        },
    },
}

# Legacy keys to remove from llamacpp (remnants of old HTTP API approach)
_LLAMACPP_REMOVED_KEYS = {"base_url", "model"}


def load_config() -> dict[str, Any]:
    """Load ~/.tamago/config.yaml. Returns defaults if file doesn't exist."""
    if not CONFIG_FILE.exists():
        return copy.deepcopy(DEFAULT_CONFIG)
    with CONFIG_FILE.open(encoding="utf-8") as f:
        loaded = yaml.safe_load(f) or {}
    # Merge with defaults (backends are merged per-backend)
    config = copy.deepcopy(DEFAULT_CONFIG)
    config.update({k: v for k, v in loaded.items() if k != "backends"})
    if "backends" in loaded:
        for name, settings in loaded["backends"].items():
            merged = settings or {}
            # Strip legacy llamacpp keys to normalize to new format
            if name == "llamacpp":
                merged = {k: v for k, v in merged.items() if k not in _LLAMACPP_REMOVED_KEYS}
            if name in config["backends"]:
                config["backends"][name].update(merged)
            else:
                config["backends"][name] = merged
    return config


def save_config(config: dict[str, Any]) -> None:
    """Save configuration to ~/.tamago/config.yaml."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)


def get_language() -> str:
    return load_config().get("language", "ja")


def get_active_backend() -> str:
    return load_config()["backend"]


def get_backend_config(backend_name: str) -> dict[str, Any]:
    config = load_config()
    return config["backends"].get(backend_name, {})


def set_backend(backend_name: str, backend_config: dict[str, Any] | None = None) -> None:
    """Change the active backend and save configuration."""
    config = load_config()
    config["backend"] = backend_name
    if backend_config:
        config["backends"].setdefault(backend_name, {}).update(backend_config)
    save_config(config)
