# type: ignore

from typing import Any

import qtvscodestyle as qtvsc
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QAction, QActionGroup, QTextOption
from PySide6.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDateTimeEdit,
    QDial,
    QDockWidget,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMenuBar,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QTableView,
    QTabWidget,
    QTextEdit,
    QToolBar,
    QToolBox,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)
from qtvscodestyle.const import FaRegular


class _Group1(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Group 1")

        # VSCode icons
        favorite_icon = qtvsc.theme_icon(FaRegular.STAR)

        # Widgets
        group_push = QGroupBox("Push Button")
        group_tool = QGroupBox("Tool Button")
        group_radio = QGroupBox("Radio Button")
        group_checkbox = QGroupBox("Check Box")

        push_button_normal = QPushButton(text="NORMAL")
        push_button_toggled = QPushButton(text="TOGGLED")
        push_button_secondary_normal = QPushButton(text="NORMAL")
        push_button_secondary_toggled = QPushButton(text="TOGGLED")
        tool_button_normal, tool_button_toggled, tool_button_text = QToolButton(), QToolButton(), QToolButton()
        radio_button_normal_1, radio_button_normal_2 = QRadioButton("Normal 1"), QRadioButton("Normal 2")
        checkbox_normal, checkbox_tristate = QCheckBox("Normal"), QCheckBox("Tristate")

        # Setup widgets
        self.setCheckable(True)
        push_button_toggled.setCheckable(True)
        push_button_toggled.setChecked(True)
        push_button_secondary_toggled.setCheckable(True)
        push_button_secondary_toggled.setChecked(True)

        tool_button_normal.setIcon(favorite_icon)
        tool_button_toggled.setIcon(favorite_icon)
        tool_button_text.setIcon(favorite_icon)
        tool_button_text.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        tool_button_text.setText("Text")
        tool_button_toggled.setCheckable(True)
        tool_button_toggled.setChecked(True)

        radio_button_normal_1.setChecked(True)
        checkbox_normal.setChecked(True)
        checkbox_tristate.setTristate(True)
        checkbox_tristate.setCheckState(Qt.CheckState.PartiallyChecked)

        # Setup qss property
        push_button_secondary_normal.setProperty("type", "secondary")
        push_button_secondary_toggled.setProperty("type", "secondary")

        # Layout
        g_layout_push = QGridLayout()
        g_layout_push.addWidget(QLabel("Main"), 0, 0)
        g_layout_push.addWidget(push_button_normal, 1, 0)
        g_layout_push.addWidget(push_button_toggled, 2, 0)
        g_layout_push.addWidget(QLabel("Secondary"), 0, 1)
        g_layout_push.addWidget(push_button_secondary_normal, 1, 1)
        g_layout_push.addWidget(push_button_secondary_toggled, 2, 1)
        group_push.setLayout(g_layout_push)

        v_layout_tool = QVBoxLayout()
        v_layout_tool.addWidget(tool_button_normal)
        v_layout_tool.addWidget(tool_button_toggled)
        v_layout_tool.addWidget(tool_button_text)
        group_tool.setLayout(v_layout_tool)

        v_layout_radio = QVBoxLayout()
        v_layout_radio.addWidget(radio_button_normal_1)
        v_layout_radio.addWidget(radio_button_normal_2)
        group_radio.setLayout(v_layout_radio)

        v_layout_checkbox = QVBoxLayout()
        v_layout_checkbox.addWidget(checkbox_normal)
        v_layout_checkbox.addWidget(checkbox_tristate)
        group_checkbox.setLayout(v_layout_checkbox)

        g_layout_main = QGridLayout(self)
        g_layout_main.addWidget(group_push, 0, 0)
        g_layout_main.addWidget(group_tool, 0, 1)
        g_layout_main.addWidget(group_radio, 1, 0)
        g_layout_main.addWidget(group_checkbox, 1, 1)


class _Group2(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Group 2")
        # Widgets
        group_spinbox = QGroupBox("Spinbox")
        group_combobox = QGroupBox("Combobox")
        group_editable = QGroupBox("Line edit")
        group_date = QGroupBox("Date time edit")

        spinbox_normal, spinbox_suffix = QSpinBox(), QSpinBox()
        combobox_normal, combobox_line_edit = QComboBox(), QComboBox()
        lineedit_normal, lineedit_warning, lineedit_error = QLineEdit(), QLineEdit(), QLineEdit()
        date_time_edit_normal, date_time_edit_calendar = QDateTimeEdit(), QDateTimeEdit()

        # Setup ui
        self.setCheckable(True)
        spinbox_suffix.setSuffix(" m")

        texts = ["Item 1", "Item 2", "Item 3"]
        combobox_normal.addItems(texts)
        combobox_line_edit.addItems(texts)
        combobox_line_edit.setEditable(True)

        lineedit_normal.setPlaceholderText("Normal")
        lineedit_warning.setPlaceholderText("Warning")
        lineedit_error.setPlaceholderText("Error")

        date_time_edit_calendar.setCalendarPopup(True)

        # Setup qss property
        lineedit_warning.setProperty("state", "warning")
        lineedit_error.setProperty("state", "error")

        # Layout
        v_layout_spin = QVBoxLayout()
        v_layout_spin.addWidget(spinbox_normal)
        v_layout_spin.addWidget(spinbox_suffix)
        group_spinbox.setLayout(v_layout_spin)

        v_layout_combo = QVBoxLayout()
        v_layout_combo.addWidget(combobox_normal)
        v_layout_combo.addWidget(combobox_line_edit)
        group_combobox.setLayout(v_layout_combo)

        v_layout_lineedit = QVBoxLayout()
        v_layout_lineedit.addWidget(lineedit_normal)
        v_layout_lineedit.addWidget(lineedit_warning)
        v_layout_lineedit.addWidget(lineedit_error)
        group_editable.setLayout(v_layout_lineedit)

        v_layout_date = QVBoxLayout()
        v_layout_date.addWidget(date_time_edit_normal)
        v_layout_date.addWidget(date_time_edit_calendar)
        group_date.setLayout(v_layout_date)

        g_layout_main = QGridLayout(self)
        g_layout_main.addWidget(group_spinbox, 0, 0)
        g_layout_main.addWidget(group_combobox, 0, 1)
        g_layout_main.addWidget(group_editable, 1, 0)
        g_layout_main.addWidget(group_date, 1, 1)


class _TableModel(QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()
        self._data = [[i * 10 + j for j in range(4)] for i in range(5)]
        self._checks = [True if i % 2 == 0 else False for i in range(5)]

    def data(self, index: QModelIndex, role: int) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        elif role == Qt.ItemDataRole.CheckStateRole and index.column() == 1:
            return Qt.CheckState.Checked if self._checks[index.row()] else Qt.CheckState.Unchecked
        elif role == Qt.ItemDataRole.EditRole and index.column() == 2:
            return self._data[index.row()][index.column()]

    def rowCount(self, index: QModelIndex) -> int:
        return len(self._data)

    def columnCount(self, index: QModelIndex) -> int:
        return len(self._data[0])

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        flag = super().flags(index)
        if index.column() == 1:
            flag |= Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsUserCheckable
            return flag
        elif index.column() == 2:
            flag |= Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable
            return flag
        elif index.column() == 3:
            flag |= Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable
        return flag

    def setData(self, index: QModelIndex, value: Any, role: int) -> bool:
        if role == Qt.ItemDataRole.CheckStateRole:
            self._checks[index.row()] = True if value == Qt.CheckState.Checked else False
            return True
        return False

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return
        if orientation == Qt.Orientation.Horizontal:
            return ["Normal", "Checkbox", "Spinbox", "LineEdit"][section]
        return super().headerData(section, orientation, role)


class _Group3(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Group 3")

        # Widgets
        tab_widget = QTabWidget()
        tab_text_edit = QTextEdit()
        tab_table = QTableView()
        tab_list = QListWidget()
        tab_tree = QTreeWidget()

        # Setup ui
        self.setCheckable(True)
        tab_widget.setTabsClosable(True)
        tab_widget.setMovable(True)
        tab_text_edit.append("<b>QtVSCodeStyle</b>")
        tab_text_edit.append("VS Code style for QtWidgets application(Qt for python).")
        tab_text_edit.append("This project is licensed under the MIT license.")
        tab_text_edit.setWordWrapMode(QTextOption.WrapMode.NoWrap)

        tab_table.setModel(_TableModel())
        tab_table.setSortingEnabled(True)

        tab_list.addItems([f"Item {i+1}" for i in range(30)])
        tab_list.setAlternatingRowColors(True)

        tab_tree.setColumnCount(2)
        tree_widget_items = []
        for i in range(5):
            tree_widget_item = QTreeWidgetItem([f"Item {i+1}" for _ in range(2)])
            for j in range(2):
                tree_widget_child_item = QTreeWidgetItem([f"Child Item {i+1}_{j+1}" for _ in range(2)])
                tree_widget_item.addChild(tree_widget_child_item)
            tree_widget_items.append(tree_widget_item)
        tab_tree.addTopLevelItems(tree_widget_items)

        # layout
        tab_widget.addTab(tab_text_edit, "Text Edit")
        tab_widget.addTab(tab_table, "Table")
        tab_widget.addTab(tab_list, "List")
        tab_widget.addTab(tab_tree, "Tree")

        v_layout_main = QVBoxLayout(self)
        v_layout_main.addWidget(tab_widget)


class _Group4(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Group 4")
        # Widgets
        toolbox = QToolBox()
        slider = QSlider(Qt.Orientation.Horizontal)
        dial_ticks = QDial()
        progressbar = QProgressBar()
        lcd_number = QLCDNumber()

        # Setup ui
        self.setCheckable(True)
        toolbox.addItem(slider, "Slider")
        toolbox.addItem(dial_ticks, "Dial")
        toolbox.addItem(progressbar, "Progress Bar")
        toolbox.addItem(lcd_number, "LCD Number")
        slider.setValue(50)
        dial_ticks.setNotchesVisible(True)
        progressbar.setValue(50)
        lcd_number.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        lcd_number.display(123)

        # Layout
        v_layout = QVBoxLayout(self)
        v_layout.addWidget(toolbox)


class HomeUI:
    def setup_ui(self, win: QWidget) -> None:
        # Widgets
        h_splitter_1, h_splitter_2 = QSplitter(Qt.Orientation.Horizontal), QSplitter(Qt.Orientation.Horizontal)

        # Setup ui
        h_splitter_1.setMinimumHeight(350)  # Fix bug layout crush

        # Layout
        h_splitter_1.addWidget(_Group1())
        h_splitter_1.addWidget(_Group2())
        h_splitter_2.addWidget(_Group3())
        h_splitter_2.addWidget(_Group4())

        v_layout = QVBoxLayout()
        v_layout.addWidget(h_splitter_1)
        v_layout.addWidget(h_splitter_2)

        widget = QWidget()
        widget.setLayout(v_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidget(widget)

        v_main_layout = QVBoxLayout(win)
        v_main_layout.addWidget(scroll_area)


class DockUI:
    def _setup_ui(self, main_win: QMainWindow) -> None:
        # Attribute
        left_dock = QDockWidget("Left dock")
        right_dock = QDockWidget("Right dock")
        top_dock = QDockWidget("Top dock")
        bottom_dock = QDockWidget("Bottom dock")
        docks = [left_dock, right_dock, top_dock, bottom_dock]

        # Setup ui
        left_dock.setWidget(QTextEdit("This is the left widget."))
        right_dock.setWidget(QTextEdit("This is the right widget."))
        top_dock.setWidget(QTextEdit("This is the top widget."))
        bottom_dock.setWidget(QTextEdit("This is the bottom widget."))
        for dock in docks:
            dock.setAllowedAreas(
                Qt.DockWidgetArea.LeftDockWidgetArea
                | Qt.DockWidgetArea.RightDockWidgetArea
                | Qt.DockWidgetArea.BottomDockWidgetArea
                | Qt.DockWidgetArea.TopDockWidgetArea
            )

        # Layout
        main_win.setCentralWidget(QTextEdit("This is the central widget."))
        main_win.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, left_dock)
        main_win.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, right_dock)
        main_win.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, top_dock)
        main_win.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, bottom_dock)


class UI:
    def setup_ui(self, main_win: QMainWindow) -> None:
        # Icons
        home_icon = qtvsc.theme_icon(qtvsc.Vsc.HOME, "activityBar.foreground")
        multi_windows_icon = qtvsc.theme_icon(qtvsc.Vsc.MULTIPLE_WINDOWS, "activityBar.foreground")
        settings_icon = qtvsc.theme_icon(qtvsc.Vsc.SETTINGS_GEAR, "activityBar.foreground")
        folder_open_icon = qtvsc.theme_icon(qtvsc.Vsc.FOLDER)
        palette_icon = qtvsc.theme_icon(qtvsc.Vsc.SYMBOL_COLOR)
        circle_icon = qtvsc.theme_icon(qtvsc.Vsc.CIRCLE_LARGE_OUTLINE)
        clear_icon = qtvsc.theme_icon(qtvsc.Vsc.CLOSE)

        # Actions
        self.action_change_home = QAction(home_icon, "Move to home")
        self.action_change_dock = QAction(multi_windows_icon, "Move to dock")
        self.action_open_folder = QAction(folder_open_icon, "Open folder dialog")
        self.action_open_color_dialog = QAction(palette_icon, "Open color dialog", main_win)
        self.action_enable = QAction(circle_icon, "Enable")
        self.action_disable = QAction(clear_icon, "Disable")

        self.action_group_toolbar = QActionGroup(main_win)

        # Widgets
        self.central_window = QMainWindow()
        self.stack_widget = QStackedWidget()

        activitybar = QToolBar("activitybar")
        toolbar = QToolBar("Toolbar")
        statusbar = QStatusBar()
        menubar = QMenuBar()
        tool_button_settings = QToolButton()
        tool_button_enable = QToolButton()
        tool_button_disable = QToolButton()

        self.spacer = QToolButton()

        # Setup Actions
        self.action_change_home.setCheckable(True)
        self.action_change_dock.setCheckable(True)
        self.action_change_home.setChecked(True)
        self.action_group_toolbar.addAction(self.action_change_home)
        self.action_group_toolbar.addAction(self.action_change_dock)

        # Setup Widgets
        self.spacer.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.spacer.setEnabled(False)

        activitybar.setMovable(False)
        activitybar.addActions([self.action_change_home, self.action_change_dock])
        activitybar.addWidget(self.spacer)
        activitybar.addWidget(tool_button_settings)

        tool_button_settings.setIcon(settings_icon)
        tool_button_settings.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        tool_button_enable.setDefaultAction(self.action_enable)
        tool_button_disable.setDefaultAction(self.action_disable)

        toolbar.addActions([self.action_open_folder, self.action_open_color_dialog])

        statusbar.addPermanentWidget(tool_button_enable)
        statusbar.addPermanentWidget(tool_button_disable)
        statusbar.showMessage("Enable")

        menu_toggle = menubar.addMenu("&Toggle")
        menu_toggle.addActions([self.action_enable, self.action_disable])
        menu_dialog = menubar.addMenu("&Dialog")
        menu_dialog.addActions([self.action_open_folder, self.action_open_color_dialog])

        tool_button_settings.setMenu(menu_toggle)

        self.action_enable.setEnabled(False)

        # setup custom property
        activitybar.setProperty("type", "activitybar")

        # layout
        stack_1 = QWidget()
        home_ui = HomeUI()
        home_ui.setup_ui(stack_1)
        self.stack_widget.addWidget(stack_1)
        stack_2 = QMainWindow()
        dock_ui = DockUI()
        dock_ui._setup_ui(stack_2)
        self.stack_widget.addWidget(stack_2)

        self.central_window.setCentralWidget(self.stack_widget)
        self.central_window.addToolBar(toolbar)

        main_win.setCentralWidget(self.central_window)
        main_win.addToolBar(Qt.ToolBarArea.LeftToolBarArea, activitybar)
        main_win.setMenuBar(menubar)
        main_win.setStatusBar(statusbar)


class WidgetGallery(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._ui = UI()
        self._ui.setup_ui(self)
        self._setup()

    def _setup(self) -> None:
        self._ui.action_change_home.triggered.connect(self._change_page)
        self._ui.action_change_dock.triggered.connect(self._change_page)
        self._ui.action_open_folder.triggered.connect(
            lambda: QFileDialog.getOpenFileName(self, "Open File", options=QFileDialog.Option.DontUseNativeDialog)
        )
        self._ui.action_open_color_dialog.triggered.connect(
            lambda: QColorDialog.getColor(parent=self, options=QColorDialog.ColorDialogOption.DontUseNativeDialog)
        )
        self._ui.action_enable.triggered.connect(self._toggle_state)
        self._ui.action_disable.triggered.connect(self._toggle_state)

    def _change_page(self) -> None:
        action_name = self.sender().text()
        self._ui.stack_widget.setCurrentIndex(0 if action_name == "Move to home" else 1)

    def _toggle_state(self) -> None:
        state = self.sender().text()
        self._ui.central_window.centralWidget().setEnabled(state == "Enable")
        self._ui.action_enable.setEnabled(state == "Disable")
        self._ui.action_disable.setEnabled(state == "Enable")
        self.statusBar().showMessage(state)
