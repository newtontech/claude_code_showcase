"""Main entry point for OpenManus GUI application."""

import sys

from PyQt6.QtWidgets import QApplication

from openmanus.gui.main_window import MainWindow


def main() -> int:
    """Main entry point for the GUI application.

    Returns:
        Application exit code
    """
    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("OpenManus")
    app.setApplicationDisplayName("OpenManus")
    app.setOrganizationName("OpenManus")

    # Set application style
    app.setStyle("Fusion")

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run the event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
