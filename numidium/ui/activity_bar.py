from __future__ import annotations

from typing import ClassVar

from PySide6.QtCore import QObject, QSize, Qt, Signal
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QFont,
    QIcon,
    QLinearGradient,
    QPainter,
)
from PySide6.QtWidgets import (
    QDockWidget,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QWidget,
)
from qtvscodestyle import Vsc, theme_icon  # type: ignore

from numidium.core.extensions import reload_active_extensions
from numidium.ui.content_browser_dock import ContentBrowserDock
from numidium.ui.extensions_dock import ExtensionsDock
from numidium.ui.mods_dock import ModsDock

GRADIENT = QLinearGradient(0, 0, 128, 128)
GRADIENT.setColorAt(0, QColor(242, 220, 134))
GRADIENT.setColorAt(1, QColor(177, 128, 62))
GRADIENT_BRUSH = QBrush(GRADIENT)


class ActivityBarItem(QListWidgetItem, QObject):
    """A custom widget that can be added to the application activity bar."""

    hovered = Signal()
    toggled = Signal(bool)
    triggered = Signal()

    _action: QAction
    _widget: QWidget

    def __init__(self, widget: QWidget, icon: QIcon | str, text: str):
        super().__init__()

        icon = self._create_icon(icon)

        font = self.font()
        font.setPointSize(10)
        font.setWeight(QFont.Weight.DemiBold)

        self.setIcon(icon)
        self.setFont(font)
        self.setText(text.upper())

        # The associated window that is visible while active.
        self._widget = widget

        # Make an action that forwards its events to the widget.
        self._action = QAction(text)
        self._action.hovered.connect(self.hovered.emit)
        self._action.toggled.connect(self.toggled.emit)
        self._action.triggered.connect(self.triggered.emit)

    @staticmethod
    def _create_icon(icon: QIcon | str) -> QIcon:
        icon = QIcon(icon) if isinstance(icon, str) else icon

        pixmap = icon.pixmap(128, 128)
        mask = pixmap.mask()

        painter = QPainter(pixmap)
        painter.fillRect(pixmap.rect(), GRADIENT_BRUSH)
        painter.end()

        pixmap.setMask(mask)

        icon = QIcon(pixmap)
        icon.addPixmap(pixmap, QIcon.Selected)

        return icon


class ActivityBar(QDockWidget):
    """The application's activity bar.

    This is the left-most area of the application window. It contains a list of `ActivityBarItem` objects that when
    selected will display their associated widget in the main window's viewport.
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
        self._list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self._list.currentItemChanged.connect(self.set_current_item)
        self._list.setStyleSheet(
            """
            QListWidget { background: #333333; }
            QListWidget::item:selected { color: #F2DC86; background: #444444; }
            """
        )

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
                icon=theme_icon(Vsc.PACKAGE),
                text="Mods",
            )
        )
        self.add_item(
            ActivityBarItem(
                widget=ContentBrowserDock(),
                icon=theme_icon(Vsc.BROWSER),
                text="Content Browser",
            )
        )
        self.add_item(
            ActivityBarItem(
                widget=ExtensionsDock(),
                icon=theme_icon(Vsc.EXTENSIONS),
                text="Extensions",
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
