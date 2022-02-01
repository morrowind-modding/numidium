from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget

from numidium.ui.widgets import OpenGithubButton, TextBlockLabel


class AboutWindow(QWidget):
    label_description: TextBlockLabel
    button_open_source_code: OpenGithubButton

    def __init__(self) -> None:
        super().__init__()

        self.label_description = TextBlockLabel(
            "Numidium is an open source mod management tool for The Elder Scrolls III: Morrowind. The application is extensible through a modular plugin system and is inteded to be a singular tool for working with TESIII installations and plugins. For more information, use the button below to view the source code repository."
        )
        self.button_open_source_code = OpenGithubButton()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)  # type: ignore[call-overload]
        layout.addWidget(self.label_description)
        layout.addWidget(self.button_open_source_code)

        self.setLayout(layout)
        self.setMaximumSize(500, 150)
        self.setWindowTitle("About")
