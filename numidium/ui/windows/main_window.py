from __future__ import annotations

from PySide6.QtCore import Qt

from numidium.config import config
from numidium.ui.activity_bar import ActivityBar
from numidium.ui.application import Numidium
from numidium.ui.windows.abstractmain import AbstractMainWindow
from numidium.ui.windows.welcome import WelcomeWindow


class MainWindow(AbstractMainWindow):
    activity_bar: ActivityBar

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Numidium")
        self.resize(self.screen().availableGeometry().size() / 1.25)  # type: ignore[call-overload]

        self.activity_bar = ActivityBar()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.activity_bar)

        if config.show_welcome or not config.setup_completed:
            self.show_welcome_window()
        else:
            self.show_activity_bar()

        self.setup_signals()

    def setup_signals(self) -> None:
        Numidium.signals.workspace_changed.connect(self.show_activity_bar)

    def show_welcome_window(self) -> None:
        if not isinstance(self.centralWidget(), WelcomeWindow):
            self.activity_bar.hide()
            self.setCentralWidget(WelcomeWindow())

    def show_activity_bar(self) -> None:
        if not self.activity_bar.isVisible():
            self.activity_bar.show()
            self.setCentralWidget(self.activity_bar._view)
