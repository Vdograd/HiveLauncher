from PyQt6.QtCore import QThread, pyqtSignal
from ..db.db_manager import Manager
from .folder_manager import *
import os
from ..utils.build import build
from ..utils.logger import logger
import shutil

class Scanning(QThread):
    error = pyqtSignal(Exception)
    finished = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        self.dbm = Manager()


    def run(self):
        try:
            self.last_version = self.dbm.get_last_version(0)
            self.currect_version = get_currect_version() # type: ignore

            if self.last_version == self.currect_version:
                self.finished.emit(1, self.currect_version)
            else:
                if self.currect_version == None:
                    self.restart_new_update()
                else:
                    self.preparing_new_version()

        except Exception as e:
            self.error.emit(e)

    def restart_new_update(self) -> None:
        try:
            # Запоминаем файлы конфигурации лаунчера
            files_config = []
            files_name = []
            config_json = os.path.join(build.folders_versions_launcher, '_internal', 'launcher', 'data', 'config.json')
            nicknames_json = os.path.join(build.folders_versions_launcher, '_internal', 'launcher', 'data', 'nicknames.json')
            versions_json = os.path.join(build.folders_versions_launcher, '_internal', 'launcher', 'data', 'versions.json')

            if os.path.exists(config_json):
                files_config.append(config_json)
                files_name.append('config.json')
            if os.path.exists(nicknames_json):
                files_config.append(nicknames_json)
                files_name.append('nicknames.json')
            if os.path.exists(versions_json):
                files_config.append(versions_json)
                files_name.append('versions.json')

            logger.info(f"\ncj: {config_json} {os.path.exists(config_json)}, \nnj: {nicknames_json} {os.path.exists(nicknames_json)}, \nvj: {versions_json} {os.path.exists(versions_json)}")

            # Создаем папку с именем последней версией, заменяя "." на "#"
            vers = self.last_version.replace('.', '#')
            os.makedirs(os.path.join(build.folders_versions_launcher, vers, '_internal', 'launcher', 'data'), exist_ok=True)

            # Копируем файлы конфигурации в новую версию
            for file_path, file_name in zip(files_config, files_name):
                target_path = os.path.join(build.folders_versions_launcher, vers, '_internal', 'launcher', 'data', file_name)
                logger.info(f'Copy file in {target_path}')
                shutil.copy2(file_path, target_path)

            # Отправляем на установку новой версии
            self.finished.emit(0, self.last_version)

        except Exception as e:
            self.error.emit(e)
    
    def preparing_new_version(self) -> None:
        self.currect_version: str
        try:
            # Запоминаем файлы конфигурации лаунчера
            files_config = []
            files_name = []
            config_json = os.path.join(build.folders_versions_launcher, f'{self.currect_version.replace(".", "#")}', '_internal', 'launcher', 'data', 'config.json')
            nicknames_json = os.path.join(build.folders_versions_launcher, f'{self.currect_version.replace(".", "#")}', '_internal', 'launcher', 'data', 'nicknames.json')
            versions_json = os.path.join(build.folders_versions_launcher, f'{self.currect_version.replace(".", "#")}', '_internal', 'launcher', 'data', 'versions.json')

            if os.path.exists(config_json):
                files_config.append(config_json)
                files_name.append('config.json')
            if os.path.exists(nicknames_json):
                files_config.append(nicknames_json)
                files_name.append('nicknames.json')
            if os.path.exists(versions_json):
                files_config.append(versions_json)
                files_name.append('versions.json')

            logger.info(f"\ncj: {config_json} {os.path.exists(config_json)}, \nnj: {nicknames_json} {os.path.exists(nicknames_json)}, \nvj: {versions_json} {os.path.exists(versions_json)}")

            # Создаем папку с именем последней версией, заменяя "." на "#"
            vers = self.last_version.replace('.', '#')
            os.makedirs(os.path.join(build.folders_versions_launcher, vers, '_internal', 'launcher', 'data'), exist_ok=True)

            # Копируем файлы конфигурации в новую версию
            for file_path, file_name in zip(files_config, files_name):
                target_path = os.path.join(build.folders_versions_launcher, vers, '_internal', 'launcher', 'data', file_name)
                logger.info(f'Copy file in {target_path}')
                shutil.copy2(file_path, target_path)

            # Отправляем на установку новой версии
            self.finished.emit(0, self.last_version)

        except Exception as e:
            self.error.emit(e)

