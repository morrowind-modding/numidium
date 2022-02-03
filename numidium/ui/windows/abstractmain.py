from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QMenuBar,
    QStatusBar,
    QWidget,
)

from numidium.config import config
from numidium.ui.application import Numidium
from numidium.ui.menu_bar import MenuBar
from numidium.ui.widgets import OpenWorkspaceAction
from numidium.ui.windows.about import AboutWindow


class AbstractMainWindow(QMainWindow):
    central_window: QWidget
    menu_bar: MenuBar

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Numidium")

        self.central_window = QWidget()

        self.setCentralWidget(self.central_window)

        self._setup_menu_bar()
        self._setup_status_bar()

    def _setup_menu_bar(self) -> None:
        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)

    def _setup_status_bar(self) -> None:
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
