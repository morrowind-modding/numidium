# type: ignore

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from numidium.config import config
from numidium.core.extensions import reload_active_extensions
from numidium.extensions.debug_menu.icon_browser import IconBrowser
from numidium.extensions.debug_menu.widget_gallery import WidgetGallery
from numidium.logger import logger
from numidium.ui.enums import AlignmentFlag
from numidium.ui.menu_bar import MenuBar
from numidium.ui.widgets import TextBlockLabel


class DebugWindow(QWidget):
    """Debug menu for application troubleshooting.

    A secondary window that exposes tools for troubleshooting the application.
    """

    _label: QLabel
    _description: TextBlockLabel
    _action_view_icons: QPushButton
    _action_view_widgets: QPushButton
    _action_reload_active_extensions: QPushButton
    _action_clear_settings: QPushButton

    _icon_browser: IconBrowser
    _widget_gallery: WidgetGallery

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(AlignmentFlag.AlignTop)

        self._label = QLabel("Debug")
        self._description = TextBlockLabel(
            "This is a debug menu for working with the application. Please do not use these buttons unless you know what you are doing."
        )
        self._action_view_icons = QPushButton("View Application Icon Set")
        self._action_view_widgets = QPushButton("View Widget Gallery")

        reload_active_extensions_shortcut = "Ctrl+Shift+R"
        self._action_reload_active_extensions = QPushButton(
            f"Reload Active Extensions ({reload_active_extensions_shortcut})"
        )
        self._action_reload_active_extensions.setShortcut(reload_active_extensions_shortcut)

        self._action_clear_settings = QPushButton("Clear Application Settings")
        self._action_clear_settings.setToolTip(
            "Resets application settings. You must restart the application afterwards."
        )

        layout.addWidget(self._label)
        layout.addWidget(self._description)
        layout.addWidget(self._action_view_icons)
        layout.addWidget(self._action_view_widgets)
        layout.addWidget(self._action_reload_active_extensions)
        layout.addWidget(self._action_clear_settings)
        self.setLayout(layout)
        self.resize(200, 400)
        self.setWindowTitle("Debug Menu")

        self._action_view_icons.clicked.connect(self._handle_view_icons)
        self._action_view_widgets.clicked.connect(self._handle_view_widgets)
        self._action_reload_active_extensions.clicked.connect(self._handle_reload_active_extensions)
        self._action_clear_settings.clicked.connect(self._handle_clear_settings)

    def _handle_view_icons(self) -> None:
        self._icon_browser = IconBrowser()
        self._icon_browser.show()

    def _handle_view_widgets(self) -> None:
        self._widget_gallery = WidgetGallery()
        self._widget_gallery.show()

    def _handle_reload_active_extensions(self) -> None:
        reload_active_extensions()

    def _handle_clear_settings(self) -> None:
        config.reset()
        config.save_path()
        logger.info("Cleared applicatioon settings! Attempting restart.")
        QMessageBox.warning(
            self.parent(),
            "Restart Application",
            "To fully clear your settings, you must restart the application. A shutdown will be attempted after clicking 'OK.' Please ropen the application afterwards.",
            QMessageBox.Ok,
        )
        if app := QApplication.instance():
            app.exit()


debug_window = DebugWindow()
action = QAction(text="Debug", shortcut="Ctrl+Shift+D")
action.triggered.connect(debug_window.show)


def register() -> None:
    MenuBar.instance().add_action(action)


def unregister() -> None:
    MenuBar.instance().remove_action(action)
