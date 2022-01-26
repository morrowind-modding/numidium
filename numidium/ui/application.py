from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QDir, Qt, Signal, SignalInstance
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qdarktheme import load_stylesheet  # type: ignore

from numidium.config import config
from numidium.ui.utility import staticproperty

QDir.addSearchPath("icons", Path().cwd() / "numidium" / "ui" / "icons")


class Numidium(QApplication):
    _workspace_changed: SignalInstance = Signal(str)  # type: ignore[assignment]

    def __init__(self) -> None:
        super().__init__()

        self.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
        self.setWindowIcon(QIcon("icons:icon.ico"))
        self.setStyleSheet(load_stylesheet("dark"))

        self.workspace_changed.connect(self._handle_workspace_changed)

    @classmethod
    def instance(cls) -> Numidium:
        return super().instance() or cls()

    def _handle_workspace_changed(self, workspace: str) -> None:
        if workspace != config.active_workspace:
            config.active_workspace = workspace
            config.recent_workspaces[workspace] = int(datetime.now().timestamp())

            # Limit to maximum of 5 recent workspaces. TODO: customizable
            if len(config.recent_workspaces) > 5:
                # sort by time
                items = list(config.recent_workspaces.items())
                items.sort(key=lambda x: x[1], reverse=True)
                # take first 5
                config.recent_workspaces.clear()
                config.recent_workspaces.update(items[:5])

            config.save_path()

    @staticproperty
    @staticmethod
    def workspace_changed() -> SignalInstance:
        return Numidium.instance()._workspace_changed
