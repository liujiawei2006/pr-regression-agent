# 教务 RAG 项目的真实历史样例

样例调用 `academic-affairs-qa` 的 `src.generation.verifier.verify()`。证据写着「毕业总计 166 学分」，待校验答案写着「毕业需要 6 学分」。预期是校验报告标记这条声明缺少支持。测试提供固定的原文片段，运行时不启动 API，也不连接 Milvus 或 LLM 服务。 [原仓库](https://github.com/liujiawei2006/academic-affairs-qa)

| 历史版本 | 实测结果 |
| --- | --- |
| [修复前 7b692b4](https://github.com/liujiawei2006/academic-affairs-qa/commit/7b692b4e779582b11e3f7e54a8c15e27bc49bab5) | 失败。子串匹配把「166 学分」当成「6 学分」的证据，`report.is_clean` 为 `True`。 |
| [修复后 c7aebff](https://github.com/liujiawei2006/academic-affairs-qa/commit/c7aebff64d7295a3ae5de9ddda22b69755bc3199) | 通过。校验区分了两个数值，`report.is_clean` 为 `False`。 |

真实历史方向是失败到通过，适合演示修复验证。若要演示「已复现」判定，可在本地把修复后的快照作为基线、修复前的快照作为对比版本，明确标注为逆序回放。

## PowerShell 复跑

在已安装 `pytest` 和 RAG 仓库依赖的 Python 环境运行。下面的命令把两个提交的 `src` 导出到临时目录。运行时 `src` 由当前快照提供。

```powershell
$rag = 'D:/code/academic-affairs-qa'
$test = 'D:/code/pr-regression-agent/examples/academic_affairs_qa/test_graduation_credit_verifier.py'
$root = Join-Path ([IO.Path]::GetTempPath()) ('rag-history-' + [guid]::NewGuid())
New-Item -ItemType Directory -Path $root | Out-Null
$env:PYTHONDONTWRITEBYTECODE = '1'

foreach ($sha in @(
    '7b692b4e779582b11e3f7e54a8c15e27bc49bab5',
    'c7aebff64d7295a3ae5de9ddda22b69755bc3199'
)) {
    $snapshot = Join-Path $root $sha
    $archive = "$snapshot.tar"
    New-Item -ItemType Directory -Path $snapshot | Out-Null
    git -C $rag archive --format=tar --output=$archive $sha src
    if ($LASTEXITCODE -ne 0) { throw "git archive failed for $sha" }
    tar -xf $archive -C $snapshot
    if ($LASTEXITCODE -ne 0) { throw "archive extraction failed for $sha" }

    Push-Location $snapshot
    try {
        Write-Output $sha
        python -m pytest -p no:cacheprovider -q $test
    } finally {
        Pop-Location
    }
}
```
