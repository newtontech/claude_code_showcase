"""Task input widget for OpenManus GUI."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class TaskInputWidget(QWidget):
    """Widget for inputting task descriptions.

    This widget provides:
    - A text area for entering task descriptions
    - A button to generate the plan
    - Signals for user interactions
    """

    # Signals
    generate_requested = pyqtSignal(str)  # Emitted when user clicks Generate

    def __init__(self, parent: QWidget | None = None):
        """Initialize the task input widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create group box
        group = QGroupBox("任务描述")
        group_layout = QVBoxLayout()

        # Instruction label
        instruction = QLabel("请描述您想要完成的任务:")
        instruction.setObjectName("subheading")
        group_layout.addWidget(instruction)

        # Text input area
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "例如：把 data/notes.txt 总结成 3 条要点，写到 out/summary.md"
        )
        self.text_input.setMinimumHeight(100)
        self.text_input.setStyleSheet("QTextEdit { font-size: 14px; }")
        group_layout.addWidget(self.text_input)

        # Button row
        button_row = QHBoxLayout()
        button_row.addStretch()

        # Generate button
        self.generate_button = QPushButton("生成计划")
        self.generate_button.setEnabled(False)
        self.generate_button.clicked.connect(self._on_generate_clicked)
        button_row.addWidget(self.generate_button)

        group_layout.addLayout(button_row)
        group.setLayout(group_layout)

        layout.addWidget(group)

        # Connect text changed signal to enable/disable button
        self.text_input.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self) -> None:
        """Enable/disable generate button based on text input."""
        text = self.text_input.toPlainText().strip()
        self.generate_button.setEnabled(bool(text))

    def _on_generate_clicked(self) -> None:
        """Handle generate button click."""
        text = self.text_input.toPlainText().strip()
        if text:
            self.generate_requested.emit(text)

    def get_task_description(self) -> str:
        """Get the current task description.

        Returns:
            The task description text
        """
        return self.text_input.toPlainText().strip()

    def clear(self) -> None:
        """Clear the task input."""
        self.text_input.clear()

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the input widget.

        Args:
            enabled: True to enable, False to disable
        """
        self.text_input.setEnabled(enabled)
        self.generate_button.setEnabled(enabled and bool(self.text_input.toPlainText().strip()))

