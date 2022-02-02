from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDockWidget, QMainWindow, QVBoxLayout, QWidget

from numidium.config import config
from numidium.ui.application import Numidium
from numidium.ui.explorer import Explorer
from numidium.ui.viewer import Viewer


class ContentBrowserDock(QWidget):
    left_dock: QDockWidget
    explorer: Explorer
    viewer: Viewer

    def __init__(self) -> None:
        super().__init__()

        # Widgets
        self.left_dock = QDockWidget("Explorer")

        # Setup widgets
        self.explorer = Explorer()
        self.explorer.update_ui(config.active_workspace)
        self.left_dock.setWidget(self.explorer)

        self.viewer = Viewer()

        # Layout
        main_win = QMainWindow()
        main_win.setCentralWidget(self.viewer)
        main_win.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)

        layout = QVBoxLayout(self)
        layout.addWidget(main_win)
        layout.setContentsMargins(0, 0, 0, 0)

        # Connect signals.
        Numidium.signals.workspace_changed.connect(self.explorer.update_ui)
        self.explorer.selected_filepath_changed.connect(self.viewer.handle_update_filepath)
