from functools import partial

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileSystemModel,
    QLabel,
    QMenu,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from numidium.ui.state import AppSettings
from numidium.ui.utility import OperatingSystemUtility


class Explorer(QWidget):
    """
    A file explorer widget for the current workspace, including an extensible context menu.
    """

    os_utility: OperatingSystemUtility
    filesystem: QFileSystemModel
    treeview: QTreeView
    message: QLabel

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.os_utility = OperatingSystemUtility()
        self.filesystem = QFileSystemModel()
        self.treeview = QTreeView()
        self.message = QLabel("Open a workspace to begin.")

        self.update_ui(AppSettings().workspace)
        self.setLayout(layout)

        AppSettings().workspace_changed.connect(self._handle_update_workspace)
        self.treeview.clicked.connect(self._handle_select_file)

        # Setup custom context menu for tree view.
        self.treeview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeview.customContextMenuRequested.connect(self._handle_custom_context_menu)

    def _handle_custom_context_menu(self, position: QPoint) -> None:
        index = self.treeview.selectedIndexes()[0]
        if not index:
            return

        filepath = self.filesystem.filePath(index)

        menu = QMenu()

        # Application actions.
        action_view = QAction("View", self)
        menu.addAction(action_view)

        action_view.triggered.connect(partial(self._handle_context_view, filepath))

        menu.addSeparator()

        # System actions.
        action_open_os_default = QAction("Open with System...", self)
        menu.addAction(action_open_os_default)
        action_open_os_explorer = QAction("Reveal in System Explorer", self)
        menu.addAction(action_open_os_explorer)

        action_open_os_default.triggered.connect(partial(self._handle_context_open_filepath, filepath))
        action_open_os_explorer.triggered.connect(partial(self._handle_context_open_explorer, filepath))

        menu.exec_(self.treeview.viewport().mapToGlobal(position))

    def _handle_context_view(self, filepath: str) -> None:
        AppSettings().active_file = filepath

    def _handle_context_open_filepath(self, filepath: str) -> None:
        self.os_utility.open_filepath_with_default_application(filepath)

    def _handle_context_open_explorer(self, filepath: str) -> None:
        self.os_utility.open_filepath_with_explorer(filepath)

    def _handle_update_workspace(self, workspace: str) -> None:
        self.update_ui(workspace)

    def _handle_select_file(self, item: str) -> None:
        index = self.treeview.selectedIndexes()[0]
        AppSettings().active_file = self.filesystem.filePath(index)  # type: ignore[arg-type]

    def update_ui(self, workspace: str) -> None:
        layout = self.layout()
        for i in range(layout.count()):
            layout.removeWidget(layout.itemAt(i).widget())

        if workspace:
            self.filesystem.setRootPath(workspace)
            self.treeview.setModel(self.filesystem)
            self.treeview.setRootIndex(self.filesystem.index(workspace))
            for i in range(1, self.filesystem.columnCount()):
                self.treeview.hideColumn(i)
            layout.addWidget(self.treeview)
        else:
            layout.addWidget(self.message)
