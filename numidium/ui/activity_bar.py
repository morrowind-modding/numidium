from __future__ import annotations

from typing import ClassVar

from PySide6.QtCore import QSize, Qt, Signal, SignalInstance
from PySide6.QtGui import QAction, QFont, QIcon
from PySide6.QtWidgets import (
    QDockWidget,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QWidget,
)

from numidium.core.extensions import reload_active_extensions
from numidium.ui.content_browser_dock import ContentBrowserDock
from numidium.ui.extensions_dock import ExtensionsDock
from numidium.ui.mods_dock import ModsDock
from numidium.ui.settings_dock import SettingsDock


class ActivityBarItem(QListWidgetItem):
    """A custom widget that can be added to the application activity bar."""

    hovered: SignalInstance = Signal()  # type: ignore[assignment]
    toggled: SignalInstance = Signal(bool)  # type: ignore[assignment]
    triggered: SignalInstance = Signal()  # type: ignore[assignment]

    _action: QAction
    _widget: QWidget

    def __init__(self, widget: QWidget, icon: QIcon | str, text: str):
        super().__init__()

        self.setIcon(QIcon(icon) if isinstance(icon, str) else icon)
        self.setText(text)

        font = self.font()
        font.setPointSize(10)
        font.setWeight(QFont.Weight.DemiBold)
        self.setFont(font)

        # The associated window that is visible while active.
        self._widget = widget

        # Make an action that forwards its events to the widget.
        self._action = QAction(self.icon(), text)
        self._action.setCheckable(True)
        self._action.hovered.connect(self.hovered.emit)
        self._action.toggled.connect(self.toggled.emit)
        self._action.triggered.connect(self.triggered.emit)


class ActivityBar(QDockWidget):
    """The application's activity bar.

    This is the left-most area of the application window. It contains a list of
    `ActivityBarItem` objects that when selected will display their associated
    widget in the main window's viewport.
    """

    # Container for ActivityBarItem widgets.
    _list: QListWidget

    # Container for associated view widgets.
    _view: QStackedWidget

    # Global instance
    _instance: ClassVar[ActivityBar]

    def __init__(self) -> None:
        super().__init__()

        self._list = QListWidget()
        self._list.setIconSize(QSize(28, 28))
        self._list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._list.currentItemChanged.connect(self.set_current_item)

        self._view = QStackedWidget()

        # Customize Look

        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setTitleBarWidget(QWidget())  # hide title bar
        self.setMinimumWidth(self._list.iconSize().width() + 12)
        self.setWidget(self._list)

        # Default Items

        self.add_item(
            ActivityBarItem(
                widget=ModsDock(),
                icon="icons:widgets_24dp.svg",
                text="Mods",
            )
        )
        self.add_item(
            ActivityBarItem(
                widget=ContentBrowserDock(),
                icon="icons:flip_to_front_24dp.svg",
                text="Content Browser",
            )
        )
        self.add_item(
            ActivityBarItem(
                widget=ExtensionsDock(),
                icon="icons:settings_24dp.svg",
                text="Extensions",
            )
        )
        self.add_item(
            ActivityBarItem(
                widget=SettingsDock(),
                icon="icons:settings_24dp.svg",
                text="Settings",
            )
        )

        # Make accessible to extensions.
        # TODO: Figure out a proper api.
        if not hasattr(self, "_instance"):
            type(self)._instance = self
            reload_active_extensions()

    def add_item(self, item: ActivityBarItem) -> None:
        """Add a new item to the activity bar."""
        self._list.addItem(item)
        self._view.addWidget(item._widget)

    def remove_item(self, item: ActivityBarItem) -> None:
        """Remove an item from the activity bar."""
        i = self._list.indexFromItem(item).row()
        if i != -1:
            self._list.takeItem(i)
            self._view.removeWidget(item._widget)

    def set_current_item(self, item: ActivityBarItem) -> None:
        """Set the currently active item in the activity bar."""
        i = self._list.indexFromItem(item).row()
        if i != -1:
            self._list.setCurrentRow(i)
            self._view.setCurrentIndex(i)

    @classmethod
    def instance(cls) -> ActivityBar:
        """Get the main application's ActivityBar instance."""
        return cls._instance
