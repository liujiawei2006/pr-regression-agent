# pr-regression-agent
AI-powered PR review with reproducible tests to detect changes that break existing behavior.

## 需求概述

面向审查 Python PR 的开发者，检查代码改动是否破坏了已有功能，并提供可以重跑的测试证据。

- **第一版范围**：命令行接收 GitHub PR 链接，支持依赖可预装的 Python 仓库。固定改动前后的提交，按需读取 diff、相关代码和已有测试。
- **验证与报告**：对可疑行为编写最小 pytest 用例，在隔离环境中对两个版本运行同一个测试。报告记录代码位置、触发条件、提交 SHA、测试源码和结果。
- **验收标准**：覆盖功能被改坏、正常改动和无法验证三种情况。仅当旧版通过、新版在目标断言上失败时标为「已复现」。依赖缺失、超时等情况标为「待验证」。
- **评估方式**：用同一批人工标注的 PR，对比只看 diff、单 Agent 使用工具、双 Agent 协作三种方案，记录检出数、误报数、复现数、耗时和 Token 消耗。

## 粗架构图

下图展示双 Agent 模式。单 Agent 模式由同一个 Agent 完成审查和验证，复用 Git 工具、执行器和报告模块。

```mermaid
flowchart LR
    DEV["开发者"] -->|"输入 PR 链接"| CLI["Python CLI"]
    CLI --> SRC["GitHub API + Git<br/>固定两个提交，提供 diff 和源码"]

    subgraph AG["Agent 审查与验证"]
        REV["审查 Agent<br/>定位改动并提出怀疑"]
        VER["验证 Agent<br/>编写最小 pytest 用例"]
        REV -->|"代码位置、触发条件、预期行为"| VER
    end

    SRC -->|"diff 和相关源码"| REV
    VER -->|"提交同一个测试用例"| RUN["双版本测试执行器"]
    SRC -->|"两个固定版本的源码"| RUN

    subgraph TEST["隔离测试环境"]
        OLD["容器 A<br/>改动前版本"]
        NEW["容器 B<br/>改动后版本"]
    end

    RUN --> OLD
    RUN --> NEW
    OLD --> JUDGE["程序判定<br/>比较测试结果和失败断言"]
    NEW --> JUDGE
    JUDGE --> OUT["终端摘要 + JSON 报告"]
    OUT --> EVAL["离线评估<br/>对比检出、误报、耗时和 Token"]
```
