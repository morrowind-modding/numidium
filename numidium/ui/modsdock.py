from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QLabel,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from ui.explorer import Explorer


class ModsDock:
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
        main_win = QMainWindow()
        main_win.setCentralWidget(QWidget())
        main_win.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)
        main_win.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.bottom_dock)

        layout = QVBoxLayout(win)
        layout.addWidget(main_win)
        layout.setContentsMargins(0, 0, 0, 0)
