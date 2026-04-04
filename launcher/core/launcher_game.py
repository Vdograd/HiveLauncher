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
from ..utils.getenv import GetEnv
import requests
import re
import time
from ..auth.auth_manager import AuthManager
import subprocess

conf = Configurator()
auth = AuthManager()

class InstallStartGame(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(float)
    hide_launcher_signal = pyqtSignal()
    show_launcher_signal = pyqtSignal()
    error = pyqtSignal(Exception)
    close = pyqtSignal()

    def __init__(self, nickname, version, play_time):
        super().__init__()
        self.username = nickname
        self.version = version
        self.play_time = play_time
        self.mode = None

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
            self.version_clear = re.sub(r'[^0-9.]', '', self.version)

            if 'Fabric' in self.version:
                version_for_get_json = self.version
                version_install = self.version_clear
                self.mode = 'Fabric'
            elif 'Forge' in self.version:
                version_for_get_json = self.version
                version_install = mn.forge.find_forge_version(self.version_clear)
                self.mode = 'Forge'
            else:
                version_for_get_json = self.version_clear
                version_install = self.version_clear
                self.mode = ''

            logger.info("Step 3 - Found version in installed versions")
            version_found = False
            all_installed_versions = conf.get_installed_versions()
            if obj_Version_Manager.version_to_folder_json(version_for_get_json) in all_installed_versions['versions']:
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

                version_name_add = obj_Version_Manager.version_to_folder_json(version_for_get_json)
                if version_name_add == None: raise
                all_installed_versions['versions'].append(version_name_add)
                with open(f"{conf.config_folder}\\versions.json", "w", encoding="ansi") as file:
                    json.dump(all_installed_versions, file, indent=4, ensure_ascii=False)

                logger.info("Step 4.2 - Version installed, starting game")
                if self.after_download_game == "nothing":
                    self.finished.emit(self.play_time)
                else:
                    self.start_game(obj_Version_Manager.version_to_folder_json(version_for_get_json))
            else:
                logger.info(f"Step 4.3 - Version found, starting game {self.version}")
                self.start_game(obj_Version_Manager.version_to_folder_json(version_for_get_json))
        except Exception as e:
            self.error.emit(e)

    def start_game(self, version_name):
        try:
            logger.info("Step 5 - Install all mods for playing")
            self.install_hlskins_skins()
            self.install_addMod()

            logger.info("Step 6 - Move files versions minecraft")
            self.copy_minecraft_files_before_start(self.version)
            
            logger.info("Step 7 - Starting game")
            self.progress.emit("Запуск...")

            logger.info('Create command to start game')
            command = mn.command.get_minecraft_command(
                version=version_name, 
                minecraft_directory=self.version_directory, 
                options=self.options
            )

            if self.after_start_game == "hide" or self.after_start_game == "close":
                logger.info(f"After start game action: {self.after_start_game}")
                self.hide_launcher_signal.emit()

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0
            
            process = subprocess.Popen(
                command,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            start_time = time.time()
            process.wait()
            end_time = time.time()
            execution_time_hours = (end_time - start_time) / 3600
            logger.info(f"Game process finished. Execution time: {execution_time_hours:.2f} hours")

            logger.info("Step 8 - Update play time in database")
            try:
                time_all = auth.update_play_time(self.username, execution_time_hours)
            except Exception as e:
                logger.error(f"Failed to update play time: {e}")
                logger.info("Write time for file")
                conf.state_time_players(self.username, execution_time_hours)
                time_all = self.play_time + execution_time_hours
            
            logger.info('Switch last minecraft version')
            versions_config = conf.get_installed_versions()
            versions_config['last_version'] = self.version
            with open(f"{conf.config_folder}\\versions.json", "w", encoding="ansi") as file:
                json.dump(versions_config, file, indent=4, ensure_ascii=False)
            
            logger.info("Step 9 - Game closed, show launcher")
            if self.after_start_game == "hide":
                self.show_launcher_signal.emit()
            elif self.after_start_game == "close":
                self.close.emit()
            self.finished.emit(time_all)
        except Exception as e:
            self.error.emit(e)

    def install_addMod(self):
        if self.version_clear == "1.16.5" and self.mode != "" or self.version_clear == "1.16.4" and self.mode != "":
            self.download_file(f'AddonMod1.16_{self.mode}.jar')

    def download_file(self, filename):
        full_mods_path = os.path.join(self.version_directory, "mods")
        try:
            os.makedirs(full_mods_path, exist_ok=True)
        except:
            pass

        save_path = os.path.join(full_mods_path, filename)

        try:
            logger.info(f"Downloading {filename}")
            return auth.download_mods_from_supabase(filename, save_path)
        except Exception as e:
            logger.error(e)
            
    def install_hlskins_skins(self):
        try:
            api_file = None
            if self.mode != "":
                file_mode_hl = f"skinsHL-{self.mode}-{self.version_clear}.jar"
                if self.mode == 'Fabric':
                    api_file = f"fabric-api-{self.version_clear}.jar"

                logger.info("Installing HLSkins mods")
                try1 = self.download_file(file_mode_hl)
                if try1 != 404 and api_file != None:
                    self.download_file(api_file)
        except Exception as e:
            logger.error(e)

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