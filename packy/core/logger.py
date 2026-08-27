"""Capture and format Qt messages in an application log file.

The logger installs a process-wide Qt message handler and appends messages to
a UTF-8 text file. In development mode, it also writes messages to standard
output.

Examples:
    Start and stop logging around the application lifecycle:

    .. code-block:: python

        from pathlib import Path

        Logger.start(Path("app.log"))
        # Run the application.
        Logger.stop()

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENCE.md file for more information.
"""

# Future library
from __future__ import annotations

# Third-party
from PySide6 import QtCore
from PySide6.QtCore import (
    QDateTime,
    QMessageLogContext,
    Qt,
    QThread,
    QtMsgType,
    qInstallMessageHandler,
)

# Standard library
import os
import sys
from threading import RLock
from typing import TYPE_CHECKING, ClassVar, Literal, TextIO, final

if TYPE_CHECKING:
    # Standard library
    from pathlib import Path


###############################################################################
@final
class Logger:
    """Manage process-wide logging for Qt messages.

    Use :meth:`start` and :meth:`stop` to install and restore the Qt message
    handler. Logging state and file access are protected by a reentrant lock.
    """

    _log_file: ClassVar[TextIO | None] = None
    _previous_handler: ClassVar[object | None] = None
    _lock: ClassVar[RLock] = RLock()

    # -------------------------------------------------------------------------
    @classmethod
    def start(cls, log_file_path: Path) -> bool:
        """Start writing Qt messages to the specified log file.

        The file is opened in append mode with UTF-8 encoding, and the current Qt
        message handler is preserved for restoration by :meth:`stop`.

        Args:
            log_file_path (Path): Path of the log file to open.

        Returns:
            bool: ``True`` if logging was started, or ``False`` if it was already
              active.

        Raises:
            OSError: The log file cannot be opened.
        """
        with cls._lock:
            if cls._log_file is not None:
                return False

            log_file: TextIO = log_file_path.open(
                mode="a",
                buffering=1,
                encoding="utf-8",
            )
            cls._log_file = log_file
            try:
                previous_handler = qInstallMessageHandler(cls.q_message_handler)
            except BaseException:
                cls._log_file = None
                log_file.close()
                raise

            cls._previous_handler = previous_handler
            return True

    # -------------------------------------------------------------------------
    @classmethod
    def stop(cls) -> bool:
        """Stop logging and restore the previous Qt message handler.

        The active log file is closed and the Logger state is cleared. If
        restoring the previous Qt handler raises, local logging resources are
        cleaned up before the exception is propagated.

        Returns:
            bool: ``True`` if logging was stopped, or ``False`` if it was not active.
        """
        with cls._lock:
            log_file = cls._log_file
            if log_file is None:
                return False

            previous_handler = cls._previous_handler

            try:
                qInstallMessageHandler(previous_handler)
            finally:
                cls._log_file = None
                cls._previous_handler = None
                log_file.close()

            return True

    # -------------------------------------------------------------------------
    @classmethod
    def is_active(cls) -> bool:
        """Check whether file logging is active.

        Returns:
            bool: ``True`` when a log file is open; otherwise, ``False``.
        """
        with cls._lock:
            return cls._log_file is not None

    # -------------------------------------------------------------------------
    @classmethod
    def q_message_handler(
        cls,
        msg_type: QtMsgType,
        msg_context: QMessageLogContext,
        msg: str,
    ) -> None:
        """Format and record a message received from Qt.

        Args:
            msg_type (QtMsgType): Qt severity of the message.
            msg_context (QMessageLogContext): Source file and line context supplied
              by Qt.
            msg (str): Message text to record.
        """
        formated_msg = cls._format_message(
            msg_type,
            msg_context.file,
            msg_context.line,
            msg,
        )
        cls._log_message(msg_type, formated_msg)

    # -------------------------------------------------------------------------
    @classmethod
    def _format_message(cls, msg_type: QtMsgType, ctx_file: str, ctx_line: int, msg: str) -> str:
        """Format a Qt message with runtime and source context.

        The result includes the current timestamp, process ID, current Qt thread
        identity, source file and line, severity name, and message text.

        .. warning::

            Since the display of "files" and "lines" only works by default when
            Qt is in debug mode, we need to set QT_MESSAGELOGCONTEXT to enable
            them. But I haven't figured out how to do that in Python
            environment.

        Args:
            msg_type (QtMsgType): Qt severity of the message.
            ctx_file (str): Source file reported by Qt.
            ctx_line (int): Source line reported by Qt.
            msg (str): Message text to include.

        Returns:
            str: The formatted log entry.
        """
        timestamp = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODateWithMs)
        pid = os.getpid()
        thread_id = id(QThread.currentThread())
        level = cls._msg_type_to_str(msg_type)
        formated_msg = (
            f"[{timestamp}][{pid},0x{thread_id:x}][{ctx_file}:{ctx_line}][{level}]: {msg}"
        )
        return formated_msg  # noqa: RET504

    # -------------------------------------------------------------------------
    @classmethod
    def _log_message(cls, msg_type: QtMsgType, msg: str) -> None:
        """Write a formatted message to the active logging outputs.

        When logging is active, the method appends the message to the log file and
        also prints it to standard output when the application is not frozen.

        Args:
            msg_type (QtMsgType): Qt severity associated with the message.
            msg (str): Formatted message to write.
        """
        with cls._lock:
            log_file = cls._log_file
            if log_file is None:
                return

            # Log in file
            log_file.write(f"{msg}\n")

            # Log in console
            in_dev_mode = not getattr(sys, "frozen", False)
            if in_dev_mode:
                print(msg)  # noqa: T201

            if msg_type == QtCore.QtMsgType.QtFatalMsg:
                log_file.flush()

    # -----------------------------------------------------------------------------
    @classmethod
    def _msg_type_to_str(
        cls,
        msg_type: QtMsgType,
    ) -> Literal["DEBUG", "INFO", "WARNING", "CRITICAL", "FATAL", "UNKNOWN"]:
        """Convert a Qt message type to its severity name.

        Args:
            msg_type (QtMsgType): Qt message type to convert.

        Returns:
            Literal["DEBUG", "INFO", "WARNING", "CRITICAL", "FATAL", "UNKNOWN"]:
              Corresponding severity name, or ``"UNKNOWN"`` for an unrecognized type.
        """
        match msg_type:
            case QtMsgType.QtDebugMsg:
                return "DEBUG"
            case QtMsgType.QtInfoMsg:
                return "INFO"
            case QtMsgType.QtWarningMsg:
                return "WARNING"
            case QtMsgType.QtCriticalMsg:
                return "CRITICAL"
            case QtMsgType.QtFatalMsg:
                return "FATAL"
            case _:
                return "UNKNOWN"

    # -------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialize a stateless logger instance."""
