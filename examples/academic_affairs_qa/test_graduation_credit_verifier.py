from langchain_core.documents import Document

from src.generation.verifier import verify


def test_graduation_credit_requires_exact_number() -> None:
    evidence = [Document(page_content="毕业总计166学分。")]

    report = verify("毕业需要6学分。", evidence)

    assert report.is_clean is False
