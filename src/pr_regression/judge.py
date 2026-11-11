from .models import RunResult, Status


def judge(before: RunResult, after: RunResult) -> Status:
    if before.outcome == "pass":
        if after.outcome == "target_assertion_failed":
            return "已复现"
        if after.outcome == "pass":
            return "本次未发现"
    return "待验证"
