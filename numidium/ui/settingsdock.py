from enum import Enum

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class SettingItemType(Enum):
    TEXT = 1
    NUMBER = 2


class SettingItem:
    def __init__(self, label, value, valueType, valueMetadata):
        self._label = label
        self._value = value
        self._valueType = valueType

        self.label = str(label)
        self.input = None

        if SettingItemType.TEXT == valueType:
            max = valueMetadata["max"] or 32767
            input = QLineEdit()
            input.setMaximumWidth(250)
            input.setMaxLength(max)
            input.setText(value)

            self.input = input

        elif SettingItemType.NUMBER == valueType:
            max = valueMetadata["max"] or 2147483647
            min = valueMetadata["min"] or -2147483647
            input = QSpinBox()
            input.setMaximumWidth(250)
            input.setMaximum(max)
            input.setMinimum(min)

            self.input = input


class PluginsTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        ####### Plugins
        formLayout = QFormLayout()

        formLayout.addRow(QLabel("This is a placeholder for our plugins information."))

        self.setLayout(formLayout)


class SettingsTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        ####### General Settings
        name = SettingItem("Name:", "Test", SettingItemType.TEXT, {"max": 50})
        email = SettingItem("Email:", "Test@gmail.com", SettingItemType.TEXT, {"max": 150})
        age = SettingItem("Age:", 2, SettingItemType.NUMBER, {"max": 150, "min": 1})

        # Layout
        formLayout = QFormLayout()
        formLayout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        formLayout.setLabelAlignment(Qt.AlignLeft)
        formLayout.setVerticalSpacing(15)

        # Add decoration
        formLayout.addRow(
            QLabel("This is a placeholder for our settings information."),
        )

        # Add inputs
        formLayout.addRow(name.label, name.input)
        formLayout.addRow(email.label, email.input)
        formLayout.addRow(age.label, age.input)

        self.setLayout(formLayout)


class SettingsDock(QWidget):
    def __init__(self) -> None:
        super().__init__()

    def setup_ui(self, win: QWidget) -> None:
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)

        tab_container = QTabWidget()
        tab_container.setTabPosition(QTabWidget.TabPosition.West)

        tab_settings = SettingsTab()
        tab_plugins = PluginsTab()

        tab_container.addTab(tab_settings, "Settings")
        tab_container.addTab(tab_plugins, "Plugins")

        layout.addWidget(tab_container)
        win.setLayout(layout)
