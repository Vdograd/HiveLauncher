import webbrowser
from PyQt6.QtWidgets import QMainWindow
from ..utils.logger import logger
from ..core.thread_classes import *

def open_github() -> None:
    try:
        logger.info('Open github repository')
        webbrowser.open('https://github.com/Vdograd/HiveLauncher')
    except Exception as e:
        logger.error(f'Failed open repository: {e}')

def scanning(self) -> None:
    self.scanning = Scanning()
    self.scanning.error.connect(lambda error: show_error(self, error))
    self.scanning.finished.connect(lambda status, version: completed_scanning(self, status,version))
    logger.info("Start scanning version update")
    self.scanning.start()


def show_error(self, error: Exception) -> None: ...

def completed_scanning(self, status: int, version: str) -> None:
    self.start = StartLauncher(status, version)
    self.start.error.connect(lambda error: show_error(self, error))
    self.start.launcher_open.connect(lambda: launcher_open(self))
    self.start.add_progress.connect(lambda x: add_progress(self, x))
    self.start.speed_realtime.connect(lambda x: speed_realtime_set(self, x))
    self.start.approximate_time.connect(lambda x: approximate_time_set(self, x))
    logger.info("Start launcher or install new version")
    self.start.start()

def add_progress(self, cur_value: int) -> None:
    self.progress_bar.setValue(cur_value+1)
    self.text_status.setText(f"Загрузка: {cur_value+1}%")

    "В новых комитах будет реализовано обновление переменной, отвечающая за хранение % загрузки"

def launcher_open(self) -> None: ...
def speed_realtime_set(self, speed: str) -> None: ...
def approximate_time_set(self, time: str) -> None: ...