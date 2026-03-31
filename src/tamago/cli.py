"""tamago CLI - 自分の分身AIを育てるCLIツール"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table

from tamago import memory, llm, training_data
from tamago.backends import AVAILABLE_BACKENDS
from tamago import config as cfg

app = typer.Typer(
    name="tamago",
    help="🥚 自分の分身AIを育てるCLIツール",
    no_args_is_help=True,
)
console = Console()


# ------------------------------------------------------------------ #
# ヘルパー
# ------------------------------------------------------------------ #

def _llm_call(label: str, fn, *args, **kwargs):
    """LLM 呼び出しをラップし、エラー時に会話ループを壊さない"""
    try:
        with console.status(f"[bold cyan]{label}[/bold cyan]"):
            return fn(*args, **kwargs)
    except Exception as e:
        console.print(f"[red]LLM エラー: {e}[/red]")
        return None


# ------------------------------------------------------------------ #
# tamago init
# ------------------------------------------------------------------ #

@app.command()
def init():
    """MEMORY.md を生成して tamago を初期化する"""
    if memory.memory_exists():
        overwrite = typer.confirm("MEMORY.md は既に存在します。上書きしますか？")
        if not overwrite:
            console.print("[yellow]初期化をキャンセルしました。[/yellow]")
            raise typer.Exit()

    # --- バックエンド選択 ---
    current = cfg.get_active_backend()
    console.print("\n[bold]LLM バックエンドを選択してください:[/bold]")
    for i, name in enumerate(AVAILABLE_BACKENDS, 1):
        marker = " [green](現在)[/green]" if name == current else ""
        console.print(f"  {i}. {name}{marker}")

    choice_str = typer.prompt(
        f"\n番号を入力 (1-{len(AVAILABLE_BACKENDS)})",
        default=str(AVAILABLE_BACKENDS.index(current) + 1),
    )
    try:
        idx = int(choice_str) - 1
        if not (0 <= idx < len(AVAILABLE_BACKENDS)):
            raise ValueError
    except ValueError:
        console.print("[red]無効な選択です。デフォルト(anthropic)を使用します。[/red]")
        idx = 0

    backend_name = AVAILABLE_BACKENDS[idx]
    backend_cfg = cfg.load_config()["backends"].get(backend_name, {})

    # バックエンド固有の追加設定
    if backend_name == "ollama":
        default_url = backend_cfg.get("base_url", "http://localhost:11434")
        backend_cfg["base_url"] = typer.prompt("サーバー URL", default=default_url)
        default_model = backend_cfg.get("model") or "llama3.2"
        backend_cfg["model"] = typer.prompt("モデル名", default=default_model)

    elif backend_name == "openai":
        default_model = backend_cfg.get("model") or "gpt-4o"
        backend_cfg["model"] = typer.prompt("モデル名", default=default_model)
        default_url = backend_cfg.get("base_url") or ""
        base_url = typer.prompt("カスタム base_url (不要なら空)", default=default_url)
        if base_url:
            backend_cfg["base_url"] = base_url

    elif backend_name == "llamacpp":
        # llama-cpp-python: GGUF を直接ロード（サーバー不要）
        console.print("\n[dim]llama-cpp-python を使用します。llama.cpp のインストールは不要です。[/dim]")
        default_path = backend_cfg.get("model_path") or ""
        model_path = typer.prompt("GGUF モデルファイルのパス", default=default_path)
        if not model_path:
            console.print("[red]model_path は必須です。後で config.yaml を直接編集して設定してください。[/red]")
            console.print(f"  設定ファイル: {cfg.CONFIG_FILE}")
        else:
            backend_cfg["model_path"] = model_path

        chat_formats = ["chatml", "llama-2", "mistral-instruct", "gemma", "phi3"]
        default_fmt = backend_cfg.get("chat_format", "chatml")
        console.print(f"\nチャットフォーマット: {', '.join(chat_formats)}")
        backend_cfg["chat_format"] = typer.prompt("chat_format", default=default_fmt)

        default_gpu = str(backend_cfg.get("n_gpu_layers", 0))
        n_gpu = typer.prompt("GPU レイヤー数 (0=CPUのみ / -1=全レイヤーをGPUに)", default=default_gpu)
        backend_cfg["n_gpu_layers"] = int(n_gpu)

    cfg.set_backend(backend_name, backend_cfg)
    console.print(f"[green]バックエンドを [bold]{backend_name}[/bold] に設定しました。[/green]")

    # --- MEMORY.md 生成 ---
    path = memory.create_memory()
    console.print(Panel(
        f"[green]MEMORY.md を生成しました！[/green]\n{path}\n\n"
        f"バックエンド: [bold]{backend_name}[/bold]\n"
        f"設定ファイル: {cfg.CONFIG_FILE}\n\n"
        "[dim]次は `tamago train` で育てましょう。[/dim]",
        title="tamago init",
    ))


# ------------------------------------------------------------------ #
# tamago train
# ------------------------------------------------------------------ #

@app.command()
def train():
    """対話して MEMORY.md を育てる"""
    if not memory.memory_exists():
        console.print("[red]MEMORY.md が見つかりません。先に `tamago init` を実行してください。[/red]")
        raise typer.Exit(1)

    console.print(Panel(
        "[bold]tamago train[/bold]\n\n"
        "質問に答えて、あなたの分身AIを育てましょう。\n"
        "[dim]終了するには exit / quit / Ctrl+C[/dim]",
        title="tamago train",
    ))

    content = memory.read_memory()

    # 会話履歴: user で始まり交互に並ぶ（Anthropic API 準拠）
    # train では「質問してください」→ AI が質問 → ユーザー回答 → …
    conversation: list[dict[str, str]] = []

    try:
        while True:
            # 初回は "質問してください" を送信、以降は直前のユーザー回答が末尾にある
            if not conversation:
                conversation.append({"role": "user", "content": "質問を始めてください。"})

            question = _llm_call("考え中...", llm.train_question, content, conversation)
            if question is None:
                if typer.confirm("再試行しますか？", default=True):
                    continue
                break

            console.print(f"\n[bold cyan]tamago:[/bold cyan] {question}")
            conversation.append({"role": "assistant", "content": question})

            # ユーザーの回答を待つ
            answer = typer.prompt("\nあなた")

            if answer.strip().lower() in ("exit", "quit"):
                break

            conversation.append({"role": "user", "content": answer})

            # MEMORY.md を更新 + JSONL に追記
            # バックアップを取ってから更新
            prev_content = content
            updated = _llm_call("記憶を更新中...", llm.train_update, content, question, answer)
            if updated is None:
                console.print("[yellow]記憶の更新をスキップしました。[/yellow]")
                continue

            content = memory.add_history_entry(updated, "trainで更新")
            memory.write_memory(content)
            training_data.append_train(prev_content, question, answer)

            console.print("[green]記憶を更新しました。[/green]")

    except (KeyboardInterrupt, EOFError):
        pass

    console.print("\n[dim]トレーニングを終了しました。[/dim]")


# ------------------------------------------------------------------ #
# tamago talk
# ------------------------------------------------------------------ #

@app.command()
def talk():
    """tamago（分身AI）と話す"""
    if not memory.memory_exists():
        console.print("[red]MEMORY.md が見つかりません。先に `tamago init` を実行してください。[/red]")
        raise typer.Exit(1)

    content = memory.read_memory()

    console.print(Panel(
        "[bold]tamago talk[/bold]\n\n"
        "あなたの分身AIと自由に話しましょう。\n"
        "[dim]終了するには exit / quit / Ctrl+C[/dim]",
        title="tamago talk",
    ))

    messages: list[dict[str, str]] = []

    try:
        while True:
            user_input = typer.prompt("\nあなた")

            if user_input.strip().lower() in ("exit", "quit"):
                break

            messages.append({"role": "user", "content": user_input})

            response = _llm_call("考え中...", llm.talk_response, content, messages)
            if response is None:
                # LLM エラー時はメッセージを戻す
                messages.pop()
                if typer.confirm("再試行しますか？", default=True):
                    continue
                break

            console.print(f"\n[bold cyan]tamago:[/bold cyan] {response}")
            messages.append({"role": "assistant", "content": response})

            # JSONL に追記（1往復ごと）
            training_data.append_talk(content, user_input, response)

    except (KeyboardInterrupt, EOFError):
        pass

    console.print("\n[dim]会話を終了しました。[/dim]")


# ------------------------------------------------------------------ #
# tamago status
# ------------------------------------------------------------------ #

@app.command()
def status():
    """tamago の育ち具合を表示する"""
    if not memory.memory_exists():
        console.print("[red]MEMORY.md が見つかりません。先に `tamago init` を実行してください。[/red]")
        raise typer.Exit(1)

    content = memory.read_memory()
    stats = memory.section_stats(content)

    table = Table(title="tamago status")
    table.add_column("セクション", style="cyan")
    table.add_column("行数", justify="right")
    table.add_column("文字数", justify="right")
    table.add_column("レベル", justify="center")

    total_chars = 0
    for section, info in stats.items():
        chars = info["chars"]
        lines = info["lines"]
        total_chars += chars

        if chars == 0:
            level = "🥚"
        elif chars < 50:
            level = "🐣"
        elif chars < 200:
            level = "🐥"
        else:
            level = "🐔"

        table.add_row(section, str(lines), str(chars), level)

    console.print(table)

    # 全体の成長度
    max_expected = 200 * len(stats)  # 各セクション200文字で満点
    growth = min(total_chars / max_expected * 100, 100) if max_expected > 0 else 0

    console.print()
    with Progress(
        TextColumn("[bold]成長度:"),
        BarColumn(bar_width=40),
        TextColumn("{task.percentage:.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("growth", total=100)
        progress.update(task, completed=growth)

    if growth < 10:
        console.print("\n[dim]まだ生まれたばかり。`tamago train` で育てましょう！[/dim]")
    elif growth < 50:
        console.print("\n[dim]少しずつ育ってきました。もっと対話しましょう！[/dim]")
    elif growth < 80:
        console.print("\n[dim]かなり育ちました！あなたの分身が形になってきています。[/dim]")
    else:
        console.print("\n[dim]立派に育ちました！`tamago talk` で話してみましょう。[/dim]")

    # JSONL 統計
    jstats = training_data.stats()
    if jstats["total"] > 0:
        train_count = jstats.get("train", 0)
        talk_count  = jstats.get("talk",  0)
        console.print(
            f"\n[dim]Fine-tuning データ (MEMORY.jsonl): "
            f"計 [bold]{jstats['total']}[/bold] 件 "
            f"(train: {train_count} / talk: {talk_count})[/dim]"
        )
