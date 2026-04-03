from ..utils.logger import logger
import shutil
import os
from ..utils.configurator import Configurator
from ..core.version_manager import obj_Version_Manager
import uuid
from PyQt6.QtCore import QThread, pyqtSignal
import minecraft_launcher_lib as mn
import json
from ..utils.error_manager import ErrorExc
import re
conf = Configurator()

class InstallStartGame(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(float)
    hide_launcher_signal = pyqtSignal(bool)
    show_launcher_signal = pyqtSignal(bool)
    close = pyqtSignal()

    def __init__(self, nickname, version, play_time):
        super().__init__()
        self.username = nickname
        self.version = version
        self.play_time = play_time

    def run(self):
        try:
            logger.info("Step 1 - Preparing options to launch the game")
            self.progress.emit("Подготовка...")

            data = conf.get_config()
            self.maxm = int(data["maxm"].split()[3])
            self.wind_size = data["window_size"].split("x")
            self.minecraft_directory = obj_Version_Manager.minecraft_directory
            self.version_directory = obj_Version_Manager.get_version_path(self.version)

            namespace = uuid.NAMESPACE_DNS
            self.options = {
                'username': self.username,
                'uuid': str(uuid.uuid5(namespace, self.username)),
                'token': '',
                "jvmArguments": [f"-Xms{int(self.maxm/2)}m", f"-Xmx{self.maxm}m"],
                "launcherName": "HiveLauncher",
                "launcherVersion": conf.version_launcher
            }
            self.options["customResolution"] = True
            self.options["resolutionWidth"] = str(self.wind_size[0])
            self.options["resolutionHeight"] = str(self.wind_size[1])

            self.after_start_game = data["after_start"]
            self.after_download_game = data["after_download"]

            logger.info("Step 2 - Preparing install version")
            version_clear = re.sub(r'[^0-9.]', '', self.version)

            if 'Fabric' in self.version:
                version_for_get_json = self.version
                version_install = version_clear
            elif 'Forge' in self.version:
                version_for_get_json = self.version
                version_install = mn.forge.find_forge_version(version_clear)
            else:
                version_for_get_json = version_clear
                version_install = version_clear

            logger.info("Step 3 - Found version in installed versions")
            version_found = False
            all_installed_versions = conf.get_installed_versions()['versions']
            if obj_Version_Manager.version_to_folder_json(version_for_get_json) in all_installed_versions:
                version_found = True

            logger.info("Step 4 - Install version | Start game")
            if not version_found:
                logger.info(f"Step 4.1 - Version not found, installing {self.version}")
                self.progress.emit("Установка...")

                if 'Forge' in self.version:
                    mn.forge.install_forge_version(version_install, self.version_directory)
                elif 'Fabric' in self.version:
                    mn.fabric.install_fabric(version_install, self.version_directory)
                else:
                    mn.install.install_minecraft_version(version_install, self.version_directory)

                all_installed_versions["versions"].append(obj_Version_Manager.version_to_folder_json(version_for_get_json))
                with open(f"{conf.config_folder}\\versions.json", "w", encoding="ansi") as file:
                    json.dump(all_installed_versions, file, indent=4, ensure_ascii=False)

                logger.info("Step 4.2 - Version installed, starting game")
                if self.after_download_game == "nothing":
                    self.finished.emit(self.play_time)
                else:
                    self.start_game(...)
            else:
                logger.info(f"Step 4.3 - Version found, starting game {self.version}")
                self.start_game(...)
        except Exception as e:
            ErrorExc(e)

    def start_game(self):
        ...

            

































    def copy_minecraft_files_before_start(self, version):
        try:
            hotbar_path = None
            command_history_path = None
            options_path = None
            servers_dat_path = None
            servers_dat_old = None

            versions_config = conf.get_installed_versions()
            last_version_used = versions_config['last_version']
            if last_version_used == version: return
            if last_version_used != None:
                path_version_last = obj_Version_Manager.get_version_path(last_version_used)
                if os.path.exists(os.path.join(path_version_last, "hotbar.nbt")):
                    hotbar_path = os.path.join(path_version_last, "hotbar.nbt")
                if os.path.exists(os.path.join(path_version_last, "command_history.txt")):
                    command_history_path = os.path.join(path_version_last, "command_history.txt")
                if os.path.exists(os.path.join(path_version_last, "options.txt")):
                    options_path = os.path.join(path_version_last, "options.txt")
                if os.path.exists(os.path.join(path_version_last, "servers.dat")):
                    servers_dat_path = os.path.join(path_version_last, "servers.dat")
                if os.path.exists(os.path.join(path_version_last, "servers.dat_old")):
                    servers_dat_old = os.path.join(path_version_last, "servers.dat_old")

                all_files_path = [hotbar_path, command_history_path, options_path, servers_dat_path, servers_dat_old]
                all_files_names = ["hotbar.nbt", "command_history.txt", "options.txt", "servers.dat", "servers.dat_old"]
                path_version_currect = obj_Version_Manager.get_version_path(version)

                for file_path, file_name in zip(all_files_path, all_files_names):
                    if file_path == None: continue
                    target_path = os.path.join(path_version_currect, file_name)
                    shutil.copy2(file_path, target_path)
        except Exception as e:
            logger.error(e)

    