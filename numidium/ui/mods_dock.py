from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QMainWindow,
    QPushButton,
    QTableView,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from numidium.config import config
from numidium.tes3.core import MorrowindInstall
from numidium.ui.enums import AlignmentFlag
from numidium.ui.widgets import DockToolbar, ObjectTableModel, PlaceholderWidget


# TODO: Add custom actions.
class ModsDockToolbar(DockToolbar):
    """Convenience class for the toolbar used on the Mods Dock.

    Contains custom actions and event handlers.
    """

    def __init__(self) -> None:
        super().__init__()


# TODO: Connect to real data. Implement literally any part of it.
dummy_installer_data = [[1, "Morrowind"], [2, "Bloodmoon"]]


class InstallersFrame(QFrame):
    """Widget that builds and shows the workspace's installer files."""

    def __init__(self) -> None:
        super().__init__()
        self.setFrameShadow(QFrame.Shadow.Plain)
        container_layout = QVBoxLayout()
        container_layout.setAlignment(AlignmentFlag.AlignLeft)

        self._table_installers = QTableView()
        self._table_installers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.model = ObjectTableModel(self, dummy_installer_data, ["Order", "Installers"])
        self._table_installers.setModel(self.model)
        self._table_installers.setSortingEnabled(True)

        container_layout.addWidget(self._table_installers)
        self.setLayout(container_layout)


# TODO: Connect engine to launcher button. Launch EXE.
# TODO: Load default engine from settings.
# TODO: Possibly allow user to add other programs, like Construction set or Mash.
class Launcher(QWidget):
    """Widget to allow user to launch an executable for the current environment."""

    def __init__(self) -> None:
        super().__init__()
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)

        combobox_engine = QComboBox()
        combobox_engine.addItems(["Morrowind.exe", "OpenMW"])
        button_launch = QPushButton(QIcon("icons:start_24dp.svg"), "Launch")

        container_layout.addWidget(combobox_engine)
        container_layout.addWidget(button_launch)
        self.setLayout(container_layout)


# TODO: Replace tab contents with implementations.
# TODO: Connect to extensions system, possibly.
class Tabs(QTabWidget):
    """Convenience class for Tab container of Mod tools tabs."""

    def __init__(self) -> None:
        super().__init__()

        # Add Load Order / Plugin tab.
        self._plugins_tab = PlaceholderWidget()
        self.addTab(self._plugins_tab, "  Plugins  ")

        # Add INI tab.
        self._ini_tab = PlaceholderWidget()
        self.addTab(self._ini_tab, "  INI  ")

        # Add Archives tab.
        self._archives_tab = PlaceholderWidget()
        self.addTab(self._archives_tab, "  Archives  ")

        # Add Saves tab.
        self._saves_tab = PlaceholderWidget()
        self.addTab(self._saves_tab, "  Saves  ")

    def load_workspace(self, install: MorrowindInstall) -> None:
        # TODO: Update tabs.
        pass


class TabsFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFrameShadow(QFrame.Shadow.Plain)

        container_layout = QVBoxLayout()
        container_layout.setAlignment(AlignmentFlag.AlignLeft)

        # TODO: Implement handling for game engine launcher change.
        self.launcher = Launcher()
        container_layout.addWidget(self.launcher)

        # TODO: Implement tabs classes.
        self.tabs = Tabs()
        container_layout.addWidget(self.tabs)

        self.setLayout(container_layout)

    def load_workspace(self, install: MorrowindInstall) -> None:
        # TODO: Update launcher.
        self.tabs.load_workspace(install)


class ModsDock(QMainWindow):
    """The Mods dock window.

    Contains tools for managing a mod installation.
    """

    morrowind_install: MorrowindInstall

    _toolbar: ModsDockToolbar
    _container: QWidget
    _layout: QHBoxLayout

    _installers_frame: InstallersFrame
    _tabs_frame: TabsFrame

    def __init__(self) -> None:
        super().__init__()

        # Configure UI
        self._container = QWidget()
        self._layout = QHBoxLayout()
        self._layout.setAlignment(AlignmentFlag.AlignHCenter)

        # Configure left panel - installers.
        self._installers_frame = InstallersFrame()
        self._layout.addWidget(self._installers_frame)

        # Configure right panel - tabs.
        self._tabs_frame = TabsFrame()
        self._layout.addWidget(self._tabs_frame)

        # Build container layout.
        self._container.setLayout(self._layout)
        self.setCentralWidget(self._container)

        # Child `self` into the higher-level parent window.
        layout = QVBoxLayout()
        layout.addWidget(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Load up Morrowind directory files.
        self.morrowind_install = MorrowindInstall()
        self.load_workspace(config.active_workspace)

        # Wrap up with toolbar.
        self._setup_toolbar()

    def _handle_workspace_changed(self, workspace: str) -> None:
        self.load_workspace(workspace)

    def load_workspace(self, workspace: str) -> None:
        if not workspace:
            return

        # Reload directory information.
        self.morrowind_install.load(workspace)

        # Update children if needed.
        # TODO: Update installers
        self._tabs_frame.load_workspace(self.morrowind_install)

    def _setup_toolbar(self) -> None:
        self._toolbar = ModsDockToolbar()
        self.addToolBar(self._toolbar)
