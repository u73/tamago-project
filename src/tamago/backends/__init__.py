# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""LLM backend factory"""

from __future__ import annotations

from tamago.backends.base import LLMBackend

_REGISTRY: dict[str, str] = {
    "anthropic": "tamago.backends.anthropic_backend.AnthropicBackend",
    "openai": "tamago.backends.openai_backend.OpenAIBackend",
    "ollama": "tamago.backends.ollama_backend.OllamaBackend",
    "llamacpp": "tamago.backends.llamacpp_backend.LlamaCppBackend",
}

AVAILABLE_BACKENDS = list(_REGISTRY.keys())


def get_backend(name: str | None = None, **kwargs: object) -> LLMBackend:
    """Return an LLMBackend instance for the given backend name.

    If name is None, uses the setting from ~/.tamago/config.yaml.
    """
    from tamago.config import get_active_backend, get_backend_config

    backend_name = name or get_active_backend()
    if backend_name not in _REGISTRY:
        raise ValueError(
            f"Unknown backend: '{backend_name}'\n"
            f"Available: {', '.join(AVAILABLE_BACKENDS)}"
        )

    # Merge backend config from config.yaml
    cfg = get_backend_config(backend_name)
    cfg.update(kwargs)

    module_path, class_name = _REGISTRY[backend_name].rsplit(".", 1)
    import importlib
    module = importlib.import_module(module_path)
    cls = getattr(module, class_name)
    return cls(**cfg)


__all__ = ["LLMBackend", "get_backend", "AVAILABLE_BACKENDS"]
