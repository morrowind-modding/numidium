import sys

from numidium.ui.application import Numidium
from numidium.ui.windows.main_window import MainWindow

if __name__ == "__main__":
    app = Numidium(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
