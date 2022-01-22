from os import path
from pathlib import Path

from PySide6.QtCore import QFile, QPoint, Qt, Signal
from PySide6.QtGui import QAction, QClipboard, QGuiApplication
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileSystemModel,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMenu,
    QMessageBox,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from numidium.logger import logger
from numidium.ui.state import AppSettings
from numidium.ui.utility import OperatingSystemUtility


class Explorer(QWidget):
    """
    A file explorer widget for the current workspace, including an extensible context menu.
    """
    selected_filepath_changed = Signal(str)

    os_utility: OperatingSystemUtility
    filesystem: QFileSystemModel
    treeview: QTreeView
    message: QLabel

    selected_filepath: str
    context_filepath: str

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.os_utility = OperatingSystemUtility()
        self.filesystem = QFileSystemModel()
        self.treeview = QTreeView()
        self.filesystem.setReadOnly(False)
        self.treeview.setSelectionMode(QAbstractItemView.SingleSelection)
        self.treeview.setDragEnabled(True)
        self.treeview.setDropIndicatorShown(True)
        self.treeview.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.treeview.setAcceptDrops(True)

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

        self.context_filepath = self.filesystem.filePath(index)

        menu = QMenu()

        # Application actions.
        action_view = QAction("View", self)
        menu.addAction(action_view)
        action_view.triggered.connect(self._handle_context_view)

        menu.addSeparator()

        # System Open actions.
        action_open_os_default = QAction("Open with Default Application", self)
        menu.addAction(action_open_os_default)
        action_open_os_default.triggered.connect(self._handle_context_open_filepath)

        action_open_os_explorer = QAction("Reveal in System Explorer", self)
        menu.addAction(action_open_os_explorer)
        action_open_os_explorer.triggered.connect(self._handle_context_open_explorer)

        menu.addSeparator()

        # System Cut/Copy actions.
        action_cut = QAction("Cut", self)
        menu.addAction(action_cut)
        action_cut.setEnabled(False)

        action_copy = QAction("Copy", self)
        menu.addAction(action_copy)
        action_copy.setEnabled(False)

        action_copy_path = QAction("Copy Path", self)
        menu.addAction(action_copy_path)
        action_copy_path.triggered.connect(self._handle_context_copy_path)

        action_copy_relative_path = QAction("Copy Relative Path", self)
        menu.addAction(action_copy_relative_path)
        action_copy_relative_path.triggered.connect(self._handle_context_copy_relative_path)

        menu.addSeparator()

        # System dangerous actions: rename, delete. Requires confirmations.
        action_rename = QAction("Rename", self)
        menu.addAction(action_rename)
        action_rename.triggered.connect(self._handle_context_rename)

        action_delete = QAction("Delete", self)
        menu.addAction(action_delete)
        action_delete.triggered.connect(self._handle_context_delete)


        menu.exec_(self.treeview.viewport().mapToGlobal(position))

    def _handle_context_view(self) -> None:
        self._handle_select_file()

    def _handle_context_open_filepath(self) -> None:
        self.os_utility.open_filepath_with_default_application(self.context_filepath)

    def _handle_context_open_explorer(self) -> None:
        self.os_utility.open_filepath_with_explorer(self.context_filepath)

    def _handle_context_copy_path(self) -> None:
        clipboard: QClipboard = QGuiApplication.clipboard()
        clipboard.setText(self.context_filepath)

    # TODO: Replace os.path with something else?
    def _handle_context_copy_relative_path(self) -> None:
        clipboard: QClipboard = QGuiApplication.clipboard()
        workspace: str = AppSettings().workspace
        relative_filepath: str = path.relpath(self.context_filepath, workspace)
        clipboard.setText(relative_filepath)

    def _handle_context_rename(self) -> None:
        path: Path = Path(self.context_filepath)
        name: str = path.name
        directory: str = path.parent
        text, ok = QInputDialog.getText(self, "Rename File", "Enter a new file name:", QLineEdit.EchoMode.Normal, name)
        if ok:
            new_path: Path = Path.joinpath(directory, text)
            path.rename(new_path)
            logger.debug("Renamed {path} to {new_path}", path=self.context_filepath, new_path = new_path)


    def _handle_context_delete(self) -> None:
        msgBox = QMessageBox()
        msgBox.setText("Are you sure you want to delete this file? It will be placed in your system recycling bin.")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel)
        result: int = msgBox.exec()

        match result:
            case QMessageBox.Yes:
                # Save was clicked. Commit the action.
                file: QFile = QFile(self.context_filepath)
                trashed: bool = file.moveToTrash()
                if not trashed:
                    logger.error("Unable to delete file: {file}", file=self.context_filepath)
                else:
                    logger.debug("Deleted file: {path}", path=self.context_filepath)

            case QMessageBox.Cancel:
                # Cancel was clicked. Return.
                return
            case _:
                # should never be reached
                raise Exception("Invalid message box result when deleting file.")

    def _handle_update_workspace(self, workspace: str) -> None:
        self.update_ui(workspace)

    def _handle_select_file(self) -> None:
        index = self.treeview.selectedIndexes()[0]
        self.selected_filepath = self.filesystem.filePath(index)  # type: ignore[arg-type]
        self.selected_filepath_changed.emit(self.selected_filepath)

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
