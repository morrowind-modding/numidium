import sys

from logger import logger

if __name__ == "__main__":
    logger.info(f"{sys.argv=}")

    if "--headless" in sys.argv:
        print("Headless Mode!")
    else:
        import ui

        ui.exec()
