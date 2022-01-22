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

from numidium.ui.state import AppSettings
from numidium.ui.widgets import (
    OpenGithubButton,
    OpenWorkspaceButton,
    Stepper,
    StepperItem,
    SubtitleLabel,
    TextBlockLabel,
    TitleLabel,
)
from numidium.ui.windows.abstractmain import AbstractMainWindow


class ConfigurationStepOneWidget(StepperItem):
    label_description: TextBlockLabel
    workspace_open_button: QPushButton
    workspace_line: QLineEdit

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)

        self.label_description = TextBlockLabel(
            "Welcome to Numidium! This multi-tool offers the ability to manage and edit your Morrowind mods, while remaining highly extensible through plugins and user settings. To get started, open a workspace! Workspaces represent a particular install of Morrowind. Simply navigate to the folder that contains your Morrowind.exe file and choose open directory. Note: After setting up your first workspace, you will be able to open and manage multiple workspaces."
        )
        self.label_description.adjustSize()

        workspace_container = QWidget()
        workspace_container_layout = QHBoxLayout()

        self.workspace_open_button = QPushButton(icon=QIcon("icons:folder_open_24dp.svg"), text="Open Workspace ")
        self.workspace_line = QLineEdit()
        self.workspace_line.setReadOnly(True)

        workspace_container_layout.addWidget(self.workspace_open_button)
        workspace_container_layout.addWidget(self.workspace_line)

        workspace_container.setLayout(workspace_container_layout)

        layout.addWidget(self.label_description)
        layout.addWidget(workspace_container)

        self.setLayout(layout)

        self.workspace_open_button.clicked.connect(self._handle_workspace_selected)

    def _handle_workspace_selected(self):
        # Default to the value of Morrowind's registry entry for "Installed Path".
        # TODO: Move this stuff to dedicated class for handling Morrowind registry settings.
        morrowind_registry = "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Bethesda Softworks\Morrowind"
        morrowind_settings = QSettings(morrowind_registry, QSettings.Format.NativeFormat)
        morrowind_directory = morrowind_settings.value("Installed Path", "")

        # First, open a supposed workspace.
        workspace = QFileDialog(directory=morrowind_directory).getExistingDirectory(
            self.parent(),
            "Open Directory",
            options=QFileDialog.Option.DontUseNativeDialog,
        )
        if workspace != "":
            # Confirm that Morrowind.ini exists in the folder - otherwise it is invalid.
            ini = Path(workspace, "Morrowind").with_suffix(".ini")
            if ini.exists():
                # Succesfully found workspace. Continue forward.
                self.workspace_line.setText(workspace)
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
        layout.setAlignment(Qt.AlignHCenter)

        self.label_description = TextBlockLabel(
            "That's it, for now! Your workspace is successfully configured. Click Finish to continue into the application."
        )
        layout.addWidget(self.label_description)
        self.setLayout(layout)
        self.set_valid()


class ConfigurationWidget(QWidget):
    stepper: Stepper
    config_step_one: QWidget
    config_step_two: QWidget

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()

        layout.addWidget(SubtitleLabel("Configuration"))

        self.config_step_one = ConfigurationStepOneWidget()
        self.config_step_two = ConfigurationStepTwoWidget()

        stepper_items = [self.config_step_one, self.config_step_two]
        self.stepper = Stepper(stepper_items)

        layout.addWidget(self.stepper)
        self.setLayout(layout)

        self.stepper.stepper_finish_clicked.connect(self._handle_complete_steps)

    def _handle_complete_steps(self):
        workspace = self.config_step_one.workspace_line.text()
        AppSettings().workspace = workspace
        AppSettings().setup_completed = True


class StartupWidget(QWidget):
    open_workspace_button: OpenWorkspaceButton | None
    open_github_button: OpenGithubButton | None
    open_welcome_on_startup_checkbox: QCheckBox | None

    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout()

        self._setup_recent_files()
        self._setup_getting_started()
        self._setup_state()

        layout.addWidget(self.container_recent_files, 0, 0)
        layout.addWidget(self.container_getting_started, 0, 1)

        self.setLayout(layout)

    def _setup_recent_files(self):
        self.container_recent_files = QWidget()
        layout = QVBoxLayout()

        subtitle_label = SubtitleLabel("Recent Files")
        layout.addWidget(subtitle_label)

        self.list = QListWidget()

        # TODO: Find better way to show recent workspaces. Connect to state & handle clicks.
        for workspace, timestamp in AppSettings().recent_workspaces.items():
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
            item.setData(Qt.UserRole, workspace)
            self.list.addItem(item)
            self.list.setItemWidget(item, item_container)

        layout.addWidget(self.list)
        self.container_recent_files.setLayout(layout)

    def _setup_getting_started(self):
        self.container_getting_started = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        subtitle_label = SubtitleLabel("Getting Started")
        self.open_workspace_button = OpenWorkspaceButton()
        self.open_github_button = OpenGithubButton()
        self.open_welcome_on_startup_checkbox = QCheckBox("Show Welcome on Startup")

        layout.addWidget(subtitle_label)
        layout.addWidget(self.open_workspace_button)
        layout.addWidget(self.open_github_button)
        layout.addWidget(self.open_welcome_on_startup_checkbox)
        self.container_getting_started.setLayout(layout)

    def _setup_state(self):
        self.list.itemClicked.connect(self._handle_welcome_screen_select_workspace)

        self.open_welcome_on_startup_checkbox.setChecked(AppSettings().show_welcome_window)
        self.open_welcome_on_startup_checkbox.stateChanged.connect(self._handle_welcome_screen_startup_checked)

    def _handle_welcome_screen_select_workspace(self, current: QListWidgetItem):
        data = current.data(Qt.UserRole)
        AppSettings().workspace = data

    def _handle_welcome_screen_startup_checked(self):
        checked = self.sender().isChecked()
        AppSettings().show_welcome_window = checked


class WelcomeWindow(AbstractMainWindow):
    layout: QVBoxLayout

    title_label: QLabel

    configuration_widget: ConfigurationWidget
    startup_widget: StartupWidget

    def __init__(self) -> None:
        super().__init__()
        self._setup_center_panel()
        self._setup_title_panel()

        # Has user gone through first time startup?
        if AppSettings().setup_completed == False:
            # Show Configuration window.
            self.configuration_widget = ConfigurationWidget()
            self.layout.addWidget(self.configuration_widget)
        else:
            # Show standard startup window.
            self.startup_widget = StartupWidget()
            self.layout.addWidget(self.startup_widget)

    def _setup_title_panel(self):
        # Setup widgets
        self.title_label = TitleLabel("> Numidium")
        banner = QPixmap("./numidium/ui/images/banner.png")
        self.title_label.setPixmap(banner.scaledToWidth(750, Qt.SmoothTransformation))

        # Create a horizontal divider line.
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Shadow.Plain)
        line.setFixedHeight(1)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(line)

    def _setup_center_panel(self):
        """Setup center panel that is shown on the welcome screen.

        This requires multiple layers of layout nesting and adjustments to work with the panel border.
        """
        # Create outermost layout with vertical and horizontal center.
        container = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)

        # Create panel widget box & layout with fixed size (relative to screen size)
        panel_height = 600
        panel_width = 800
        spacer_height = container.height() / 2 - panel_height
        central_widget = QWidget()
        central_widget.setContentsMargins(10, spacer_height, 10, spacer_height)

        central_widget.setFixedSize(panel_width, panel_height)
        central_layout = QVBoxLayout()

        # Create Frame container.
        frame = QFrame()
        frame.setFrameShadow(QFrame.Shadow.Plain)

        # Create actual layout to contain widgets, within frame.
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        frame.setLayout(self.layout)

        central_layout.addWidget(frame)
        central_widget.setLayout(central_layout)

        layout.addWidget(central_widget)
        container.setLayout(layout)
        self.setCentralWidget(container)
