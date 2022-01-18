from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QStatusBar

from numidium.ui.state import AppSettings
from numidium.ui.widgets import OpenWorkspaceAction
from numidium.ui.windows.about import AboutWindow
from numidium.ui.windows.debug import DebugWindow


class AbstractMainWindow(QMainWindow):
    central_window: QMainWindow
    about_window: AboutWindow
    debug_window: DebugWindow

    action_open_workspace: QAction
    action_about: QAction
    action_debug: QAction
    action_exit: QAction

    menu_bar: QMenuBar
    menu_bar_recent_workspaces: QMenu

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Python CS")

        self.central_window = QMainWindow()
        self.about_window = AboutWindow()
        self.debug_window = DebugWindow()

        self.setCentralWidget(self.central_window)

        self._setup_actions()
        self._setup_menu_bar()
        self._setup_status_bar()

        self._load_state()

    def _setup_actions(self):
        self.action_open_workspace = OpenWorkspaceAction(parent=self)

        self.action_about = QAction(parent=self, text="About")
        self.action_about.triggered.connect(self._handle_show_about_window)

        self.action_debug = QAction(parent=self, text="Debug", shortcut="Ctrl+Shift+D")
        self.action_debug.triggered.connect(self._handle_show_debug_window)

        self.action_exit = QAction(parent=self, text="E&xit", shortcut="Ctrl+Q")
        self.action_exit.triggered.connect(lambda _: QApplication.instance().quit())

    def _setup_menu_bar(self):
        self.menu_bar = QMenuBar(parent=self)

        # File Menu
        menu_file = self.menu_bar.addMenu("&File")
        menu_file.addAction(self.action_open_workspace)
        self.menu_bar_recent_workspaces = menu_file.addMenu(QIcon("icons:crop_din_24dp.svg"), "Recent Workspaces...")
        menu_file.addSeparator()
        menu_file.addAction(self.action_exit)

        # About Menu
        menu_about = self.menu_bar.addMenu("&About")
        menu_about.addAction(self.action_about)
        menu_about.addAction(self.action_debug)
        self.setMenuBar(self.menu_bar)

    def _setup_status_bar(self):
        self.status_bar = QStatusBar(parent=self)
        self.setStatusBar(self.status_bar)

    def _load_state(self):
        # Build recent workspaces menu for first time. Can be refreshed later.
        self._load_state_recent_workspaces()

        # Connect to State signals to handle changes. Only connect once.
        AppSettings().recent_workspaces_changed.connect(self._handle_recent_workspaces_changed)

    def _load_state_recent_workspaces(self):
        self.menu_bar_recent_workspaces.clear()
        for recent_workspace in AppSettings().recent_workspaces:
            action = QAction(text=recent_workspace, parent=self)
            action.triggered.connect(self._handle_change_workspace)
            self.menu_bar_recent_workspaces.addAction(action)

    def _handle_recent_workspaces_changed(self, workspace) -> None:
        self._load_state_recent_workspaces()

    def _handle_change_workspace(self) -> None:
        path = self.sender().text()
        AppSettings().workspace = path

    def _handle_show_about_window(self) -> None:
        if self.about_window is None:
            self.about_window = AboutWindow()
        self.about_window.show()

    def _handle_show_debug_window(self) -> None:
        if self.debug_window is None:
            self.debug_window = DebugWindow()
        self.debug_window.show()
