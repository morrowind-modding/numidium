from __future__ import annotations

from typing import ClassVar

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QMenuBar,
    QStatusBar,
    QWidget,
)

from numidium.config import config
from numidium.ui.application import Numidium
from numidium.ui.widgets import OpenWorkspaceAction
from numidium.ui.windows.about import AboutWindow


class MenuBar(QMenuBar):
    _central_window: QWidget
    _about_window: AboutWindow

    _action_open: QAction
    _action_about: QAction
    _action_debug: QAction
    _action_exit: QAction

    _menu_bar_recent_workspaces: QMenu

    _menu_tools: QMenu

    # Global instance
    _instance: ClassVar[MenuBar]

    def __init__(self) -> None:
        super().__init__()
        self._about_window = AboutWindow()

        self._setup_actions()
        self._setup_menu_bar()

        # Make accessible to extensions.
        # TODO: Figure out a proper api.
        if not hasattr(self, "_instance"):
            type(self)._instance = self

    def _setup_actions(self) -> None:
        self._action_open = OpenWorkspaceAction()

        self._action_about = QAction(text="About")
        self._action_about.triggered.connect(self._about_window.show)

        self._action_exit = QAction(text="E&xit", shortcut="Ctrl+Q")  # type:ignore[call-overload]
        self._action_exit.triggered.connect(lambda _: app.quit() if (app := QApplication.instance()) else None)

    def _setup_menu_bar(self) -> None:
        # File Menu
        menu_file = self.addMenu("&File")
        menu_file.addAction(self._action_open)
        self._menu_bar_recent_workspaces = menu_file.addMenu(
            QIcon("icons:folder_copy_24dp.svg"), "Recent Workspaces..."
        )
        menu_file.addSeparator()
        menu_file.addAction(self._action_exit)

        # Extension Menu
        self._menu_tools = self.addMenu("&Tools")

        # About Menu
        menu_about = self.addMenu("&About")
        menu_about.addAction(self._action_about)

        self._rebuild_recent_workspaces()

    def _rebuild_recent_workspaces(self) -> None:
        self._menu_bar_recent_workspaces.clear()
        for recent_workspace in config.recent_workspaces:
            action = QAction(text=recent_workspace, parent=self._menu_bar_recent_workspaces)
            action.triggered.connect(self._handle_change_workspace)
            self._menu_bar_recent_workspaces.addAction(action)

    def _handle_change_workspace(self) -> None:
        Numidium.signals.workspace_changed.emit(self.sender().text())

    def add_action(self, action: QAction) -> None:
        """Add a new action to the menu bar."""
        self._menu_tools.addAction(action)

    def remove_action(self, action: QAction) -> None:
        """Remove an action from the menu bar."""
        self._menu_tools.removeAction(action)

    @classmethod
    def instance(cls) -> MenuBar:
        """Get the main application's MenuBar instance."""
        return cls._instance
