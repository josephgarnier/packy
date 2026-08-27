"""Fixtures shared by the test suite.

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENSE.md file for more information.
"""

# Local application

# Local application
from packy.core.app import App
from packy.core.app_config import AppConfig

# Third-party
import pytest
from PySide6.QtCore import QSettings

# Standard library
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Local application
    from packy.ui.main_window import MainWindow

    # Third-party
    from PySide6.QtWidgets import QApplication
    from pytest_mock import MockerFixture
    from pytestqt.qtbot import QtBot

    # Standard library
    from collections.abc import Generator
    from pathlib import Path
    from unittest.mock import MagicMock


###############################################################################
### App fixtures
###############################################################################
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def qapp_args() -> list[str]:
    """Provide arguments for the unique QApplication instance."""
    return []


# -----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def qapp_cls() -> type[App]:
    """Use PackY's custom QApplication class in pytest-qt."""
    return App


# -----------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def isolate_qsettings(tmp_path: Path) -> None:
    """Use distinct QSettings storage for each test."""
    user_directory: Path = tmp_path / "settings_user"
    system_directory: Path = tmp_path / "settings_system"

    user_directory.mkdir()
    system_directory.mkdir()

    QSettings.setDefaultFormat(QSettings.Format.IniFormat)
    QSettings.setPath(
        QSettings.Format.IniFormat,
        QSettings.Scope.UserScope,
        str(user_directory),
    )
    QSettings.setPath(
        QSettings.Format.IniFormat,
        QSettings.Scope.SystemScope,
        str(system_directory),
    )


# -----------------------------------------------------------------------------
@pytest.fixture
def app(qapp: QApplication) -> Generator[App]:
    """Provide a clean PackY application and restore clean lifecycle state afterward."""
    # Setup
    assert isinstance(qapp, App)

    try:
        qapp.dispose()
        yield qapp
    finally:
        # Teardown
        qapp.dispose()


# -----------------------------------------------------------------------------
@pytest.fixture
def app_config(mocker: MockerFixture, tmp_path: Path) -> AppConfig:
    """Provide the default application configuration test double."""
    log_path = tmp_path / "app.log"
    mocker.patch.object(
        AppConfig,
        "_determine_log_path",
        autospec=True,
        return_value=log_path,
    )
    return AppConfig(
        DEFAULT_LANGUAGE_CODE="en-US",
        MAX_RECENT_BATCHES=3,
        VERSION="1.2.3",
    )


# -----------------------------------------------------------------------------
@pytest.fixture
def initialized_app(
    app: App,
    app_config: AppConfig,
) -> App:
    """Provide an initialized PackY application."""
    app.initialize(app_config)
    return app


# -----------------------------------------------------------------------------
@pytest.fixture
def main_window(
    initialized_app: App,
    mocker: MockerFixture,
    qtbot: QtBot,
) -> MainWindow:
    """Launch the application and provide its initialized main window."""
    app_exec_mock: MagicMock = mocker.patch.object(
        initialized_app,
        "exec",
        return_value=0,
    )

    exit_code = initialized_app.run()
    assert exit_code == 0
    app_exec_mock.assert_called_once_with()

    window = initialized_app.main_window
    assert window is not None

    qtbot.waitUntil(window.isVisible)

    return window
