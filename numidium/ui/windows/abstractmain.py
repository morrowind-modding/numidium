from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QStatusBar

from numidium.config import config
from numidium.ui.application import Numidium
from numidium.ui.widgets import OpenWorkspaceAction
from numidium.ui.windows.about import AboutWindow
from numidium.ui.windows.debug import DebugWindow


class AbstractMainWindow(QMainWindow):
    central_window: QMainWindow
    about_window: AboutWindow
    debug_window: DebugWindow

    action_open: QAction
    action_about: QAction
    action_debug: QAction
    action_exit: QAction

    menu_bar: QMenuBar
    menu_bar_recent_workspaces: QMenu

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Numidium")

        self.central_window = QMainWindow()
        self.about_window = AboutWindow()
        self.debug_window = DebugWindow()

        self.setCentralWidget(self.central_window)

        self._setup_actions()
        self._setup_menu_bar()
        self._setup_status_bar()

    def _setup_actions(self):
        self.action_open = OpenWorkspaceAction()

        self.action_about = QAction(text="About")
        self.action_about.triggered.connect(self.about_window.show)

        self.action_debug = QAction(text="Debug", shortcut="Ctrl+Shift+D")
        self.action_debug.triggered.connect(self.debug_window.show)

        self.action_exit = QAction(text="E&xit", shortcut="Ctrl+Q")
        self.action_exit.triggered.connect(lambda _: QApplication.instance().quit())

    def _setup_menu_bar(self):
        self.menu_bar = QMenuBar()

        # File Menu
        menu_file = self.menu_bar.addMenu("&File")
        menu_file.addAction(self.action_open)
        self.menu_bar_recent_workspaces = menu_file.addMenu(QIcon("icons:crop_din_24dp.svg"), "Recent Workspaces...")
        menu_file.addSeparator()
        menu_file.addAction(self.action_exit)

        # About Menu
        menu_about = self.menu_bar.addMenu("&About")
        menu_about.addAction(self.action_about)
        menu_about.addAction(self.action_debug)

        # Finished
        self.setMenuBar(self.menu_bar)

        self.rebuild_recent_workspaces()

    def _setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def rebuild_recent_workspaces(self):
        self.menu_bar_recent_workspaces.clear()
        for recent_workspace in config.recent_workspaces:
            action = QAction(text=recent_workspace, parent=self.menu_bar_recent_workspaces)
            action.triggered.connect(self._handle_change_workspace)
            self.menu_bar_recent_workspaces.addAction(action)

    def _handle_change_workspace(self) -> None:
        Numidium.workspace_changed.emit(self.sender().text())
