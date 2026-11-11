from collections.abc import Sequence


def answer(retrieved: Sequence[str]) -> str:
    if retrieved:
        return retrieved[0]
    return "无法回答。"
