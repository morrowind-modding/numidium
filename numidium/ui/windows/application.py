from PySide6.QtCore import QSize, Qt

from numidium.ui.activity_bar import ActivityBar
from numidium.ui.windows.about import AboutWindow
from numidium.ui.windows.abstractmain import AbstractMainWindow


class ApplicationWindow(AbstractMainWindow):

    activity_bar: ActivityBar

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Setup activity bar
        self.activity_bar = ActivityBar(parent=self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.activity_bar)
        self.central_window.setCentralWidget(self.activity_bar._view)

    def _show_about_window(self) -> None:
        if self.about_window is None:
            self.about_window = AboutWindow()
        self.about_window.show()
