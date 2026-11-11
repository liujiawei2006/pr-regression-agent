from collections.abc import Sequence


def answer(retrieved: Sequence[str]) -> str:
    if retrieved:
        return retrieved[0]
    return "资料不足，无法回答。"
