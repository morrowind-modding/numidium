if __name__ == "__main__":
    import sys

    if "--headless" not in sys.argv:
        from numidium.ui.application import Numidium
        from numidium.ui.windows.manager import ManagerWindow

        application = Numidium()
        window = ManagerWindow()
        window.show()
        sys.exit(application.exec())
