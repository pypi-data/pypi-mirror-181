"""Energy-ES.

Energy-ES is a Python desktop application that shows an interactive chart with
the hourly values of the Spot Market and PVPC energy prices of the current day
in Spain. The data is provided by some APIs of "Red Eléctrica de España".
"""

# We import the "energy_es.env" module to set a environment variable before
# importing PySide6 through the "energy_es.ui" module.
from energy_es import env
from energy_es.ui import start_ui


__version__ = "0.1.0"


def main():
    """Application main function."""
    start_ui()
