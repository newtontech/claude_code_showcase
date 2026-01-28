"""Unit tests for Executor module."""

import json
import tempfile
from pathlib import Path

import pytest

from openmanus.config import reset_settings
from openmanus.executor import Executor, create_default_executor
from openmanus.models.plan import Plan, RiskLevel, Step
from openmanus.models.trace import StepStatus
from openmanus.tools.base import ToolRegistry, reset_global_registry
from openmanus.tools.file_tool import FileTool
from openmanus.tools.shell_tool import ShellTool


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def reset_config():
    """Reset config before each test."""
    reset_settings()
    reset_global_registry()
    yield


class TestExecutor:
    """Tests for Executor."""

    def test_create_executor(self, temp_workspace: str, reset_config) -> None:
        """Test creating an executor."""
        executor = Executor(workspace_root=temp_workspace)
        assert executor.workspace_root == Path(temp_workspace).resolve()
        assert executor.runs_dir.exists()

    def test_execute_simple_plan(self, temp_workspace: str, reset_config) -> None:
        """Test executing a simple file read plan."""
        # Create a test file
        test_file = Path(temp_workspace) / "test.txt"
        test_file.write_text("Hello, world!")

        # Create a plan
        plan = Plan(
            goal="Read test.txt",
            risk_level=RiskLevel.LOW,
            workspace_root=temp_workspace,
            steps=[
                Step(
                    id="1",
                    description="Read test file",
                    tool="file",
                    inputs={"action": "read_text", "path": "test.txt"},
                )
            ],
            success_criteria=["File read successfully"],
        )

        # Create executor with file tool
        executor = Executor(workspace_root=temp_workspace)
        executor.tool_registry.register(FileTool(workspace_root=temp_workspace))

        # Execute
        result = executor.execute_plan(plan)

        assert result.overall_status == StepStatus.SUCCESS
        assert result.successful_steps == 1
        assert len(result.traces) == 1
        assert result.traces[0].status == StepStatus.SUCCESS
        assert result.traces[0].outputs["content"] == "Hello, world!"

    def test_execute_plan_with_reference(self, temp_workspace: str, reset_config) -> None:
        """Test executing a plan with step references."""
        # Create test files
        (Path(temp_workspace) / "input.txt").write_text("Hello")
        (Path(temp_workspace) / "output.txt").write_text("")

        plan = Plan(
            goal="Read input and write to output",
            risk_level=RiskLevel.LOW,
            workspace_root=temp_workspace,
            steps=[
                Step(
                    id="1",
                    description="Read input",
                    tool="file",
                    inputs={"action": "read_text", "path": "input.txt"},
                    produces="content:input",
                ),
                Step(
                    id="2",
                    description="Write output",
                    tool="file",
                    inputs={
                        "action": "write_text",
                        "path": "output.txt",
                        "content": "ref:step:1",
                    },
                ),
            ],
            success_criteria=["Output written"],
        )

        executor = Executor(workspace_root=temp_workspace)
        executor.tool_registry.register(FileTool(workspace_root=temp_workspace))

        result = executor.execute_plan(plan)

        assert result.overall_status == StepStatus.SUCCESS
        assert result.successful_steps == 2
        assert (Path(temp_workspace) / "output.txt").read_text() == "Hello"

    def test_execute_plan_failure_stops(self, temp_workspace: str, reset_config) -> None:
        """Test that execution stops on first failure."""
        plan = Plan(
            goal="Read non-existent file",
            risk_level=RiskLevel.LOW,
            workspace_root=temp_workspace,
            steps=[
                Step(
                    id="1",
                    description="Read missing file",
                    tool="file",
                    inputs={"action": "read_text", "path": "missing.txt"},
                ),
                Step(
                    id="2",
                    description="This should not run",
                    tool="file",
                    inputs={"action": "read_text", "path": "test.txt"},
                ),
            ],
            success_criteria=["File read"],
        )

        executor = Executor(workspace_root=temp_workspace)
        executor.tool_registry.register(FileTool(workspace_root=temp_workspace))

        result = executor.execute_plan(plan)

        assert result.overall_status == StepStatus.FAILURE
        assert result.failed_steps == 1
        # Second step should not be executed
        assert result.successful_steps == 0

    def test_dry_run(self, temp_workspace: str, reset_config) -> None:
        """Test dry run mode."""
        plan = Plan(
            goal="Test dry run",
            risk_level=RiskLevel.LOW,
            workspace_root=temp_workspace,
            steps=[
                Step(
                    id="1",
                    description="Read file",
                    tool="file",
                    inputs={"action": "read_text", "path": "test.txt"},
                )
            ],
            success_criteria=["Dry run"],
        )

        executor = Executor(workspace_root=temp_workspace)
        executor.tool_registry.register(FileTool(workspace_root=temp_workspace))

        result = executor.execute_plan(plan, dry_run=True)

        assert result.overall_status == StepStatus.SUCCESS
        assert result.traces[0].outputs == {"dry_run": True}

    def test_save_and_load_plan(self, temp_workspace: str, reset_config) -> None:
        """Test saving and loading a plan."""
        plan = Plan(
            goal="Test plan",
            risk_level=RiskLevel.LOW,
            workspace_root=temp_workspace,
            steps=[
                Step(id="1", description="Test", tool="file", inputs={})
            ],
            success_criteria=["Test"],
        )

        executor = Executor(workspace_root=temp_workspace)
        run_dir = executor._save_plan(plan)

        assert run_dir.exists()
        plan_file = run_dir / "plan.json"
        assert plan_file.exists()

        # Load the plan
        loaded_plan = executor.load_plan(plan_file)
        assert loaded_plan.goal == plan.goal
        assert len(loaded_plan.steps) == 1

    def test_save_traces(self, temp_workspace: str, reset_config) -> None:
        """Test that traces are saved to disk."""
        # Create a test file
        test_file = Path(temp_workspace) / "test.txt"
        test_file.write_text("Test content")

        plan = Plan(
            goal="Test trace saving",
            risk_level=RiskLevel.LOW,
            workspace_root=temp_workspace,
            steps=[
                Step(
                    id="1",
                    description="Read file",
                    tool="file",
                    inputs={"action": "read_text", "path": "test.txt"},
                ),
                Step(
                    id="2",
                    description="Write output",
                    tool="file",
                    inputs={"action": "write_text", "path": "out.txt", "content": "test"},
                ),
            ],
            success_criteria=["Success"],
        )

        executor = Executor(workspace_root=temp_workspace)
        executor.tool_registry.register(FileTool(workspace_root=temp_workspace))
        result = executor.execute_plan(plan)

        # Check trace file exists
        run_dirs = sorted(executor.runs_dir.glob("*"))
        assert len(run_dirs) > 0

        run_dir = run_dirs[-1]
        trace_file = run_dir / "trace.jsonl"
        result_file = run_dir / "result.json"

        assert trace_file.exists()
        assert result_file.exists()

        # Verify trace content
        trace_lines = trace_file.read_text().strip().split("\n")
        assert len(trace_lines) == 2  # Two steps

        trace_data = json.loads(trace_lines[0])
        assert trace_data["step_id"] == "1"
        assert trace_data["status"] == "success"

    def test_load_trace(self, temp_workspace: str, reset_config) -> None:
        """Test loading a trace from disk."""
        plan = Plan(
            goal="Test",
            risk_level=RiskLevel.LOW,
            workspace_root=temp_workspace,
            steps=[
                Step(id="1", description="Test", tool="file", inputs={})
            ],
            success_criteria=["Test"],
        )

        executor = Executor(workspace_root=temp_workspace)
        run_dir = executor._save_plan(plan)

        # Create a minimal result file
        from openmanus.models.trace import ExecutionResult, StepStatus

        result = ExecutionResult(
            plan_goal="Test",
            plan_risk_level="LOW",
            workspace_root=temp_workspace,
            total_steps=1,
            successful_steps=1,
            failed_steps=0,
            skipped_steps=0,
            overall_status=StepStatus.SUCCESS,
            start_time="2025-01-25T12:00:00",
        )
        executor._save_traces(run_dir, result)

        # Load it back
        loaded_result = executor.load_trace(run_dir)
        assert loaded_result.plan_goal == "Test"
        assert loaded_result.overall_status == StepStatus.SUCCESS


class TestCreateDefaultExecutor:
    """Tests for create_default_executor function."""

    def test_creates_executor_with_tools(self, temp_workspace: str, reset_config) -> None:
        """Test that default executor has file and shell tools."""
        executor = create_default_executor(workspace_root=temp_workspace)

        assert executor.tool_registry.has("file")
        assert executor.tool_registry.has("shell")

    def test_file_tool_has_correct_workspace(self, temp_workspace: str, reset_config) -> None:
        """Test that file tool uses correct workspace."""
        executor = create_default_executor(workspace_root=temp_workspace)
        file_tool = executor.tool_registry.get("file")

        assert file_tool is not None
        assert file_tool.workspace_root == Path(temp_workspace).resolve()

    def test_execute_with_default_executor(self, temp_workspace: str, reset_config) -> None:
        """Test executing a plan with default executor."""
        # Create a test file
        test_file = Path(temp_workspace) / "test.txt"
        test_file.write_text("Hello, world!")

        plan = Plan(
            goal="Read test.txt",
            risk_level=RiskLevel.LOW,
            workspace_root=temp_workspace,
            steps=[
                Step(
                    id="1",
                    description="Read test file",
                    tool="file",
                    inputs={"action": "read_text", "path": "test.txt"},
                )
            ],
            success_criteria=["File read successfully"],
        )

        executor = create_default_executor(workspace_root=temp_workspace)
        result = executor.execute_plan(plan)

        assert result.overall_status == StepStatus.SUCCESS
        assert result.traces[0].outputs["content"] == "Hello, world!"
