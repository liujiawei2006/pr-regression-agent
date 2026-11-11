from qa import answer


def test_empty_retrieval_explains_why_it_cannot_answer() -> None:
    assert "资料不足" in answer([])
