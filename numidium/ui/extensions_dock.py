from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QSizePolicy,
    QTextEdit,
    QWidget,
)

from numidium.core.extensions import Extension, available_extensions
from numidium.logger import logger


class ExtensionsListItem(QListWidgetItem):
    """A custom widget that can be added to the extensions dock list."""

    extension: Extension

    def __init__(self, extension: Extension):
        super().__init__()
        self.extension = extension
        self.setText(extension.name)
        self.setIcon(QIcon("icons:settings_24dp.svg"))


class ExtensionsDock(QWidget):

    _list: QListWidget
    _text: QTextEdit

    def __init__(self) -> None:
        super().__init__()

        self._list = QListWidget()
        self._list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._list.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self._list.currentItemChanged.connect(self.set_current_item)

        self._text = QTextEdit()
        self._text.setReadOnly(True)
        self._text.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        layout = QHBoxLayout(self)
        layout.addWidget(self._list)
        layout.addWidget(self._text)

        for extension in available_extensions():
            self.add_item(ExtensionsListItem(extension))

    def add_item(self, item: ExtensionsListItem) -> None:
        self._list.addItem(item)

    def set_current_item(self, item: ExtensionsListItem) -> None:
        readme_path = item.extension.path / "README.md"

        try:
            readme_text = readme_path.read_text()
        except (OSError, UnicodeDecodeError) as e:
            readme_text = "Not a valid README.md"
            logger.error("Invalid 'README.md' for extension: {}", item.extension.name)
            logger.error(e)

        self._text.setMarkdown(readme_text)
