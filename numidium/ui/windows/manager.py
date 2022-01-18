import qdarktheme  # type: ignore
from PySide6.QtWidgets import QApplication, QMainWindow

from numidium.ui.state import AppSettings
from numidium.ui.windows.application import ApplicationWindow
from numidium.ui.windows.welcome import WelcomeWindow


class ManagerWindow(QMainWindow):
    welcome_window: WelcomeWindow | None
    application_window: ApplicationWindow | None

    def __init__(self) -> None:
        super().__init__()
        self.welcome_window = None
        self.application_window = None

        self._handle_setup_theme(AppSettings().enable_dark_mode)
        if AppSettings().show_welcome_window == True or AppSettings().setup_completed == False:
            self._setup_windows((AppSettings().show_welcome_window))
        else:
            self._setup_windows(False)

        AppSettings().workspace_changed.connect(self._handle_workspace_changed)
        AppSettings().enable_dark_mode_changed.connect(self._handle_setup_theme)
        AppSettings().setup_completed_changed.connect(self._handle_setup_completed_changed)

    def _handle_workspace_changed(self) -> None:
        if self.welcome_window is not None:
            self._setup_windows(show_welcome=False)

    def _handle_setup_theme(self, enabled: bool) -> None:
        theme = "dark"
        if enabled == False:
            theme = "light"
        stylesheet = qdarktheme.load_stylesheet(theme)
        if app := QApplication.instance():
            app.setStyleSheet(stylesheet)

    def _handle_setup_completed_changed(self, completed: bool) -> None:
        self._setup_windows(not completed)

    def _setup_windows(self, show_welcome: bool) -> None:
        if show_welcome == True:
            if self.application_window is not None:
                self.application_window.deleteLater()
                self.application_window = None

            self.welcome_window = WelcomeWindow()
            self.setCentralWidget(self.welcome_window)
        else:
            if self.welcome_window is not None:
                self.welcome_window.deleteLater()
                self.welcome_window = None

            self.application_window = ApplicationWindow()
            self.setCentralWidget(self.application_window)
