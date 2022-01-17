import qdarktheme
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMenu,
    QMenuBar,
    QStatusBar,
)
from ui.state import AppSettings
from ui.widgets import OpenWorkspaceAction
from ui.windows.about import AboutWindow


class AbstractMainWindow(QMainWindow):
    central_window: QMainWindow
    about_window: AboutWindow

    action_open_workspace: QAction
    action_about: QAction
    action_exit: QAction

    menu_bar: QMenuBar
    menu_bar_recent_workspaces: QMenu

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Python CS")

        self.central_window = QMainWindow()
        self.about_window = AboutWindow()

        self.setCentralWidget(self.central_window)

        self._setup_actions()
        self._setup_menu_bar()
        self._setup_status_bar()

        self._load_state()

    def _setup_actions(self):
        self.action_open_workspace = OpenWorkspaceAction(parent=self)

        self.action_about = QAction(parent=self, text="About")
        self.action_about.triggered.connect(self._show_about_window)

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
        self.setMenuBar(self.menu_bar)

    def _setup_status_bar(self):
        self.status_bar = QStatusBar(parent=self)
        self.setStatusBar(self.status_bar)

    def _load_state(self):
        # Build recent workspaces menu for first time. Can be refreshed later.
        self._load_state_recent_workspaces()

        # Connect to State signals to handle changes. Only connect once.
        AppSettings().recent_workspaces_changed.connect(self._recent_workspaces_changed)

    def _load_state_recent_workspaces(self):
        self.menu_bar_recent_workspaces.clear()
        for recent_workspace in AppSettings().recent_workspaces:
            action = QAction(text=recent_workspace, parent=self)
            action.triggered.connect(self._change_workspace)
            self.menu_bar_recent_workspaces.addAction(action)

    def _recent_workspaces_changed(self, workspace) -> None:
        self._load_state_recent_workspaces()

    def _change_workspace(self) -> None:
        path: str = self.sender().text()  # type: QAction
        AppSettings().workspace = path
        AppSettings().add_recent_workspace(AppSettings().workspace)

    def _show_about_window(self) -> None:
        if self.about_window is None:
            self.about_window = AboutWindow()
        self.about_window.show()

    def _change_theme(self) -> None:
        AppSettings().enable_dark_mode = self.sender().isChecked()
