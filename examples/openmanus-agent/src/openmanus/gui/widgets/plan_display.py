"""Plan display widget for showing generated plans."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QScrollArea,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from openmanus.models.plan import Plan, RiskLevel


class PlanDisplayWidget(QWidget):
    """Widget for displaying plan details.

    Shows:
    - Plan goal
    - Risk level with color coding
    - Steps in a tree format
    - Success criteria
    """

    def __init__(self, parent: QWidget | None = None):
        """Initialize the plan display widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        self._setup_ui()
        self._current_plan = None

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area for plan content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        # Container widget
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(8, 8, 8, 8)
        self.container_layout.setSpacing(12)

        scroll.setWidget(self.container)
        layout.addWidget(scroll)

    def set_plan(self, plan: Plan) -> None:
        """Display a plan.

        Args:
            plan: The plan to display
        """
        self._current_plan = plan
        self._update_display()

    def _update_display(self) -> None:
        """Update the display with current plan data."""
        # Clear existing content
        while self.container_layout.count():
            child = self.container_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if self._current_plan is None:
            placeholder = QLabel("暂无计划")
            placeholder.setStyleSheet("color: #888; font-style: italic;")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.container_layout.addWidget(placeholder)
            return

        plan = self._current_plan

        # Goal section
        goal_label = QLabel("任务目标")
        goal_label.setObjectName("subheading")
        self.container_layout.addWidget(goal_label)

        goal_value = QLabel(plan.goal)
        goal_value.setWordWrap(True)
        goal_value.setStyleSheet("font-size: 14px; padding: 4px 8px; background-color: #1e1e1e; border-radius: 4px;")
        self.container_layout.addWidget(goal_value)

        # Risk level section
        risk_label = QLabel("风险等级")
        risk_label.setObjectName("subheading")
        self.container_layout.addWidget(risk_label)

        risk_colors = {
            RiskLevel.LOW: "#30d158",
            RiskLevel.MEDIUM: "#ffd60a",
            RiskLevel.HIGH: "#ff453a",
        }
        risk_descriptions = {
            RiskLevel.LOW: "低风险 - 只读操作或安全写入",
            RiskLevel.MEDIUM: "中风险 - 涉及文件写入或批量操作",
            RiskLevel.HIGH: "高风险 - 包含删除或危险命令",
        }

        risk_color = risk_colors.get(plan.risk_level, "#888")
        risk_desc = risk_descriptions.get(plan.risk_level, "")

        risk_value = QLabel(f"● {plan.risk_level.value}")
        risk_value.setStyleSheet(f"color: {risk_color}; font-size: 16px; font-weight: bold; padding: 4px 8px;")
        self.container_layout.addWidget(risk_value)

        risk_detail = QLabel(risk_desc)
        risk_detail.setStyleSheet(f"color: {risk_color}; font-size: 12px; padding: 0 8px;")
        self.container_layout.addWidget(risk_detail)

        # Workspace section
        workspace_label = QLabel("工作目录")
        workspace_label.setObjectName("subheading")
        self.container_layout.addWidget(workspace_label)

        workspace_value = QLabel(plan.workspace_root)
        workspace_value.setStyleSheet("color: #888; font-family: monospace; padding: 4px 8px;")
        self.container_layout.addWidget(workspace_value)

        # Steps section
        steps_label = QLabel(f"执行步骤 ({len(plan.steps)})")
        steps_label.setObjectName("subheading")
        self.container_layout.addWidget(steps_label)

        steps_tree = QTreeWidget()
        steps_tree.setHeaderLabels(["步骤", "工具", "描述"])
        steps_tree.setColumnWidth(0, 50)
        steps_tree.setColumnWidth(1, 80)
        steps_tree.setRootIsDecorated(False)
        steps_tree.setMaximumHeight(150)

        for i, step in enumerate(plan.steps):
            item = QTreeWidgetItem(steps_tree)
            item.setText(0, str(i + 1))
            item.setText(1, step.tool)
            item.setText(2, step.description)

        steps_tree.setSizePolicy(
            steps_tree.sizePolicy().horizontalPolicy(),
            steps_tree.sizePolicy().verticalPolicy(),
        )
        self.container_layout.addWidget(steps_tree)

        # Success criteria section
        criteria_label = QLabel("成功标准")
        criteria_label.setObjectName("subheading")
        self.container_layout.addWidget(criteria_label)

        for criteria in plan.success_criteria:
            criteria_item = QLabel(f"• {criteria}")
            criteria_item.setStyleSheet("padding: 2px 8px;")
            self.container_layout.addWidget(criteria_item)

        # Add stretch at the end
        self.container_layout.addStretch()

    def clear(self) -> None:
        """Clear the display."""
        self._current_plan = None
        self._update_display()

    def get_plan(self) -> Plan | None:
        """Get the currently displayed plan.

        Returns:
            The current plan or None
        """
        return self._current_plan
