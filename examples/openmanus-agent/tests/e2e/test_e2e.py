"""End-to-end tests for OpenManus.

These tests use the MockPlanner to ensure deterministic behavior without
requiring real LLM API calls.
"""

import json
import tempfile
from pathlib import Path

import pytest

from openmanus.executor import create_default_executor
from openmanus.models.plan import RiskLevel
from openmanus.planner.mock_planner import MockPlanner
from openmanus.tools.base import reset_global_registry


@pytest.fixture
def e2e_workspace():
    """Create a temporary workspace for E2E tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        # Create test data directory
        (workspace / "data").mkdir()
        (workspace / "data" / "notes.txt").write_text(
            "This is a test file.\nIt has multiple lines.\nAnd three key points."
        )
        yield workspace


@pytest.fixture(autouse=True)
def reset_state():
    """Reset global state before each test."""
    reset_global_registry()
    yield
    reset_global_registry()


def test_case_a_file_summarization(e2e_workspace: Path) -> None:
    """Case A: File summarization - reads notes.txt and writes summary.md"""
    # Given: workspace/data/notes.txt exists
    notes_file = e2e_workspace / "data" / "notes.txt"
    assert notes_file.exists()

    # When: execute summarization task
    planner = MockPlanner()
    plan = planner.generate_plan(
        goal="把 data/notes.txt 总结成 3 条要点，写到 out/summary.md",
        workspace_root=str(e2e_workspace),
    )

    executor = create_default_executor(workspace_root=str(e2e_workspace))
    result = executor.execute_plan(plan)

    # Then:
    # 1. out/summary.md exists
    summary_file = e2e_workspace / "out" / "summary.md"
    assert summary_file.exists(), "Summary file should exist"

    # 2. File contains 3 bullet points starting with '-'
    content = summary_file.read_text()
    lines = [line.strip() for line in content.split("\n") if line.strip()]
    bullet_lines = [line for line in lines if line.startswith("-")]
    assert len(bullet_lines) == 3, f"Should have 3 bullet points, got {len(bullet_lines)}"

    # 3. trace shows all steps successful
    assert result.overall_status == "success"
    assert result.successful_steps == len(plan.steps)
    assert result.failed_steps == 0


def test_case_b_dry_run(e2e_workspace: Path) -> None:
    """Case B: dry-run - only generate plan without executing"""
    # Given: workspace exists
    planner = MockPlanner()
    plan = planner.generate_plan(
        goal="把 data/notes.txt 总结成 3 条要点",
        workspace_root=str(e2e_workspace),
    )

    executor = create_default_executor(workspace_root=str(e2e_workspace))

    # When: execute with dry_run=True
    result = executor.execute_plan(plan, dry_run=True)

    # Then:
    # 1. out/summary.md should NOT exist
    summary_file = e2e_workspace / "out" / "summary.md"
    assert not summary_file.exists(), "Summary file should not exist in dry run"

    # 2. Plan should still be saved
    runs = list(executor.runs_dir.glob("*"))
    assert len(runs) > 0, "Plan should be saved"

    # 3. Trace should show dry_run
    assert result.traces[0].outputs.get("dry_run") is True


def test_case_c_dangerous_command_rejection(e2e_workspace: Path) -> None:
    """Case C: Dangerous command - shell tool should reject dangerous commands"""
    # Given: workspace exists
    planner = MockPlanner()
    plan = planner.generate_plan(
        goal="删除 workspace 下所有文件（用 rm -rf）",
        workspace_root=str(e2e_workspace),
    )

    # Then: Plan should be marked as HIGH risk
    assert plan.risk_level == RiskLevel.HIGH

    executor = create_default_executor(workspace_root=str(e2e_workspace))

    # When: execute the plan
    result = executor.execute_plan(plan)

    # Then:
    # 1. Execution should fail (shell tool rejects rm command)
    assert result.overall_status == "failure"

    # 2. Trace should show rejection reason
    failed_trace = [t for t in result.traces if t.status == "failure"][0]
    assert failed_trace.error is not None
    assert "not allowed" in failed_trace.error.lower() or "not in the allowed list" in failed_trace.error.lower()

    # 3. Files should still exist (not deleted)
    notes_file = e2e_workspace / "data" / "notes.txt"
    assert notes_file.exists(), "Files should not be deleted"


def test_case_d_plan_persistence(e2e_workspace: Path) -> None:
    """Case D: Plan can be saved and loaded"""
    # Given: a plan is generated
    planner = MockPlanner()
    original_plan = planner.generate_plan(
        goal="test plan",
        workspace_root=str(e2e_workspace),
    )

    executor = create_default_executor(workspace_root=str(e2e_workspace))

    # When: save and load the plan
    run_dir = executor._save_plan(original_plan)
    plan_file = run_dir / "plan.json"
    loaded_plan = executor.load_plan(plan_file)

    # Then: plans should match
    assert loaded_plan.goal == original_plan.goal
    assert loaded_plan.risk_level == original_plan.risk_level
    assert len(loaded_plan.steps) == len(original_plan.steps)
    for i, step in enumerate(original_plan.steps):
        assert loaded_plan.steps[i].id == step.id
        assert loaded_plan.steps[i].description == step.description
        assert loaded_plan.steps[i].tool == step.tool


def test_case_e_trace_persistence(e2e_workspace: Path) -> None:
    """Case E: Trace can be saved and loaded"""
    # Given: a plan is executed
    planner = MockPlanner()
    # Use a unique goal that won't match other patterns - use a word without "summarize"/"test"
    plan = planner.generate_plan(
        goal="xyz123 persistence check",
        workspace_root=str(e2e_workspace),
    )

    executor = create_default_executor(workspace_root=str(e2e_workspace))
    result = executor.execute_plan(plan)

    # The plan goal should be preserved in the result
    assert result.plan_goal == "xyz123 persistence check"

    # Find the run directory (use the most recent one)
    runs = sorted(executor.runs_dir.glob("*"))
    assert len(runs) > 0
    run_dir = runs[-1]

    # When: load the trace
    loaded_result = executor.load_trace(run_dir)

    # Then: results should match
    assert loaded_result.plan_goal == result.plan_goal
    assert loaded_result.total_steps == result.total_steps
    assert loaded_result.successful_steps == result.successful_steps
    assert loaded_result.failed_steps == result.failed_steps


def test_case_f_step_reference_resolution(e2e_workspace: Path) -> None:
    """Case F: Step outputs can be referenced in subsequent steps"""
    # Given: input.txt exists
    (e2e_workspace / "input.txt").write_text("Hello, World!")

    # Use the summarization flow which tests reference resolution
    (e2e_workspace / "data" / "notes.txt").write_text("Test content for summary")

    planner = MockPlanner()
    # The summarization plan reads and writes, testing basic execution
    plan = planner.generate_plan(
        goal="总结 data/notes.txt 并写入 out/summary.md",
        workspace_root=str(e2e_workspace),
    )

    executor = create_default_executor(workspace_root=str(e2e_workspace))
    result = executor.execute_plan(plan)

    # Then: execution should succeed
    assert result.overall_status == "success"
    assert result.successful_steps == len(plan.steps)


def test_case_g_failure_stops_execution(e2e_workspace: Path) -> None:
    """Case G: Execution stops on first failure"""
    # Given: a plan with a step that will fail
    plan = planner = MockPlanner().generate_plan(
        goal="Read non-existent file",
        workspace_root=str(e2e_workspace),
    )

    executor = create_default_executor(workspace_root=str(e2e_workspace))
    result = executor.execute_plan(plan)

    # Then:
    # 1. Overall status should be failure
    assert result.overall_status == "failure"

    # 2. At least one step should have failed
    assert result.failed_steps > 0

    # 3. Successful steps should be less than total
    assert result.successful_steps < result.total_steps
