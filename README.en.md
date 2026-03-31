# tamago

> [日本語](README.md)

A CLI tool for raising your AI clone.

Through conversation, `MEMORY.md` grows and learns your thoughts, values, and communication style — allowing you to chat with an AI that speaks as you.

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/u73/tamago-project.git
cd tamago-project

# 2. Install dependencies
uv sync

# 3. Initialize (select language & backend → generate MEMORY.md)
tamago init

# 4. Train
tamago train

# 5. Talk
tamago talk
```

---

## Commands

| Command | Description |
|---------|-------------|
| `tamago init` | Generate MEMORY.md and configure backend |
| `tamago train` | Grow MEMORY.md through Q&A |
| `tamago talk` | Chat with your AI clone |
| `tamago status` | Check growth progress |

---

## Supported LLM Backends

| Backend | Requirements | Offline |
|---------|-------------|---------|
| `anthropic` | Anthropic API key | No |
| `openai` | OpenAI API key | No |
| `ollama` | Ollama server | Yes |
| `llamacpp` | GGUF model file | Yes |

---

## Documentation

- [Installation Guide](docs/en/installation.md) — Setup & backend configuration
- [Usage Guide](docs/en/usage.md) — Command details & configuration

---

## License

MIT
