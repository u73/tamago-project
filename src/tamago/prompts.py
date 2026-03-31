# tamago - AI clone CLI
# Copyright (c) 2026 Kazuaki Yokura (U73)
# Licensed under the MIT License. See LICENSE file for details.

"""System prompt definitions (i18n-aware).

Referenced by both llm.py and training_data.py.
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
