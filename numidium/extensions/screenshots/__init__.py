from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QWidget

from numidium.tes3.core import MorrowindInstall
from numidium.ui.activity_bar import ActivityBar, ActivityBarItem
from numidium.ui.explorer import Explorer
from numidium.ui.state import AppSettings
from numidium.ui.viewer import Viewer


class Container(QWidget):
    """Container that shows the screenshots folder for the current workspace, with the ability to select and view a screenshot."""

    _viewer: Viewer
    _explorer: Explorer
    _install: MorrowindInstall

    def __init__(self) -> None:
        super().__init__()
        self._viewer = Viewer()
        self._explorer = Explorer()
        self._explorer.setMaximumWidth(300)

        container_layout = QHBoxLayout()
        container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # type: ignore[call-overload]
        container_layout.addWidget(self._explorer)
        container_layout.addWidget(self._viewer)
        self.setLayout(container_layout)


        # TODO: REPLACE WITH CACHED VERSION
        self._install = MorrowindInstall()
        self._install.load(AppSettings().workspace)
        self._explorer.update_ui(str(self._install.directory_screenshots))
        AppSettings().workspace_changed.connect(self._handle_workspace_changed)

        # Connect widgets together.
        self._explorer.selected_filepath_changed.connect(self._viewer.handle_update_filepath)

    def _handle_workspace_changed(self, workspace: str) -> None:
        self._install.load(workspace)
        self._explorer.update_ui(str(self._install.directory_screenshots))
        self._viewer.clear()

    def load_screenshots_directory(self, directory: Path) -> None:
        self._explorer.update_ui(str(directory))


item = ActivityBarItem(widget=Container(), icon="icons:palette_24dp.svg", text="Screenshots")


def register() -> None:
    ActivityBar.instance().add_item(item)


def unregister() -> None:
    ActivityBar.instance().remove_item(item)
