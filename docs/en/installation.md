# Installation Guide

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (package manager)

### Installing uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Installing tamago

```bash
git clone https://github.com/u73/tamago-project.git
cd tamago-project
uv sync
```

This sets up the `anthropic` backend by default.

---

## Backend Setup

### 1. Anthropic (Claude) — Default

**Required:** Anthropic API key ([get one here](https://console.anthropic.com/))

```bash
# Create .env in the project root
cp .env.example .env

# Edit .env and set your API key
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

No additional packages needed — `anthropic` is included with `uv sync`.

---

### 2. OpenAI (GPT-4o, etc.)

**Required:** OpenAI API key ([get one here](https://platform.openai.com/))

```bash
# Add the openai package
uv add openai

# Add your API key to .env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

Select `openai` as the backend during `tamago init`.

> **Custom endpoints**
> For Azure OpenAI or compatible APIs (LM Studio, etc.),
> enter the custom `base_url` during `tamago init`.

---

### 3. Ollama — Local & Fully Offline

**Required:** Ollama ([official site](https://ollama.com/))

```bash
# Install Ollama (macOS)
brew install ollama

# Or use the official script
curl -fsSL https://ollama.com/install.sh | sh
```

```bash
# Download a model (e.g., Llama 3.2)
ollama pull llama3.2

# Start the Ollama server (skip if already running)
ollama serve
```

```bash
# Add the ollama package to tamago
uv add ollama
```

Select `ollama` during `tamago init` and enter the model name (e.g., `llama3.2`).

---

### 4. llama-cpp-python — Direct GGUF Execution

No llama.cpp binary or external server needed. The Python package runs GGUF models in-process.

#### Getting GGUF Models

Search for models with the `GGUF` tag on [Hugging Face](https://huggingface.co).

```bash
# Download using huggingface-cli
pip install huggingface-hub
huggingface-cli download \
  bartowski/Llama-3.2-3B-Instruct-GGUF \
  --include "Llama-3.2-3B-Instruct-Q4_K_M.gguf" \
  --local-dir ~/models
```

Quantization guide:

| Quantization | Size | Quality | Recommended |
|-------------|------|---------|-------------|
| Q2_K | Smallest | Low | |
| Q4_K_M | Small | Good | Best balance |
| Q5_K_M | Medium | High | Quality-focused |
| Q8_0 | Large | Highest | If you have RAM |

#### Installing llama-cpp-python

> Compilation required — first install may take **several minutes**.

```bash
# CPU only (default)
uv add llama-cpp-python

# Apple Silicon GPU (Metal)
CMAKE_ARGS="-DGGML_METAL=on" uv add llama-cpp-python

# NVIDIA GPU (CUDA)
CMAKE_ARGS="-DGGML_CUDA=on" uv add llama-cpp-python
```

After installation, select `llamacpp` during `tamago init` and enter the path to your GGUF file.

---

## Verify Installation

```bash
tamago --help
```

You should see output like:

```
 Usage: tamago [OPTIONS] COMMAND [ARGS]...

 tamago - AI clone CLI / 自分の分身AIを育てるCLIツール

╭─ Commands ─────────────────────────────────────────────────────╮
│ init    Generate MEMORY.md and initialize tamago               │
│ train   Train MEMORY.md through conversation                   │
│ talk    Talk with tamago (your AI clone)                        │
│ status  Show tamago's growth status                             │
╰────────────────────────────────────────────────────────────────╯
```
