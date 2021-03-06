from __future__ import annotations

from PySide6.QtCore import QDir, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qtvscodestyle import load_stylesheet  # type: ignore

from numidium.ui.signals import Signals
from numidium.ui.utility import staticproperty

QDir.addSearchPath("icons", "numidium/ui/icons")


class Numidium(QApplication):
    _signals: Signals

    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)

        self._signals = Signals()

        self.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
        self.setWindowIcon(QIcon("icons:icon.ico"))
        self.setStyleSheet(load_stylesheet())

    @staticproperty
    @staticmethod
    def signals() -> Signals:
        assert isinstance(app := Numidium.instance(), Numidium)
        return app._signals
