# Usage Guide

## Basic Flow

```
tamago init → tamago train → tamago train → ... → tamago talk
```

1. `init` — Set up MEMORY.md and choose your backend
2. `train` — Repeatedly train to grow MEMORY.md
3. `talk` — Chat with your trained AI clone
4. `status` — Check growth progress anytime

---

## tamago init

Generates MEMORY.md and configures the LLM backend.

```bash
tamago init
```

**Example output:**

```
Select language / 言語を選択してください:
  1. 日本語 (Japanese)
  2. English
1-2 [1]: 2

Select LLM backend:
  1. anthropic (current)
  2. openai
  3. ollama
  4. llamacpp

Enter number (1-4) [1]: 1

╭─────────────────── tamago init ───────────────────╮
│ MEMORY.md created!                                │
│ /path/to/your/project/MEMORY.md                   │
│                                                   │
│ Backend: anthropic                                │
│ Config: ~/.tamago/config.yaml                     │
│                                                   │
│ Next: run `tamago train` to start growing.        │
╰───────────────────────────────────────────────────╯
```

**Generated files:**

| File | Location | Description |
|------|----------|-------------|
| `MEMORY.md` | Current directory | AI clone's memory file |
| `config.yaml` | `~/.tamago/config.yaml` | Backend & language settings |

> **Note:** `MEMORY.md` is created per directory.
> To maintain multiple clones, run `tamago init` in separate directories.

---

## tamago train

The AI interviews you and records your answers in `MEMORY.md`.

```bash
tamago train
```

**Example output:**

```
╭──────────────── tamago train ────────────────╮
│ Answer questions to grow your AI clone.      │
│ Type exit / quit / Ctrl+C to end             │
╰──────────────────────────────────────────────╯

tamago: What value do you consider absolutely non-negotiable?

You: Intellectual honesty. Being able to say "I don't know" when I don't.

Memory updated.

tamago: What technical areas or domains do you focus on professionally?

You: exit
```

**Tips:**
- The AI prioritizes sections with less information
- Answers are automatically sorted into the appropriate section (values, expertise, etc.)
- You can answer as many questions as you like per session — progress is saved even if you exit early
- Run as many sessions as you want to keep growing

---

## tamago talk

Loads `MEMORY.md` and lets you chat with your AI clone.

```bash
tamago talk
```

**Example output:**

```
╭──────────────── tamago talk ─────────────────╮
│ Chat freely with your AI clone.              │
│ Type exit / quit / Ctrl+C to end             │
╰──────────────────────────────────────────────╯

You: What's been on your mind lately?

tamago: Honestly, I've been thinking less about LLM architecture improvements
        and more about how to connect them with human thinking.
        It's not about technical accuracy — it's about designing
        "intellectual resonance." That's the interesting problem.

You: exit
```

**Tips:**
- The more information in `MEMORY.md`, the more accurate the clone
- An almost-empty `MEMORY.md` produces low-accuracy results
- Conversation history is kept only during the session (not saved to `MEMORY.md`)
- Each exchange is automatically appended to `MEMORY.jsonl` (accumulated as fine-tuning data)

---

## tamago status

Check the fullness of each section in `MEMORY.md`.

```bash
tamago status
```

**Example output:**

```
              tamago status
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃ Section                ┃ Lines ┃ Chars ┃ Level ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━┩
│ Basic Info             │     3 │    89 │  🐥   │
│ Values & Beliefs       │     5 │   210 │  🐔   │
│ Expertise              │     2 │    54 │  🐣   │
│ Interests              │     0 │     0 │  🥚   │
│ Thinking Style         │     1 │    32 │  🐣   │
│ Tone & Communication   │     0 │     0 │  🥚   │
│ Dislikes & Avoidances  │     0 │     0 │  🥚   │
└────────────────────────┴───────┴───────┴───────┘

Growth: ████████████░░░░░░░░░░ 35%

Growing steadily. Keep training!
```

**Level guide:**

| Icon | Chars | Status |
|------|-------|--------|
| 🥚 | 0 | Nothing recorded yet |
| 🐣 | 1–49 | Just getting started |
| 🐥 | 50–199 | Growing well |
| 🐔 | 200+ | Fully developed |

If `MEMORY.jsonl` exists, fine-tuning data counts are also shown:

```
Fine-tuning data (MEMORY.jsonl): 24 entries (train: 8 / talk: 16)
```

---

## Configuration

Backend and language settings are managed in `~/.tamago/config.yaml`.

```yaml
language: en            # ja or en
backend: anthropic      # Active backend

backends:
  anthropic:
    model: claude-sonnet-4-20250514

  openai:
    model: gpt-4o
    base_url: null      # Set custom endpoint here

  ollama:
    model: llama3.2
    base_url: http://localhost:11434

  llamacpp:
    model_path: ~/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf
    chat_format: chatml
    n_ctx: 4096
    n_gpu_layers: 0     # -1 to run all layers on GPU
```

To switch backends, re-run `tamago init` or edit `config.yaml` directly.

---

## MEMORY.jsonl Structure (Fine-tuning Data)

Auto-generated in the same directory as `MEMORY.md`. Both `tamago train` and `tamago talk` append to it.

```jsonl
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "What values matter most to you?"}, {"role": "assistant", "content": "Intellectual honesty. Being able to..."}], "metadata": {"source": "train", "timestamp": "2026-03-30T12:00:00"}}
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "What's on your mind lately?"}, {"role": "assistant", "content": "I've been thinking about how LLMs..."}], "metadata": {"source": "talk", "timestamp": "2026-03-30T12:05:00"}}
```

| Field | Content |
|-------|---------|
| `messages[0]` system | Personality prompt containing MEMORY.md |
| `messages[1]` user | train: AI's question / talk: your message |
| `messages[2]` assistant | train: your answer / talk: tamago's response |
| `metadata.source` | `"train"` or `"talk"` |
| `metadata.timestamp` | Timestamp (ISO 8601) |

**Fine-tuning usage examples:**

```bash
# OpenAI fine-tuning API
openai api fine_tuning.jobs.create \
  -t MEMORY.jsonl \
  -m gpt-4o-mini

# Axolotl / LLaMA-Factory / Unsloth
# → Can be used directly as a dataset (messages format)
```

---

## MEMORY.md Structure

```markdown
# MEMORY.md

## Basic Info
Name, age, occupation, etc.

## Values & Beliefs
Core values and convictions

## Expertise
Areas of deep knowledge

## Interests
Topics and areas of curiosity

## Thinking Style
How you approach problems, cognitive patterns

## Tone & Communication
Writing style, speech patterns

## Dislikes & Avoidances
Things you dislike or want to avoid

## History
- [2026-03-29 12:00] Updated via train
```

You can edit `MEMORY.md` manually. `tamago train` reads its current content before generating questions.
