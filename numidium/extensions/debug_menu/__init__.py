import qtvscodestyle as qtvsc
from PySide6.QtCore import QSize, QSortFilterProxyModel, QStringListModel, Qt, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from numidium.config import config
from numidium.logger import logger
from numidium.ui.enums import AlignmentFlag
from numidium.ui.menu_bar import MenuBar
from numidium.ui.widgets import TextBlockLabel

# TODO: Set icon colour and copy code with color kwarg

VIEW_COLUMNS = 5
AUTO_SEARCH_TIMEOUT = 500
ALL_COLLECTIONS = "All"


class IconBrowser(QMainWindow):
    """
    A small browser window that allows the user to search through all icons from
    the available version of QtAwesome.  You can also copy the name and python
    code for the currently selected icon.
    """
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 500)
        self.setWindowTitle("Icon Browser")

        icon_names, font_names = [], []
        for vs_id in qtvsc.Vsc:
            icon_names.append(f"vs.{vs_id.name.lower()}")
            font_names.append(vs_id.name.lower())
        for fa_b_id in qtvsc.FaBrands:
            icon_names.append(f"fa-b.{fa_b_id.name.lower()}")
            font_names.append(fa_b_id.name.lower())
        for fa_r_id in qtvsc.FaRegular:
            icon_names.append(f"fa-r.{fa_r_id.name.lower()}")
            font_names.append(fa_r_id.name.lower())
        for fa_s_id in qtvsc.FaSolid:
            icon_names.append(f"fa-s.{fa_s_id.name.lower()}")
            font_names.append(fa_s_id.name.lower())

        self._filter_timer = QTimer(self)
        self._filter_timer.setSingleShot(True)
        self._filter_timer.setInterval(AUTO_SEARCH_TIMEOUT)
        self._filter_timer.timeout.connect(self._update_filter)

        model = IconModel()
        model.setStringList(sorted(icon_names))

        self._proxy_model = QSortFilterProxyModel()
        self._proxy_model.setSourceModel(model)
        self._proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self._list_view = IconListView(self)
        self._list_view.setUniformItemSizes(True)
        self._list_view.setViewMode(QListView.ViewMode.IconMode)
        self._list_view.setModel(self._proxy_model)
        self._list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._list_view.doubleClicked.connect(self._copy_icon_text)

        self._line_edit = QLineEdit(self)
        self._line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._line_edit.textChanged.connect(self._trigger_delayed_update)
        self._line_edit.returnPressed.connect(self._trigger_immediate_update)

        self._theme_combobox = QComboBox(self)
        self._theme_combobox.addItems([theme.value["name"] for theme in qtvsc.Theme])
        self._theme_combobox.setCurrentText(qtvsc.Theme.DARK_VS.value["name"])
        self._theme_combobox.currentTextChanged.connect(self._change_theme)
        self._theme_combobox.setMinimumWidth(200)

        lyt = QHBoxLayout()
        lyt.setContentsMargins(0, 0, 0, 0)
        lyt.addWidget(self._theme_combobox)
        lyt.addWidget(self._line_edit)

        searchbar_frame = QFrame(self)
        searchbar_frame.setLayout(lyt)

        self._copy_button = QPushButton("Copy Name", self)
        self._copy_button.clicked.connect(self._copy_icon_text)

        lyt = QVBoxLayout()
        lyt.addWidget(searchbar_frame)
        lyt.addWidget(self._list_view)
        lyt.addWidget(self._copy_button)

        frame = QFrame(self)
        frame.setLayout(lyt)

        self.setCentralWidget(frame)



    def _update_filter(self):
        """
        Update the string used for filtering in the proxy model with the
        current text from the line edit.
        """
        re_string = ""

        search_term = self._line_edit.text()
        if search_term:
            re_string += f".*{search_term}.*$"

        self._proxy_model.setFilterRegularExpression(re_string)

    def _trigger_delayed_update(self):
        """
        Reset the timer used for committing the search term to the proxy model.
        """
        self._filter_timer.stop()
        self._filter_timer.start()

    def _trigger_immediate_update(self):
        """
        Stop the timer used for committing the search term and update the
        proxy model immediately.
        """
        self._filter_timer.stop()
        self._update_filter()

    def _copy_icon_text(self):
        """
        Copy the name of the currently selected icon to the clipboard.
        """
        indexes = self._list_view.selectedIndexes()
        if not indexes:
            return

        clipboard = QApplication.instance().clipboard()
        clipboard.setText(indexes[0].data())

    def _change_theme(self, theme_name) -> None:
        for theme in qtvsc.Theme:
            if theme.value["name"] == theme_name:
                QApplication.instance().setStyleSheet(qtvsc.load_stylesheet(theme))


class IconListView(QListView):
    """
    A QListView that scales it's grid size to ensure the same number of
    columns are always drawn.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def resizeEvent(self, event):
        """
        Re-implemented to re-calculate the grid size to provide scaling icons

        Parameters
        ----------
        event : QtCore.QEvent
        """
        width = self.viewport().width() - 30
        # The minus 30 above ensures we don't end up with an item width that
        # can't be drawn the expected number of times across the view without
        # being wrapped. Without this, the view can flicker during resize
        tile_width = width / VIEW_COLUMNS
        iconWidth = int(tile_width * 0.8)
        # tile_width needs to be an integer for setGridSize
        tile_width = int(tile_width)

        self.setGridSize(QSize(tile_width, tile_width))
        self.setIconSize(QSize(iconWidth, iconWidth))

        return super().resizeEvent(event)


class IconModel(QStringListModel):
    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def data(self, index, role):
        """
        Re-implemented to return the icon for the current index.

        Parameters
        ----------
        index : QtCore.QModelIndex
        role : int
        Returns
        -------
        Any
        """
        if role == Qt.ItemDataRole.DecorationRole:
            icon_string = self.data(index, Qt.ItemDataRole.DisplayRole)
            prefix, icon_name = icon_string.split(".")  # type: ignore
            specifiers = {"vs": qtvsc.Vsc, "fa-r": qtvsc.FaRegular, "fa-b": qtvsc.FaBrands, "fa-s": qtvsc.FaSolid}
            specifier = specifiers[prefix]
            for specifier in specifiers[prefix]:
                if specifier.name.lower() == icon_name:
                    return qtvsc.theme_icon(specifier)
        return super().data(index, role)

class DebugWindow(QWidget):
    """Debug menu for application troubleshooting.

    A secondary window that exposes tools for troubleshooting the application.
    """

    _label: QLabel
    _description: TextBlockLabel
    _action_view_icons: QPushButton
    _action_clear_settings: QPushButton

    _icon_browser: IconBrowser

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(AlignmentFlag.AlignTop)

        self._label = QLabel("Debug")
        self._description = TextBlockLabel(
            "This is a debug menu for working with the application. Please do not use these buttons unless you know what you are doing."
        )
        self._action_view_icons = QPushButton("View Application Icon Set")
        self._action_clear_settings = QPushButton("Clear Application Settings")
        self._action_clear_settings.setToolTip(
            "Resets application settings. You must restart the application afterwards."
        )

        layout.addWidget(self._label)
        layout.addWidget(self._description)
        layout.addWidget(self._action_view_icons)
        layout.addWidget(self._action_clear_settings)
        self.setLayout(layout)
        self.resize(200, 400)
        self.setWindowTitle("Debug Menu")

        self._action_view_icons.clicked.connect(self._handle_view_icons)
        self._action_clear_settings.clicked.connect(self._handle_clear_settings)

    def _handle_view_icons(self) -> None:
        self._icon_browser = IconBrowser()
        self._icon_browser.show()

    def _handle_clear_settings(self) -> None:
        config.reset()
        config.save_path()
        logger.info("Cleared applicatioon settings! Attempting restart.")
        QMessageBox.warning(
            self.parent(),
            "Restart Application",
            "To fully clear your settings, you must restart the application. A shutdown will be attempted after clicking 'OK.' Please ropen the application afterwards.",
            QMessageBox.Ok,
        )
        if app := QApplication.instance():
            app.exit()

debug_window = DebugWindow()
action = QAction(text="Debug", shortcut="Ctrl+Shift+D")
action.triggered.connect(debug_window.show)

def register() -> None:
    MenuBar.instance().add_action(action)

def unregister() -> None:
    MenuBar.instance().remove_action(action)
