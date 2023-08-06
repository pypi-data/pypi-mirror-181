"""Energy-ES - User Interface."""

from PySide6.QtWidgets import QApplication

from energy_es.ui.main_window import MainWindow


def start_ui():
    """User interface main function.

    This function displays the main window.
    """
    app = QApplication([])

    win = MainWindow()
    win.show()

    app.exec()
