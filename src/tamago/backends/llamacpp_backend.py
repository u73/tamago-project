# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""llama-cpp-python backend (direct GGUF model execution)"""

from __future__ import annotations

from pathlib import Path

from tamago.backends.base import LLMBackend

DEFAULT_CHAT_FORMAT = "chatml"
DEFAULT_N_CTX = 4096
DEFAULT_N_GPU_LAYERS = 0  # 0 = CPU only. Use -1 for all layers on GPU


class LlamaCppBackend(LLMBackend):
    """Run GGUF models in-process via llama-cpp-python.

    No llama.cpp binary or external server required.

    Install:
        uv add llama-cpp-python              # CPU only
        CMAKE_ARGS="-DGGML_METAL=on" uv add llama-cpp-python   # Apple Silicon GPU
        CMAKE_ARGS="-DGGML_CUDA=on"  uv add llama-cpp-python   # NVIDIA GPU
    """

    def __init__(
        self,
        model_path: str | None = None,
        chat_format: str = DEFAULT_CHAT_FORMAT,
        n_ctx: int = DEFAULT_N_CTX,
        n_gpu_layers: int = DEFAULT_N_GPU_LAYERS,
        **_kwargs: object,
    ) -> None:
        try:
            from llama_cpp import Llama  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "llama-cpp-python is required:\n"
                "  CPU only:          uv add llama-cpp-python\n"
                "  Apple Silicon GPU: CMAKE_ARGS=\"-DGGML_METAL=on\" uv add llama-cpp-python\n"
                "  NVIDIA GPU:        CMAKE_ARGS=\"-DGGML_CUDA=on\"  uv add llama-cpp-python"
            )

        if not model_path:
            raise ValueError(
                "llamacpp backend requires model_path.\n"
                "Re-run `tamago init` to set the GGUF file path."
            )

        resolved = Path(model_path).expanduser().resolve()
        if not resolved.exists():
            raise FileNotFoundError(f"GGUF model not found: {resolved}")

        self._llm = Llama(
            model_path=str(resolved),
            chat_format=chat_format,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            verbose=False,
        )

    @property
    def name(self) -> str:
        return "llamacpp"

    def chat(
        self,
        system: str,
        messages: list[dict[str, str]],
        max_tokens: int = 1024,
    ) -> str:
        full_messages = [{"role": "system", "content": system}, *messages]
        response = self._llm.create_chat_completion(
            messages=full_messages,
            max_tokens=max_tokens,
        )
        return response["choices"][0]["message"]["content"] or ""
