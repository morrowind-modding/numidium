from PySide6.QtWidgets import QFileSystemModel, QLabel, QTreeView, QVBoxLayout, QWidget

from numidium.ui.state import AppSettings


class Explorer(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.filesystem = QFileSystemModel()
        self.treeview = QTreeView()
        self.message = QLabel("Open a workspace to begin.")

        self.update_ui(AppSettings().workspace)
        self.setLayout(layout)

        AppSettings().workspace_changed.connect(self._handle_update_workspace)
        self.treeview.clicked.connect(self._handle_select_file)

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
            layout.addWidget(self.treeview)
        else:
            layout.addWidget(self.message)
