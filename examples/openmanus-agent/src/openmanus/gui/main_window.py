"""Main window for OpenManus GUI application."""

from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from openmanus.config import get_settings
from openmanus.executor import create_default_executor
from openmanus.gui.widgets.task_input import TaskInputWidget
from openmanus.gui.widgets.plan_display import PlanDisplayWidget
from openmanus.gui.widgets.confirm_dialog import PlanConfirmDialog
from openmanus.models.plan import Plan, RiskLevel
from openmanus.planner.llm_planner import LLMPlanner
from openmanus.planner.mock_planner import MockPlanner
from openmanus.gui.workers.planner_worker import PlannerWorker


class MainWindow(QMainWindow):
    """Main application window for OpenManus GUI.

    This window provides the main interface for:
    - Inputting task descriptions
    - Viewing generated plans
    - Confirming and executing plans
    - Viewing execution results
    """

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        self.settings = get_settings()
        self.executor = create_default_executor()
        self.planner = None
        self.current_plan = None
        self.planner_worker = None

        self._setup_ui()
        self._setup_planner()
        self._load_stylesheet()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("OpenManus - macOS 本地助手")
        self.setMinimumSize(800, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # Header
        header = self._create_header()
        main_layout.addWidget(header)

        # Task input widget
        self.task_input = TaskInputWidget()
        self.task_input.generate_requested.connect(self._on_generate_plan)
        main_layout.addWidget(self.task_input)

        # Plan display widget
        self.plan_display = PlanDisplayWidget()
        main_layout.addWidget(self.plan_display, 1)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪 - 请输入任务描述")

    def _create_header(self) -> QWidget:
        """Create the header widget.

        Returns:
            Header widget
        """
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title
        title = QLabel("OpenManus")
        title.setObjectName("heading")
        layout.addWidget(title)

        layout.addStretch()

        # Mode indicator
        self.mode_label = QLabel()
        self._update_mode_label()
        layout.addWidget(self.mode_label)

        return header

    def _update_mode_label(self) -> None:
        """Update the mode label based on current planner type."""
        if isinstance(self.planner, MockPlanner):
            mode = "模拟模式"
            color = "#30d158"
        else:
            mode = "LLM 模式"
            color = "#007aff"

        self.mode_label.setText(f"● {mode}")
        self.mode_label.setStyleSheet(f"color: {color}; font-size: 12px;")

    def _setup_planner(self) -> None:
        """Set up the planner.

        Tries to initialize LLMPlanner, falls back to MockPlanner if API key is missing.
        """
        try:
            self.planner = LLMPlanner()
        except Exception as e:
            # Fall back to mock planner
            self.planner = MockPlanner()
            self.status_bar.showMessage(f"使用模拟模式 (未配置 API key): {e}")

        self._update_mode_label()

    def _load_stylesheet(self) -> None:
        """Load and apply the application stylesheet."""
        style_path = Path(__file__).parent / "resources" / "styles.qss"
        if style_path.exists():
            with open(style_path, encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def _on_generate_plan(self, task_description: str) -> None:
        """Handle generate plan request.

        Args:
            task_description: The task description from the input widget
        """
        # Disable input during generation
        self.task_input.set_enabled(False)
        self.status_bar.showMessage("正在生成计划...")

        # Create and start planner worker
        self.planner_worker = PlannerWorker(
            self.planner,
            task_description,
            str(self.settings.workspace_root),
        )
        self.planner_worker.started.connect(self._on_plan_generation_started)
        self.planner_worker.progress.connect(self._on_plan_progress)
        self.planner_worker.finished.connect(self._on_plan_generated)
        self.planner_worker.error.connect(self._on_plan_error)
        self.planner_worker.start()

    def _on_plan_generation_started(self) -> None:
        """Handle plan generation started event."""
        self.status_bar.showMessage("正在生成计划...")

    def _on_plan_progress(self, message: str) -> None:
        """Handle plan generation progress event.

        Args:
            message: Progress message
        """
        self.status_bar.showMessage(message)

    def _on_plan_generated(self, plan: Plan) -> None:
        """Handle successful plan generation.

        Args:
            plan: The generated plan
        """
        self.current_plan = plan
        self.task_input.set_enabled(True)

        # Display the plan
        self.plan_display.set_plan(plan)

        # Show confirmation dialog
        self._show_plan_confirmation(plan)

        self.status_bar.showMessage("计划已生成，请确认执行")

    def _on_plan_error(self, error_message: str) -> None:
        """Handle plan generation error.

        Args:
            error_message: Error message
        """
        self.task_input.set_enabled(True)

        # Show error dialog
        QMessageBox.critical(
            self,
            "计划生成失败",
            f"生成计划时发生错误:\n\n{error_message}",
        )

        self.status_bar.showMessage("计划生成失败")

    def _show_plan_confirmation(self, plan: Plan) -> None:
        """Show plan confirmation dialog.

        Args:
            plan: The plan to confirm
        """
        dialog = PlanConfirmDialog(plan, self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self._execute_plan(plan)
        else:
            self.status_bar.showMessage("已取消执行")

    def _execute_plan(self, plan: Plan) -> None:
        """Execute the plan.

        Args:
            plan: The plan to execute
        """
        # TODO: Implement execution with real-time progress display
        # For now, use a simple message
        self.status_bar.showMessage("正在执行计划...")

        # Execute the plan
        result = self.executor.execute_plan(plan)

        # Show result
        if result.overall_status.value == "success":
            QMessageBox.information(
                self,
                "执行成功",
                f"计划执行成功!\n\n"
                f"总步骤: {result.total_steps}\n"
                f"成功: {result.successful_steps}\n"
                f"失败: {result.failed_steps}\n"
                f"耗时: {result.duration_ms}ms" if result.duration_ms else "",
            )
        else:
            QMessageBox.warning(
                self,
                "执行失败",
                f"计划执行失败!\n\n"
                f"总步骤: {result.total_steps}\n"
                f"成功: {result.successful_steps}\n"
                f"失败: {result.failed_steps}",
            )

        self.status_bar.showMessage(f"执行{'成功' if result.overall_status.value == 'success' else '失败'}")

    def closeEvent(self, event):
        """Handle window close event.

        Args:
            event: Close event
        """
        # Clean up any running workers
        if self.planner_worker and self.planner_worker.isRunning():
            self.planner_worker.terminate()
            self.planner_worker.wait()

        event.accept()
