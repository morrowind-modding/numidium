from datetime import datetime

from PySide6.QtCore import QObject, Signal

from numidium.config import config


class Signals(QObject):
    workspace_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.workspace_changed.connect(self.handle_workspace_changed)

    def handle_workspace_changed(self, workspace: str) -> None:
        if workspace != config.active_workspace:
            config.active_workspace = workspace
            config.recent_workspaces[workspace] = int(datetime.now().timestamp())

            # Limit to maximum of 5 recent workspaces. TODO: customizable
            if len(config.recent_workspaces) > 5:
                # sort by time
                items = list(config.recent_workspaces.items())
                items.sort(key=lambda x: x[1], reverse=True)
                # take first 5
                config.recent_workspaces.clear()
                config.recent_workspaces.update(items[:5])

            config.save_path()
