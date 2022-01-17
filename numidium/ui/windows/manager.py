import qdarktheme
from PySide6.QtWidgets import QApplication, QMainWindow
from ui.state import AppSettings
from ui.windows.application import ApplicationWindow
from ui.windows.welcome import WelcomeWindow


class ManagerWindow(QMainWindow):
    welcome_window: WelcomeWindow | None
    application_window: ApplicationWindow | None

    def __init__(self) -> None:
        super().__init__()
        self.welcome_window = None
        self.application_window = None

        self._setup_theme(AppSettings().enable_dark_mode)
        if AppSettings().show_welcome_window == True or AppSettings().setup_completed == False:
            self._setup_windows((AppSettings().show_welcome_window))

        AppSettings().workspace_changed.connect(self._workspace_changed)
        AppSettings().enable_dark_mode_changed.connect(self._setup_theme)
        AppSettings().setup_completed_changed.connect(self._setup_completed_changed)

    def _workspace_changed(self):
        if self.welcome_window is not None:
            self._setup_windows(show_welcome=False)

    def _setup_theme(self, enabled):
        theme = "dark"
        if enabled == False:
            theme = "light"
        stylesheet = qdarktheme.load_stylesheet(theme)
        QApplication.instance().setStyleSheet(stylesheet)

    def _setup_completed_changed(self, completed):
        self._setup_windows(not completed)

    def _setup_windows(self, show_welcome):
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
