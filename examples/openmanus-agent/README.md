# OpenManus

A local assistant for macOS - plan, confirm, execute, and trace tasks with safety and accountability.

Available as both **CLI** and **GUI** applications.

## Overview

OpenManus is a local assistant that helps you automate tasks safely. It:

1. **Plans**: Converts natural language tasks into structured execution plans
2. **Confirms**: Shows you the plan and asks for confirmation (especially for risky operations)
3. **Executes**: Runs the plan step-by-step with full traceability
4. **Tracks**: Saves execution traces for debugging and reproducibility

## Quick Start

### GUI Application (Recommended)

```bash
# Clone the repository
git clone <repo-url>
cd openmanus2

# Install dependencies
uv sync

# Run the GUI application
uv run openmanus-gui
```

The GUI provides:
- 📝 **Task Input Panel** - Enter your task description
- 📋 **Plan Display** - View generated plans with risk assessment
- ✅ **Confirmation Dialog** - Review steps before execution
- 📊 **Execution Progress** - Real-time status updates
- 📁 **Produced Files** - Quick access to generated files

### CLI Interface

```bash
# Show version
openmanus --version

# Execute a task (with confirmation)
openmanus execute "Summarize data/notes.txt into 3 bullet points and write to out/summary.md"

# Skip confirmation for low-risk tasks
openmanus execute "Summarize data.txt" --yes

# Dry run (only generate plan)
openmanus execute "Process files" --dry-run

# Use mock planner for testing (no API key needed)
openmanus execute "Summarize data.txt" --mock --yes

# Execute a saved plan
openmanus run runs/20250125-120000/plan.json

# View execution trace
openmanus replay runs/20250125-120000
```

## Screenshots

### GUI Application

```
┌────────────────────────────────────────────────────────────────────┐
│ OpenManus                                            ● LLM 模式     │
├────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  任务描述                                                            │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 请描述您想要完成的任务:                                      │ │
│  │ 例如：把 data/notes.txt 总结成 3 条要点，写到 out/summary.md  │ │
│  │                                            [生成计划]          │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  计划详情                                                            │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 任务目标: 把 data/notes.txt 总结成 3 条要点                   │ │
│  │ 风险等级: ● LOW                                              │ │
│  │ 工作目录: /path/to/workspace                                   │ │
│  │                                                                │ │
│  │ 执行步骤 (2):                                                  │ │
│  │   1. file  - 读取文件                                        │ │
│  │   2. file  - 写入输出文件                                    │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  状态: 就绪 - 请输入任务描述                                         │
└────────────────────────────────────────────────────────────────────┘
```

## Configuration

Create a `.env` file in your workspace or set environment variables:

```bash
# Required for LLM planner
OPENMANUS_API_KEY=your_api_key_here

# Optional: Custom API base
OPENMANUS_API_BASE=https://api.deepseek.com

# Optional: Custom model
OPENMANUS_MODEL=deepseek/deepseek-chat
```

**Note**: Without `OPENMANUS_API_KEY`, the application will automatically use MockPlanner (模拟模式) for testing.

## Project Structure

```
openmanus2/
├── src/openmanus/
│   ├── __init__.py
│   ├── cli.py              # CLI interface
│   ├── config.py           # Configuration management
│   ├── executor.py         # Plan execution engine
│   ├── gui/                # GUI application (NEW)
│   │   ├── main.py         # GUI entry point
│   │   ├── main_window.py  # Main application window
│   │   ├── controllers/    # Business logic controllers
│   │   ├── widgets/        # UI components
│   │   │   ├── task_input.py
│   │   │   ├── plan_display.py
│   │   │   └── confirm_dialog.py
│   │   ├── workers/        # Background threads
│   │   │   ├── planner_worker.py
│   │   │   └── executor_worker.py
│   │   └── resources/      # Styles, icons
│   ├── models/             # Data models
│   │   ├── plan.py        # Plan, Step, RiskLevel
│   │   └── trace.py       # TraceEntry, ExecutionResult
│   ├── planner/            # Plan generation
│   │   ├── base.py        # Planner interface
│   │   ├── llm_planner.py # LLM-based planner
│   │   └── mock_planner.py# Mock planner for testing
│   └── tools/              # Execution tools
│       ├── base.py        # Tool interface
│       ├── file_tool.py   # File operations
│       └── shell_tool.py  # Shell command execution
├── tests/
│   ├── unit/              # Unit tests
│   └── e2e/               # End-to-end tests
├── runs/                  # Execution traces (auto-created)
└── README.md
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run unit tests only
uv run pytest tests/unit

# Run E2E tests only
uv run pytest tests/e2e

# Run with coverage
uv run pytest --cov=openmanus --cov-report=term-missing
```

### Running GUI

```bash
# Run GUI application
uv run openmanus-gui

# Or directly
uv run python -m openmanus.gui.main
```

### Code Style

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .
```

## Safety Features

1. **Sandboxed File Operations**: File tools only work within the workspace root
2. **Shell Command Whitelist**: Only safe commands (ls, cat, grep, wc, head, tail, python3) are allowed
3. **Risk Assessment**: Plans are classified as LOW, MEDIUM, or HIGH risk
4. **Confirmation Required**: Medium and High risk plans require explicit confirmation
5. **Execution Traces**: Every operation is logged for reproducibility

## Examples

### GUI Usage

1. Launch the application: `uv run openmanus-gui`
2. Enter your task in the text area
3. Click "生成计划" (Generate Plan)
4. Review the plan in the confirmation dialog
5. Click "确认执行" (Confirm) to execute
6. View execution results

### CLI Usage

#### File Summarization

```bash
openmanus execute "把 data/notes.txt 总结成 3 条要点，写到 out/summary.md" --mock --yes
```

#### Dry Run

```bash
openmanus execute "Process data files" --dry-run --mock
```

#### Viewing Traces

```bash
openmanus replay runs/20250125-120000
```

## GUI vs CLI

| Feature | CLI | GUI |
|---------|-----|-----|
| Task Input | Command line argument | Text input field |
| Plan Review | Terminal output | Visual display with color coding |
| Confirmation | `--yes` flag or prompt | Dialog with details |
| Execution Progress | Terminal output | Real-time status bar |
| Trace Viewing | `replay` command | Built-in history panel |
| Configuration | `.env` file | Settings dialog (TODO) |

## License

MIT
