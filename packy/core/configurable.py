"""Define the protocol for objects that load and save user settings.

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENCE.md file for more information.
"""

# Local application
from packy.core.user_settings import UserSettings

# Third-party
from PySide6.QtCore import Slot

# Standard library
from abc import abstractmethod
from typing import Protocol, runtime_checkable


###############################################################################
@runtime_checkable
class Configurable(Protocol):
    """Define the protocol for objects that load and save user settings."""

    @Slot(UserSettings, result=None)
    @abstractmethod
    def load_settings(self, settings: UserSettings) -> None:
        """Load configuration values from the specified user settings.

        Args:
            settings (UserSettings): User settings from which to load configuration
              values.
        """
        raise NotImplementedError

    @Slot(UserSettings, result=None)
    @abstractmethod
    def save_settings(self, settings: UserSettings) -> None:
        """Save configuration values to the specified user settings.

        Args:
            settings (UserSettings): User settings in which to save configuration
              values.
        """
        raise NotImplementedError
