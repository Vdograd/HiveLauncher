from launcher.utils.error_manager.error import ErrorExc
from launcher.utils.download_update import update_file
from launcher.auth.auth_manager import auth_manager
from launcher.utils.build import RestartConfig
from launcher.ui.manager import HiveLauncher
from PyQt6.QtWidgets import QApplication
from launcher.utils.logger import logger
import sys

def main() -> None:
    try:
        update_file()
    except Exception as e:
        ErrorExc(e)
    try:
        logger.info("Initial connect db")
        auth_manager.initial_database()
    except Exception as e:
        ErrorExc(e)
    try:
        logger.info("Fixed system config")
        RestartConfig()
    except Exception as e:
        ErrorExc(e)

    try:
        logger.info('Init minecraft directory')
        #obj_Version_Manager.init_minecraft_directory()
    except Exception as e:
        ErrorExc(e)

    try:
        logger.info("Retryed update play time (if needed)")
        auth_manager.retry_update_time()
    except Exception as e:
        logger.error(f"Failed updated play time: {e}")

    logger.info("Connect Window")
    app = QApplication(sys.argv)
    try:
        window = HiveLauncher()
        window.show()
        return app.exec() #type: ignore
    except Exception as e:
        ErrorExc(e)

if __name__ == "__main__":
    sys.exit(main())


