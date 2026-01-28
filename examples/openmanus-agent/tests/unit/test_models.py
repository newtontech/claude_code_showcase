"""Unit tests for data models."""

import json

import pytest

from openmanus.models.plan import Plan, RiskLevel, Step
from openmanus.models.trace import ExecutionResult, StepStatus, TraceEntry


class TestStep:
    """Tests for Step model."""

    def test_create_step(self) -> None:
        """Test creating a basic step."""
        step = Step(
            id="1",
            description="Read a file",
            tool="file",
            inputs={"action": "read_text", "path": "data/test.txt"},
        )
        assert step.id == "1"
        assert step.tool == "file"
        assert step.inputs["action"] == "read_text"
        assert step.produces is None

    def test_create_step_with_produces(self) -> None:
        """Test creating a step that produces output."""
        step = Step(
            id="2",
            description="Write summary",
            tool="file",
            inputs={"action": "write_text", "path": "out/summary.md"},
            produces="file:out/summary.md",
        )
        assert step.produces == "file:out/summary.md"

    def test_step_serialization(self) -> None:
        """Test step can be serialized to JSON."""
        step = Step(
            id="1",
            description="Read a file",
            tool="file",
            inputs={"action": "read_text", "path": "data/test.txt"},
        )
        json_str = step.model_dump_json()
        data = json.loads(json_str)
        assert data["id"] == "1"
        assert data["tool"] == "file"

    def test_step_deserialization(self) -> None:
        """Test step can be deserialized from JSON."""
        json_str = '{"id":"1","description":"Read","tool":"file","inputs":{"path":"test.txt"}}'
        step = Step.model_validate_json(json_str)
        assert step.id == "1"
        assert step.tool == "file"


class TestPlan:
    """Tests for Plan model."""

    def test_create_plan_low_risk(self) -> None:
        """Test creating a low-risk plan."""
        plan = Plan(
            goal="Read and summarize a file",
            risk_level=RiskLevel.LOW,
            workspace_root="/tmp/test",
            steps=[
                Step(
                    id="1",
                    description="Read file",
                    tool="file",
                    inputs={"action": "read_text", "path": "data/test.txt"},
                )
            ],
            success_criteria=["File exists", "Summary created"],
        )
        assert plan.risk_level == RiskLevel.LOW
        assert len(plan.steps) == 1
        assert plan.workspace_root == "/tmp/test"

    def test_create_plan_high_risk(self) -> None:
        """Test creating a high-risk plan."""
        plan = Plan(
            goal="Delete all files",
            risk_level=RiskLevel.HIGH,
            workspace_root="/tmp/test",
            steps=[
                Step(
                    id="1",
                    description="Delete files",
                    tool="shell",
                    inputs={"cmd": "rm -rf /tmp/test/*"},
                )
            ],
            success_criteria=["All files deleted"],
        )
        assert plan.risk_level == RiskLevel.HIGH

    def test_plan_serialization(self) -> None:
        """Test plan can be serialized to JSON."""
        plan = Plan(
            goal="Test plan",
            risk_level=RiskLevel.LOW,
            workspace_root="/tmp/test",
            steps=[
                Step(
                    id="1",
                    description="Test step",
                    tool="file",
                    inputs={"path": "test.txt"},
                )
            ],
            success_criteria=["Success"],
        )
        json_str = plan.model_dump_json()
        data = json.loads(json_str)
        assert data["goal"] == "Test plan"
        assert data["risk_level"] == "LOW"

    def test_plan_deserialization(self) -> None:
        """Test plan can be deserialized from JSON."""
        json_str = """
        {
            "goal": "Test plan",
            "risk_level": "LOW",
            "workspace_root": "/tmp/test",
            "steps": [
                {
                    "id": "1",
                    "description": "Test step",
                    "tool": "file",
                    "inputs": {"path": "test.txt"}
                }
            ],
            "success_criteria": ["Success"],
            "created_at": "2025-01-25T12:00:00"
        }
        """
        plan = Plan.model_validate_json(json_str)
        assert plan.goal == "Test plan"
        assert len(plan.steps) == 1

    def test_get_step_by_id(self) -> None:
        """Test retrieving a step by ID."""
        step1 = Step(id="1", description="First", tool="file", inputs={})
        step2 = Step(id="2", description="Second", tool="shell", inputs={})
        plan = Plan(
            goal="Test",
            risk_level=RiskLevel.LOW,
            workspace_root="/tmp",
            steps=[step1, step2],
            success_criteria=[],
        )
        assert plan.get_step_by_id("1") is step1
        assert plan.get_step_by_id("2") is step2
        assert plan.get_step_by_id("3") is None

    def test_get_max_step_id(self) -> None:
        """Test getting the maximum step ID."""
        steps = [
            Step(id="1", description="First", tool="file", inputs={}),
            Step(id="3", description="Third", tool="shell", inputs={}),
            Step(id="2", description="Second", tool="file", inputs={}),
        ]
        plan = Plan(
            goal="Test",
            risk_level=RiskLevel.LOW,
            workspace_root="/tmp",
            steps=steps,
            success_criteria=[],
        )
        assert plan.get_max_step_id() == "3"

    def test_get_max_step_id_empty(self) -> None:
        """Test getting max step ID with no steps."""
        plan = Plan(
            goal="Test",
            risk_level=RiskLevel.LOW,
            workspace_root="/tmp",
            steps=[],
            success_criteria=[],
        )
        assert plan.get_max_step_id() == "0"


class TestTraceEntry:
    """Tests for TraceEntry model."""

    def test_create_trace_entry(self) -> None:
        """Test creating a trace entry."""
        trace = TraceEntry(
            step_id="1",
            tool="file",
            inputs_digest="read_text:data/test.txt",
            inputs={"action": "read_text", "path": "data/test.txt"},
        )
        assert trace.step_id == "1"
        assert trace.tool == "file"
        assert trace.status == StepStatus.PENDING
        assert trace.error is None

    def test_mark_started(self) -> None:
        """Test marking a trace as started."""
        trace = TraceEntry(
            step_id="1",
            tool="file",
            inputs_digest="test",
            inputs={},
        )
        trace.mark_started()
        assert trace.status == StepStatus.RUNNING
        assert trace.start_time is not None

    def test_mark_success(self) -> None:
        """Test marking a trace as successful."""
        trace = TraceEntry(
            step_id="1",
            tool="file",
            inputs_digest="test",
            inputs={},
        )
        trace.mark_success({"content": "Hello world"})
        assert trace.status == StepStatus.SUCCESS
        assert trace.end_time is not None
        assert trace.outputs == {"content": "Hello world"}

    def test_mark_failure(self) -> None:
        """Test marking a trace as failed."""
        trace = TraceEntry(
            step_id="1",
            tool="file",
            inputs_digest="test",
            inputs={},
        )
        trace.mark_failure("File not found")
        assert trace.status == StepStatus.FAILURE
        assert trace.end_time is not None
        assert trace.error == "File not found"

    def test_duration_calculation(self) -> None:
        """Test calculating execution duration."""
        trace = TraceEntry(
            step_id="1",
            tool="file",
            inputs_digest="test",
            start_time="2025-01-25T12:00:00",
            end_time="2025-01-25T12:00:01",
            inputs={},
        )
        assert trace.duration_ms == 1000

    def test_duration_none(self) -> None:
        """Test duration calculation when end_time is None."""
        trace = TraceEntry(
            step_id="1",
            tool="file",
            inputs_digest="test",
            start_time="2025-01-25T12:00:00",
            inputs={},
        )
        assert trace.duration_ms is None


class TestExecutionResult:
    """Tests for ExecutionResult model."""

    def test_create_execution_result(self) -> None:
        """Test creating an execution result."""
        result = ExecutionResult(
            plan_goal="Test goal",
            plan_risk_level="LOW",
            workspace_root="/tmp/test",
            total_steps=3,
            successful_steps=3,
            failed_steps=0,
            skipped_steps=0,
            overall_status=StepStatus.SUCCESS,
            start_time="2025-01-25T12:00:00",
        )
        assert result.plan_goal == "Test goal"
        assert result.total_steps == 3
        assert result.successful_steps == 3
        assert result.overall_status == StepStatus.SUCCESS

    def test_success_rate(self) -> None:
        """Test calculating success rate."""
        result = ExecutionResult(
            plan_goal="Test",
            plan_risk_level="LOW",
            workspace_root="/tmp",
            total_steps=4,
            successful_steps=3,
            failed_steps=1,
            skipped_steps=0,
            overall_status=StepStatus.FAILURE,
            start_time="2025-01-25T12:00:00",
        )
        assert result.success_rate == 75.0

    def test_add_trace(self) -> None:
        """Test adding a trace entry."""
        result = ExecutionResult(
            plan_goal="Test",
            plan_risk_level="LOW",
            workspace_root="/tmp",
            total_steps=1,
            successful_steps=0,
            failed_steps=0,
            skipped_steps=0,
            overall_status=StepStatus.PENDING,
            start_time="2025-01-25T12:00:00",
        )
        trace = TraceEntry(step_id="1", tool="file", inputs_digest="test", inputs={})
        result.add_trace(trace)
        assert len(result.traces) == 1

    def test_finalize_success(self) -> None:
        """Test finalizing a successful execution."""
        result = ExecutionResult(
            plan_goal="Test",
            plan_risk_level="LOW",
            workspace_root="/tmp",
            total_steps=2,
            successful_steps=0,
            failed_steps=0,
            skipped_steps=0,
            overall_status=StepStatus.PENDING,
            start_time="2025-01-25T12:00:00",
        )
        result.traces = [
            TraceEntry(
                step_id="1",
                tool="file",
                inputs_digest="test",
                status=StepStatus.SUCCESS,
                start_time="2025-01-25T12:00:00",
                end_time="2025-01-25T12:00:01",
                inputs={},
            ),
            TraceEntry(
                step_id="2",
                tool="file",
                inputs_digest="test",
                status=StepStatus.SUCCESS,
                start_time="2025-01-25T12:00:01",
                end_time="2025-01-25T12:00:02",
                inputs={},
            ),
        ]
        result.finalize()
        assert result.successful_steps == 2
        assert result.failed_steps == 0
        assert result.overall_status == StepStatus.SUCCESS
        assert result.end_time is not None

    def test_finalize_failure(self) -> None:
        """Test finalizing a failed execution."""
        result = ExecutionResult(
            plan_goal="Test",
            plan_risk_level="LOW",
            workspace_root="/tmp",
            total_steps=2,
            successful_steps=0,
            failed_steps=0,
            skipped_steps=0,
            overall_status=StepStatus.PENDING,
            start_time="2025-01-25T12:00:00",
        )
        result.traces = [
            TraceEntry(
                step_id="1",
                tool="file",
                inputs_digest="test",
                status=StepStatus.SUCCESS,
                start_time="2025-01-25T12:00:00",
                end_time="2025-01-25T12:00:01",
                inputs={},
            ),
            TraceEntry(
                step_id="2",
                tool="file",
                inputs_digest="test",
                status=StepStatus.FAILURE,
                start_time="2025-01-25T12:00:01",
                end_time="2025-01-25T12:00:02",
                error="File not found",
                inputs={},
            ),
        ]
        result.finalize()
        assert result.successful_steps == 1
        assert result.failed_steps == 1
        assert result.overall_status == StepStatus.FAILURE

    def test_duration_calculation(self) -> None:
        """Test calculating execution duration."""
        result = ExecutionResult(
            plan_goal="Test",
            plan_risk_level="LOW",
            workspace_root="/tmp",
            total_steps=1,
            successful_steps=1,
            failed_steps=0,
            skipped_steps=0,
            overall_status=StepStatus.SUCCESS,
            start_time="2025-01-25T12:00:00",
            end_time="2025-01-25T12:00:05",
        )
        assert result.duration_ms == 5000
