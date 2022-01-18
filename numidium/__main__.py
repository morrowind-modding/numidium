import sys

from numidium.logger import logger

if __name__ == "__main__":
    logger.info(f"{sys.argv=}")

    if "--headless" in sys.argv:
        print("Headless Mode!")
    else:
        from numidium import ui

        ui.exec()
