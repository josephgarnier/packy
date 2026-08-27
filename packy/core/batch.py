"""Provide the batch model, persistence operations, and job tracking.

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENSE.md file for more information.
"""

# Local application
from packy.core.archiver import Archiver

# Third-party
from PySide6.QtCore import (
    QCoreApplication,
    QDateTime,
    QFileInfo,
    QObject,
    Signal,
)

# Standard library
from dataclasses import dataclass
from pathlib import Path
from typing import final, override


###############################################################################
@final
class Batch(QObject):
    """Represent a batch file with archiving settings and queued jobs.

    A batch tracks its file path, last-save timestamp, modified state, archiver
    settings, and ordered jobs. Changes to archiver settings or jobs mark the
    batch as modified. A successful save resets the modified state.

    Signals:
        file_path_changed: Emitted after the file path changes, with
          ``old_file_path`` and ``new_file_path``.
        modified_changed: Emitted after the modified state changes, with
          ``is_modified``.
        format_changed: Emitted after the archive format changes, with
          ``old_format`` and ``new_format``.
        compression_level_changed: Emitted after the compression level changes,
          with ``old_compression_level`` and ``new_compression_level``.
        compression_method_changed: Emitted after the compression method changes,
          with ``old_compression_method`` and ``new_compression_method``.
        saved: Emitted after a file is saved successfully.
        job_added: Emitted after a job is appended, with ``job``.
        job_removed: Emitted after a job is removed, with ``job``.
    """

    ###########################################################################
    @dataclass
    class ArchiverSettings:
        """Store the archiving settings used by a batch.

        Attributes:
            format (Archiver.Format): Archive format. Defaults to
              ``Archiver.Format.ZIP``.
            compression_level (Archiver.CompressionLevel): Compression level. Defaults
              to ``Archiver.CompressionLevel.NORMAL``.
            compression_method (Archiver.CompressionMethod): Compression method.
              Defaults to ``Archiver.CompressionMethod.STORE``.
        """

        format: Archiver.Format = Archiver.Format.ZIP
        compression_level: Archiver.CompressionLevel = Archiver.CompressionLevel.NORMAL
        compression_method: Archiver.CompressionMethod = Archiver.CompressionMethod.STORE

        # ---------------------------------------------------------------------
        @override
        def __repr__(self) -> str:
            cls_name = self.__class__.__name__
            return (
                f"{cls_name}(\n"
                f"  format={self.format!r},\n"
                f"  compression_level={self.compression_level!r},\n"
                f"  compression_method={self.compression_method!r}\n"
                f")"
            )

        # ---------------------------------------------------------------------
        @override
        def __str__(self) -> str:
            cls_name = self.__class__.__name__
            return f"{cls_name}({self.format}, {self.compression_level}, {self.compression_method})"

        # ---------------------------------------------------------------------
        @override
        def __format__(self, format_spec: str) -> str:
            return format(str(self), format_spec)

    # -------------------------------------------------------------------------
    file_path_changed = Signal(Path, Path, arguments=["old_file_path", "new_file_path"])
    modified_changed = Signal(bool, arguments=["is_modified"])
    format_changed = Signal(
        Archiver.Format,
        Archiver.Format,
        arguments=["old_format", "new_format"],
    )
    compression_level_changed = Signal(
        Archiver.CompressionLevel,
        Archiver.CompressionLevel,
        arguments=["old_compression_level", "new_compression_level"],
    )
    compression_method_changed = Signal(
        Archiver.CompressionMethod,
        Archiver.CompressionMethod,
        arguments=["old_compression_method", "new_compression_method"],
    )
    saved = Signal()
    job_added = Signal(str, arguments=["job"])
    job_removed = Signal(str, arguments=["job"])

    # -------------------------------------------------------------------------
    @staticmethod
    def default_filename() -> str:
        """Return the default filename for a new batch.

        Returns:
            str: The filename ``untitled-batch.json``.
        """
        return "untitled-batch.json"

    # -------------------------------------------------------------------------
    def __init__(self, abs_file_path: Path, parent: QObject | None = None) -> None:
        """Initialize a batch for an absolute file path.

        Args:
            abs_file_path (Path): Absolute path associated with the batch.
            parent (QObject | None): Qt parent object, or ``None`` for no parent.
        """
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

        assert abs_file_path.is_absolute()
        self._file_path: Path = abs_file_path
        self._last_saved = QDateTime()
        self._is_modified: bool = False
        self._archiver_settings = Batch.ArchiverSettings()
        self._jobs: list[str] = []

    # -------------------------------------------------------------------------
    @override
    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return (
            f"{cls_name}(\n"
            f"  archiver_settings='{self._archiver_settings!r}', \n"
            f"  file_path={self._file_path!r}, \n"
            f"  last_saved={self._last_saved!r}, \n"
            f"  is_modified={self._is_modified!r}, \n"
            f"  jobs={self._jobs!r}\n"
            f")"
        )

    # -------------------------------------------------------------------------
    @override
    def __str__(self) -> str:
        cls_name = self.__class__.__name__
        return (
            f"{cls_name}("
            f"{self._archiver_settings}, "
            f"{self._file_path}, "
            f"{self._last_saved}, "
            f"{self._is_modified}, "
            f"{self._jobs})"
        )

    # -------------------------------------------------------------------------
    @override
    def __format__(self, format_spec: str) -> str:
        return format(str(self), format_spec)

    # -------------------------------------------------------------------------
    @property
    def file_path(self) -> Path:
        """The absolute path associated with the batch."""
        return self._file_path

    # -------------------------------------------------------------------------
    def _set_file_path(self, file_path: Path) -> None:
        """Set the batch file path.

        If the path changes, emit :attr:`file_path_changed` with the previous and new
        paths.

        Args:
            file_path (Path): New file path associated with the batch.
        """
        if self._file_path == file_path:
            return
        old_file_path = self._file_path
        self._file_path = file_path
        self.file_path_changed.emit(old_file_path, file_path)

    # -------------------------------------------------------------------------
    @property
    def display_name(self) -> str:
        """The file name component of the batch path."""
        return self._file_path.name

    # -------------------------------------------------------------------------
    @property
    def last_saved(self) -> QDateTime:
        """The file modification timestamp recorded by the latest successful save."""
        return self._last_saved

    # -------------------------------------------------------------------------
    @property
    def is_modified(self) -> bool:
        """Whether the batch is marked as modified."""
        return self._is_modified

    # -------------------------------------------------------------------------
    def _set_is_modified(self) -> None:
        """Mark the batch as modified.

        If the batch was not already marked as modified, update its state and emit
        :attr:`modified_changed`.
        """
        if self._is_modified:
            return

        self._is_modified = True
        self.modified_changed.emit(True)  # noqa: FBT003

    # -------------------------------------------------------------------------
    def _reset_is_modified(self) -> None:
        """Mark the batch as unmodified.

        If the batch was marked as modified, update its state and emit
        :attr:`modified_changed`.
        """
        if not self._is_modified:
            return

        self._is_modified = False
        self.modified_changed.emit(False)  # noqa: FBT003

    # -------------------------------------------------------------------------
    @property
    def archiver_format(self) -> Archiver.Format:
        """The archive format used by the batch.

        Assigning a different value emits :attr:`format_changed`.
        """
        return self._archiver_settings.format

    # -------------------------------------------------------------------------
    @archiver_format.setter
    def archiver_format(self, format: Archiver.Format) -> None:  # noqa: A002
        """Set the archive format.

        If the format changes, mark the batch as modified and emit
        :attr:`format_changed` with the previous and new formats.

        Args:
            format (Archiver.Format): Archive format to use.
        """
        if self._archiver_settings.format == format:
            return

        old_format = self._archiver_settings.format
        self._archiver_settings.format = format

        self._set_is_modified()
        self.format_changed.emit(old_format, format)

    # -------------------------------------------------------------------------
    @property
    def archiver_compression_level(self) -> Archiver.CompressionLevel:
        """The archive compression level used by the batch.

        Assigning a different value emits :attr:`compression_level_changed`.
        """
        return self._archiver_settings.compression_level

    # -------------------------------------------------------------------------
    @archiver_compression_level.setter
    def archiver_compression_level(self, level: Archiver.CompressionLevel) -> None:
        """Set the archive compression level.

        If the compression level changes, mark the batch as modified and emit
        :attr:`compression_level_changed` with the previous and new levels.

        Args:
            level (Archiver.CompressionLevel): Archive compression level to use.
        """
        if self._archiver_settings.compression_level == level:
            return

        old_compression_level = self._archiver_settings.compression_level
        self._archiver_settings.compression_level = level

        self._set_is_modified()
        self.compression_level_changed.emit(old_compression_level, level)

    # -------------------------------------------------------------------------
    @property
    def archiver_compression_method(self) -> Archiver.CompressionMethod:
        """The archive compression method used by the batch.

        Assigning a different value emits :attr:`compression_method_changed`.
        """
        return self._archiver_settings.compression_method

    # -------------------------------------------------------------------------
    @archiver_compression_method.setter
    def archiver_compression_method(self, method: Archiver.CompressionMethod) -> None:
        """Set the archive compression method.

        If the compression method changes, mark the batch as modified and emit
        :attr:`compression_method_changed` with the previous and new methods.

        Args:
            method (Archiver.CompressionMethod): Archive compression method to use.
        """
        if self._archiver_settings.compression_method == method:
            return

        old_compression_method = self._archiver_settings.compression_method
        self._archiver_settings.compression_method = method

        self._set_is_modified()
        self.compression_method_changed.emit(old_compression_method, method)

    # -------------------------------------------------------------------------
    def save(self, to_abs_file_path: Path | None = None) -> tuple[bool, str]:
        """Save the batch to a file.

        On success, reset the modified state, update the file path and last-save
        timestamp, and emit :attr:`saved`.

        Args:
            to_abs_file_path (Path | None): Absolute destination path, or ``None``
              to use the current file path.

        Returns:
            tuple[bool, str]: A success flag and error message. The message is empty
              when the operation succeeds.
        """
        dst_file_path: Path = self._file_path
        if to_abs_file_path is not None:
            assert to_abs_file_path.is_absolute()
            dst_file_path = to_abs_file_path

        try:
            with dst_file_path.open("wt", encoding="utf-8") as file:
                file.write("placeholder for futur code")
        except OSError as ex:
            return (
                False,
                self.tr("Could not open file '{0}' for writing: {1}.").format(
                    dst_file_path,
                    ex.strerror,
                ),
            )

        self._set_file_path(dst_file_path)
        self._last_saved = QFileInfo(dst_file_path).lastModified()
        self._reset_is_modified()

        self.saved.emit()
        return (True, "")

    # -------------------------------------------------------------------------
    @staticmethod
    def load(abs_batch_file_path: Path) -> tuple[Batch | None, str]:
        """Create a batch for an existing readable batch file.

        The file contents are read but are not applied to the returned batch.

        Args:
            abs_batch_file_path (Path): Absolute path to the batch file to read.

        Returns:
            tuple[Batch | None, str]: A batch and an empty message on success, or
              ``None`` and an error message if the file is missing or cannot be read.
        """
        if not abs_batch_file_path.exists():
            return (
                None,
                QCoreApplication.translate("Batch", "File not found: '{0}'.").format(
                    abs_batch_file_path,
                ),
            )
        try:
            # Open for reading ('r') and text mode ('t').
            with abs_batch_file_path.open("rt", encoding="utf-8") as file:
                content = file.read()
        except OSError as ex:
            return (
                None,
                QCoreApplication.translate("Batch", "Unable to read file '{0}': {1}.").format(
                    abs_batch_file_path,
                    ex.strerror,
                ),
            )
        return (Batch(abs_batch_file_path), "")

    # -------------------------------------------------------------------------
    def add_job(self, job: str) -> None:
        """Append a job to the batch.

        After appending the job, emit :attr:`job_added`. This marks the batch as
        modified and may emit :attr:`modified_changed`.

        Args:
            job (str): Job string to append.
        """
        self._jobs.append(job)

        self._set_is_modified()
        self.job_added.emit(job)

    # -------------------------------------------------------------------------
    def remove_job(self, index: int) -> None:
        """Remove the job at the specified index.

        After removing the job, emit :attr:`job_removed`. This marks the batch as
        modified and may emit :attr:`modified_changed`.

        Args:
            index (int): Zero-based index of an existing job.
        """
        assert 0 <= index < len(self._jobs)

        job = self._jobs[index]
        del self._jobs[index]

        self._set_is_modified()
        self.job_removed.emit(job)

    # -------------------------------------------------------------------------
    @property
    def jobs(self) -> tuple[str, ...]:
        """The jobs in the batch."""
        return tuple(self._jobs)
