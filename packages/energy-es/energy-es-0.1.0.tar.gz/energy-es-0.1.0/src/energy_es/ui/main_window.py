"""Energy-ES - User Interface - Main Window."""

from os.path import join, dirname

from PySide6.QtCore import Qt, QUrl, QThread
from PySide6.QtGui import QIcon, QAction

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QMenu, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QSizePolicy
)

from PySide6.QtWebEngineWidgets import QWebEngineView

from energy_es.ui.chart import get_message_html
from energy_es.ui.workers import ChartWorker
from energy_es.ui.about_dialog import AboutDialog


class MainWidget(QWidget):
    """Main widget of the main window."""

    PRICE_UNITS = ["k", "m"]

    def __init__(self):
        """Class initializer."""
        super().__init__()
        self.create_widgets()

    def create_widgets(self):
        """Create window widgets."""
        # Layout 1
        self._layout_1 = QVBoxLayout()
        self.setLayout(self._layout_1)

        # Chart
        self._chart = QWebEngineView()
        self._chart.setContextMenuPolicy(Qt.NoContextMenu)

        self._layout_1.addWidget(self._chart)

        # Layout 2
        self._layout_2 = QHBoxLayout()
        self._layout_1.addLayout(self._layout_2)

        # Unit label
        self._unit_lab = QLabel(text="Prices unit:")

        self._layout_2.addWidget(
            self._unit_lab, alignment=Qt.AlignmentFlag.AlignLeft
        )

        # Unit combo box
        self._unit_combo = QComboBox()
        self._unit_combo.setFixedWidth(150)
        self._unit_combo.addItems(["€/kWh", "€/MWh"])
        self._unit_combo.currentIndexChanged.connect(self.on_unit_changed)

        self._layout_2.addWidget(
            self._unit_combo, stretch=True,
            alignment=Qt.AlignmentFlag.AlignLeft
        )

        # Initial chart generation
        self.update_chart("k")

    def update_chart(self, unit: str):
        """Update the chart widget.

        :param unit: Prices unit. It must be "k" to have the prices in €/kWh or
        "m" to have them in €/MWh.
        """
        def on_success(path: str):
            url = QUrl.fromLocalFile(path)
            self._chart.load(url)

        def on_error(html: str):
            self._chart.setHtml(html)

        self.chart_thread = QThread()
        self.chart_worker = ChartWorker(unit)
        self.chart_worker.moveToThread(self.chart_thread)

        self.chart_thread.started.connect(self.chart_worker.do_work)
        self.chart_worker.finished.connect(self.chart_thread.quit)

        self.chart_worker.finished.connect(self.chart_worker.deleteLater)
        self.chart_thread.finished.connect(self.chart_thread.deleteLater)

        self.chart_worker.success.connect(on_success)
        self.chart_worker.error.connect(on_error)

        html = get_message_html("Generating the chart...")
        self._chart.setHtml(html)
        self.chart_thread.start()

    def on_unit_changed(self, x: int):
        """Run logic when the prices unit has changed.

        :param x: Selected unit index.
        """
        unit = MainWidget.PRICE_UNITS[x]
        self.update_chart(unit)


class MainWindow(QMainWindow):
    """Main window."""

    def __init__(self):
        """Class initializer."""
        super().__init__()

        self.setWindowTitle("Energy-ES")
        self.set_window_icon()
        self.resize(900, 550)
        self.setMinimumSize(750, 450)

        self.create_menu_bar()
        self.create_widgets()

    def set_window_icon(self):
        """Set the window icon."""
        img_dir = join(dirname(__file__), "images")
        logo_path = join(img_dir, "logo.png")

        icon = QIcon(logo_path)
        self.setWindowIcon(icon)

    def create_menu_bar(self):
        """Create the window menu."""
        self.menu_bar = self.menuBar()

        # File menu
        self.file_menu = QMenu("&File", self)

        exit_act = QAction("&Exit", self)
        exit_act.setMenuRole(QAction.QuitRole)
        exit_act.triggered.connect(self.on_exit)

        self.file_menu.addAction(exit_act)

        # Help menu
        self.help_menu = QMenu("&Help", self)

        about_act = QAction("&About", self)
        about_act.setMenuRole(QAction.AboutRole)
        about_act.triggered.connect(self.on_about)

        self.help_menu.addAction(about_act)

        # Add menus
        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.help_menu)

    def on_exit(self):
        """Run logic when the Exit menu option is clicked."""
        self.close()

    def on_about(self):
        """Run logic when the About menu option is clicked."""
        self._about_dialog = AboutDialog()
        self._about_dialog.show()

    def create_widgets(self):
        """Create window widgets."""
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)
