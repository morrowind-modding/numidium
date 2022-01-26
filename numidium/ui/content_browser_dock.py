from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QLabel,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from numidium.config import config
from numidium.logger import logger
from numidium.ui.explorer import Explorer
from numidium.ui.viewer import Viewer


class ContentBrowserDock(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Widgets
        self.left_dock = QDockWidget("Explorer")
        self.bottom_dock = QDockWidget("Bottom dock")

        # Setup widgets
        self.explorer = Explorer()
        self.explorer.update_ui(config.active_workspace)
        self.left_dock.setWidget(self.explorer)

        self.bottom_dock.setWidget(QTextEdit("This is the bottom editor widget. -- NI"))
        for dock in (self.left_dock, self.bottom_dock):
            dock.setAllowedAreas(
                Qt.DockWidgetArea.LeftDockWidgetArea
                | Qt.DockWidgetArea.RightDockWidgetArea
                | Qt.DockWidgetArea.BottomDockWidgetArea
                | Qt.DockWidgetArea.TopDockWidgetArea
            )

        self.viewer = Viewer()

        # Layout
        main_win = QMainWindow()
        main_win.setCentralWidget(self.viewer)
        main_win.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)
        main_win.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.bottom_dock)

        layout = QVBoxLayout(self)
        layout.addWidget(main_win)
        layout.setContentsMargins(0, 0, 0, 0)

        # Connect signals.
        # config.active_workspace_changed.connect(self.explorer.update_ui)
        self.explorer.selected_filepath_changed.connect(self.viewer.handle_update_filepath)
