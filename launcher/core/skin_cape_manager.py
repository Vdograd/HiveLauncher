from PyQt6.QtCore import QThread, pyqtSignal
from dotenv import load_dotenv
import os
import shutil
import hashlib
import requests
from ..utils.logger import logger
from ..utils.configurator import Configurator

config = Configurator()

url_s = os.getenv('SYSTEM_SKIN_CAPE_URL')
key_s = f"OAuth {os.getenv('SYSTEM_SKIN_CAPE_KEY')}"
url_delete = os.getenv('SYSTEM_SKIN_CAPE_URL_DEL')
url_get = os.getenv('SYSTEM_HEAD_TEXTURE_URL')
key_get = f"OAuth {os.getenv('SYSTEM_HEAD_TEXTURE_KEY')}"

class LoadSkin(QThread):
    progress = pyqtSignal()
    finished = pyqtSignal(str, int)
    error = pyqtSignal(str)

    def __init__(self, user, file_path, size):
        super().__init__()
        self.user = user
        self.file_path = file_path
        self.size = size

    def move_copy_file(self):
        try:
            file = self.file_path
            target_directory = f"{config.static_folder}\\head_skins_response\\{self.user}"
            new_filename = f"{self.user}.png"
            target_path = os.path.join(target_directory, new_filename)
            shutil.copy2(file, target_path)
        except Exception as e:
            logger.error(str(e))
            self.error.emit("Ошибка")

    def run(self):
        self.progress.emit()
        sha256 = hashlib.sha256()
        sha256.update(self.user.encode('utf-8'))
        file_name = sha256.hexdigest()

        url = url_s
        headers = {
            "Authorization": key_s
        }

        params = {
            "path": f"/HiveLauncherSkins/{file_name}.png",
            "overwrite": "true"
        }
        try:
            logger.info('Try get response from loadskin')
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            upload_info = response.json()
            upload_url = upload_info["href"]

            with open(self.file_path, 'rb') as file:
                logger.info('Try put response from loadskin')
                upload_response = requests.put(upload_url, files={'file': file})
                upload_response.raise_for_status()
                output_dir = f"{config.static_folder}\\head_skins_response\\{self.user}"
                os.makedirs(output_dir, exist_ok=True)
                self.move_copy_file()
                self.finished.emit(self.user, self.size)
        except Exception as e:
            logger.error(str(e))
            self.error.emit("Ошибка")

class ClearSkin(QThread):
    progress = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, user):
        super().__init__()
        self.user = user

    def run(self):
        self.progress.emit()
        sha256 = hashlib.sha256()
        sha256.update(self.user.encode('utf-8'))
        file_name = sha256.hexdigest()

        url = url_delete
        headers = {
            "Authorization": key_s
        }

        params = {
            "path": f"/HiveLauncherSkins/{file_name}.png",
            "permanently": True
        }
        try:
            logger.info('Try delete response from loadskin')
            response = requests.delete(url, headers=headers, params=params)
            if response.status_code == 204 or response.status_code == 404:
                self.finished.emit()
            else:
                self.finished.emit()
                logger.error(f'Code delete skin: {response.status_code}')
        except Exception as e:
            logger.error(str(e))
            self.finished.emit()

class LoadCape(QThread):
    progress = pyqtSignal()
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, user, file_path):
        super().__init__()
        self.user = user
        self.file_path = file_path

    def run(self):
        self.progress.emit()
        sha256 = hashlib.sha256()
        sha256.update(self.user.encode('utf-8'))
        file_name = f"{sha256.hexdigest()}_cape"

        url = url_s
        headers = {
            "Authorization": key_s
        }
        if self.file_path.endswith('.png'):
            clape = 'png'
        elif self.file_path.endswith('.gif'):
            clape = 'gif'
        params = {
            "path": f"/HiveLauncherSkins/{file_name}.{clape}",
            "overwrite": "true"
        }
        try:
            if clape == "gif":
                url_del = url_delete
                pm = {
                    "path": f"/HiveLauncherSkins/{file_name}.png",
                    "permanently": True
                }
                logger.info('Try delete response from LoadCape')
                requests.delete(url_del, headers=headers, params=pm)
            logger.info('Try get response from loadCape')
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            upload_info = response.json()
            upload_url = upload_info["href"]

            with open(self.file_path, 'rb') as file:
                logger.info('Try put response from loadCape')
                upload_response = requests.put(upload_url, files={'file': file})
                upload_response.raise_for_status()
                self.finished.emit()
        except Exception as e:
            logger.error(str(e))
            self.error.emit("Ошибка")

class ClearCape(QThread):
    progress = pyqtSignal()
    finished = pyqtSignal()
    def __init__(self, user):
        super().__init__()
        self.user = user

    def run(self):
        self.progress.emit()
        sha256 = hashlib.sha256()
        sha256.update(self.user.encode('utf-8'))
        file_name = f"{sha256.hexdigest()}_cape"

        url = url_delete
        headers = {
            "Authorization": key_s
        }

        all_params = [
            {
                "path": f"/HiveLauncherSkins/{file_name}.png",
                "permanently": True
            },
            {
                "path": f"/HiveLauncherSkins/{file_name}.gif",
                "permanently": True
            }
        ]

        try:
            for param in all_params:
                logger.info('Try delete response from ClearCape')
                requests.delete(url, headers=headers, params=param)
            else:
                self.finished.emit()
        except Exception as e:
            logger.error(str(e))
            self.finished.emit()

class ClassicSlimSkin(QThread):
    progress = pyqtSignal()
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, user, skin_type):
        super().__init__()
        self.user = user
        self.skin_type = skin_type

    def run(self):
        self.progress.emit()

        hash256 = hashlib.sha256()
        hash256.update(self.user.encode('utf-8'))
        file_name = f"{hash256.hexdigest()}_slim"

        if self.skin_type == "classic":
            url = url_s
            headers = {
                "Authorization": key_s
            }

            params = {
                "path": f"/HiveLauncherSkins/{file_name}",
                "overwrite": "true"
            }
            try:
                logger.info('Try change classic -> slim')
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                upload_info = response.json()
                upload_url = upload_info["href"]
                with open(f"{config.static_folder}\\{file_name}", 'w') as file:
                    file.write("")
                with open(f"{config.static_folder}\\{file_name}", 'rb') as file:
                    logger.info('Try put response from change classic -> slim')
                    upload_response = requests.put(upload_url, files={'file': file})
                    upload_response.raise_for_status()
                self.finished.emit('slim')
            except Exception as e:
                logger.error(str(e))
                self.error.emit('Ошибка')

        elif self.skin_type == "slim":
            url = url_delete
            headers = {
                "Authorization": key_s
            }

            params = {
                "path": f"/HiveLauncherSkins/{file_name}",
                "permanently": True
            }
            try:
                logger.info('Try change slim -> classic')
                response = requests.delete(url, headers=headers, params=params)
                if response.status_code == 204 or response.status_code == 404:
                    self.finished.emit('classic')
                else:
                    self.error.emit('Ошибка')
                    logger.error(f'Code change slim -> classic: {response.status_code}')
            except Exception as e:
                logger.error(str(e))
                self.error.emit('Ошибка')

def get_type_skin_nickname(nickname):
    hash256 = hashlib.sha256()
    hash256.update(nickname.encode('utf-8'))
    file_name = f"{hash256.hexdigest()}_slim"

    url = url_get
    headers = {
        "Authorization": key_get
    }

    params = {
        "path": f"/HiveLauncherSkins/{file_name}"
    }
    try:
        logger.info('Try get type skin nickname')
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return 'slim'
        elif response.status_code == 404:
            return 'classic'
        else:
            logger.error(f'Code get type skin nickname: {response.status_code}')
            return 'classic'
    except Exception as e:
        logger.error(str(e))
        return 'classic'