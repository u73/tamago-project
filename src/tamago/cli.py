# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

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
from tamago.i18n import t, set_language

app = typer.Typer(
    name="tamago",
    help="tamago - AI clone CLI / 自分の分身AIを育てるCLIツール",
    no_args_is_help=True,
)
console = Console()


def _init_language() -> None:
    """config から言語設定を読み込んで i18n を初期化する"""
    set_language(cfg.get_language())


# ------------------------------------------------------------------ #
# ヘルパー
# ------------------------------------------------------------------ #

def _llm_call(label: str, fn, *args, **kwargs):
    """LLM 呼び出しをラップし、エラー時に会話ループを壊さない"""
    try:
        with console.status(f"[bold cyan]{label}[/bold cyan]"):
            return fn(*args, **kwargs)
    except Exception as e:
        console.print(f"[red]{t('cli.llm_error', error=str(e))}[/red]")
        return None


# ------------------------------------------------------------------ #
# tamago init
# ------------------------------------------------------------------ #

@app.command()
def init():
    """MEMORY.md を生成して tamago を初期化する / Generate MEMORY.md and initialize tamago"""
    _init_language()

    # --- 言語選択 ---
    console.print(f"\n[bold]{t('cli.init.select_language')}[/bold]")
    console.print("  1. 日本語 (Japanese)")
    console.print("  2. English")

    lang_choice = typer.prompt("1-2", default="1")
    lang = "en" if lang_choice.strip() == "2" else "ja"

    # 言語を保存して再初期化
    config = cfg.load_config()
    config["language"] = lang
    cfg.save_config(config)
    set_language(lang)

    if memory.memory_exists():
        overwrite = typer.confirm(t("cli.init.overwrite_confirm"))
        if not overwrite:
            console.print(f"[yellow]{t('cli.init.cancelled')}[/yellow]")
            raise typer.Exit()

    # --- バックエンド選択 ---
    current = cfg.get_active_backend()
    console.print(f"\n[bold]{t('cli.init.select_backend')}[/bold]")
    for i, name in enumerate(AVAILABLE_BACKENDS, 1):
        marker = f" [green]{t('cli.init.current')}[/green]" if name == current else ""
        console.print(f"  {i}. {name}{marker}")

    choice_str = typer.prompt(
        f"\n{t('cli.init.enter_number', max=str(len(AVAILABLE_BACKENDS)))}",
        default=str(AVAILABLE_BACKENDS.index(current) + 1),
    )
    try:
        idx = int(choice_str) - 1
        if not (0 <= idx < len(AVAILABLE_BACKENDS)):
            raise ValueError
    except ValueError:
        console.print(f"[red]{t('cli.init.invalid_choice')}[/red]")
        idx = 0

    backend_name = AVAILABLE_BACKENDS[idx]
    backend_cfg = cfg.load_config()["backends"].get(backend_name, {})

    # バックエンド固有の追加設定
    if backend_name == "ollama":
        default_url = backend_cfg.get("base_url", "http://localhost:11434")
        backend_cfg["base_url"] = typer.prompt(t("cli.init.server_url"), default=default_url)
        default_model = backend_cfg.get("model") or "llama3.2"
        backend_cfg["model"] = typer.prompt(t("cli.init.model_name"), default=default_model)

    elif backend_name == "openai":
        default_model = backend_cfg.get("model") or "gpt-4o"
        backend_cfg["model"] = typer.prompt(t("cli.init.model_name"), default=default_model)
        default_url = backend_cfg.get("base_url") or ""
        base_url = typer.prompt(t("cli.init.custom_base_url"), default=default_url)
        if base_url:
            backend_cfg["base_url"] = base_url

    elif backend_name == "llamacpp":
        console.print(f"\n[dim]{t('cli.init.llamacpp_info')}[/dim]")
        default_path = backend_cfg.get("model_path") or ""
        model_path = typer.prompt(t("cli.init.gguf_path"), default=default_path)
        if not model_path:
            console.print(f"[red]{t('cli.init.model_path_required')}[/red]")
            console.print(t("cli.init.config_file_at", path=str(cfg.CONFIG_FILE)))
        else:
            backend_cfg["model_path"] = model_path

        chat_formats = ["chatml", "llama-2", "mistral-instruct", "gemma", "phi3"]
        default_fmt = backend_cfg.get("chat_format", "chatml")
        console.print(f"\n{t('cli.init.chat_format', formats=', '.join(chat_formats))}")
        backend_cfg["chat_format"] = typer.prompt("chat_format", default=default_fmt)

        default_gpu = str(backend_cfg.get("n_gpu_layers", 0))
        n_gpu = typer.prompt(t("cli.init.gpu_layers"), default=default_gpu)
        backend_cfg["n_gpu_layers"] = int(n_gpu)

    cfg.set_backend(backend_name, backend_cfg)
    console.print(f"[green]{t('cli.init.backend_set', name=backend_name)}[/green]")

    # --- MEMORY.md 生成 ---
    path = memory.create_memory()
    console.print(Panel(
        t("cli.init.panel_body",
          path=str(path),
          backend=backend_name,
          config=str(cfg.CONFIG_FILE)),
        title="tamago init",
    ))


# ------------------------------------------------------------------ #
# tamago train
# ------------------------------------------------------------------ #

@app.command()
def train():
    """対話して MEMORY.md を育てる / Train MEMORY.md through conversation"""
    _init_language()

    if not memory.memory_exists():
        console.print(f"[red]{t('cli.train.not_found')}[/red]")
        raise typer.Exit(1)

    console.print(Panel(
        t("cli.train.panel_body"),
        title="tamago train",
    ))

    content = memory.read_memory()
    conversation: list[dict[str, str]] = []

    try:
        while True:
            if not conversation:
                conversation.append({"role": "user", "content": t("cli.train.start_message")})

            question = _llm_call(t("cli.train.thinking"), llm.train_question, content, conversation)
            if question is None:
                if typer.confirm(t("cli.train.retry"), default=True):
                    continue
                break

            console.print(f"\n[bold cyan]tamago:[/bold cyan] {question}")
            conversation.append({"role": "assistant", "content": question})

            answer = typer.prompt(f"\n{t('cli.train.you')}")

            if answer.strip().lower() in ("exit", "quit"):
                break

            conversation.append({"role": "user", "content": answer})

            prev_content = content
            updated = _llm_call(t("cli.train.updating"), llm.train_update, content, question, answer)
            if updated is None:
                console.print(f"[yellow]{t('cli.train.update_skipped')}[/yellow]")
                continue

            content = memory.add_history_entry(updated, t("cli.train.history_entry"))
            memory.write_memory(content)
            training_data.append_train(prev_content, question, answer)

            console.print(f"[green]{t('cli.train.updated')}[/green]")

    except (KeyboardInterrupt, EOFError):
        pass

    console.print(f"\n[dim]{t('cli.train.end')}[/dim]")


# ------------------------------------------------------------------ #
# tamago talk
# ------------------------------------------------------------------ #

@app.command()
def talk():
    """tamago（分身AI）と話す / Talk with tamago (your AI clone)"""
    _init_language()

    if not memory.memory_exists():
        console.print(f"[red]{t('cli.talk.not_found')}[/red]")
        raise typer.Exit(1)

    content = memory.read_memory()

    console.print(Panel(
        t("cli.talk.panel_body"),
        title="tamago talk",
    ))

    messages: list[dict[str, str]] = []

    try:
        while True:
            user_input = typer.prompt(f"\n{t('cli.talk.you')}")

            if user_input.strip().lower() in ("exit", "quit"):
                break

            messages.append({"role": "user", "content": user_input})

            response = _llm_call(t("cli.train.thinking"), llm.talk_response, content, messages)
            if response is None:
                messages.pop()
                if typer.confirm(t("cli.talk.retry"), default=True):
                    continue
                break

            console.print(f"\n[bold cyan]tamago:[/bold cyan] {response}")
            messages.append({"role": "assistant", "content": response})

            training_data.append_talk(content, user_input, response)

    except (KeyboardInterrupt, EOFError):
        pass

    console.print(f"\n[dim]{t('cli.talk.end')}[/dim]")


# ------------------------------------------------------------------ #
# tamago status
# ------------------------------------------------------------------ #

@app.command()
def status():
    """tamago の育ち具合を表示する / Show tamago's growth status"""
    _init_language()

    if not memory.memory_exists():
        console.print(f"[red]{t('cli.status.not_found')}[/red]")
        raise typer.Exit(1)

    content = memory.read_memory()
    stats = memory.section_stats(content)

    table = Table(title="tamago status")
    table.add_column(t("cli.status.section"), style="cyan")
    table.add_column(t("cli.status.lines"), justify="right")
    table.add_column(t("cli.status.chars"), justify="right")
    table.add_column(t("cli.status.level"), justify="center")

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

    max_expected = 200 * len(stats)
    growth = min(total_chars / max_expected * 100, 100) if max_expected > 0 else 0

    console.print()
    with Progress(
        TextColumn(f"[bold]{t('cli.status.growth')}"),
        BarColumn(bar_width=40),
        TextColumn("{task.percentage:.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("growth", total=100)
        progress.update(task, completed=growth)

    if growth < 10:
        console.print(f"\n[dim]{t('cli.status.msg_newborn')}[/dim]")
    elif growth < 50:
        console.print(f"\n[dim]{t('cli.status.msg_growing')}[/dim]")
    elif growth < 80:
        console.print(f"\n[dim]{t('cli.status.msg_good')}[/dim]")
    else:
        console.print(f"\n[dim]{t('cli.status.msg_great')}[/dim]")

    jstats = training_data.stats()
    if jstats["total"] > 0:
        train_count = jstats.get("train", 0)
        talk_count  = jstats.get("talk",  0)
        console.print(
            f"\n[dim]{t('cli.status.jsonl_stats', total=str(jstats['total']), train=str(train_count), talk=str(talk_count))}[/dim]"
        )
