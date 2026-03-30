import sys
from PyQt6.QtWidgets import QApplication
from launcher.ui.page_manager import HiveLauncher
from launcher.auth.auth_manager import AuthManager
from launcher.utils.logger import logger
from launcher.utils.configurator import Configurator
from launcher.core.version_manager import obj_Version_Manager
from launcher.utils.error_manager import ErrorExc

def main():
    auth_mng = AuthManager()
    conf = Configurator()

    try:
        logger.session_start()
        logger.info("Initial connect db")
        auth_mng.initial_database()
        logger.info("Fixed system config")
        conf.fixed_system_config()
        logger.info('Init minecraft directory')
        obj_Version_Manager.init_minecraft_directory()
    except Exception as e:
        ErrorExc(e)

    logger.info("Connect Window")
    app = QApplication(sys.argv)
    window = HiveLauncher()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
