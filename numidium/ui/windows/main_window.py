from __future__ import annotations

from PySide6.QtCore import Qt

from numidium.config import config
from numidium.ui.activity_bar import ActivityBar
from numidium.ui.application import Numidium
from numidium.ui.console import Console
from numidium.ui.windows.abstractmain import AbstractMainWindow
from numidium.ui.windows.welcome import WelcomeWindow


class MainWindow(AbstractMainWindow):

    activity_bar: ActivityBar
    console: Console

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Numidium")
        self.resize(self.screen().availableGeometry().size() * 0.8)

        self.activity_bar = ActivityBar()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.activity_bar)

        self.console = Console()
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.console)

        if config.show_welcome or not config.recent_workspaces:
            self.show_welcome_window()
        else:
            self.show_default_window()

        self.setup_signals()

    def setup_signals(self) -> None:
        Numidium.signals.workspace_changed.connect(self.show_default_window)

    def show_welcome_window(self) -> None:
        self.activity_bar.hide()
        self.console.hide()
        self.setCentralWidget(WelcomeWindow())

    def show_default_window(self) -> None:
        self.activity_bar.show()
        self.console.show()
        self.setCentralWidget(self.activity_bar._view)
