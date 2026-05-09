import webbrowser
from ..utils.logger import logger

def open_github():
    try:
        logger.info('Open github repository')
        webbrowser.open('https://github.com/Vdograd/HiveLauncher')
    except Exception as e:
        logger.error(f'Failed open repository: {e}')