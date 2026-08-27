"""File filters.

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENSE.md file for more information.
"""

# Local application
from packy.utils.translation import PACKY_TRANSLATE_NOOP

# Standard library
from dataclasses import dataclass


###############################################################################
@dataclass(frozen=True)
class FileFilter:
    ALL_FILES: str = PACKY_TRANSLATE_NOOP("FileFilter", "All files (*)")
    BATCH_FILE: str = PACKY_TRANSLATE_NOOP("FileFilter", "Batch file (*.json)")
