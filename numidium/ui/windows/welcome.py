from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from numidium.config import config
from numidium.logger import logger
from numidium.ui.application import Numidium
from numidium.ui.widgets import (
    OpenGithubButton,
    OpenWorkspaceButton,
    Stepper,
    StepperItem,
    SubtitleLabel,
    TextBlockLabel,
)
from numidium.ui.windows.abstractmain import AbstractMainWindow


class ConfigurationStepOneWidget(StepperItem):
    description_label: TextBlockLabel
    open_workspace_button: QPushButton
    open_workspace_line: QLineEdit

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # type: ignore[call-overload]

        self.description_label = TextBlockLabel(
            "Welcome to Numidium! This multi-tool offers the ability to manage and edit your Morrowind mods, while remaining highly extensible through plugins and user settings. To get started, open a workspace! Workspaces represent a particular install of Morrowind. Simply navigate to the folder that contains your Morrowind.exe file and choose open directory. Note: After setting up your first workspace, you will be able to open and manage multiple workspaces."
        )
        self.description_label.adjustSize()

        workspace_container = QWidget()
        workspace_container_layout = QHBoxLayout()

        self.open_workspace_button = QPushButton(icon=QIcon("icons:folder_open_24dp.svg"), text="Open Workspace ")
        self.open_workspace_line = QLineEdit()
        self.open_workspace_line.setReadOnly(True)

        workspace_container_layout.addWidget(self.open_workspace_button)
        workspace_container_layout.addWidget(self.open_workspace_line)

        workspace_container.setLayout(workspace_container_layout)

        layout.addWidget(self.description_label)
        layout.addWidget(workspace_container)

        self.setLayout(layout)

        self.open_workspace_button.clicked.connect(self._handle_workspace_selected)

    def _handle_workspace_selected(self) -> None:
        # Default to the value of Morrowind's registry entry for "Installed Path".
        # TODO: Move this stuff to dedicated class for handling Morrowind registry settings.
        morrowind_registry = "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Bethesda Softworks\Morrowind"
        morrowind_settings = QSettings(morrowind_registry, QSettings.Format.NativeFormat)
        morrowind_directory = morrowind_settings.value("Installed Path", "")

        # First, open a supposed workspace.
        workspace = QFileDialog(directory=morrowind_directory).getExistingDirectory(  # type: ignore[call-overload]
            parent=self,
            caption="Open Directory",
            options=QFileDialog.Option.DontUseNativeDialog,
        )
        if workspace:
            # Confirm that Morrowind.ini exists in the folder - otherwise it is invalid.
            ini_path = Path(workspace) / "Morrowind.ini"
            if ini_path.exists():
                # Succesfully found workspace. Continue forward.
                self.open_workspace_line.setText(workspace)
                self.set_valid()
            else:
                # Not a workspace. Warn user and prevent progression.
                self.set_valid(
                    False,
                    "Sorry, that directory does not contain a valid Morrowind.ini file. Please choose a Morrowind installation with a Morrowind.ini file.",
                )


class ConfigurationStepTwoWidget(StepperItem):
    label_description: TextBlockLabel

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # type: ignore[call-overload]

        self.label_description = TextBlockLabel(
            "That's it, for now! Your workspace is successfully configured. Click Finish to continue into the application."
        )
        layout.addWidget(self.label_description)
        self.setLayout(layout)
        self.set_valid()


class ConfigurationWidget(QWidget):
    stepper: Stepper
    config_step_one: ConfigurationStepOneWidget
    config_step_two: ConfigurationStepTwoWidget

    def __init__(self) -> None:
        super().__init__()

        self.config_step_one = ConfigurationStepOneWidget()
        self.config_step_two = ConfigurationStepTwoWidget()

        self.stepper = Stepper([self.config_step_one, self.config_step_two])
        self.stepper.stepper_finish_clicked.connect(self._handle_complete_steps)

        layout = QVBoxLayout()
        layout.addWidget(SubtitleLabel("Configuration"))
        layout.addWidget(self.stepper)
        self.setLayout(layout)

    def _handle_complete_steps(self) -> None:
        Numidium.workspace_changed.emit(self.config_step_one.open_workspace_line.text())
        config.setup_completed = True


class StartupWidget(QWidget):
    open_workspace_button: OpenWorkspaceButton
    open_github_button: OpenGithubButton
    open_welcome_on_startup_checkbox: QCheckBox

    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout()

        self._setup_recent_files()
        self._setup_getting_started()
        self._setup_state()

        layout.addWidget(self.container_recent_files, 0, 0)
        layout.addWidget(self.container_getting_started, 0, 1)

        self.setLayout(layout)

    def _setup_recent_files(self) -> None:
        self.container_recent_files = QWidget()
        layout = QVBoxLayout()

        subtitle_label = SubtitleLabel("Recent Files")
        layout.addWidget(subtitle_label)

        self.list = QListWidget()

        # TODO: Find better way to show recent workspaces. Connect to state & handle clicks.
        for workspace, timestamp in config.recent_workspaces.items():
            item = QListWidgetItem(self.list)

            item_container = QWidget()
            item_layout = QVBoxLayout()

            label_workspace = QLabel(workspace)
            label_workspace_font = label_workspace.font()
            new_point_size = int(label_workspace_font.pointSize() * 1.25)
            label_workspace_font.setPointSize(new_point_size)
            label_workspace.setFont(label_workspace_font)

            label_timestamp = QLabel(str(datetime.fromtimestamp(timestamp)))

            item_layout.addWidget(label_workspace)
            item_layout.addWidget(label_timestamp)

            item_container.setLayout(item_layout)

            item_layout.setSizeConstraint(QVBoxLayout.SetFixedSize)
            item.setSizeHint(item_container.sizeHint())
            item.setData(Qt.ItemDataRole.UserRole, workspace)  # type:ignore[arg-type]
            self.list.addItem(item)
            self.list.setItemWidget(item, item_container)

        layout.addWidget(self.list)
        self.container_recent_files.setLayout(layout)

    def _setup_getting_started(self) -> None:
        self.container_getting_started = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # type: ignore[call-overload]

        subtitle_label = SubtitleLabel("Getting Started")
        self.open_workspace_button = OpenWorkspaceButton()
        self.open_github_button = OpenGithubButton()
        self.open_welcome_on_startup_checkbox = QCheckBox("Show Welcome on Startup")

        layout.addWidget(subtitle_label)
        layout.addWidget(self.open_workspace_button)
        layout.addWidget(self.open_github_button)
        layout.addWidget(self.open_welcome_on_startup_checkbox)
        self.container_getting_started.setLayout(layout)

    def _setup_state(self) -> None:
        self.list.itemClicked.connect(self._handle_welcome_screen_select_workspace)

        self.open_welcome_on_startup_checkbox.setChecked(config.show_welcome)
        self.open_welcome_on_startup_checkbox.stateChanged.connect(self._handle_welcome_screen_startup_checked)

    def _handle_welcome_screen_select_workspace(self, current: QListWidgetItem) -> None:
        data = current.data(Qt.ItemDataRole.UserRole)  # type: ignore[arg-type]
        Numidium.workspace_changed.emit(data)

    def _handle_welcome_screen_startup_checked(self) -> None:
        checked = self.sender().isChecked()
        config.show_welcome = checked
        config.save_path()


class WelcomeWindow(AbstractMainWindow):

    layout: QVBoxLayout
    widget: StartupWidget | ConfigurationWidget

    def __init__(self) -> None:
        super().__init__()

        # Create actual layout to contain widgets, within frame.
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # type: ignore[call-overload]

        self._setup_center_panel()
        self._setup_title_panel()

        if config.setup_completed:
            self.widget = StartupWidget()
        else:
            self.widget = ConfigurationWidget()

        self.layout.addWidget(self.widget)

    def _setup_center_panel(self) -> None:
        """Setup center panel that is shown on the welcome screen.

        This requires multiple layers of layout nesting and adjustments to work with the panel border.
        """
        # Create outermost layout with vertical and horizontal center.
        container = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # type: ignore[call-overload]

        # Create panel widget box & layout with fixed size (relative to screen size)
        panel_height = 600
        panel_width = 800

        spacer_height = container.height() // 2 - panel_height

        central_widget = QWidget()
        central_widget.setContentsMargins(10, spacer_height, 10, spacer_height)

        central_widget.setFixedSize(panel_width, panel_height)
        central_layout = QVBoxLayout()

        # Create Frame container.
        frame = QFrame()
        frame.setFrameShadow(QFrame.Shadow.Plain)
        frame.setLayout(self.layout)

        central_layout.addWidget(frame)
        central_widget.setLayout(central_layout)

        layout.addWidget(central_widget)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _setup_title_panel(self) -> None:
        # Create banner
        banner = QLabel()
        banner.setPixmap(QPixmap("./numidium/ui/images/banner.png"))
        self.layout.addWidget(banner)

        # Create a horizontal divider line.
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        self.layout.addWidget(line)
