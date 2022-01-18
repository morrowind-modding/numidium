import operator
import pathlib
from operator import attrgetter

import tes3
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QHeaderView,
    QListWidget,
    QMainWindow,
    QPlainTextEdit,
    QTableView,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from numidium.tes3.esp.plugin import Plugin
from numidium.ui.explorer import Explorer
from numidium.ui.state import AppSettings
from numidium.ui.widgets import ObjectTableModel


class FileViewer(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)

        self.update_ui(AppSettings().active_file)
        layout.addWidget(self.editor)
        self.setLayout(layout)

        AppSettings().active_file_changed.connect(self._handle_update_active_file)

    def _handle_update_active_file(self, file):
        self.update_ui(file)

    def update_ui(self, file):
        text = ""

        path = pathlib.Path(file)
        if path.is_file() and path.exists():
            try:
                text = path.read_text()
            except UnicodeError:
                pass

        self.editor.setPlainText(text)
        self.editor.update()


class TableInfo:
    header: list[str]
    fields: list[str]

    def __init__(self, header, fields):
        self.header = header
        self.fields = fields

    def get_field_values(self, obj):
        return [getter(obj) for getter in map(attrgetter, self.fields)]


# fmt: off
TABLE_INFO = {
    "Activator": TableInfo(
        header=["Id", "Name", "Mesh", "Script"],
        fields=["id", "name", "mesh", "script"]
    ),
    "Alchemy": TableInfo(
        header=["Id", "Name", "Mesh", "Icon", "Script"],
        fields=["id", "name", "mesh", "icon", "script"]
    ),
    "Apparatus": TableInfo(
        header=["Id", "Name", "Mesh", "Icon", "Script"],
        fields=["id", "name", "mesh", "icon", "script"]
    ),
    "Armor": TableInfo(
        header=["Id", "Name", "Mesh", "Icon", "Script", "Enchanting"],
        fields=["id", "name", "mesh", "icon", "script", "enchanting"],
    ),
    "Birthsign": TableInfo(
        header=["Id", "Name"],
        fields=["id", "name"]
    ),
    "Bodypart": TableInfo(
        header=["Id", "Name", "Mesh"],
        fields=["id", "name", "mesh"]
    ),
    "Book": TableInfo(
        header=["Id", "Name", "Mesh", "Icon", "Script", "Enchanting"],
        fields=["id", "name", "mesh", "icon", "script", "enchanting"],
    ),
    "Cell": TableInfo(
        header=["Name"],
        fields=["name"]
    ),
    "Class": TableInfo(
        header=["Id", "Name"],
        fields=["id", "name"]
    ),
    "Clothing": TableInfo(
        header=["Id", "Name", "Mesh", "Icon", "Script", "Enchanting"],
        fields=["id", "name", "mesh", "icon", "script", "enchanting"],
    ),
    "Container": TableInfo(
        header=["Id", "Name", "Mesh", "Script"],
        fields=["id", "name", "mesh", "script"]
    ),
    "Creature": TableInfo(
        header=["Id", "Name", "Mesh", "Script"],
        fields=["id", "name", "mesh", "script"]
    ),
    "Dialogue": TableInfo(
        header=["Id"],
        fields=["id"]
    ),
    "Door": TableInfo(
        header=["Id", "Name", "Mesh", "Script"],
        fields=["id", "name", "mesh", "script"]
    ),
    "Enchantment": TableInfo(
        header=["Id"],
        fields=["id"]
    ),
    "Faction": TableInfo(
        header=["Id", "Name"],
        fields=["id", "name"]
    ),
    "GameSetting": TableInfo(
        header=["Id"],
        fields=["id"]
    ),
    "GlobalVariable": TableInfo(
        header=["Id"],
        fields=["id"]
    ),
    "Header": TableInfo(
        header=[],
        fields=[]
    ),
    "Info": TableInfo(
        header=[],
        fields=[]
    ),
    "Ingredient": TableInfo(
        header=["Id", "Name", "Mesh", "Icon", "Script"],
        fields=["id", "name", "mesh", "icon", "script"]
    ),
    "Landscape": TableInfo(
        header=[],
        fields=[]
    ),
    "LandscapeTexture": TableInfo(
        header=["Id"],
        fields=["id"]
    ),
    "LevelledCreature": TableInfo(
        header=["Id"],
        fields=["id"]
    ),
    "LevelledItem": TableInfo(
        header=["Id"],
        fields=["id"]
    ),
    "Light": TableInfo(
        header=["Id", "Name", "Mesh", "Icon", "Script"],
        fields=["id", "name", "mesh", "icon", "script"]
    ),
    "Lockpick": TableInfo(
        header=["Id", "Name", "Mesh", "Icon", "Script"],
        fields=["id", "name", "mesh", "icon", "script"]
    ),
    "MagicEffect": TableInfo(
        header=["Icon"],
        fields=["icon"]
    ),
    "MiscItem": TableInfo(
        header=["Id", "Name", "Mesh", "Icon", "Script"],
        fields=["id", "name", "mesh", "icon", "script"]
    ),
    "Npc": TableInfo(
        header=["Id", "Name", "Mesh", "Script"],
        fields=["id", "name", "mesh", "script"]
    ),
    "PathGrid": TableInfo(
        header=[],
        fields=[]
    ),
    "Probe": TableInfo(
        header=["Id", "Name", "Mesh", "Icon", "Script"],
        fields=["id", "name", "mesh", "icon", "script"]
    ),
    "Race": TableInfo(
        header=["Id", "Name"],
        fields=["id", "name"]
    ),
    "Reference": TableInfo(
        header=["Id"],
        fields=["id"]
    ),
    "Region": TableInfo(
        header=["Id", "Name"],
        fields=["id", "name"]
    ),
    "RepairTool": TableInfo(
        header=["Id", "Name", "Mesh", "Icon", "Script"],
        fields=["id", "name", "mesh", "icon", "script"]
    ),
    "Script": TableInfo(
        header=["Id"],
        fields=["id"]
    ),
    "Skill": TableInfo(
        header=[],
        fields=[]
    ),
    "Sound": TableInfo(
        header=["Id"],
        fields=["id"]
    ),
    "SoundGen": TableInfo(
        header=["Id"],
        fields=["id"]
    ),
    "Spell": TableInfo(
        header=["Id", "Name"],
        fields=["id", "name"]
    ),
    "StartScript": TableInfo(
        header=["Id", "Script"],
        fields=["id", "script"]
    ),
    "Static": TableInfo(
        header=["Id", "Mesh"],
        fields=["id", "mesh"]
    ),
    "Weapon": TableInfo(
        header=["ID", "Name", "Weight", "Value", "Icon", "Mesh"],
        fields=["id", "name", "data.weight", "data.value", "icon", "mesh"],
    ),
}
# fmt: on


class ObjectTypeList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QListWidget.SelectionBehavior.SelectRows)
        self.addItems(TABLE_INFO.keys())

        self.setCurrentRow(0)
        self.setMaximumWidth(self.sizeHintForColumn(0) + 15)


class ObjectTable(QTableView):
    def __init__(self):
        super().__init__()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)


class PluginViewer(QWidget):
    object_type_list: QListWidget
    object_table: QTableView

    plugin: Plugin

    def __init__(self):
        super().__init__()

        self.object_type_list = ObjectTypeList()
        self.object_table = ObjectTable()

        self._load_file(AppSettings().active_file)
        self._update_ui()

        layout = QHBoxLayout(self)
        layout.addWidget(self.object_type_list)
        layout.addWidget(self.object_table)
        self.setLayout(layout)

        AppSettings().active_file_changed.connect(self._handle_update_active_file)
        self.object_type_list.currentItemChanged.connect(self._handle_object_type_changed)

    def _handle_update_active_file(self, file):
        self._load_file(file)
        self._update_ui()

    def _handle_object_type_changed(self):
        self._update_ui()

    def _load_file(self, file):
        path = pathlib.Path(file)
        if path.exists():
            self.plugin = tes3.Plugin.load(file)

    def _update_ui(self):
        if not self.plugin:
            return

        header = []
        values = []

        object_type = self.object_type_list.currentItem().text()
        object_type_info = TABLE_INFO.get(object_type)

        if object_type_info:
            header = object_type_info.header
            values = [
                object_type_info.get_field_values(obj) for obj in self.plugin.objects if obj.type_name == object_type
            ]

        self.model = ObjectTableModel(self, values, header)
        self.object_table.setModel(self.model)
        self.object_table.setSortingEnabled(True)


class Viewer(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.update_ui(AppSettings().active_file)
        self.setLayout(layout)

        AppSettings().active_file_changed.connect(self._handle_update_active_file)

    def _handle_update_active_file(self, file):
        self.update_ui(file)

    def update_ui(self, file):
        layout = self.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if file:
            if pathlib.Path(file).suffix.lower() in [".esm", ".esp"]:
                self.widget = PluginViewer()
                layout.addWidget(self.widget)
            else:
                self.widget = FileViewer()
                layout.addWidget(self.widget)


class EditorDock(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Widgets
        self.left_dock = QDockWidget("Editor")
        self.bottom_dock = QDockWidget("Bottom dock")

        # Setup widgets
        self.explorer = Explorer()
        self.left_dock.setWidget(self.explorer)

        self.bottom_dock.setWidget(QTextEdit("This is the bottom editor widget. -- NI"))
        for dock in (self.left_dock, self.bottom_dock):
            dock.setAllowedAreas(
                Qt.DockWidgetArea.LeftDockWidgetArea
                | Qt.DockWidgetArea.RightDockWidgetArea
                | Qt.DockWidgetArea.BottomDockWidgetArea
                | Qt.DockWidgetArea.TopDockWidgetArea
            )

        # Layout
        main_win = QMainWindow()
        main_win.setCentralWidget(Viewer())
        main_win.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)
        main_win.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.bottom_dock)

        layout = QVBoxLayout(self)
        layout.addWidget(main_win)
        layout.setContentsMargins(0, 0, 0, 0)
