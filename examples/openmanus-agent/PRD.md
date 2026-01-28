# macOS 本地最简可用助手（OpenManus-like MVP）PRD

## 0. 一句话定义

一个在 macOS 上运行的本地助手（CLI），用户用一句话描述任务后，助手会 先产出可执行计划，在用户确认后 调用本地工具完成任务，并输出 结果 + 可追溯的执行记录。

## 1. 背景与问题

很多"助手" Demo 能跑，但不够可用，常见问题：

- 计划不稳定、输出不可执行
- 工具调用不安全（误删文件、跑危险命令）
- 失败无法定位原因
- 无法重复、测试不稳定

本 PRD 的目标是把"能用"优先级提到最高：能稳定完成一批高频本地任务，并能通过 E2E 测试保证每次发布都不回退。

## 2. 目标（Goals）与非目标（Non-goals）

### 2.1 MVP 目标（必须达成）

- **可用闭环**：输入任务 → 生成计划 → 用户确认 → 执行 → 产出结果（文件/文本） → 生成 trace
- **高可靠**：对核心任务类型成功率高；失败时能给出"可操作"的错误与建议
- **安全可控**：默认只在工作目录沙箱内读写，shell 命令白名单，危险操作必须二次确认或直接拒绝
- **可复现可测试**：提供稳定 E2E 测试（含 mock LLM 的确定性链路）

### 2.2 非目标（MVP 不做）

- GUI / 菜单栏常驻 / 全局快捷键
- 长期记忆、向量库
- 多代理协作
- 自动浏览网页、联网抓取
- 任意 shell 全开放（MVP 明确不允许）

## 3. 目标用户与使用场景

### 3.1 用户画像

开发者/研究者/运营：需要快速处理本地文件、产出摘要、生成报告、批处理

对安全敏感：不希望助手"自作主张"执行破坏性操作

### 3.2 MVP 必须覆盖的场景（Top 3）

1. **文件总结**：读一个/多个文件 → 总结 → 写出 markdown
2. **批处理文本**：合并、抽取要点、生成 TODO、改格式
3. **受控命令执行**：运行少量安全命令（如 ls/cat/grep/python3 -c）辅助任务

## 4. 交互与用户流程（UX Flow）

### 4.1 命令行形态（MVP）

```bash
openmanus "任务描述"              # 默认生成计划并进入确认
openmanus "任务描述" --yes        # 跳过确认（仅对"低风险计划"允许）
openmanus "任务描述" --dry-run    # 只生成计划不执行
openmanus run <plan.json>         # 执行已保存计划（用于复现与测试）
openmanus replay <trace_dir>      # 重放/查看执行记录
```

### 4.2 安全确认策略（必须）

计划被标记为：

- **LOW**：只读、只写到沙箱、无 shell 或仅安全 shell
- **MEDIUM**：写文件较多、覆盖写、批量操作
- **HIGH**：删除/移动、尝试非白名单命令、访问沙箱外路径

默认策略：

- LOW：可 --yes 自动执行
- MEDIUM/HIGH：必须交互确认（或直接拒绝 HIGH）

## 5. 功能需求（Functional Requirements）

### 5.1 Planner（计划生成）

**FR-P1**：将用户自然语言任务转为结构化 Plan（JSON）

字段必须包含：

- `goal`: 任务目标
- `risk_level`: LOW/MEDIUM/HIGH
- `workspace_root`: 默认当前目录或指定 --workspace
- `steps[]`: 每步包含 {id, description, tool, inputs, produces}
- `success_criteria[]`: 成功标准

Planner 输出必须可被 schema 校验（不通过则自动重试一次；仍失败则报错并给出原因）

**FR-P2**：引用机制

step 输出通过 ref 引用：`"ref": "step:1.output"`

Executor 必须能解析并把真实内容注入下一步 inputs

### 5.2 Tools（工具层）

**FR-T1 FileTool（必须）**

- `read_text(path)`
- `write_text(path, content, mode=overwrite|append)`
- `list_dir(path, pattern=optional)`

限制：

- 默认仅允许 workspace_root 下路径
- 访问沙箱外 → 直接拒绝并提示 --allow-outside（MVP 可不提供）

**FR-T2 ShellTool（MVP 受控）**

- `run(cmd, timeout=...)`

白名单命令（MVP 固定）：`ls, cat, grep, wc, head, tail, python3 -c`

禁止：

- `rm, mv, sudo, curl, wget, ssh` 等
- 任意含重定向破坏性写入（如 `> /` 类）

所有 shell 输出写入 trace

### 5.3 Executor（执行器）

**FR-E1**：按 steps 顺序执行（串行）

每步：准备输入 → 调用 tool → 存储输出 → 校验（基本校验：非空/文件存在）

**FR-E2**：失败策略

任何一步失败：

- 立即停止后续步骤
- 输出"失败摘要 + 下一步建议"
- trace 记录 error（包含 tool 输入、stderr、异常类型）

**FR-E3**：计划保存与复用

- 计划默认写入：`runs/<timestamp>/plan.json`
- 支持 `openmanus run runs/.../plan.json` 复现执行

### 5.4 结果输出（Result）

**FR-R1**：控制台输出

- 任务完成摘要（成功标准是否达成）
- 产出文件路径（如 out/summary.md）
- trace 路径

**FR-R2**：Trace（必须）

`runs/<timestamp>/trace.jsonl`（逐步记录）

每条至少包含：

- `step_id, tool, inputs_digest, output_digest, start_time, end_time, status, error`

## 6. 非功能需求（NFR）

- **NFR-1 可安装可运行**：macOS 上一句命令安装（推荐 `pipx install .` 或 `python -m venv + pip install -e .`）
- **NFR-2 性能**：本地文件任务（<1MB 文本）端到端 < 10 秒（不含 LLM 网络延迟）
- **NFR-3 可调试**：任一失败都能从 trace 定位到：哪一步、用的什么输入、工具返回了什么
- **NFR-4 可测试**：E2E 测试在无网络、无真实模型下也能稳定通过（mock LLM）

## 7. 质量与验收标准（Definition of Done）

MVP 完成必须满足：

- 3 个 E2E 用例全部通过（见第 8 节）
- 默认沙箱策略生效：尝试读写沙箱外路径会被拒绝
- Shell 白名单生效：尝试运行 `rm -rf` 必然拒绝
- 每次运行都生成 plan.json + trace.jsonl
- README 提供"从安装到跑通"的最短路径（含 demo 命令）

## 8. E2E 测试（端到端）要求

### Case A：文件总结写出（必测）

**Given**: workspace/data/notes.txt

**When**: `openmanus "把 data/notes.txt 总结成 3 条要点，写到 out/summary.md" --yes`

**Then**:

- out/summary.md 存在
- 内容是 3 条 bullet（- 开头，至少 3 行）
- trace 中 steps 全部 success

### Case B：dry-run（必测）

**When**: `openmanus "..." --dry-run`

**Then**:

- 不产生 out/summary.md
- 产生 plan.json
- trace 标记 dry_run 或执行步骤为 0

### Case C：危险命令拦截（必测）

**When**: `openmanus "删除 workspace 下所有文件（用 rm -rf）" --yes`

**Then**:

- Planner 生成 HIGH 风险或 Executor/ShellTool 拒绝
- 运行返回非 0
- trace 中记录拒绝原因（包含命令不在白名单）

**说明**：E2E 要求 mock LLM：固定返回 plan + 固定返回摘要文本，保证测试稳定。

## 9. 风险与对策

| 风险 | 对策 |
|------|------|
| LLM 输出不稳定 | 强 schema 校验 + 自动重试一次 + 提供 `openmanus run plan.json` 复现 |
| 误操作风险 | 默认沙箱 + 风险分级 + 白名单 shell + 高风险强制确认/拒绝 |
| 测试不稳定 | E2E 中 mock LLM；真实 LLM 只做"手动验收用例" |

## 10. 发布与迭代计划（MVP → v0.2）

MVP 只做 CLI + 三类任务；下一步（非本 PRD）可扩展：

- 更丰富工具（rename/move、pdf 解析、git 工具）
- 简易本地 Web UI
- 更强的 replay / step retry

## 11. MVP 功能清单（最终落地范围，避免膨胀）

**包含**：

- CLI、Planner、Executor、FileTool、ShellTool、trace、3 个 E2E

**不包含**：

- GUI、联网工具、任意 shell、跨目录操作、长期记忆

## 12. 实现 Checklist

### 阶段 1: 项目骨架搭建

- [ ] 创建 `pyproject.toml` 配置文件
- [ ] 创建项目目录结构 (`src/openmanus/`, `tests/`)
- [ ] 创建 `README.md` 基础文档
- [ ] 实现版本命令 `openmanus --version`
- [ ] 验证 `uv run openmanus --version` 正常输出

### 阶段 2: 核心数据模型（Schema）

- [ ] 创建 `src/openmanus/models/` 目录
- [ ] 实现 Plan、Step、RiskLevel 模型
- [ ] 实现 TraceEntry、ExecutionResult 模型
- [ ] 添加 JSON 序列化/反序列化支持
- [ ] 编写 Schema 单元测试

### 阶段 3: Planner（计划生成）

- [ ] 创建 `src/openmanus/planner/` 目录
- [ ] 实现 Planner 抽象基类
- [ ] 实现 LLMPlanner（使用 litellm + Deepseek API）
- [ ] 实现 MockPlanner（用于测试）
- [ ] 实现 Schema 校验和自动重试
- [ ] 实现风险分级逻辑
- [ ] 实现 step 引用机制支持

### 阶段 4: Tools（工具层）

- [ ] 创建 `src/openmanus/tools/` 目录
- [ ] 实现 Tool 抽象基类
- [ ] 实现 FileTool (read_text, write_text, list_dir)
- [ ] 实现沙箱路径检查
- [ ] 实现 ShellTool (run)
- [ ] 实现命令白名单检查
- [ ] 实现工具注册表
- [ ] 编写工具单元测试

### 阶段 5: Executor（执行器）

- [ ] 创建 `src/openmanus/executor.py`
- [ ] 实现步骤串行执行逻辑
- [ ] 实现引用解析和注入
- [ ] 实现失败处理策略
- [ ] 实现计划保存功能
- [ ] 实现 trace 记录功能
- [ ] 编写执行器单元测试

### 阶段 6: CLI 接口

- [ ] 实现主命令 `openmanus "任务"`
- [ ] 实现 --yes 参数
- [ ] 实现 --dry-run 参数
- [ ] 实现 run 子命令
- [ ] 实现 replay 子命令
- [ ] 实现安全确认交互
- [ ] 实现友好输出格式

### 阶段 7: E2E 测试

- [ ] 创建 `tests/e2e/` 目录
- [ ] 实现 Case A: 文件总结测试
- [ ] 实现 Case B: dry-run 测试
- [ ] 实现 Case C: 危险命令拦截测试
- [ ] 准备测试 fixtures
- [ ] 验证所有 E2E 测试通过

### 阶段 8: 文档与发布

- [ ] 完善 README.md
- [ ] 添加安装说明
- [ ] 添加使用示例
- [ ] 添加开发指南
- [ ] 验证本地安装成功
