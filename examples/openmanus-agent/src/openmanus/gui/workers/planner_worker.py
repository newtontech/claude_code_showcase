"""Worker thread for plan generation."""

from PyQt6.QtCore import QThread, pyqtSignal

from openmanus.models.plan import Plan
from openmanus.planner.base import PlanningError


class PlannerWorker(QThread):
    """Background worker for generating plans.

    This worker runs the planner in a separate thread to prevent
    blocking the UI during LLM API calls.
    """

    # Signals
    started = pyqtSignal()
    progress = pyqtSignal(str)  # Progress message
    finished = pyqtSignal(object)  # Plan object
    error = pyqtSignal(str)  # Error message

    def __init__(self, planner, goal: str, workspace_root: str):
        """Initialize the planner worker.

        Args:
            planner: Planner instance (LLMPlanner or MockPlanner)
            goal: User's task description
            workspace_root: Root directory for operations
        """
        super().__init__()
        self.planner = planner
        self.goal = goal
        self.workspace_root = workspace_root

    def run(self) -> None:
        """Execute plan generation in background thread.

        Emits:
            started: When generation begins
            progress: With status updates
            finished: With the generated Plan
            error: If generation fails
        """
        try:
            self.started.emit()
            self.progress.emit("正在生成计划...")

            # Generate the plan
            plan = self.planner.generate_plan(self.goal, self.workspace_root)

            self.progress.emit("计划生成完成")
            self.finished.emit(plan)

        except PlanningError as e:
            self.error.emit(f"计划生成失败: {e}")
        except Exception as e:
            self.error.emit(f"生成计划时发生错误: {e}")
