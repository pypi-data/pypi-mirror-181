"""Energy-ES - User Interface - Workers."""

from PySide6.QtCore import QObject, Signal

from energy_es.ui.chart import get_message_html, get_chart_path


class ChartWorker(QObject):
    """Chart thread class.

    This class is used to generate the chart HTML file in a separate, parallel
    thread.
    """

    success = Signal(str)
    error = Signal(str)
    finished = Signal()

    def __init__(self, unit: str):
        """Initialize the instance.

        :param unit: Prices unit. It must be "k" to have the prices in €/kWh or
        "m" to have them in €/MWh.
        """
        super().__init__()
        self._unit = unit

    def do_work(self):
        """Do the thread work.

        This method generates the chart HTML file in a separate, parallel
        thread and emits the file path or an error message HTML code if there
        is any error.
        """
        try:
            path = get_chart_path(self._unit)  # Absolute path
            self.success.emit(path)
        except Exception as e:
            title = "There was an error generating the chart"
            html = get_message_html(title, str(e))
            self.error.emit(html)
        finally:
            self.finished.emit()
