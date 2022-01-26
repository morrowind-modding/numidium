from operator import attrgetter
from pathlib import Path
from typing import Any

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QImage, QImageReader, QPixmap, QWheelEvent
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QListWidget,
    QTableView,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from numidium.logger import logger
from numidium.tes3 import Plugin, dds
from numidium.tes3.esp.object import TES3Object
from numidium.ui.widgets import ObjectTableModel


class ViewerItem(QWidget):
    name: str = "Unknown"
    filepath: str

    def __init__(self, filepath: str) -> None:
        super().__init__()
        self.filepath = filepath

    @classmethod
    def get_supported_file_types(cls) -> tuple[str, ...]:
        logger.error("Method should be overriden.")
        raise NotImplementedError()


class TextFileViewer(ViewerItem):
    name: str = "Text Viewer"
    editor: QTextEdit

    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)
        self.filepath = filepath
        layout = QVBoxLayout(self)

        self.editor = QTextEdit()
        self.editor.setReadOnly(True)

        layout.addWidget(self.editor)
        self.setLayout(layout)
        self.update_ui()

    def set_filepath(self, filepath: str, update_ui: bool = True) -> None:
        self.filepath = filepath
        if update_ui:
            self.update_ui()

    def update_ui(self) -> None:
        text = ""

        path = Path(self.filepath)
        if path.is_file() and path.exists():
            try:
                text = path.read_text()
            except UnicodeError:
                pass

        suffix = path.suffix.lower()
        if suffix in (".txt", ".log"):
            self.editor.setPlainText(text)
        elif suffix == ".md":
            self.editor.setMarkdown(text)
        else:
            logger.warning("Invalid file detected. Suffix {suffix}", suffix=path.suffix)

        self.editor.update()

    @classmethod
    def get_supported_file_types(cls) -> tuple[str, ...]:
        return (".txt", ".log", ".md")


class TableInfo:
    header: list[str]
    fields: list[str]

    def __init__(self, header: list[str], fields: list[str]) -> None:
        self.header = header
        self.fields = fields

    def get_field_values(self, obj: TES3Object) -> list[Any]:
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


class PluginViewer(ViewerItem):
    name: str = "Plugin Viewer"

    object_type_list: QListWidget
    object_table: QTableView

    plugin: Plugin

    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)
        # Setup Object Type List
        self.object_type_list = QListWidget()
        self.object_type_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.object_type_list.setSelectionBehavior(QListWidget.SelectionBehavior.SelectRows)
        self.object_type_list.addItems(TABLE_INFO.keys())  # type: ignore

        self.object_type_list.setCurrentRow(0)
        self.object_type_list.setMaximumWidth(self.object_type_list.sizeHintForColumn(0) + 15)

        # Setup Object Table
        self.object_table = QTableView()
        self.object_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.object_table.setSelectionBehavior(QTableView.SelectRows)
        self.object_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        self.load_plugin(filepath)
        self.update_ui()

        layout = QHBoxLayout(self)
        layout.addWidget(self.object_type_list)
        layout.addWidget(self.object_table)
        self.setLayout(layout)
        self.object_type_list.currentItemChanged.connect(self._handle_object_type_changed)

    def _handle_object_type_changed(self) -> None:
        self.update_ui()

    def load_plugin(self, file: str, update_ui: bool = True) -> None:
        self.plugin = Plugin.load(file)
        if update_ui:
            self.update_ui()

    def update_ui(self) -> None:
        if not self.plugin:
            logger.warning("No plugin currently loaded.")
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

    @classmethod
    def get_supported_file_types(cls) -> tuple[str, ...]:
        return (".esm", ".esp")


# TODO: Fix default size.
class ImageViewport(QGraphicsView):
    """An image viewer that supports panning and zooming."""

    item: QGraphicsPixmapItem
    zoom: int = 0

    # TODO: Use or remove.
    supported_formats: list[str] = [fmt.data().decode() for fmt in QImageReader().supportedImageFormats()]
    supported_formats += ["dds"]

    def __init__(self) -> None:
        super().__init__()

        self.item = QGraphicsPixmapItem()
        self.zoom = 0

        self.setScene(QGraphicsScene())
        self.scene().addItem(self.item)

        self.setFrameShape(QFrame.NoFrame)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setPixmap(self, pixmap: QPixmap | None = None) -> None:
        self.zoom = 0
        if pixmap and not pixmap.isNull():
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.item.setPixmap(pixmap)
            self.setSceneRect(pixmap.rect())
            if not self.rect().contains(pixmap.rect()):
                self.fitInView(self.item, Qt.AspectRatioMode.KeepAspectRatio)
        else:
            self.setDragMode(QGraphicsView.NoDrag)
            self.item.setPixmap(QPixmap())

    def wheelEvent(self, event: QWheelEvent) -> None:
        if not self.item.pixmap().isNull():
            if event.angleDelta().y() > 0:
                self.zoom += 1
                self.scale(1.20, 1.20)
            else:
                self.zoom -= 1
                self.scale(0.80, 0.80)


class ImageViewer(ViewerItem):
    name: str = "Image Viewer"

    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)
        layout = QVBoxLayout()

        self.viewer = ImageViewport()
        if filepath.lower().endswith(".dds"):
            self.viewer.setPixmap(self._load_dds(filepath))
        else:
            self.viewer.setPixmap(QPixmap(filepath))

        layout.addWidget(self.viewer)
        self.setLayout(layout)

    @classmethod
    def get_supported_file_types(cls) -> tuple[str, ...]:
        # Accepted files taken from: https://doc.qt.io/qt-5/qpixmap.html
        # + dds
        return (".jpg", ".png", ".gif", ".bmp", ".jpeg", ".pbm", ".pgm", ".ppm", ".xbm", ".xpm", ".dds")

    @staticmethod
    def _load_dds(filepath: str) -> QPixmap:
        data, width, height = dds.decompress(filepath)
        image = QImage(data, width, height, QImage.Format.Format_ARGB32)
        image.rgbSwapped_inplace()
        return QPixmap.fromImage(image)


class UnsupportedFileViewer(ViewerItem):
    name: str = "Unsupported File"

    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignHCenter)  # type: ignore[call-overload]
        layout.addWidget(QLabel("This file type is not currently supported."))
        self.setLayout(layout)


# TODO: Allow extensions to register their own viewers.
class Viewer(QWidget):
    type_list: dict[str, list[type[ViewerItem]]]

    def __init__(self) -> None:
        super().__init__()
        self.type_list = {}
        self.setLayout(QVBoxLayout(self))

        viewer_items: tuple[type[ViewerItem], ...] = (PluginViewer, TextFileViewer, ImageViewer)

        for viewer_item in viewer_items:
            for suffix in viewer_item.get_supported_file_types():
                self.type_list.setdefault(suffix, []).append(viewer_item)

    def handle_update_filepath(self, filepath: str) -> None:
        self.update_ui(filepath)

    def update_ui(self, filepath: str) -> None:
        layout = self.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if filepath:
            path = Path(filepath)
            if path.exists():
                suffix = path.suffix.lower()
                if suffix in self.type_list:
                    widget_types: list[type[ViewerItem]] = self.type_list[suffix]
                    if len(widget_types) > 1:
                        tabs = QTabWidget()
                        widget_type: type[ViewerItem]
                        for widget_type in widget_types:
                            widget = widget_type(filepath)
                            tabs.addTab(widget, widget.name)
                        self.widget = tabs
                    else:
                        self.widget = widget_types[0](filepath)
                    layout.addWidget(self.widget)
                else:
                    self.widget = UnsupportedFileViewer(filepath)
                    layout.addWidget(self.widget)
            else:
                logger.warning("File not found: {filepath}", filepath=filepath)
