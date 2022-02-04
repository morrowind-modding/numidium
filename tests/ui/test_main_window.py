# type: ignore

from pytestqt.qtbot import QtBot

from numidium.ui.windows.main_window import MainWindow


def test_welcome_window(qtbot: QtBot):
    window = MainWindow()
    window.show()

    qtbot.addWidget(window)

    window.show_welcome_window()


def test_default_window(qtbot: QtBot):
    window = MainWindow()
    window.show()

    qtbot.addWidget(window)

    window.show_default_window()
