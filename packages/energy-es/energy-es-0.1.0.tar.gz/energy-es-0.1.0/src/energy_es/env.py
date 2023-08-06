"""Energy-ES - Environment Variables."""

from os import environ

# Reduce the number of PySide log messages
environ["QT_LOGGING_RULES"] = "*.info=false;*.dispatch=false"
