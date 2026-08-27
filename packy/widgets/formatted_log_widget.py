"""Provide log-related enums and a color-coded Qt text widget.

The widget displays general messages and formatted file-operation results.

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENCE.md file for more information.
"""

# Third-party
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QContextMenuEvent
from PySide6.QtWidgets import QMenu, QTextEdit, QWidget

# Standard library
from enum import IntEnum, StrEnum, auto, unique
from typing import final, override


###############################################################################
@unique
class LogLevel(IntEnum):
    """Represent the severity levels supported by the log widget."""

    INFO = 1
    SUCCESS = auto()
    ERROR = auto()


###############################################################################
@unique
class FileOperation(StrEnum):
    """Represent translatable file-operation message templates.

    Each value contains one replacement field for the affected file path.
    """

    COPY = "Copy file {}"
    MOVE = "Move file {}"
    DELETE = "Delete file {}"
    WIPE = "Wipe file {}"
    LINK = "Create link {}"
    SYM_LINK = "Create symlink {}"
    MK_DIR = "Create directory {}"
    RM_DIR = "Remove directory {}"
    WIPE_DIR = "Wipe directory {}"
    PACK = "Pack to file {}"
    EXTRACT = "Extract file {}"
    TEST = "Test file integrity {}"


###############################################################################
@unique
class OperationStatus(StrEnum):
    """Represent translatable prefixes for operation results."""

    INFO = "Info: "
    SUCCES = "Done: "
    ERROR = "Error: "


###############################################################################
@final
class FormattedLogWidget(QTextEdit):
    """Display color-coded log messages in a text editor.

    The standard context menu includes an additional action that removes all
    messages.
    """

    # -------------------------------------------------------------------------
    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the formatted log widget.

        Args:
            parent (QWidget | None): Parent widget, or ``None`` to create a
              top-level widget.
        """
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    # -------------------------------------------------------------------------
    @override
    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu: QMenu = super().createStandardContextMenu()
        menu.addSeparator()
        clear_action: QAction = QAction(self.tr("Clear"), self)
        clear_action.triggered.connect(self.clear)
        menu.addAction(clear_action)
        menu.exec(event.globalPos())

    # -------------------------------------------------------------------------
    @Slot(result=None)
    def clear(self) -> None:
        """Removes all messages from the log view."""
        super().clear()

    # -------------------------------------------------------------------------
    @Slot(result=None)
    def write_line(self, message: str, severity: LogLevel = LogLevel.INFO) -> None:
        """Append a color-coded message to the log.

        Information, success, and error messages are displayed in blue, green, and
        red, respectively.

        Args:
            message (str): Message to append. The text is interpreted as HTML by
              :meth:`QTextEdit.append`.
            severity (LogLevel): Severity that determines the message color.
        """
        match severity:
            case LogLevel.INFO:
                msg_font_color = "blue"
            case LogLevel.SUCCESS:
                msg_font_color = "green"
            case LogLevel.ERROR:
                msg_font_color = "red"

        message = f"<font color='{msg_font_color}'>{message}</font>"
        super().append(message)

    # -------------------------------------------------------------------------
    @Slot(result=None)
    def write_file_operation(
        self,
        op_status: OperationStatus,
        op_type: FileOperation,
        affected_file_path: str,
    ) -> None:
        """Append a formatted file-operation result to the log.

        The operation status determines the message severity and color.

        Args:
            op_status (OperationStatus): Status prefix and severity of the operation.
            op_type (FileOperation): Message template describing the operation.
            affected_file_path (str): File-system path inserted into the operation
              template.
        """
        match op_status:
            case OperationStatus.INFO:
                severity = LogLevel.INFO
            case OperationStatus.SUCCES:
                severity = LogLevel.SUCCESS
            case OperationStatus.ERROR:
                severity = LogLevel.ERROR

        message = self.tr(op_status)
        message += self.tr(op_type).format(affected_file_path)
        self.write_line(message, severity)
