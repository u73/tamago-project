"""多言語対応 (i18n) — dict ベースの軽量翻訳"""

from __future__ import annotations

_lang: str = "ja"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "ja": {
        # ── CLI 全般 ──
        "cli.help": "自分の分身AIを育てるCLIツール",
        "cli.llm_error": "LLM エラー: {error}",

        # ── init ──
        "cli.init.help": "MEMORY.md を生成して tamago を初期化する",
        "cli.init.select_language": "言語を選択してください / Select language:",
        "cli.init.overwrite_confirm": "MEMORY.md は既に存在します。上書きしますか？",
        "cli.init.cancelled": "初期化をキャンセルしました。",
        "cli.init.select_backend": "LLM バックエンドを選択してください:",
        "cli.init.current": "(現在)",
        "cli.init.enter_number": "番号を入力 (1-{max})",
        "cli.init.invalid_choice": "無効な選択です。デフォルト(anthropic)を使用します。",
        "cli.init.server_url": "サーバー URL",
        "cli.init.model_name": "モデル名",
        "cli.init.custom_base_url": "カスタム base_url (不要なら空)",
        "cli.init.llamacpp_info": "llama-cpp-python を使用します。llama.cpp のインストールは不要です。",
        "cli.init.gguf_path": "GGUF モデルファイルのパス",
        "cli.init.model_path_required": "model_path は必須です。後で config.yaml を直接編集して設定してください。",
        "cli.init.config_file_at": "  設定ファイル: {path}",
        "cli.init.chat_format": "チャットフォーマット: {formats}",
        "cli.init.gpu_layers": "GPU レイヤー数 (0=CPUのみ / -1=全レイヤーをGPUに)",
        "cli.init.backend_set": "バックエンドを [bold]{name}[/bold] に設定しました。",
        "cli.init.panel_body": (
            "[green]MEMORY.md を生成しました！[/green]\n{path}\n\n"
            "バックエンド: [bold]{backend}[/bold]\n"
            "設定ファイル: {config}\n\n"
            "[dim]次は `tamago train` で育てましょう。[/dim]"
        ),

        # ── train ──
        "cli.train.help": "対話して MEMORY.md を育てる",
        "cli.train.not_found": "MEMORY.md が見つかりません。先に `tamago init` を実行してください。",
        "cli.train.panel_body": (
            "[bold]tamago train[/bold]\n\n"
            "質問に答えて、あなたの分身AIを育てましょう。\n"
            "[dim]終了するには exit / quit / Ctrl+C[/dim]"
        ),
        "cli.train.thinking": "考え中...",
        "cli.train.retry": "再試行しますか？",
        "cli.train.you": "あなた",
        "cli.train.updating": "記憶を更新中...",
        "cli.train.update_skipped": "記憶の更新をスキップしました。",
        "cli.train.updated": "記憶を更新しました。",
        "cli.train.end": "トレーニングを終了しました。",
        "cli.train.start_message": "質問を始めてください。",
        "cli.train.history_entry": "trainで更新",

        # ── talk ──
        "cli.talk.help": "tamago（分身AI）と話す",
        "cli.talk.not_found": "MEMORY.md が見つかりません。先に `tamago init` を実行してください。",
        "cli.talk.panel_body": (
            "[bold]tamago talk[/bold]\n\n"
            "あなたの分身AIと自由に話しましょう。\n"
            "[dim]終了するには exit / quit / Ctrl+C[/dim]"
        ),
        "cli.talk.you": "あなた",
        "cli.talk.retry": "再試行しますか？",
        "cli.talk.end": "会話を終了しました。",

        # ── status ──
        "cli.status.help": "tamago の育ち具合を表示する",
        "cli.status.not_found": "MEMORY.md が見つかりません。先に `tamago init` を実行してください。",
        "cli.status.section": "セクション",
        "cli.status.lines": "行数",
        "cli.status.chars": "文字数",
        "cli.status.level": "レベル",
        "cli.status.growth": "成長度:",
        "cli.status.msg_newborn": "まだ生まれたばかり。`tamago train` で育てましょう！",
        "cli.status.msg_growing": "少しずつ育ってきました。もっと対話しましょう！",
        "cli.status.msg_good": "かなり育ちました！あなたの分身が形になってきています。",
        "cli.status.msg_great": "立派に育ちました！`tamago talk` で話してみましょう。",
        "cli.status.jsonl_stats": (
            "Fine-tuning データ (MEMORY.jsonl): "
            "計 [bold]{total}[/bold] 件 "
            "(train: {train} / talk: {talk})"
        ),

        # ── memory ──
        "memory.not_found": "{file} が見つかりません。`tamago init` を実行してください。",

        # ── セクション名 ──
        "section.basic_info": "基本情報",
        "section.values": "思想・価値観",
        "section.expertise": "専門知識・領域",
        "section.interests": "興味・関心",
        "section.thinking_style": "思考スタイル",
        "section.tone": "話し方のトーン",
        "section.dislikes": "嫌いなもの・避けたいこと",
        "section.history": "更新履歴",

        # ── テンプレート ──
        "template.memory": (
            "# MEMORY.md\n\n"
            "> このファイルはtamagoによって生成・管理されています。\n"
            "> あなたの分身AIの記憶です。\n\n"
            "## 基本情報\n\n\n"
            "## 思想・価値観\n\n\n"
            "## 専門知識・領域\n\n\n"
            "## 興味・関心\n\n\n"
            "## 思考スタイル\n\n\n"
            "## 話し方のトーン\n\n\n"
            "## 嫌いなもの・避けたいこと\n\n\n"
            "## 更新履歴\n\n"
        ),

        # ── プロンプト ──
        "prompt.train_question": (
            "あなたはユーザーの分身AI「tamago」のトレーナーです。\n"
            "ユーザーのことを深く理解するために質問をしてください。\n\n"
            "以下がユーザーの現在のMEMORY.mdです：\n\n"
            "{memory_content}\n\n"
            "ルール：\n"
            "- まだ情報が少ないセクションを優先して質問する\n"
            "- 1回に1つの質問だけする\n"
            "- 知的で深い質問をする（表面的なプロフィール情報ではなく、思考や価値観を引き出す）\n"
            "- 親しみやすく、でも軽薄ではないトーンで\n"
            "- 質問だけを返す（前置きや説明は不要）"
        ),
        "prompt.train_update": (
            "あなたはユーザーの分身AI「tamago」のメモリ管理者です。\n"
            "ユーザーの回答を元に、MEMORY.mdを更新してください。\n\n"
            "現在のMEMORY.md：\n\n"
            "{memory_content}\n\n"
            "ルール：\n"
            "- 回答内容を適切なセクションに追記する\n"
            "- 既存の情報は保持する（削除しない）\n"
            "- 箇条書きで簡潔に記録する\n"
            "- 更新履歴セクションには触れない（自動管理される）\n"
            "- MEMORY.md全文をそのまま返す（マークダウンのコードブロックは使わない）\n"
            "- ヘッダーやフォーマットは元のまま維持する"
        ),
        "prompt.train_update_user": (
            "質問: {question}\n\n回答: {answer}\n\n"
            "上記を踏まえて、更新後のMEMORY.md全文を返してください。"
        ),
        "prompt.talk": (
            "あなたはユーザーの分身AIです。\n"
            "以下のMEMORY.mdに記録された情報に基づいて、ユーザーの人格を再現して会話してください。\n\n"
            "{memory_content}\n\n"
            "ルール：\n"
            "- MEMORY.mdに記録された思想、価値観、話し方のトーンを忠実に再現する\n"
            "- ユーザーの専門知識や興味に基づいた発言をする\n"
            "- 分からないことは分からないと言う（MEMORY.mdにないことは勝手に作らない）\n"
            "- 自然な会話を心がける"
        ),
        "prompt.train_finetune": (
            "以下はあなた自身についての記録です。\n"
            "この情報に基づいて、あなたとして質問に答えてください。\n\n"
            "{memory_content}"
        ),
    },

    "en": {
        # ── CLI general ──
        "cli.help": "CLI tool for raising your AI clone",
        "cli.llm_error": "LLM Error: {error}",

        # ── init ──
        "cli.init.help": "Generate MEMORY.md and initialize tamago",
        "cli.init.select_language": "言語を選択してください / Select language:",
        "cli.init.overwrite_confirm": "MEMORY.md already exists. Overwrite?",
        "cli.init.cancelled": "Initialization cancelled.",
        "cli.init.select_backend": "Select LLM backend:",
        "cli.init.current": "(current)",
        "cli.init.enter_number": "Enter number (1-{max})",
        "cli.init.invalid_choice": "Invalid choice. Using default (anthropic).",
        "cli.init.server_url": "Server URL",
        "cli.init.model_name": "Model name",
        "cli.init.custom_base_url": "Custom base_url (leave empty if not needed)",
        "cli.init.llamacpp_info": "Using llama-cpp-python. No need to install llama.cpp separately.",
        "cli.init.gguf_path": "Path to GGUF model file",
        "cli.init.model_path_required": "model_path is required. Please edit config.yaml later to set it.",
        "cli.init.config_file_at": "  Config file: {path}",
        "cli.init.chat_format": "Chat format: {formats}",
        "cli.init.gpu_layers": "GPU layers (0=CPU only / -1=all layers on GPU)",
        "cli.init.backend_set": "Backend set to [bold]{name}[/bold].",
        "cli.init.panel_body": (
            "[green]MEMORY.md created![/green]\n{path}\n\n"
            "Backend: [bold]{backend}[/bold]\n"
            "Config: {config}\n\n"
            "[dim]Next: run `tamago train` to start growing.[/dim]"
        ),

        # ── train ──
        "cli.train.help": "Train MEMORY.md through conversation",
        "cli.train.not_found": "MEMORY.md not found. Run `tamago init` first.",
        "cli.train.panel_body": (
            "[bold]tamago train[/bold]\n\n"
            "Answer questions to grow your AI clone.\n"
            "[dim]Type exit / quit / Ctrl+C to end[/dim]"
        ),
        "cli.train.thinking": "Thinking...",
        "cli.train.retry": "Retry?",
        "cli.train.you": "You",
        "cli.train.updating": "Updating memory...",
        "cli.train.update_skipped": "Memory update skipped.",
        "cli.train.updated": "Memory updated.",
        "cli.train.end": "Training ended.",
        "cli.train.start_message": "Please start asking questions.",
        "cli.train.history_entry": "Updated via train",

        # ── talk ──
        "cli.talk.help": "Talk with tamago (your AI clone)",
        "cli.talk.not_found": "MEMORY.md not found. Run `tamago init` first.",
        "cli.talk.panel_body": (
            "[bold]tamago talk[/bold]\n\n"
            "Chat freely with your AI clone.\n"
            "[dim]Type exit / quit / Ctrl+C to end[/dim]"
        ),
        "cli.talk.you": "You",
        "cli.talk.retry": "Retry?",
        "cli.talk.end": "Conversation ended.",

        # ── status ──
        "cli.status.help": "Show tamago's growth status",
        "cli.status.not_found": "MEMORY.md not found. Run `tamago init` first.",
        "cli.status.section": "Section",
        "cli.status.lines": "Lines",
        "cli.status.chars": "Chars",
        "cli.status.level": "Level",
        "cli.status.growth": "Growth:",
        "cli.status.msg_newborn": "Just hatched! Run `tamago train` to start growing!",
        "cli.status.msg_growing": "Growing steadily. Keep training!",
        "cli.status.msg_good": "Looking great! Your clone is taking shape.",
        "cli.status.msg_great": "Fully grown! Try `tamago talk` to chat with your clone.",
        "cli.status.jsonl_stats": (
            "Fine-tuning data (MEMORY.jsonl): "
            "[bold]{total}[/bold] entries "
            "(train: {train} / talk: {talk})"
        ),

        # ── memory ──
        "memory.not_found": "{file} not found. Run `tamago init` first.",

        # ── section names ──
        "section.basic_info": "Basic Info",
        "section.values": "Values & Beliefs",
        "section.expertise": "Expertise",
        "section.interests": "Interests",
        "section.thinking_style": "Thinking Style",
        "section.tone": "Tone & Communication",
        "section.dislikes": "Dislikes & Avoidances",
        "section.history": "History",

        # ── template ──
        "template.memory": (
            "# MEMORY.md\n\n"
            "> This file is generated and managed by tamago.\n"
            "> It stores the memory of your AI clone.\n\n"
            "## Basic Info\n\n\n"
            "## Values & Beliefs\n\n\n"
            "## Expertise\n\n\n"
            "## Interests\n\n\n"
            "## Thinking Style\n\n\n"
            "## Tone & Communication\n\n\n"
            "## Dislikes & Avoidances\n\n\n"
            "## History\n\n"
        ),

        # ── prompts ──
        "prompt.train_question": (
            "You are a trainer for \"tamago\", the user's AI clone.\n"
            "Ask questions to deeply understand the user.\n\n"
            "Here is the user's current MEMORY.md:\n\n"
            "{memory_content}\n\n"
            "Rules:\n"
            "- Prioritize sections with less information\n"
            "- Ask only one question at a time\n"
            "- Ask deep, thoughtful questions (draw out thinking and values, not surface-level profile info)\n"
            "- Use a friendly but not frivolous tone\n"
            "- Return only the question (no preamble or explanation)"
        ),
        "prompt.train_update": (
            "You are the memory manager for \"tamago\", the user's AI clone.\n"
            "Update MEMORY.md based on the user's answer.\n\n"
            "Current MEMORY.md:\n\n"
            "{memory_content}\n\n"
            "Rules:\n"
            "- Add the answer content to the appropriate section\n"
            "- Preserve existing information (do not delete)\n"
            "- Record concisely in bullet points\n"
            "- Do not touch the History section (it is managed automatically)\n"
            "- Return the full MEMORY.md as-is (do not use markdown code blocks)\n"
            "- Keep the original headers and formatting"
        ),
        "prompt.train_update_user": (
            "Question: {question}\n\nAnswer: {answer}\n\n"
            "Based on the above, return the updated full MEMORY.md."
        ),
        "prompt.talk": (
            "You are the user's AI clone.\n"
            "Based on the information recorded in MEMORY.md below, replicate the user's personality in conversation.\n\n"
            "{memory_content}\n\n"
            "Rules:\n"
            "- Faithfully replicate the values, beliefs, and tone recorded in MEMORY.md\n"
            "- Speak based on the user's expertise and interests\n"
            "- Say you don't know when you don't (don't make things up that aren't in MEMORY.md)\n"
            "- Keep the conversation natural"
        ),
        "prompt.train_finetune": (
            "The following is a record about yourself.\n"
            "Based on this information, answer questions as yourself.\n\n"
            "{memory_content}"
        ),
    },
}

# セクション識別用キー（言語非依存）
SECTION_KEYS = [
    "basic_info",
    "values",
    "expertise",
    "interests",
    "thinking_style",
    "tone",
    "dislikes",
    "history",
]


def set_language(lang: str) -> None:
    """アクティブ言語を設定する"""
    global _lang
    if lang in TRANSLATIONS:
        _lang = lang


def get_language() -> str:
    """現在の言語を返す"""
    return _lang


def t(key: str, **kwargs: str) -> str:
    """翻訳キーに対応する文字列を返す

    kwargs が渡された場合は .format() を適用する。
    キーが見つからなければ ja にフォールバック。
    """
    text = TRANSLATIONS.get(_lang, {}).get(key)
    if text is None:
        text = TRANSLATIONS["ja"].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text
