import json
from ...utils.configurator import Configurator
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QSize
from PyQt6 import QtCore, QtGui, QtWidgets
import hashlib
import requests
import os
import minecraft_launcher_lib as mn
from ...utils.logger import logger
from ...core.texture_manager import TextureSize64, TextureSize1024
from PIL import Image
configurator = Configurator()
logger = logger

def how_start_page():
    try:
        with open(f"{configurator.config_folder}\\nicknames.json", "r", encoding="ansi") as file:
            data = json.load(file)
            return 'setup' if data["nicknames"] == [] else 'login'
    except Exception as e:
        return e

def create_shadow(type_shadow):
    if type_shadow == 'light':
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 50))
    elif type_shadow == 'dark':
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(91, 91, 91, 50))
    return shadow

class GetPixture(QThread):
    progress = pyqtSignal()
    finished = pyqtSignal(list)
    def __init__(self, nicks):
        super().__init__()
        self.nicks = nicks
        
    def download_texture_skin_with(self, nickname):
        sha256 = hashlib.sha256()
        sha256.update(nickname.encode('utf-8'))
        file_name = sha256.hexdigest()

        url = os.getenv("SYSTEM_HEAD_TEXTURE_URL")
        headers = {
            "Authorization": f"OAuth {os.getenv('SYSTEM_HEAD_TEXTURE_KEY')}"
        }

        params = {
            "path": f"/HiveLauncherSkins/{file_name}.png"
        }

        try:
            logger.info('Start downloading head texture')
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 404:
                logger.warn('Not found head texture in api')
                return False
            elif response.status_code == 401:
                logger.error("Unauthorized in api")
                return
            elif response.status_code == 403:
                logger.error("Not access for api")
                return
            
            response.raise_for_status()
            download_info = response.json()
            
            if "href" not in download_info:
                logger.error(f"Invalid response from API: {download_info}")
                return
                
            download_url = download_info["href"]
            
            download_response = requests.get(download_url)
            download_response.raise_for_status()
            os.makedirs(f"{configurator.static_folder}\\head_skins_response\\{nickname}", exist_ok=True)
            with open(f"{configurator.static_folder}\\head_skins_response\\{nickname}\\{nickname}.png", 'wb') as file:
                file.write(download_response.content)
            return True
        except Exception as e:
            logger.error(e)

    def run(self):
        self.progress.emit()
        nicks = self.nicks
        status_current = self.download_texture_skin_with(nicks)
        if status_current == True:
            img = Image.open(f"{configurator.static_folder}\\head_skins_response\\{nicks}\\{nicks}.png")
            if img.size == (1024,1024):
                logger.info("Get 1024 head texture")
                TextureSize1024().save_texture(nicks)
            elif img.size == (64,64):
                logger.info("Get 64 head texture")
                TextureSize64().save_texture(nicks)
            head_img = [f"{configurator.static_folder}\\head_skins_response\\{nicks}\\{nicks}_50x50.png", 
                        f"{configurator.static_folder}\\head_skins_response\\{nicks}\\{nicks}_150x150.png"]
        elif status_current == False:
            head_img = [f"{configurator.static_folder}\\home\\none_account_50.png", f"{configurator.static_folder}\\account\\none_account_150.png"]
        self.finished.emit(head_img)

def forge_enabled_bool() -> bool:
    forge = False
    try:
        response_ip = requests.get("http://ip-api.com/json/", timeout=3)
        if response_ip.status_code == 429:
            logger.warn(f"Too many requests to IP API: {response_ip.status_code}")
            forge = True
        elif response_ip.status_code != 200:
            logger.warn(f'Error response from IP API: {response_ip.status_code}')
            forge = False
        elif response_ip.json()["countryCode"] == "RU":
            forge = False
        else:
            forge = True
    except requests.exceptions.Timeout as e:
        logger.error(e)
    except Exception as e:
        forge = False
        logger.error(e)
    return forge

def versions_add(self):
    self.select_version = QtWidgets.QComboBox(parent=self.centralwidget)
    self.select_version.setGeometry(QtCore.QRect(400, 623, 300, 55))
    self.select_version.setFont(self.font.get_font(12, "1"))
    self.select_version.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
    self.select_version.setIconSize(QtCore.QSize(26, 26)) 
    self.select_version.setGraphicsEffect(create_shadow(configurator.get_color_theme()))
    self.select_version.setObjectName("select_version")

    self.select_version_view = QtWidgets.QListView(self.select_version)
    self.select_version_view.setFont(self.font.get_font(12, "1"))
    self.select_version_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    self.select_version_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
    self.select_version_view.setObjectName("select_version_view")
    self.select_version.setView(self.select_version_view)
    self.select_version.hide()

    forge = forge_enabled_bool()
    try:
        for version_get in mn.utils.get_version_list():
            versions_not_use = ["1.7.9", "1.7.8", "1.7.7", "1.7.6", "1.7.5", "1.7.4", "1.7.3", "1.7.2", "1.6.4", "1.6.3", "1.6.2", "1.6.1", "1.5.2", "1.5.1", "1.5", "1.4.7", "1.4.6", "1.4.5", "1.4.4", "1.4.3", "1.4.2", "1.4.1", "1.3.2", "1.3.1", "1.2.5", "1.2.4", "1.2.3", "1.2.2", "1.2.1", "1.1", "1.0"]
            if version_get['id'] in versions_not_use:
                pass
            else:
                if version_get['type'] == 'release':
                    color = configurator.get_color_theme()
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Normal,QtGui.QIcon.State.On)
                    icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.Off)
                    icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.On)
                    icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.Off)
                    icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.On)
                    icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.Off)
                    icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.On)
                    self.select_version.addItem(icon, f'Minecraft {version_get['id']}')
                if version_get['type'] == 'release':
                    for version_fabric in mn.fabric.get_stable_minecraft_versions():
                        if version_fabric == version_get['id']:
                            icon1 = QtGui.QIcon()
                            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Normal,QtGui.QIcon.State.On)
                            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.Off)
                            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.On)
                            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.Off)
                            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.On)
                            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.Off)
                            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.On)       
                            self.select_version.addItem(icon1, f'Minecraft Fabric {version_fabric}')
                if version_get['type'] == 'release':
                    if forge:
                        versions_forge = mn.forge.find_forge_version(version_get['id'])
                        if not versions_forge: pass
                        else:
                            icon2 = QtGui.QIcon()
                            icon2.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\forge.svg"), QtGui.QIcon.Mode.Normal,QtGui.QIcon.State.On)
                            icon2.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\forge.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.Off)
                            icon2.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\forge.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.On)
                            icon2.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\forge.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.Off)
                            icon2.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\forge.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.On)
                            icon2.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\forge.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.Off)
                            icon2.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\forge.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.On)       
                            self.select_version.addItem(icon2, f'Minecraft Forge {version_get["id"]}')
    except Exception as e:
        logger.error(e)
    vpl = configurator.get_installed_versions()
    if vpl["last_version"] != None:
        self.select_version.setCurrentText(vpl["last_version"])