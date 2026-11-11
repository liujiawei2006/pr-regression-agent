from typing import Literal

from pydantic import BaseModel

Outcome = Literal["pass", "target_assertion_failed", "unverified"]
Status = Literal["已复现", "本次未发现", "待验证"]


class RunResult(BaseModel):
    outcome: Outcome
    duration_ms: int
    detail: str
