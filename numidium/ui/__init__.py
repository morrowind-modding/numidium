import sys
from pathlib import Path

from PySide6.QtCore import QDir, Qt
from PySide6.QtWidgets import QApplication
from ui.windows.manager import ManagerWindow


def exec() -> None:
    QDir.addSearchPath("icons", Path().cwd() / "numidium" / "ui" / "icons")

    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    window = ManagerWindow()
    window.resize(window.screen().availableGeometry().size() / 1.25)
    window.show()

    sys.exit(app.exec())
