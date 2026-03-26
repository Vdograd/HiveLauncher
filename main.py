import sys
from PyQt6.QtWidgets import QApplication
from launcher.ui.page_manager import HiveLauncher
from launcher.auth.auth_manager import AuthManager
from launcher.utils.logger import logger
from launcher.utils.configurator import Configurator

def main():
    auth_mng = AuthManager()
    conf = Configurator()

    logger.session_start()
    logger.info("Initial connect db")
    try:
        auth_mng.initial_database()
    except Exception as e:
        logger.error(str(e))
    try:
        conf.fixed_system_config()
    except Exception as e:
        logger.error(f'Critical error: {e}')

    logger.info("Connect Window")
    app = QApplication(sys.argv)
    window = HiveLauncher()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())