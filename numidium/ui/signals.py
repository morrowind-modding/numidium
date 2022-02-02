from datetime import datetime
from os.path import isdir

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
        if isdir(workspace):
            self.update_active_worskpace(workspace)
            self.update_recent_workspaces(workspace)

    def update_active_worskpace(self, workspace: str) -> None:
        # self.watcher.removePath(config.active_workspace)
        # self.watcher.addPath(workspace)
        config.active_workspace = workspace

    def update_recent_workspaces(self, workspace: str) -> None:
        """Update and sort the list of recent workspaces."""
        # TODO: move this to Config class
        config.recent_workspaces[workspace] = int(datetime.now().timestamp())
        items = list(config.recent_workspaces.items())
        items.sort(key=lambda x: x[1], reverse=True)
        config.recent_workspaces.clear()
        config.recent_workspaces.update(items)
        config.save_path()
