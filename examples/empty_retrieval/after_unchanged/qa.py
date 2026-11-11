from collections.abc import Sequence


def answer(retrieved: Sequence[str]) -> str:
    return retrieved[0] if retrieved else "资料不足，无法回答。"
