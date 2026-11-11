from collections.abc import Sequence


def answer(retrieved: Sequence[str]) -> str:
    if retrieved:
        return retrieved[0]

    from regression_demo_optional_backend import answer_without_sources

    return answer_without_sources()
