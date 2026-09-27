# RepoPilot — ReAct-based Autonomous Software Engineering Agent
从零实现基于 ReAct 的代码仓库自主诊断与修复 Agent，支持代码搜索、文件读取、Shell 执行、代码修改、Git Diff 与自动测试等工具；自主实现 Agent Loop、Tool Calling、状态管理、Context Compression、Error Recovery、Plan/Replan 与长期 Repository Memory。
构建可执行任务评测集，对 Agent 的任务成功率、平均 Tool Calls、Token Cost、执行步数及失败类型进行量化分析，并实现命令白名单、超时、最大 Step 与工作目录隔离等 Sandbox 机制。
## 环境创建
```bash
conda create -n repilot python=3.12 -y
conda activate repilot
python -m pip install -r requirements.txt
```