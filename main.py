import sys
from PyQt6.QtWidgets import QApplication
from app.utils.logger import logger
from app.utils.build import build
#from app.utils.error import ErrorExc
from app.ui.window_update import App

def main():
    try:
        logger.session_start()
        logger.info("Connect Window")
        app = QApplication(sys.argv)
        window = App()
        window.show()
        return app.exec()
    except Exception as e:
        pass
        #ErrorExc(e)

if __name__ == "__main__":
    sys.exit(main())