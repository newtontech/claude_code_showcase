"""Test script for GUI functionality verification."""

from openmanus.gui.main_window import MainWindow
from openmanus.models.plan import Plan, RiskLevel, Step
from PyQt6.QtWidgets import QApplication
import sys


def test_gui_basic():
    """Test basic GUI functionality."""
    # Create application
    app = QApplication(sys.argv)

    # Create main window
    window = MainWindow()
    window.show()

    print("✓ GUI window created successfully")
    print(f"  - Window title: {window.windowTitle()}")
    print(f"  - Min size: {window.minimumWidth()}x{window.minimumHeight()}")
    print(f"  - Planner type: {type(window.planner).__name__}")

    # Test plan display
    test_plan = Plan(
        goal="测试任务：读取文件",
        risk_level=RiskLevel.LOW,
        workspace_root="/tmp/test",
        steps=[
            Step(id="1", description="读取文件", tool="file", inputs={})
        ],
        success_criteria=["文件读取成功"]
    )

    window.plan_display.set_plan(test_plan)
    print("✓ Plan display widget works")

    # Test task input
    window.task_input.text_input.setPlainText("测试任务描述")
    print(f"✓ Task input works: '{window.task_input.get_task_description()}'")

    # Clean up
    window.close()

    print("\n✓ All basic GUI tests passed!")
    print("\nTo run the full GUI application:")
    print("  uv run openmanus-gui")
    print("  OR")
    print("  uv run python -m openmanus.gui.main")


if __name__ == "__main__":
    test_gui_basic()
