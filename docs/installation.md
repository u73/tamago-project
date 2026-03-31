# インストールガイド

## 前提条件

- Python 3.10 以上
- [uv](https://docs.astral.sh/uv/) （パッケージマネージャー）

### uv のインストール

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## tamago のインストール

```bash
git clone https://github.com/yourname/tamago.git
cd tamago
uv sync
```

これで `anthropic` バックエンドが使える状態になります。

---

## バックエンド別セットアップ

### 1. Anthropic (Claude) — デフォルト

**必要なもの:** Anthropic API キー（[取得はこちら](https://console.anthropic.com/)）

```bash
# プロジェクトルートに .env を作成
cp .env.example .env

# .env を編集して API キーを設定
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

追加パッケージは不要です。`uv sync` で入る `anthropic` パッケージのみで動作します。

---

### 2. OpenAI (GPT-4o など)

**必要なもの:** OpenAI API キー（[取得はこちら](https://platform.openai.com/)）

```bash
# openai パッケージを追加
uv add openai

# .env に API キーを追加
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

`tamago init` でバックエンドに `openai` を選択してください。

> **カスタムエンドポイントについて**
> Azure OpenAI や互換 API（LM Studio 等）を使う場合は、
> `tamago init` で `カスタム base_url` を入力してください。

---

### 3. Ollama — ローカル・完全オフライン

**必要なもの:** Ollama（[公式サイト](https://ollama.com/)）

```bash
# Ollama 本体のインストール（macOS）
brew install ollama

# または公式スクリプト
curl -fsSL https://ollama.com/install.sh | sh
```

```bash
# モデルのダウンロード（例: Llama 3.2）
ollama pull llama3.2

# Ollama サーバーを起動（既に起動している場合は不要）
ollama serve
```

```bash
# tamago に ollama パッケージを追加
uv add ollama
```

`tamago init` でバックエンドに `ollama` を選択し、モデル名（例: `llama3.2`）を入力してください。

---

### 4. llama-cpp-python — GGUF モデルを直接実行

llama.cpp バイナリや外部サーバーは**不要**です。Python パッケージだけで GGUF モデルをプロセス内で実行します。

#### GGUF モデルの入手

[Hugging Face](https://huggingface.co) で `GGUF` タグのモデルを検索してダウンロードします。

```bash
# huggingface-cli でダウンロードする場合
pip install huggingface-hub
huggingface-cli download \
  bartowski/Llama-3.2-3B-Instruct-GGUF \
  --include "Llama-3.2-3B-Instruct-Q4_K_M.gguf" \
  --local-dir ~/models
```

量子化の目安：

| 量子化 | サイズ | 品質 | 推奨 |
|-------|-------|------|------|
| Q2_K | 最小 | 低 | |
| Q4_K_M | 小 | 良好 | ✓ バランス最良 |
| Q5_K_M | 中 | 高 | ✓ 品質重視 |
| Q8_0 | 大 | 最高 | RAMに余裕があれば |

#### llama-cpp-python のインストール

> ⚠️ コンパイルが発生するため、初回は**数分**かかります。

```bash
# CPU のみ（デフォルト）
uv add llama-cpp-python

# Apple Silicon GPU (Metal) を使う場合
CMAKE_ARGS="-DGGML_METAL=on" uv add llama-cpp-python

# NVIDIA GPU (CUDA) を使う場合
CMAKE_ARGS="-DGGML_CUDA=on" uv add llama-cpp-python
```

インストール後、`tamago init` でバックエンドに `llamacpp` を選択し、GGUF ファイルのパスを入力してください。

---

## インストール確認

```bash
tamago --help
```

以下のように表示されれば成功です：

```
 Usage: tamago [OPTIONS] COMMAND [ARGS]...

 🥚 自分の分身AIを育てるCLIツール

╭─ Commands ──────────────────────────────────────╮
│ init    MEMORY.md を生成して tamago を初期化する │
│ train   対話して MEMORY.md を育てる             │
│ talk    tamago（分身AI）と話す                  │
│ status  tamago の育ち具合を表示する             │
╰─────────────────────────────────────────────────╯
```
