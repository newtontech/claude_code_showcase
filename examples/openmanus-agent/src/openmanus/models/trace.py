"""Trace and ExecutionResult models for tracking execution."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class StepStatus(str, Enum):
    """Status of a step execution."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"


class TraceEntry(BaseModel):
    """A single trace entry recording the execution of a step.

    Each entry contains all information needed to reproduce and debug
    the execution of a single step.
    """

    step_id: str = Field(..., description="ID of the step that was executed")
    tool: str = Field(..., description="Name of the tool that was invoked")
    inputs_digest: str = Field(..., description="Hash/summary of inputs (for reproducibility)")
    output_digest: str | None = Field(
        default=None,
        description="Hash/summary of outputs (for reproducibility)",
    )
    start_time: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="ISO timestamp when execution started",
    )
    end_time: str | None = Field(default=None, description="ISO timestamp when execution ended")
    status: StepStatus = Field(
        default=StepStatus.PENDING,
        description="Execution status",
    )
    error: str | None = Field(default=None, description="Error message if execution failed")
    inputs: dict = Field(
        default_factory=dict,
        description="Actual inputs passed to the tool (after ref resolution)",
    )
    outputs: dict | None = Field(
        default=None,
        description="Actual outputs returned by the tool",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "step_id": "1",
                    "tool": "file",
                    "inputs_digest": "read_text:data/notes.txt",
                    "output_digest": "content:1234 chars",
                    "start_time": "2025-01-25T12:00:00",
                    "end_time": "2025-01-25T12:00:01",
                    "status": "success",
                    "error": None,
                    "inputs": {"action": "read_text", "path": "data/notes.txt"},
                    "outputs": {"content": "This is the file content..."},
                }
            ]
        }
    )

    @property
    def duration_ms(self) -> int | None:
        """Calculate execution duration in milliseconds."""
        if self.end_time is None:
            return None
        try:
            start = datetime.fromisoformat(self.start_time)
            end = datetime.fromisoformat(self.end_time)
            return int((end - start).total_seconds() * 1000)
        except (ValueError, TypeError):
            return None

    def mark_started(self) -> None:
        """Mark the step as started."""
        self.status = StepStatus.RUNNING
        self.start_time = datetime.now().isoformat()

    def mark_success(self, outputs: dict) -> None:
        """Mark the step as successful."""
        self.status = StepStatus.SUCCESS
        self.end_time = datetime.now().isoformat()
        self.outputs = outputs

    def mark_failure(self, error: str) -> None:
        """Mark the step as failed."""
        self.status = StepStatus.FAILURE
        self.end_time = datetime.now().isoformat()
        self.error = error


class ExecutionResult(BaseModel):
    """Result of executing a complete plan.

    Contains summary information about the execution and
    references to detailed trace entries.
    """

    plan_goal: str = Field(..., description="The original goal from the plan")
    plan_risk_level: str = Field(..., description="Risk level of the executed plan")
    workspace_root: str = Field(..., description="Workspace root path")
    total_steps: int = Field(..., description="Total number of steps in the plan")
    successful_steps: int = Field(..., description="Number of successfully executed steps")
    failed_steps: int = Field(..., description="Number of failed steps")
    skipped_steps: int = Field(..., description="Number of skipped steps")
    overall_status: StepStatus = Field(..., description="Overall execution status")
    start_time: str = Field(..., description="ISO timestamp when execution started")
    end_time: str | None = Field(default=None, description="ISO timestamp when execution ended")
    traces: list[TraceEntry] = Field(
        default_factory=list,
        description="List of trace entries for each executed step",
    )
    error_summary: str | None = Field(
        default=None,
        description="Summary of errors if execution failed",
    )
    produced_files: list[str] = Field(
        default_factory=list,
        description="List of files produced during execution",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "plan_goal": "Summarize notes.txt",
                    "plan_risk_level": "LOW",
                    "workspace_root": "/Users/user/project",
                    "total_steps": 3,
                    "successful_steps": 3,
                    "failed_steps": 0,
                    "skipped_steps": 0,
                    "overall_status": "success",
                    "start_time": "2025-01-25T12:00:00",
                    "end_time": "2025-01-25T12:00:05",
                    "traces": [],
                    "error_summary": None,
                    "produced_files": ["out/summary.md"],
                }
            ]
        }
    )

    @property
    def duration_ms(self) -> int | None:
        """Calculate total execution duration in milliseconds."""
        if self.end_time is None:
            return None
        try:
            start = datetime.fromisoformat(self.start_time)
            end = datetime.fromisoformat(self.end_time)
            return int((end - start).total_seconds() * 1000)
        except (ValueError, TypeError):
            return None

    @property
    def success_rate(self) -> float:
        """Calculate success rate as a percentage."""
        if self.total_steps == 0:
            return 0.0
        return (self.successful_steps / self.total_steps) * 100

    def add_trace(self, trace: TraceEntry) -> None:
        """Add a trace entry to the result."""
        self.traces.append(trace)

    def finalize(self) -> None:
        """Finalize the execution result."""
        self.end_time = datetime.now().isoformat()
        self.failed_steps = sum(1 for t in self.traces if t.status == StepStatus.FAILURE)
        self.successful_steps = sum(1 for t in self.traces if t.status == StepStatus.SUCCESS)
        self.skipped_steps = sum(1 for t in self.traces if t.status == StepStatus.SKIPPED)

        if self.failed_steps > 0:
            self.overall_status = StepStatus.FAILURE
        elif self.successful_steps == self.total_steps:
            self.overall_status = StepStatus.SUCCESS
        else:
            self.overall_status = StepStatus.PENDING
