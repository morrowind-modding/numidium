import operator
from typing import Any

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
    Signal,
    SignalInstance,
)
from PySide6.QtGui import QAction, QDesktopServices, QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from numidium.config import config
from numidium.ui.application import Numidium


class PlaceholderWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is a placeholder widget! TODO: Replace it."))
        self.setLayout(layout)


class TextBlockLabel(QLabel):
    """Convenience subclass for `QLabel`.

    Subclasses `QLabel` and sets properties to allow for auto-expanding long text blocks.
    """

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setWordWrap(True)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)


class TitleLabel(QLabel):
    """Convenience subclass for `QLabel`.

    Subclasses `QLabel` and sets properties for text type 'Title.'
    """

    def __init__(self, text: str) -> None:
        super().__init__(text)
        font = self.font()
        font.setPointSize(36)
        font.setBold(True)
        self.setFont(font)


class SubtitleLabel(QLabel):
    """Convenience subclass for `QLabel`.

    Subclasses `QLabel` and sets properties for text type 'Subtitle.'
    """

    def __init__(self, text: str) -> None:
        super().__init__(text)
        font = self.font()
        font.setPointSize(16)
        font.setBold(True)
        self.setFont(font)


class OpenWorkspaceObject(QWidget):
    """Open Workspace base object.

    Base object that provides an 'open workspace' shared event handler for subclassing classes. Event handler selects Directory using a file dialog and updates application state.
    """

    def __init__(self) -> None:
        super().__init__()

    def _handle_open_workspace(self) -> None:
        workspace = QFileDialog.getExistingDirectory(
            self.parent(), "Open Directory", options=QFileDialog.Option.DontUseNativeDialog  # type: ignore[arg-type]
        )
        if workspace:
            Numidium.workspace_changed.emit(workspace)


class OpenWorkspaceAction(QAction, OpenWorkspaceObject):
    """Convenience subclass for `QAction,` `OpenWorkspaceObject`, for the Open Workspace action.

    `QAction` with default text, icon, shortcut, that implements `OpenWorkspaceObject` event handler.
    """

    def __init__(self) -> None:
        super().__init__(icon=QIcon("icons:folder_open_24dp.svg"), text="Open Workspace")
        self.setShortcut("Ctrl+Shift+O")
        self.triggered.connect(self._handle_open_workspace)


class OpenWorkspaceButton(QPushButton, OpenWorkspaceObject):
    """Convenience subclass for `QPushButton,` `OpenWorkspaceObject`, for the Open Workspace button.

    `QPushButton` with default text, icon, shortcut, that implements `OpenWorkspaceObject` event handler.
    """

    def __init__(self) -> None:
        super().__init__(icon=QIcon("icons:folder_open_24dp.svg"), text="Open Workspace ")

        self.setCheckable(True)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.clicked.connect(self._handle_open_workspace)


class OpenGithubButton(QPushButton):
    """Convenience subclass for `QPushButton for the Open Github button.

    `QPushButton` with default text, icon, that opens the project source code on GitHub when clicked.
    """

    def __init__(self) -> None:
        super().__init__(text="Open Source Code")

        self.setCheckable(True)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.clicked.connect(self._handle_open_github)

    def _handle_open_github(self) -> None:
        QDesktopServices.openUrl("https://github.com/morrowind-modding/numidium")


class DockToolbar(QToolBar):
    """Convenience subclass for `QToolBar` for the Dock toolbars.

    `QToolBar` with default actions and buttons. User can add additional actions and buttons through class methods.

    Attributes
    ----------
    action_open_workspace : OpenWorkspaceAction
        An action for opening a workspace.
    """

    action_open_workspace: OpenWorkspaceAction

    def __init__(self) -> None:
        super().__init__()

        # Setup Widgets
        self.action_open_workspace = OpenWorkspaceAction()
        self.addAction(self.action_open_workspace)
        self.addSeparator()

        # TODO: Implement ability to add custom actions and widgets here.

        # Fill the rest with a spacer.
        spacer = QToolButton()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        spacer.setEnabled(False)
        self.addWidget(spacer)


class StepperItem(QWidget):
    """Convenience subclass for use in conjunction with `Stepper`. Represents a step in a multi-step widget.

    Subclassing objects should manage step validity through attributes or class methods, so that `Stepper` can update accordingly.

    Attributes
    ----------
    valid_changed : Signal(bool)
        A `Signal` that emits when the `valid` attribute is changed.
    valid : bool
        The current state of the step. If true, step is valid.
    validation_message : str
        The current validation message.
    """

    valid_changed: SignalInstance = Signal(bool)  # type: ignore[assignment]
    valid: bool
    validation_message: str

    def __init__(self) -> None:
        super().__init__()
        self.valid = False
        self.validation_message = ""

    def set_valid(self, valid: bool = True, validation_message: str = "") -> None:
        self.valid = valid
        self.validation_message = validation_message
        self.valid_changed.emit(self.valid)


class Stepper(QWidget):
    """Convenience subclass for use in conjunction with `Stepper`. Represents a step in a multi-step widget.

    Subclassing objects should manage step validity through attributes or class
    methods, so that `Stepper` can update accordingly.

    Attributes
    ----------
    stepper_finish_clicked : Signal
        A `Signal` that emits when the 'Finish' button is clicked and the stepper is completed.
    items : list[StepperItem]
        A list of the stepper items.
    active_item : StepperItem
        The currently shown stepper item.
    """

    stepper_finish_clicked: SignalInstance = Signal()  # type: ignore[assignment]

    items: list[StepperItem]
    active_item: StepperItem

    _current_step: int
    _last_step: int
    _label_validation_message: TextBlockLabel
    _layout: QVBoxLayout
    _container: QWidget
    _container_layout: QVBoxLayout
    _container_stepper: QWidget
    _button_left: QPushButton
    _button_right: QPushButton
    _button_finish: QPushButton

    def __init__(self, items: list[StepperItem]) -> None:
        super().__init__()
        self._items = items
        self._current_step = 1
        self._last_step = len(items)
        self._layout = QVBoxLayout()
        self._container = QWidget()
        self._container_layout = QVBoxLayout()
        for item in self._items:
            self._container_layout.addWidget(item)
            item.valid_changed.connect(self._handle_item_valid_changed)
        self._container.setLayout(self._container_layout)
        self.setLayout(self._layout)

        self._layout.addWidget(self._container)

        self._setup_stepper()
        self._update_active_step()
        self._layout.addWidget(self._container_stepper)

    def _setup_stepper(self) -> None:
        self._container_stepper = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)  # type: ignore[call-overload]

        self._label_validation_message = TextBlockLabel("")
        font = self._label_validation_message.font()
        font.setItalic(True)
        font.setBold(True)
        self._label_validation_message.setFont(font)
        self._button_left = QPushButton("< Prev")
        self._button_right = QPushButton("> Next")
        self._button_finish = QPushButton("Finish")

        layout.addWidget(self._label_validation_message)
        layout.addWidget(self._button_left)
        layout.addWidget(self._button_right)
        layout.addWidget(self._button_finish)

        self._container_stepper.setLayout(layout)

        self._button_left.clicked.connect(self._handle_open_previous_step)
        self._button_right.clicked.connect(self._handle_open_next_step)
        self._button_finish.clicked.connect(self._handle_complete_stepper)

    def _handle_item_valid_changed(self, valid: bool) -> None:
        if self._current_step == self._last_step:
            self._button_finish.setEnabled(valid)
        else:
            self._button_right.setEnabled(valid)
        self._update_active_step()

    def _handle_open_previous_step(self) -> None:
        if self._current_step > 1:
            self._current_step -= 1
            self._update_active_step()

    def _handle_open_next_step(self) -> None:
        if self._current_step < self._last_step:
            self._current_step += 1
            self._update_active_step()

    def _handle_complete_stepper(self) -> None:
        self.stepper_finish_clicked.emit()

    def _update_stepper(self) -> None:
        if self._current_step == 1:
            self._button_left.setEnabled(False)
        else:
            self._button_left.setEnabled(True)

        if self._current_step == self._last_step:
            self._button_right.setVisible(False)
            self._button_finish.setVisible(True)
            self._button_finish.setEnabled(self.active_item.valid)
        else:
            self._button_right.setVisible(True)
            self._button_finish.setVisible(False)
            self._button_right.setEnabled(self.active_item.valid)

    def _update_active_step(self) -> None:
        layout = self._container_layout
        for i in range(layout.count()):
            layout.itemAt(i).widget().setVisible(False)

        self.active_item = self._items[self._current_step - 1]
        self.active_item.setVisible(True)
        if self.active_item.valid == False:
            self._label_validation_message.setText(self.active_item.validation_message)
        else:
            self._label_validation_message.setText("")

        self._update_stepper()


class ObjectTableModel(QAbstractTableModel):
    """Convienence class for `QAbstractTableModel` that allows for managing data with an `QTableView` object."""

    _list: list[Any]
    header: list[str]

    def __init__(self, parent: QWidget, items: list[Any], header: list[str]) -> None:
        super().__init__(parent)
        self._list = items
        self.header = header

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QPersistentModelIndex()) -> int:
        return len(self._list)

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex = QPersistentModelIndex()) -> int:
        if self._list:
            return len(self._list[0])
        else:
            return 0

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = 0) -> Any:
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:  # type: ignore[comparison-overlap]
            return None
        return self._list[index.row()][index.column()]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = 0) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:  # type: ignore[comparison-overlap]
            return self.header[section]
        return None

    def sort(self, col: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder) -> None:
        """sort table by given column number col"""
        if col < len(self._list):
            self._list = sorted(self._list, key=operator.itemgetter(col))
            if order == Qt.DescendingOrder:
                self._list.reverse()
            self.dataChanged.emit(QModelIndex(), QModelIndex())
