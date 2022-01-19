from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDockWidget,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QMainWindow,
    QPushButton,
    QTableView,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from numidium.ui.widgets import DockToolbar, ObjectTableModel


# TODO: Add custom actions.
class ModsDockToolbar(DockToolbar):
    """Convenience class for the toolbar used on the Mods Dock. Contains custom actions and event handlers."""

    def __init__(self) -> None:
        super().__init__()


# TODO: Connect to real data. Implement literally any part of it.
dummy_installer_data = [[1, "Morrowind"], [2, "Bloodmoon"]]


class InstallersFrame(QFrame):
    """Widget that builds and shows the workspace's installer files in a `QTableView`, as well as does formatting and event handling."""

    def __init__(self) -> None:
        super().__init__()
        self.setFrameShadow(QFrame.Shadow.Plain)
        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignLeft)

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
    """Widget to allow user to select a game-engine or other executable from a dropdown and launch it for the current environment."""

    def __init__(self) -> None:
        super().__init__()
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)

        combobox_engine = QComboBox()
        combobox_engine.addItems(["Morrowind.exe", "OpenMW"])
        button_launch = QPushButton("Launch")

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
        self._plugins_tab = QWidget()
        self.addTab(self._plugins_tab, "  Plugins  ")

        # Add INI tab.
        self._ini_tab = QWidget()
        self.addTab(self._ini_tab, "  INI  ")

        # Add Archives tab.
        self._archives_tab = QWidget()
        self.addTab(self._archives_tab, "  Archives  ")

        # Add Saves tab.
        self._saves_tab = QWidget()
        self.addTab(self._saves_tab, "  Saves  ")

        # Add Screenshots tab.
        self._screenshots_tab = QWidget()
        self.addTab(self._screenshots_tab, "  Screenshots  ")


class TabsFrame(QFrame):
    """Widget that builds and shows the workspace's mod management options, including the current game engine. Mod management options are shown in a `QTabWidget` depending on the selected game engine."""

    def __init__(self) -> None:
        super().__init__()
        self.setFrameShadow(QFrame.Shadow.Plain)

        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignLeft)

        # TODO: Implement handling for game engine launcher change.
        self.launcher = Launcher()
        container_layout.addWidget(self.launcher)

        # TODO: Implement tabs classes.
        tabs = Tabs()
        container_layout.addWidget(tabs)

        self.setLayout(container_layout)


class ModsDock(QMainWindow):
    """The Mods dock window. Contains tools for managing a mod installation."""

    _toolbar: ModsDockToolbar
    _container: QWidget
    _layout: QHBoxLayout

    _installers_frame: InstallersFrame
    _tabs_frame: TabsFrame

    _bottom_dock: QDockWidget

    def __init__(self) -> None:
        super().__init__()

    def setup_ui(self, win: QWidget) -> None:
        """Set up ui."""
        self._container = QWidget()
        self._layout = QHBoxLayout()
        self._layout.setAlignment(Qt.AlignHCenter)

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
        layout = QVBoxLayout(win)
        layout.addWidget(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Wrap up with toolbar and bottom dock.
        self._setup_toolbar()
        self._setup_bottom_dock()

    def _setup_toolbar(self):
        self._toolbar = ModsDockToolbar()
        self.addToolBar(self._toolbar)

    def _setup_bottom_dock(self):
        # Dock Widgets
        self._bottom_dock = QDockWidget("Bottom dock")
        self._bottom_dock.setWidget(QTextEdit("This is the bottom widget. -- NI"))
        self._bottom_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea
            | Qt.DockWidgetArea.RightDockWidgetArea
            | Qt.DockWidgetArea.BottomDockWidgetArea
            | Qt.DockWidgetArea.TopDockWidgetArea
        )
        self._bottom_dock.setFeatures(QDockWidget.DockWidgetClosable.DockWidgetMovable)

        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._bottom_dock)
