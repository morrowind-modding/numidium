if __name__ == "__main__":
    import sys

    if "--headless" not in sys.argv:
        from numidium.ui.application import Numidium
        from numidium.ui.windows.main_window import MainWindow

        application = Numidium()
        window = MainWindow()
        window.show()
        sys.exit(application.exec())
