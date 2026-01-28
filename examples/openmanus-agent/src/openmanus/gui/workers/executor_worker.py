"""Worker thread for plan execution."""

from PyQt6.QtCore import QThread, pyqtSignal

from openmanus.models.plan import Plan
from openmanus.models.trace import ExecutionResult, TraceEntry


class ExecutorWorker(QThread):
    """Background worker for executing plans.

    This worker runs the executor in a separate thread to prevent
    blocking the UI during plan execution.
    """

    # Signals
    started = pyqtSignal()
    progress = pyqtSignal(int, int, str)  # current, total, message
    step_started = pyqtSignal(object)  # TraceEntry
    step_complete = pyqtSignal(object)  # TraceEntry
    finished = pyqtSignal(object)  # ExecutionResult
    error = pyqtSignal(str)  # Error message

    def __init__(self, executor, plan: Plan, dry_run: bool = False):
        """Initialize the executor worker.

        Args:
            executor: Executor instance
            plan: Plan to execute
            dry_run: If True, only simulate execution
        """
        super().__init__()
        self.executor = executor
        self.plan = plan
        self.dry_run = dry_run

    def run(self) -> None:
        """Execute plan in background thread.

        Emits:
            started: When execution begins
            progress: With current step, total steps, and message
            step_started: When a step begins execution
            step_complete: When a step completes
            finished: With the ExecutionResult
            error: If execution fails
        """
        try:
            self.started.emit()
            total_steps = len(self.plan.steps)

            for i, step in enumerate(self.plan.steps, 1):
                self.progress.emit(i, total_steps, f"执行步骤 {i}: {step.description}")

                # For real-time updates, we need to hook into the executor
                # This is a simplified version - the full implementation
                # would integrate more deeply with the executor

            # Execute the plan
            result = self.executor.execute_plan(self.plan, dry_run=self.dry_run)

            # Emit step completion signals for each trace
            for trace in result.traces:
                if trace.status.value in ("success", "failure"):
                    self.step_complete.emit(trace)

            self.finished.emit(result)

        except Exception as e:
            self.error.emit(f"执行计划时发生错误: {e}")
