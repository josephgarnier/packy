"""Settings keys.

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENSE.md file for more information.
"""

# Standard library
from dataclasses import dataclass


###############################################################################
@dataclass(frozen=True)
class MainWindowSettings:
    SETTINGS_GROUP: str = "MainWindow"
    STATE: str = "State"


###############################################################################
@dataclass(frozen=True)
class WorkspaceSettings:
    SETTINGS_GROUP: str = "Workspace"
    RECENT_BATCHES: str = "RecentBatches"

###############################################################################
@dataclass(frozen=True)
class BatchSettings:
    SETTINGS_GROUP: str = "Batch"
