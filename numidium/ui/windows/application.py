from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup, QIcon
from PySide6.QtWidgets import QStackedWidget, QToolBar, QToolButton, QWidget

from numidium.ui.editordock import EditorDock
from numidium.ui.modsdock import ModsDock
from numidium.ui.settingsdock import SettingsDock
from numidium.ui.state import AppSettings
from numidium.ui.windows.about import AboutWindow
from numidium.ui.windows.abstractmain import AbstractMainWindow


class ApplicationWindow(AbstractMainWindow):
    stack_widget: QStackedWidget

    activity_bar: QToolBar
    activity_bar_action_group: QActionGroup

    def __init__(self) -> None:
        super().__init__()

        self.stack_widget = QStackedWidget()

        for dock in ModsDock, EditorDock, SettingsDock:
            container = QWidget(parent=self)
            dock().setup_ui(container)
            self.stack_widget.addWidget(container)

        self.stack_widget.setCurrentIndex(AppSettings().dock_index)
        self.central_window.setCentralWidget(self.stack_widget)

        self._setup_activity_bar()
        self._load_application_state()

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
