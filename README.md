# tamago 🥚

自分の分身AIを育てるCLIツール。

対話を重ねるごとに `MEMORY.md` が育ち、あなたの思想・価値観・話し方を学習した分身AIと会話できます。

---

## クイックスタート

```bash
# 1. リポジトリをクローン
git clone https://github.com/yourname/tamago.git
cd tamago

# 2. 依存インストール
uv sync

# 3. 初期化（バックエンド選択 → MEMORY.md 生成）
tamago init

# 4. 育てる
tamago train

# 5. 話す
tamago talk
```

---

## コマンド一覧

| コマンド | 説明 |
|---------|------|
| `tamago init` | MEMORY.md を生成・バックエンドを設定 |
| `tamago train` | 対話して MEMORY.md を育てる |
| `tamago talk` | 分身AIと自由に話す |
| `tamago status` | 育ち具合を確認する |

---

## 対応 LLM バックエンド

| バックエンド | 必要なもの | オフライン |
|------------|-----------|-----------|
| `anthropic` | Anthropic API キー | ✗ |
| `openai` | OpenAI API キー | ✗ |
| `ollama` | Ollama サーバー | ✓ |
| `llamacpp` | GGUF モデルファイル | ✓ |

---

## ドキュメント

- [インストールガイド](docs/installation.md) — 環境構築・バックエンド別セットアップ
- [使い方ガイド](docs/usage.md) — 各コマンドの詳細・設定ファイルの説明

---

## ライセンス

MIT
