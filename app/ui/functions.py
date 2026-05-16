import webbrowser
from PyQt6.QtWidgets import QMainWindow
from ..utils.logger import logger
from ..core.thread_classes import *
import subprocess
from PyQt6 import QtCore, QtWidgets
from .style import set_style

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
    self.scanning.start_s.connect(lambda version: start_s(self, version))
    logger.info("Start scanning version update")
    self.scanning.start()

def start_s(self, version):
    self.progress_bar.setValue(0)
    self.text_version.setText(version)
    self.text_version.setObjectName('text_first_version_step_1')
    self.text_global_status.setText('Проверка обновлений')
    self.text_status.setText("Сканирование...")
    self.cloud_layout_ver.setObjectName('first_version_step_1')
    self.ellips_cur_ver.setObjectName('ellips_first_version_step_1')
    self.text_approximate_time.hide()
    self.text_speed_realtime.hide()
    self.text_speed.hide()
    self.cloud_layout_new_ver.hide()
    self.arrow_version.hide()
    try:
        set_style(self, self.color)
    except Exception as e:
        show_error(self, e)

def start_download(self, version) -> None:
    self.progress_bar.setValue(0)
    self.text_version.setObjectName('text_first_version_step_2')
    self.text_global_status.setText('Установка обновлений')
    self.text_status.setText("Загрузка: 0%")
    self.cloud_layout_ver.setObjectName('first_version_step_2')
    self.ellips_cur_ver.setObjectName('ellips_first_version_step_2')
    self.arrow_version.show()
    self.text_new_version.setText(f"v{version}")
    self.cloud_layout_new_ver.show()
    self.text_speed.show()
    self.text_approximate_time.show()
    self.text_speed_realtime.show()
    try:
        set_style(self, self.color)
    except Exception as e:
        show_error(self, e)


def show_error(self, error: Exception) -> None: logger.error(error)

def completed_scanning(self, status: int, version: str) -> None:
    self.start = StartLauncher(status, version)
    self.start.error.connect(lambda error: show_error(self, error))
    self.start.launcher_open.connect(lambda path, version: launcher_open(self, path, version))
    self.start.start_download.connect(lambda version: start_download(self, version))
    self.start.add_progress.connect(lambda x: add_progress(self, x))
    self.start.speed_realtime.connect(lambda x: speed_realtime_set(self, x))
    self.start.approximate_time.connect(lambda x: approximate_time_set(self, x))
    logger.info("Start launcher or install new version")
    self.start.start()

def add_progress(self, cur_value: int) -> None:
    self.progress_bar.setValue(cur_value)
    self.text_status.setText(f"Загрузка: {cur_value}%")

def launcher_open(self, path: str, version: str) -> None:
    if os.path.exists(path):
        logger.info('Open launcher and close update-file')
        process = subprocess.Popen(f'"{path}"', cwd=os.path.join(build.folders_versions_launcher, version))
        logger.info(f"Launcher open, PID: {process.pid if process else 'unknown'}")
        logger.info('Close update-file')
        close_application(self)
    else:
        logger.warn('HiveLauncher.exe not found. Send process on scanning')
        scanning(self)

def close_application(self):
    try:
        app = QtWidgets.QApplication.instance()
        if app:
            app.quit()
    except Exception as e:
        show_error(self, e)

def speed_realtime_set(self, speed: str) -> None:
    self.text_speed_realtime.setText(speed)

def approximate_time_set(self, time: str) -> None:
    self.text_approximate_time.setText(time)