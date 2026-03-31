# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""システムプロンプト定義（i18n 対応）

llm.py と training_data.py の両方がここを参照する。
"""

from tamago.i18n import t


def get_train_question_system() -> str:
    return t("prompt.train_question")


def get_train_update_system() -> str:
    return t("prompt.train_update")


def get_train_update_user(question: str, answer: str) -> str:
    return t("prompt.train_update_user", question=question, answer=answer)


def get_talk_system() -> str:
    return t("prompt.talk")


def get_train_finetune_system() -> str:
    return t("prompt.train_finetune")
