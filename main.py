"""Provide the application entry point for Packy.

This module provides the application entry point, initializes the logger,
launches the Qt application, and stops the logger before returning.

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENCE.md file for more information.
"""

# Local application
from packy.core.app import App
from packy.core.app_config import AppConfig
from packy.core.logger import Logger

# Third-party
from PySide6 import QtCore

# Standard library
import sys
import traceback


# -----------------------------------------------------------------------------
def main() -> int:
    """Run the Packy application entry point.

    The function prints a traceback when an exception occurs during logger
    initialization, application execution, or logger shutdown.

    Returns: int: The exit code returned by :meth:`App.launch`, or ``0`` if no
      exit code is obtained.

    Raises:
        Exception: Propagates any exception raised during application
            execution after being caught and logged.
    """
    exit_code: int = 0
    try:
        # Initialize logging
        config: AppConfig = AppConfig()
        has_started = Logger.start(config.LOG_FILE_PATH)
        if not has_started:
            QtCore.qWarning("Debug logger has been started twice!")

        # Launch application
        exit_code = App.launch(App(sys.argv))
        has_stopped = Logger.stop()
        if not has_stopped:
            QtCore.qWarning("Debug logger cannot be stopped!")
    except Exception:  # noqa: BLE001
        traceback.print_exc()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
