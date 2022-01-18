from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDockWidget, QMainWindow, QTextEdit, QVBoxLayout, QWidget

from numidium.ui.explorer import Explorer
from numidium.ui.widgets import DockToolbar


class ModsDock(QWidget):
    toolbar: DockToolbar
    main_win: QMainWindow
    left_dock: QDockWidget
    bottom_dock: QDockWidget

    def __init__(self) -> None:
        super().__init__()
        self.workspaceDirectory = None

    def setup_ui(self, win: QWidget) -> None:
        """Set up ui."""
        # Widgets
        self.left_dock = QDockWidget("Explorer")
        self.bottom_dock = QDockWidget("Bottom dock")

        # Setup widgets
        self.explorer = Explorer()
        self.left_dock.setWidget(self.explorer)

        self.bottom_dock.setWidget(QTextEdit("This is the bottom widget. -- NI"))
        for dock in (self.left_dock, self.bottom_dock):
            dock.setAllowedAreas(
                Qt.DockWidgetArea.LeftDockWidgetArea
                | Qt.DockWidgetArea.RightDockWidgetArea
                | Qt.DockWidgetArea.BottomDockWidgetArea
                | Qt.DockWidgetArea.TopDockWidgetArea
            )

        # Layout
        self.main_win = QMainWindow()
        self.main_win.setCentralWidget(QWidget())
        self.main_win.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)
        self.main_win.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.bottom_dock)

        layout = QVBoxLayout(win)
        layout.addWidget(self.main_win)
        layout.setContentsMargins(0, 0, 0, 0)

        self._setup_toolbar()


    def _setup_toolbar(self):
        self.toolbar = DockToolbar()

        # TODO: Add custom actions.

        self.main_win.addToolBar(self.toolbar)
