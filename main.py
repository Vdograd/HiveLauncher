import sys
from PyQt6.QtWidgets import QApplication
from launcher.ui.page_manager import HiveLauncher
from launcher.auth.auth_manager import AuthManager
from launcher.utils.logger import Logger

def main():
    logger = Logger()
    auth_mng = AuthManager()
    logger.session_start()
    logger.info("Initial connect db")
    auth_mng.initial_database()

    logger.info("Connect Window")
    app = QApplication(sys.argv)
    window = HiveLauncher()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())