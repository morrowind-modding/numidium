from json import tool

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup, QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QToolBar,
    QToolButton,
    QWidget,
)
from ui.editordock import EditorDock
from ui.modsdock import ModsDock
from ui.settingsdock import SettingsDock
from ui.state import AppSettings
from ui.windows.about import AboutWindow
from ui.windows.abstractmain import AbstractMainWindow


class ApplicationWindow(AbstractMainWindow):
    stack_widget: QStackedWidget

    activity_bar: QToolBar
    activity_bar_action_group: QActionGroup

    toolbar: QToolBar
    toolbar_dark_mode_button: QPushButton

    def __init__(self) -> None:
        super().__init__()

        self.stack_widget = QStackedWidget()

        for dock in ModsDock, EditorDock, SettingsDock:
            container = QWidget(parent=self)
            dock().setup_ui(container)
            self.stack_widget.addWidget(container)

        self.stack_widget.setCurrentIndex(AppSettings().dock_index)
        self.central_window.setCentralWidget(self.stack_widget)

        self._setup_toolbar()
        self._setup_activity_bar()

        self._load_application_state()

    def _setup_toolbar(self):
        self.toolbar = QToolBar(parent=self)

        # Setup Widgets
        self.toolbar.addAction(self.action_open_workspace)
        self.toolbar.addSeparator()

        # Fill the rest with a spacer.
        spacer = QToolButton(parent=self.toolbar)
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        spacer.setEnabled(False)
        self.toolbar.addWidget(spacer)

        # Add dark mode toggle at the end.
        self.toolbar_dark_mode_button = QPushButton(parent=self.toolbar)
        self.toolbar_dark_mode_button.setIcon(QIcon("icons:contrast_24dp.svg"))
        self.toolbar_dark_mode_button.setText("Dark Mode ")  # extra space because idk how to set spacing :(
        self.toolbar_dark_mode_button.setCheckable(True)
        self.toolbar_dark_mode_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.toolbar_dark_mode_button.clicked.connect(self._change_theme)
        self.toolbar.addWidget(self.toolbar_dark_mode_button)

        self.central_window.addToolBar(self.toolbar)

    def _setup_activity_bar(self):
        """Setup the main window's activity bar.

        This is the left-most area of the main window. It contains buttons for switching between different 'modes' (Editor, Settings, etc).
        """
        # create the activity toolbar
        self.activity_bar = QToolBar(parent=self)
        self.activity_bar.setMovable(False)

        # Create an action group for the different mode switches.
        self.activity_bar_action_group = QActionGroup(self.activity_bar)

        # TODO: Add ability to collapse acitivity panel and hide text.
        for icon, text, tooltip in (
            ("icons:widgets_24dp.svg", "Mods", "Move to Mods"),
            ("icons:flip_to_front_24dp.svg", "Editor", "Move to Editor"),
            ("icons:settings_24dp.svg", "Settings", "Move to Settings"),
        ):
            action = QAction(QIcon(icon), text)
            action.setCheckable(True)
            action.setToolTip(tooltip)
            action.triggered.connect(self._change_page)
            button = QToolButton()
            button.setDefaultAction(action)
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            self.activity_bar_action_group.addAction(action)

            # Add the tool button to the activity bar. This lets us show the text within the bar.
            self.activity_bar.addWidget(button)


        # Finally add the activity bar to the main window.
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.activity_bar)

    def _load_application_state(self):
        # Restore the users previously active selection.
        actions = self.activity_bar_action_group.actions()
        actions[AppSettings().dock_index].setChecked(True)

        self.toolbar_dark_mode_button.setChecked(AppSettings().enable_dark_mode)

    def _show_about_window(self) -> None:
        if self.about_window is None:
            self.about_window = AboutWindow()
        self.about_window.show()

    def _change_page(self) -> None:
        action_name: str = self.sender().text()  # type: ignore
        if "Mods" in action_name:
            AppSettings().dock_index = 0
        elif "Editor" in action_name:
            AppSettings().dock_index = 1
        elif "Settings" in action_name:
            AppSettings().dock_index = 2
        self.stack_widget.setCurrentIndex(AppSettings().dock_index)
