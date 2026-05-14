import webbrowser
from PyQt6.QtWidgets import QMainWindow
from ..utils.logger import logger

def open_github() -> None:
    try:
        logger.info('Open github repository')
        webbrowser.open('https://github.com/Vdograd/HiveLauncher')
    except Exception as e:
        logger.error(f'Failed open repository: {e}')

def add_progress(self: QMainWindow, cur_value: int) -> None:
    self.progress_bar.setValue(cur_value+1)
    self.text_status.setText(f"Загрузка: {cur_value+1}%")

    "В новых комитах будет реализовано обновление переменной, отвечающая за хранение % загрузки"





