from PySide6.QtCore import Qt, Signal
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

from numidium.ui.state import AppSettings


class TextBlockLabel(QLabel):
    def __init__(self, text) -> None:
        super().__init__(text)
        self.setWordWrap(True)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)


class TitleLabel(QLabel):
    def __init__(self, text) -> None:
        super().__init__(text)
        font = self.font()
        font.setPointSize(36)
        font.setBold(True)
        self.setFont(font)


class SubtitleLabel(QLabel):
    def __init__(self, text) -> None:
        super().__init__(text)
        font = self.font()
        font.setPointSize(16)
        font.setBold(True)
        self.setFont(font)


class OpenWorkspaceObject(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

    def _open_workspace(self) -> None:
        workspace = QFileDialog.getExistingDirectory(
            self.parent(), "Open Directory", options=QFileDialog.Option.DontUseNativeDialog
        )
        if workspace != "":
            AppSettings().workspace = workspace
            AppSettings().add_recent_workspace(AppSettings().workspace)


class OpenWorkspaceAction(QAction, OpenWorkspaceObject):
    def __init__(self, parent=None) -> None:
        super().__init__(
            parent=parent, icon=QIcon("icons:folder_open_24dp.svg"), text="Open Workspace", shortcut="Ctrl+Shift+O"
        )

        self.triggered.connect(self._open_workspace)


class OpenWorkspaceButton(QPushButton, OpenWorkspaceObject):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent, icon=QIcon("icons:folder_open_24dp.svg"), text="Open Workspace ")

        self.setCheckable(True)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.clicked.connect(self._open_workspace)


class OpenGithubButton(QPushButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent, text="Open Source Code")

        self.setCheckable(True)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.clicked.connect(self._open_github)

    def _open_github(self):
        QDesktopServices.openUrl("https://github.com/morrowind-modding/numidium")

class ChangeDarkModeButton(QPushButton):
    def __init__(self, parent=None) -> None:
        super().__init__(text ="Dark Mode", parent=parent)
        self.setIcon(QIcon("icons:contrast_24dp.svg"))
        self.setCheckable(True)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.clicked.connect(self._change_theme)
        self.setChecked(AppSettings().enable_dark_mode)

    def _change_theme(self) -> None:
        AppSettings().enable_dark_mode = self.sender().isChecked()

class DockToolbar(QToolBar):
    action_open_workspace: OpenWorkspaceAction
    button_dark_mode: ChangeDarkModeButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.actions = []
        self.widgets = []

        # Setup Widgets
        self.action_open_workspace = OpenWorkspaceAction(parent=self)
        self.addAction(self.action_open_workspace)
        self.addSeparator()

        # TODO: Implement ability to add custom actions and widgets here.

        # Fill the rest with a spacer.
        spacer = QToolButton(parent=self)
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        spacer.setEnabled(False)
        self.addWidget(spacer)

        # Add dark mode toggle at the end.
        self.button_dark_mode = ChangeDarkModeButton(parent=self)
        self.addWidget(self.button_dark_mode)

class StepperItem(QWidget):
    valid_changed = Signal(bool)
    valid: bool
    validation_message: str

    def __init__(self) -> None:
        super().__init__()
        self.valid = False
        self.validation_message = ""

    def set_valid(self, valid=True, validation_message=""):
        self.valid = valid
        self.validation_message = validation_message
        self.valid_changed.emit(self.valid)


class Stepper(QWidget):
    stepper_finish_clicked = Signal()

    current_step: int
    last_step: int

    items: list[StepperItem]
    active_item: StepperItem
    label_validation_message: TextBlockLabel

    layout: QVBoxLayout
    container: QWidget
    container_layout: QVBoxLayout
    container_stepper: QWidget

    def __init__(self, items: list[StepperItem]) -> None:
        super().__init__()
        self.items = items
        self.current_step = 1
        self.last_step = len(items)
        self.layout = QVBoxLayout()
        self.container = QWidget()
        self.container_layout = QVBoxLayout()
        for item in self.items:
            self.container_layout.addWidget(item)
            item.valid_changed.connect(self._item_valid_changed)
        self.container.setLayout(self.container_layout)
        self.setLayout(self.layout)

        self.layout.addWidget(self.container)

        self._setup_stepper()
        self._update_active_step()
        self.layout.addWidget(self.container_stepper)

    def _setup_stepper(self):
        self.container_stepper = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)

        self.label_validation_message = TextBlockLabel("")
        font = self.label_validation_message.font()
        font.setItalic(True)
        font.setBold(True)
        self.label_validation_message.setFont(font)
        self.button_left = QPushButton("< Prev")
        self.button_right = QPushButton("> Next")
        self.button_finish = QPushButton("Finish")

        layout.addWidget(self.label_validation_message)
        layout.addWidget(self.button_left)
        layout.addWidget(self.button_right)
        layout.addWidget(self.button_finish)

        self.container_stepper.setLayout(layout)

        self.button_left.clicked.connect(self._open_previous_step)
        self.button_right.clicked.connect(self._open_next_step)
        self.button_finish.clicked.connect(self._complete_stepper)

    def _item_valid_changed(self, valid):
        if self.current_step == self.last_step:
            self.button_finish.setEnabled(valid)
        else:
            self.button_right.setEnabled(valid)
        self._update_active_step()

    def _open_previous_step(self):
        if self.current_step > 1:
            self.current_step -= 1
            self._update_active_step()

    def _open_next_step(self):
        if self.current_step < self.last_step:
            self.current_step += 1
            self._update_active_step()

    def _complete_stepper(self):
        self.stepper_finish_clicked.emit()

    def _update_stepper(self):
        if self.current_step == 1:
            self.button_left.setEnabled(False)
        else:
            self.button_left.setEnabled(True)

        if self.current_step == self.last_step:
            self.button_right.setVisible(False)
            self.button_finish.setVisible(True)
            self.button_finish.setEnabled(self.active_item.valid)
        else:
            self.button_right.setVisible(True)
            self.button_finish.setVisible(False)
            self.button_right.setEnabled(self.active_item.valid)

    def _update_active_step(self):
        layout = self.container_layout
        for i in range(layout.count()):
            layout.itemAt(i).widget().setVisible(False)

        self.active_item = self.items[self.current_step - 1]
        self.active_item.setVisible(True)
        if self.active_item.valid == False:
            self.label_validation_message.setText(self.active_item.validation_message)
        else:
            self.label_validation_message.setText("")

        self._update_stepper()
