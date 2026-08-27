"""Provide the application's About dialog.

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENCE.md file for more information.
"""

# Local application
from packy.ui.ui_about_dialog import Ui_AboutDialog

# Third-party
from PySide6.QtWidgets import QDialog, QWidget


###############################################################################
class AboutDialog(QDialog):
    """Display the application's About dialog."""

    # -------------------------------------------------------------------------
    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the About dialog and its user interface.

        Args:
            parent (QWidget | None): Parent widget for the dialog.
        """
        super().__init__(parent)
        self._ui = Ui_AboutDialog()
        self._ui.setupUi(self)
