from PySide6.QtWidgets import QMessageBox


def register() -> None:
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Example")
    msg_box.setText("Hello World!")
    msg_box.exec()


def unregister() -> None:
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Example")
    msg_box.setText("Goodbye World!")
    msg_box.exec()
