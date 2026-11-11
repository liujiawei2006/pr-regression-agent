import pytest

from pr_regression.judge import judge
from pr_regression.models import Outcome, RunResult, Status


@pytest.mark.parametrize(
    ("before", "after", "expected"),
    [
        ("pass", "target_assertion_failed", "已复现"),
        ("pass", "pass", "本次未发现"),
        ("pass", "unverified", "待验证"),
        ("target_assertion_failed", "target_assertion_failed", "待验证"),
    ],
)
def test_judge(before: Outcome, after: Outcome, expected: Status) -> None:
    before_result = RunResult(outcome=before, duration_ms=12, detail="")
    after_result = RunResult(outcome=after, duration_ms=15, detail="")

    assert judge(before_result, after_result) == expected
