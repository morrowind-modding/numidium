from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.label = QLabel("About")
        self.description = QLabel("This is a placeholder for our about information.")

        layout.addWidget(self.label)
        layout.addWidget(self.description)
        self.setLayout(layout)
        self.resize(200, 400)
