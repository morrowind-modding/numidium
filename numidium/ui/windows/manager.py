from __future__ import annotations

from PySide6.QtWidgets import QMainWindow

from numidium.config import config
from numidium.ui.application import Numidium
from numidium.ui.windows.application import ApplicationWindow
from numidium.ui.windows.welcome import WelcomeWindow


class ManagerWindow(QMainWindow):
    widget: WelcomeWindow | ApplicationWindow

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Numidium")
        self.resize(self.screen().availableGeometry().size() / 1.25)  # type: ignore[call-overload]

        if config.show_welcome or not config.setup_completed:
            self.widget = WelcomeWindow()
        else:
            self.widget = ApplicationWindow()

        Numidium.workspace_changed.connect(self.handle_workspace_changed)

        self.setCentralWidget(self.widget)

    def handle_workspace_changed(self, workspace: str) -> None:
        if isinstance(self.widget, WelcomeWindow):
            self.widget.deleteLater()
            self.widget = ApplicationWindow()
            self.setCentralWidget(self.widget)
