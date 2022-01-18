from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileSystemModel, QLabel, QTreeView, QVBoxLayout, QWidget
from numidium.ui.state import AppSettings


class Explorer(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.filesystem = QFileSystemModel()
        self.treeview = QTreeView()
        self.message = QLabel("Open a workspace to begin.")

        self.update_ui(AppSettings().workspace)
        self.setLayout(layout)

        AppSettings().workspace_changed.connect(self._update_workspace)
        self.treeview.clicked.connect(self._select_file)

    def _update_workspace(self, workspace):
        self.update_ui(workspace)

    def _select_file(self, item):
        index = self.treeview.selectedIndexes()[0]
        AppSettings().active_file = self.filesystem.filePath(index)

    def update_ui(self, workspace):
        layout = self.layout()
        for i in range(layout.count()):
            layout.removeWidget(layout.itemAt(i).widget())

        if workspace:
            self.filesystem.setRootPath(workspace)
            self.treeview.setModel(self.filesystem)
            self.treeview.setRootIndex(self.filesystem.index(workspace))
            layout.addWidget(self.treeview)
        else:
            layout.addWidget(self.message)
