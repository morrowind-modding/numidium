from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QHBoxLayout, QListView, QSizePolicy, QTextEdit, QWidget

from numidium.config import config
from numidium.core.extensions import Extension, available_extensions
from numidium.logger import logger


class ExtensionsListItem(QStandardItem):
    """A custom widget that can be added to the extensions dock list."""

    extension: Extension

    def __init__(self, extension: Extension):
        super().__init__()
        self.extension = extension
        self.setText(extension.name)
        self.setIcon(QIcon(extension.icon))
        self.setCheckable(True)
        if extension.name in config.active_extensions:
            self.setCheckState(Qt.CheckState.Checked)


class ExtensionsDock(QWidget):

    extension_info: QTextEdit
    extension_list: QListView

    def __init__(self) -> None:
        super().__init__()

        self.extension_info = QTextEdit()
        self.extension_info.setReadOnly(True)
        self.extension_info.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.extension_list = QListView()
        self.extension_list.setUniformItemSizes(True)
        self.extension_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.extension_list.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.extension_list.pressed.connect(self._handle_item_clicked)
        self.extension_list.entered.connect(self._handle_item_mouse_over)

        self.extension_list.setModel(QStandardItemModel())
        self.extension_list.model().itemChanged.connect(self._handle_item_changed)

        layout = QHBoxLayout(self)
        layout.addWidget(self.extension_list)
        layout.addWidget(self.extension_info)

        for extension in available_extensions():
            self.add_item(ExtensionsListItem(extension))

        self.set_current_row(0)  # default to first item

    def add_item(self, item: ExtensionsListItem) -> None:
        self.extension_list.model().appendRow(item)

    def set_current_row(self, row: int) -> None:
        index = self.extension_list.model().index(row, 0)
        self.extension_list.setCurrentIndex(index)
        self._handle_item_clicked(index)

    def _handle_item_changed(self, item: ExtensionsListItem) -> None:
        is_checked = item.checkState() == Qt.Checked
        is_registered = item.extension.module

        if is_checked and not is_registered:
            item.extension.register()
        elif is_registered and not is_checked:
            item.extension.unregister()

    def _handle_item_mouse_over(self, index: QModelIndex) -> None:
        pass

    def _handle_item_clicked(self, index: QModelIndex) -> None:
        model = self.extension_list.model()
        item = model.itemFromIndex(index)

        readme_path = item.extension.path / "README.md"
        try:
            readme_text = readme_path.read_text()
        except (OSError, UnicodeDecodeError) as e:
            readme_text = "Not a valid README.md"
            logger.error("Invalid 'README.md' for extension: {}", item.extension.name)
            logger.error(e)

        self.extension_info.setMarkdown(readme_text)
