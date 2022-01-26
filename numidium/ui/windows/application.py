from PySide6.QtCore import Qt

from numidium.ui.activity_bar import ActivityBar
from numidium.ui.windows.abstractmain import AbstractMainWindow


class ApplicationWindow(AbstractMainWindow):

    activity_bar: ActivityBar

    def __init__(self) -> None:
        super().__init__()

        # Setup activity bar
        self.activity_bar = ActivityBar()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.activity_bar)
        self.central_window.setCentralWidget(self.activity_bar._view)
