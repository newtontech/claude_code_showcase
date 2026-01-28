"""Confirmation dialog for plan execution."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from openmanus.models.plan import Plan, RiskLevel


class PlanConfirmDialog(QDialog):
    """Dialog for confirming plan execution.

    Shows plan details and allows user to confirm or cancel execution.
    Displays warnings for high-risk plans.
    """

    def __init__(self, plan: Plan, parent: QWidget | None = None):
        """Initialize the confirmation dialog.

        Args:
            plan: The plan to confirm
            parent: Parent widget
        """
        super().__init__(parent)

        self.plan = plan
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("确认执行计划")
        self.setMinimumWidth(600)

        layout = QVBoxLayout(self)

        # Risk warning for high risk plans
        if self.plan.risk_level == RiskLevel.HIGH:
            warning = QLabel("⚠️  高风险操作")
            warning.setStyleSheet(
                "color: #ff453a; font-size: 16px; font-weight: bold; padding: 8px;"
            )
            warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(warning)

            warning_detail = QLabel(
                "此操作包含可能危险的操作，请仔细检查每个步骤后再确认。"
            )
            warning_detail.setStyleSheet(
                "color: #ff453a; font-size: 12px; padding: 0 0 8px 0;"
            )
            warning_detail.setWordWrap(True)
            warning_detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(warning_detail)

        # Plan summary
        summary = self._create_plan_summary()
        layout.addWidget(summary)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        yes_button = button_box.button(QDialogButtonBox.StandardButton.Yes)
        no_button = button_box.button(QDialogButtonBox.StandardButton.No)

        if self.plan.risk_level == RiskLevel.HIGH:
            yes_button.setText("确认执行")
            yes_button.setStyleSheet("background-color: #ff453a; color: white;")
            no_button.setText("取消")
            no_button.setStyleSheet("background-color: #444;")
        else:
            yes_button.setText("确认执行")
            no_button.setText("取消")

        layout.addWidget(button_box)

    def _create_plan_summary(self) -> QLabel:
        """Create plan summary text.

        Returns:
            Label with formatted plan summary
        """
        risk_colors = {
            RiskLevel.LOW: "#30d158",
            RiskLevel.MEDIUM: "#ffd60a",
            RiskLevel.HIGH: "#ff453a",
        }
        risk_color = risk_colors.get(self.plan.risk_level, "#888")

        summary_text = f"""
<span style='font-size: 13px;'>
<b>任务目标:</b> {self.plan.goal}

<br>
<b>风险等级:</b> <span style='color: {risk_color}; font-weight: bold;'>{self.plan.risk_level.value}</span>

<br>
<b>工作目录:</b> <span style='color: #888; font-family: monospace;'>{self.plan.workspace_root}</span>

<br>
<b>执行步骤 ({len(self.plan.steps)}):</b>
"""

        for i, step in enumerate(self.plan.steps, 1):
            summary_text += f"<br>&nbsp;&nbsp;{i}. {step.description} <span style='color: #666;'>[{step.tool}]</span>"

        summary_text += "<br><br><b>成功标准:</b>"
        for criteria in self.plan.success_criteria:
            summary_text += f"<br>&nbsp;&nbsp;• {criteria}"

        summary_text += "</span>"

        summary = QLabel(summary_text)
        summary.setWordWrap(True)
        summary.setStyleSheet("padding: 8px; background-color: #1e1e1e; border-radius: 6px;")

        return summary
