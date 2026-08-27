"""Provide recent batch history management for the batch workspace.

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENSE.md file for more information.
"""
# Future library
from __future__ import annotations

# Local application
from packy.constants.settings_keys import WorkspaceSettings

# Third-party
from PySide6 import QtCore
from PySide6.QtCore import QObject, Signal

# Standard library
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    # Local application
    from packy.core.user_settings import UserSettings

    # Standard library
    from pathlib import Path


###############################################################################
class BatchWorkspaceHistory(QObject):
    """Maintain and persist the recently opened batch history.

    Signals:
        recent_batches_changed (list): Emitted when the persisted recent batch
          paths change.
    """

    # -------------------------------------------------------------------------
    recent_batches_changed = Signal(list, arguments=["recent_batch_paths"])

    # -------------------------------------------------------------------------
    def __init__(
        self,
        max_recent_batches: int,
        settings: UserSettings,
        parent: QObject | None = None,
    ) -> None:
        """Initialize the recent batch history manager.

        Args:
            max_recent_batches (int): Maximum number of recent batch paths to retain.
            settings (UserSettings): Settings store used to persist the history.
            parent (QObject | None): Parent Qt object, or ``None`` for no parent.
        """
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

        self._max_recent_batches: Final[int] = max_recent_batches
        self._settings = settings
        self._recent_batches: list[Path] = []

    # -------------------------------------------------------------------------
    @property
    def recently_opened(self) -> tuple[Path, ...]:
        """The recent batch paths, ordered from most to least recently opened."""
        return tuple(self._recent_batches)

    # -------------------------------------------------------------------------
    @property
    def latest_opened(self) -> Path | None:
        """The most recently opened batch path, or ``None`` if the history is empty."""
        return self._recent_batches[0] if self._recent_batches else None

    # -------------------------------------------------------------------------
    def add_recently_opened(self, batch_path: Path) -> None:
        """Add a batch path to the front of the recent batch history.

        If the path is already present, move it to the front. Trim the history to the
        configured maximum size, then persist the updated history.

        Args:
            batch_path (Path): Batch path to add to the recent history.
        """
        QtCore.qDebug("Adding batch to the recent batch history.")
        if batch_path in self._recent_batches:
            self._recent_batches.remove(batch_path)
        self._recent_batches.insert(0, batch_path)
        while len(self._recent_batches) > self._max_recent_batches:
            self._recent_batches.pop()

        self.save_to_settings(self._settings)

    # -------------------------------------------------------------------------
    def clear_recently_opened(self) -> None:
        """Clear the recent batch history and persist the empty history."""
        QtCore.qDebug("Clearing recent batch history.")
        self._recent_batches.clear()

        self.save_to_settings(self._settings)

    # -------------------------------------------------------------------------
    def load_from_settings(self, settings: UserSettings) -> None:
        """Load the recent batch history from user settings.

        Emit ``recent_batches_changed`` with the loaded paths after updating the
        in-memory history.

        Args:
            settings (UserSettings): Settings object in which to store the recent
              batch paths.
        """
        QtCore.qDebug(
            f"Loading {self.objectName()} settings from {WorkspaceSettings.SETTINGS_GROUP}.",
        )
        settings.begin_group(WorkspaceSettings.SETTINGS_GROUP)
        self._recent_batches = settings.value(WorkspaceSettings.RECENT_BATCHES, [])
        self.recent_batches_changed.emit(self._recent_batches)
        settings.end_group()

    # -------------------------------------------------------------------------
    def save_to_settings(self, settings: UserSettings) -> None:
        """Persist the recent batch history to user settings.

        Args:
            settings (UserSettings): Settings object in which to store the recent
              batch paths.
        """
        QtCore.qDebug(
            f"Saving {self.objectName()} settings in {WorkspaceSettings.SETTINGS_GROUP}.",
        )
        settings.begin_group(WorkspaceSettings.SETTINGS_GROUP)
        settings.set_value(
            WorkspaceSettings.RECENT_BATCHES,
            self._recent_batches,
            self.recent_batches_changed.emit,
        )
        settings.end_group()
