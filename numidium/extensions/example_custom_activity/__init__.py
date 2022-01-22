from PySide6.QtWidgets import QLabel

from numidium.ui.activity_bar import ActivityBar, ActivityBarItem

item = ActivityBarItem(widget=QLabel("Hello World!"), icon="icons:circle_24dp.svg", text="Custom Activity")


def register() -> None:
    ActivityBar.instance().add_item(item)


def unregister() -> None:
    ActivityBar.instance().remove_item(item)
