from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AboutWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.label = QLabel("About")
        self.description = QLabel("This is a placeholder for our about information.")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.description)

        self.setLayout(layout)
        self.resize(200, 400)
