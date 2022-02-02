from PySide6.QtCore import QFileSystemWatcher, QObject, Signal

from numidium.config import config


class Signals(QObject):
    workspace_changed = Signal(str)

    watcher: QFileSystemWatcher
    directory_changed = Signal(str)
    file_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.workspace_changed.connect(self.handle_workspace_changed)

        self.watcher = QFileSystemWatcher(parent=self)
        self.watcher.directoryChanged.connect(self.directory_changed.emit)
        self.watcher.fileChanged.connect(self.file_changed.emit)

    def handle_workspace_changed(self, workspace: str) -> None:
        config.active_workspace = workspace
