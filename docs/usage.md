# 使い方ガイド

## 基本的な流れ

```
tamago init → tamago train → tamago train → ... → tamago talk
```

1. `init` で MEMORY.md とバックエンドを設定
2. `train` を繰り返して MEMORY.md を育てる
3. `talk` で育てた分身AIと会話する
4. `status` でいつでも育ち具合を確認

---

## tamago init

MEMORY.md を生成し、使用する LLM バックエンドを設定します。

```bash
tamago init
```

**実行例:**

```
LLM バックエンドを選択してください:
  1. anthropic (現在)
  2. openai
  3. ollama
  4. llamacpp

番号を入力 (1-4) [1]: 1

╭─────────────────── tamago init ───────────────────╮
│ MEMORY.md を生成しました！                        │
│ /path/to/your/project/MEMORY.md                   │
│                                                   │
│ バックエンド: anthropic                           │
│ 設定ファイル: ~/.tamago/config.yaml               │
│                                                   │
│ 次は `tamago train` で育てましょう。              │
╰───────────────────────────────────────────────────╯
```

**生成されるファイル:**

| ファイル | 場所 | 説明 |
|---------|------|------|
| `MEMORY.md` | カレントディレクトリ | 分身AIの記憶ファイル |
| `config.yaml` | `~/.tamago/config.yaml` | バックエンド設定 |

> **注意:** `MEMORY.md` はプロジェクトごとに作成されます。
> 複数の分身を使い分けたい場合は、ディレクトリを分けて `tamago init` してください。

---

## tamago train

AI がインタビュアーとなってあなたに質問し、回答を `MEMORY.md` に記録します。

```bash
tamago train
```

**実行例:**

```
╭──────────────── tamago train ────────────────╮
│ 質問に答えて、あなたの分身AIを育てましょう。 │
│ 終了するには exit / quit / Ctrl+C            │
╰──────────────────────────────────────────────╯

tamago: あなたが「これだけは譲れない」と思う価値観はなんですか？

あなた: 知的誠実さ。分からないことを分からないと言えること。

記憶を更新しました。

tamago: 専門的に取り組んでいる技術や領域はありますか？

あなた: exit
```

**ポイント:**
- AI はまだ情報が少ないセクションを優先して質問します
- 回答は自動的に適切なセクション（思想・価値観、専門知識など）に振り分けられます
- 1セッションで何問でも答えられます。途中で抜けても記録は保存されます
- 何度でも実行して育て続けられます

---

## tamago talk

育てた `MEMORY.md` を読み込み、あなたの分身AIと自由に会話します。

```bash
tamago talk
```

**実行例:**

```
╭──────────────── tamago talk ─────────────────╮
│ あなたの分身AIと自由に話しましょう。         │
│ 終了するには exit / quit / Ctrl+C            │
╰──────────────────────────────────────────────╯

あなた: 最近気になってることある？

tamago: そうだな、LLMのアーキテクチャ改善よりも、
        どう人間の思考と接続するかのほうが
        ずっと面白い問題だと思っていて。
        技術的な精度より「知的共鳴」をどう設計するか、かな。

あなた: exit
```

**ポイント:**
- `MEMORY.md` に記録された情報が多いほど、より精度の高い分身になります
- `MEMORY.md` がほぼ空の状態だと、分身としての精度は低くなります
- 会話履歴はセッション中のみ保持されます（`MEMORY.md` には保存されません）
- 1往復ごとに `MEMORY.jsonl` へ自動追記されます（fine-tuning データとして蓄積）

---

## tamago status

`MEMORY.md` の各セクションの充実度を確認します。

```bash
tamago status
```

**実行例:**

```
               tamago status
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ セクション             ┃ 行数 ┃ 文字数 ┃ レベル ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ 基本情報               │    3 │     89 │   🐥   │
│ 思想・価値観           │    5 │    210 │   🐔   │
│ 専門知識・領域         │    2 │     54 │   🐣   │
│ 興味・関心             │    0 │      0 │   🥚   │
│ 思考スタイル           │    1 │     32 │   🐣   │
│ 話し方のトーン         │    0 │      0 │   🥚   │
│ 嫌いなもの・避けたいこと│   0 │      0 │   🥚   │
└────────────────────────┴──────┴────────┴────────┘

成長度: ████████████░░░░░░░░░░ 35%

少しずつ育ってきました。もっと対話しましょう！
```

**レベルの目安:**

| アイコン | 文字数 | 状態 |
|---------|-------|------|
| 🥚 | 0 | まだ何も記録されていない |
| 🐣 | 1〜49 | 少し記録されている |
| 🐥 | 50〜199 | 育ってきた |
| 🐔 | 200〜 | 十分に育っている |

`MEMORY.jsonl` が存在する場合、fine-tuning データの件数も合わせて表示されます：

```
Fine-tuning データ (MEMORY.jsonl): 計 24 件 [train: 8 / talk: 16]
```

---

## 設定ファイル

`~/.tamago/config.yaml` でバックエンド設定を管理しています。

```yaml
backend: anthropic   # 現在のアクティブバックエンド

backends:
  anthropic:
    model: claude-sonnet-4-20250514

  openai:
    model: gpt-4o
    base_url: null   # カスタムエンドポイントはここに記述

  ollama:
    model: llama3.2
    base_url: http://localhost:11434

  llamacpp:
    model_path: ~/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf
    chat_format: chatml
    n_ctx: 4096
    n_gpu_layers: 0   # -1 にすると全レイヤーを GPU で実行
```

バックエンドを切り替えたい場合は `tamago init` を再実行するか、直接 `config.yaml` を編集してください。

---

## MEMORY.jsonl の構造（Fine-tuning データ）

`MEMORY.md` と同じディレクトリに自動生成されます。`tamago train` と `tamago talk` の両方が追記します。

```jsonl
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "大事にしている価値観は？"}, {"role": "assistant", "content": "知的誠実さ。分からないことを..."}], "metadata": {"source": "train", "timestamp": "2026-03-30T12:00:00"}}
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "最近気になることある？"}, {"role": "assistant", "content": "LLMのアーキテクチャより..."}], "metadata": {"source": "talk", "timestamp": "2026-03-30T12:05:00"}}
```

| フィールド | 内容 |
|-----------|------|
| `messages[0]` system | MEMORY.md の内容を含む人格定義プロンプト |
| `messages[1]` user | train: AI の質問 / talk: あなたの発言 |
| `messages[2]` assistant | train: あなたの回答 / talk: tamago の応答 |
| `metadata.source` | `"train"` または `"talk"` |
| `metadata.timestamp` | 記録日時（ISO 8601） |

**fine-tuning ツールへの入力例:**

```bash
# OpenAI fine-tuning API
openai api fine_tuning.jobs.create \
  -t MEMORY.jsonl \
  -m gpt-4o-mini

# Axolotl / LLaMA-Factory / Unsloth
# → そのまま dataset として指定可能（messages 形式）
```

---

## MEMORY.md の構造

```markdown
# MEMORY.md

## 基本情報
名前・年齢・職業など

## 思想・価値観
大切にしていること、信念

## 専門知識・領域
得意分野、深く知っていること

## 興味・関心
興味を持っていること、追っているトピック

## 思考スタイル
問題へのアプローチ方法、思考の癖

## 話し方のトーン
文体、言葉遣いの特徴

## 嫌いなもの・避けたいこと
苦手なこと、やりたくないこと

## 更新履歴
- [2026-03-29 12:00] trainで更新
```

`MEMORY.md` は手動で編集しても構いません。`tamago train` はその内容を読み込んでから質問を生成します。
