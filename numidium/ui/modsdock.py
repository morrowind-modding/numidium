import operator

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDockWidget,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QMainWindow,
    QTableView,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from numidium.ui.explorer import Explorer
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


class TabsFrame(QFrame):
    """Widget that builds and shows the workspace's mod management options, including the current game engine. Mod management options are shown in a `QTabWidget` depending on the selected game engine."""

    def __init__(self) -> None:
        super().__init__()
        self.setFrameShadow(QFrame.Shadow.Plain)

        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignLeft)

        # TODO: Implement game engine selector.
        combobox_engine = QComboBox()
        container_layout.addWidget(combobox_engine)

        # TODO: Implement tabs classes.
        tabs = QTabWidget()
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
