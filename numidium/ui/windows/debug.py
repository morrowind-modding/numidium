from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from numidium.config import config
from numidium.logger import logger
from numidium.ui.enums import AlignmentFlag
from numidium.ui.widgets import TextBlockLabel


class DebugWindow(QWidget):
    """Debug menu for application troubleshooting.

    A secondary window that exposes tools for troubleshooting the application.
    """

    _label: QLabel
    _description: TextBlockLabel
    _action_clear_settings: QPushButton

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(AlignmentFlag.AlignTop)

        self._label = QLabel("Debug")
        self._description = TextBlockLabel(
            "This is a debug menu for working with the application. Please do not use these buttons unless you know what you are doing."
        )
        self._action_clear_settings = QPushButton("Clear Application Settings")
        self._action_clear_settings.setToolTip(
            "Resets application settings. You must restart the application afterwards."
        )

        layout.addWidget(self._label)
        layout.addWidget(self._description)
        layout.addWidget(self._action_clear_settings)
        self.setLayout(layout)
        self.resize(200, 400)

        self._action_clear_settings.clicked.connect(self._handle_clear_settings)

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