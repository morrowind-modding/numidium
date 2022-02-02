import sys
from typing import Any

from PySide6.QtCore import QObject, Qt, Signal, SignalInstance
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDockWidget, QPlainTextEdit

from numidium.config import config
from numidium.logger import logger


class StdoutWrapper(QObject):
    text_written: SignalInstance = Signal(str)  # type: ignore[assignment]

    def write(self, text: str) -> None:
        self.text_written.emit(text)

    def __getattr__(self, name: str) -> Any:
        return getattr(sys.__stdout__, name)


class Console(QDockWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Console")
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable)

        text_edit = QPlainTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        text_edit.setMaximumBlockCount(500)

        font = text_edit.font()
        font.setFamily("Courier New")
        font.setStyleHint(QFont.Monospace)
        text_edit.setFont(font)

        self.setWidget(text_edit)

        sys.stdout = StdoutWrapper()
        sys.stdout.text_written.connect(text_edit.insertPlainText)

        logger.add(sys.stdout, format="{time:HH:mm:ss.SSS}  |  {level:<8}  |  {message}", colorize=False)
        logger.info(f"{config.active_workspace=}")
        logger.info(f"{config.active_extensions=}")
