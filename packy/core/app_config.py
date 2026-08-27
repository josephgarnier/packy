"""Define immutable application configuration definitions.

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENCE.md file for more information.
"""

# Third-party
from PySide6.QtCore import QStandardPaths

# Standard library
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, final


###############################################################################
@final
@dataclass(frozen=True, slots=True)
class AppConfig:
    """Store immutable application configuration values.

    Attributes:
        DEFAULT_LANGUAGE_CODE (Final[str]): Default locale code used by the
          application.
        MAX_RECENT_BATCHES (Final[int]): Maximum number of recent batches retained.
        VERSION (Final[str]): Application version.
        LOG_FILE_PATH (Final[Path]): Log file path for the current execution
          environment.
    """

    DEFAULT_LANGUAGE_CODE: Final[str] = "en-US"
    MAX_RECENT_BATCHES: Final[int] = 5
    VERSION: Final[str] = "0.9.0.0"
    LOG_FILE_PATH: Final[Path] = field(
        init=False,
        default_factory=lambda: AppConfig._determine_log_path(),  # noqa: PLW0108
    )

    @staticmethod
    def _determine_log_path() -> Path:
        """Determine the log file path for the current execution environment.

        Development executions use ``./logs/log.txt``. Frozen application executions
        use ``log.txt`` in Qt's writable application-data location.

        Returns:
            Path: Path to the application log file.
        """
        in_dev_mode = not getattr(sys, "frozen", False)
        if in_dev_mode:
            folder_path = Path("./logs")
        else:
            app_data_location = QStandardPaths.StandardLocation.AppDataLocation
            folder_path = Path(QStandardPaths.writableLocation(app_data_location))
        return folder_path / "app.log"
