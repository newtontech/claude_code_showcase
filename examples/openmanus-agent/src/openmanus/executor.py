"""Executor for running plans and tracking results."""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from openmanus.config import get_settings
from openmanus.models.plan import Plan, Step
from openmanus.models.trace import ExecutionResult, StepStatus, TraceEntry
from openmanus.tools.base import Tool, ToolRegistry, reset_global_registry


class Executor:
    """Executes plans and tracks results.

    The executor is responsible for:
    - Resolving step references (e.g., "ref:step:1.output")
    - Executing steps sequentially
    - Tracking execution traces
    - Saving plans and results to disk
    """

    def __init__(
        self,
        tool_registry: ToolRegistry | None = None,
        workspace_root: str | None = None,
    ) -> None:
        """Initialize the executor.

        Args:
            tool_registry: Registry of available tools. If None, creates a new one.
            workspace_root: Root directory for execution. If None, uses settings.
        """
        settings = get_settings()
        self.workspace_root = Path(workspace_root or settings.workspace_root).resolve()
        self.runs_dir = Path(settings.runs_dir).resolve()
        self.runs_dir.mkdir(parents=True, exist_ok=True)

        self.tool_registry = tool_registry or ToolRegistry()
        self._step_outputs: dict[str, Any] = {}

    @property
    def name(self) -> str:
        """Return the name of this executor."""
        return "executor"

    def execute_plan(
        self,
        plan: Plan,
        dry_run: bool = False,
    ) -> ExecutionResult:
        """Execute a plan and return the result.

        Args:
            plan: The plan to execute
            dry_run: If True, only simulate execution without actually running tools

        Returns:
            ExecutionResult with traces and status
        """
        # Create execution result
        result = ExecutionResult(
            plan_goal=plan.goal,
            plan_risk_level=plan.risk_level.value,
            workspace_root=str(self.workspace_root),
            total_steps=len(plan.steps),
            successful_steps=0,
            failed_steps=0,
            skipped_steps=0,
            overall_status=StepStatus.PENDING,
            start_time=datetime.now().isoformat(),
        )

        # Save the plan
        run_dir = self._save_plan(plan)

        # Execute each step
        for i, step in enumerate(plan.steps):
            trace = TraceEntry(
                step_id=step.id,
                tool=step.tool,
                inputs_digest=self._make_digest(step.inputs),
                inputs=step.inputs.copy(),
            )
            result.add_trace(trace)

            if dry_run:
                trace.mark_success({"dry_run": True})
                self._step_outputs[step.id] = {"dry_run": True}
                continue

            # Execute the step
            try:
                # Resolve references in inputs
                resolved_inputs = self._resolve_inputs(step.inputs)

                # Get the tool
                tool = self.tool_registry.get(step.tool)
                if tool is None:
                    raise ValueError(f"Tool '{step.tool}' not found in registry")

                # Execute
                trace.mark_started()
                output = tool.execute(resolved_inputs)

                # Store output for reference resolution
                self._step_outputs[step.id] = output.data

                if output.success:
                    trace.mark_success(output.data or {})

                    # Track produced files
                    if output.data and isinstance(output.data, dict):
                        if "path" in output.data:
                            result.produced_files.append(output.data["path"])
                else:
                    trace.mark_failure(output.error or "Unknown error")
                    # Stop on failure
                    break

            except Exception as e:
                trace.mark_failure(str(e))
                # Stop on failure
                break

        # Finalize the result
        result.finalize()

        # Save traces
        self._save_traces(run_dir, result)

        return result

    def _resolve_inputs(self, inputs: dict) -> dict:
        """Resolve references in inputs.

        Args:
            inputs: Input dict that may contain references like "ref:step:1.output"

        Returns:
            Resolved inputs dict
        """
        resolved = {}

        for key, value in inputs.items():
            if isinstance(value, str):
                # Check for reference pattern: ref:step:<id>.output or ref:step:<id>
                if value.startswith("ref:step:"):
                    ref_key = value
                    # Extract step ID
                    parts = ref_key.split(":")
                    if len(parts) >= 3:
                        step_id = parts[2]
                        # Get the output from that step
                        if step_id in self._step_outputs:
                            step_output = self._step_outputs[step_id]
                            # If output is a dict with a 'content' key, use that
                            if isinstance(step_output, dict) and "content" in step_output:
                                resolved[key] = step_output["content"]
                            else:
                                resolved[key] = step_output
                        else:
                            # Reference to step that hasn't executed yet
                            resolved[key] = value
                    else:
                        resolved[key] = value
                else:
                    resolved[key] = value
            elif isinstance(value, dict):
                # Recursively resolve nested dicts
                resolved[key] = self._resolve_inputs(value)
            elif isinstance(value, list):
                # Resolve lists
                resolved[key] = [
                    self._resolve_inputs({k: v})["k"] if isinstance(v, dict) else v
                    for v in value
                ]
            else:
                resolved[key] = value

        return resolved

    def _make_digest(self, data: Any) -> str:
        """Create a digest/hash of data for trace identification.

        Args:
            data: Data to hash

        Returns:
            Hex digest string
        """
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()[:16]

    def _save_plan(self, plan: Plan) -> Path:
        """Save plan to disk.

        Args:
            plan: The plan to save

        Returns:
            Path to the run directory
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_dir = self.runs_dir / timestamp
        run_dir.mkdir(parents=True, exist_ok=True)

        plan_file = run_dir / "plan.json"
        plan_file.write_text(plan.model_dump_json(indent=2), encoding="utf-8")

        return run_dir

    def _save_traces(self, run_dir: Path, result: ExecutionResult) -> None:
        """Save traces to disk as JSONL.

        Args:
            run_dir: Directory to save traces to
            result: Execution result containing traces
        """
        trace_file = run_dir / "trace.jsonl"

        with trace_file.open("w", encoding="utf-8") as f:
            for trace in result.traces:
                f.write(trace.model_dump_json() + "\n")

        # Also save the result summary
        summary_file = run_dir / "result.json"
        summary_file.write_text(result.model_dump_json(indent=2), encoding="utf-8")

    def load_plan(self, plan_path: Path) -> Plan:
        """Load a plan from disk.

        Args:
            plan_path: Path to the plan.json file

        Returns:
            The loaded Plan

        Raises:
            ValueError: If the file cannot be loaded or parsed
        """
        try:
            content = plan_path.read_text(encoding="utf-8")
            return Plan.model_validate_json(content)
        except Exception as e:
            raise ValueError(f"Failed to load plan from {plan_path}: {e}")

    def load_trace(self, trace_dir: Path) -> ExecutionResult:
        """Load a trace from disk.

        Args:
            trace_dir: Directory containing trace.jsonl

        Returns:
            The loaded ExecutionResult

        Raises:
            ValueError: If the file cannot be loaded or parsed
        """
        try:
            result_file = trace_dir / "result.json"
            content = result_file.read_text(encoding="utf-8")
            return ExecutionResult.model_validate_json(content)
        except Exception as e:
            raise ValueError(f"Failed to load trace from {trace_dir}: {e}")


def create_default_executor(workspace_root: str | None = None) -> Executor:
    """Create an executor with default tools registered.

    Args:
        workspace_root: Root directory for execution

    Returns:
        Executor with FileTool and ShellTool registered
    """
    from openmanus.tools.file_tool import FileTool
    from openmanus.tools.shell_tool import ShellTool

    reset_global_registry()
    executor = Executor(workspace_root=workspace_root)
    executor.tool_registry.register(FileTool(workspace_root=workspace_root))
    executor.tool_registry.register(ShellTool())

    return executor
