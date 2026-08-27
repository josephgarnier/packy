"""_summary_

_description_

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENCE.md file for more information.
"""

# Local application
from packy.graveyard.files_model import FilesModel

# Third-party
from PySide6.QtCore import QObject, Signal, Slot

# Standard library
import uuid
from pathlib import Path
from typing import final, override


###############################################################################
@final
class TaskModel(QObject):
    """_summary_

    _description_
    """

    folder_path_error = Signal(str)
    name_changed = Signal()
    source_folder_changed = Signal()
    destination_folder_changed = Signal()

    # -------------------------------------------------------------------------
    def __init__(self, parent: QObject | None = None) -> None:
        """Initialize a task.

        Args:
            parent (QWidget | None): The parent object. Defaults to None.
        """
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

        self.__id: uuid.UUID = uuid.uuid4()
        self.__is_enabled: bool = False
        self.__name: str = ""
        self.__source_folder: Path | None = None
        self.__source_files: FilesModel = FilesModel()
        self.__destination_folder: Path | None = None
        self.__output_filename: str | None = None

    # -------------------------------------------------------------------------
    @property
    def id(self) -> uuid.UUID:
        return self.__id

    # -------------------------------------------------------------------------
    @property
    def is_enabled(self) -> bool:
        return self.__is_enabled

    # -------------------------------------------------------------------------
    @property
    def name(self) -> str:
        return self.__name

    # -------------------------------------------------------------------------
    @property
    def source_folder(self) -> Path | None:
        return self.__source_folder

    # -------------------------------------------------------------------------
    @property
    def source_files(self) -> FilesModel:
        return self.__source_files

    # -------------------------------------------------------------------------
    @property
    def destination_folder(self) -> Path | None:
        return self.__destination_folder

    # -------------------------------------------------------------------------
    @property
    def output_filename(self) -> str | None:
        return self.__output_filename

    # -------------------------------------------------------------------------
    @override
    def __repr__(self) -> str:
        return (
            f"TaskModel("
            f"id='{self.__id}', "
            f"is_enabled='{self.__is_enabled}', "
            f"source_folders='{self.__source_folder}', "
            f"source_files='{self.__source_files}', "
            f"destination_folder='{self.__destination_folder}'"
            f")"
        )

    # -------------------------------------------------------------------------
    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, TaskModel) and other.__source_folder == self.__source_folder

    # -------------------------------------------------------------------------
    @override
    def __hash__(self) -> int:
        return hash(self.__source_folder)

    # -------------------------------------------------------------------------
    @Slot(result=None)
    def enable(self) -> None:
        self.__is_enabled = True

    # -------------------------------------------------------------------------
    @Slot(result=None)
    def disable(self) -> None:
        self.__is_enabled = False

    # -------------------------------------------------------------------------
    @Slot(str, result=None)  # pyright: ignore[reportArgumentType]
    def set_name(self, name: str) -> None:
        if self.__name != name:
            self.__name = name
            self.name_changed.emit()

    # -------------------------------------------------------------------------
    @Slot(Path, result=bool)  # pyright: ignore[reportArgumentType]
    def set_source_folder(self, new_folder: Path) -> bool:
        if not new_folder.exists():
            self.folder_path_error.emit(
                self.tr("The source folder does not exist: ") + str(new_folder),
            )
            return False
        if self.__source_folder == new_folder:
            return False
        self.__source_folder = new_folder
        self.source_folder_changed.emit()
        return True

    # -------------------------------------------------------------------------
    @Slot(Path, result=bool)  # pyright: ignore[reportArgumentType]
    def set_destination_folder(self, new_folder: Path) -> bool:
        if not new_folder.exists():
            self.folder_path_error.emit(
                self.tr("The destination folder does not exist: ") + str(new_folder),
            )
            return False
        if self.__destination_folder == new_folder:
            return False
        self.__destination_folder = new_folder
        self.destination_folder_changed.emit()
        return True

    # -------------------------------------------------------------------------
    @Slot(str, result=None) # pyright: ignore[reportArgumentType]
    def set_output_filename(self, new_filename: str) -> None:
        self.__output_filename = new_filename
