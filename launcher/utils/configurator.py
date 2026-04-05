import os
import json
import minecraft_launcher_lib as mn
from .helper import Helper
import shutil
import sys

class Configurator:
    def __init__(self):
        self.folder_launcher = f"{os.path.dirname(os.path.abspath("main.py"))}\\_internal"
        self.static_folder = f"{os.path.dirname(os.path.abspath("main.py"))}\\_internal\\launcher\\data\\static"
        self.config_folder = f"{os.path.dirname(os.path.abspath("main.py"))}\\_internal\\launcher\\data"
        self.theme_folder = f"{os.path.dirname(os.path.abspath("main.py"))}\\_internal\\launcher\\data\\themes"
        self.logs_folder = f"{os.path.dirname(os.path.abspath("main.py"))}\\_internal\\launcher\\data\\logs"
        self.version_launcher = "3.3.0"
        self.helper = Helper()
    
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return relative_path

    def get_color_theme(self):
        try:
            with open(f"{self.config_folder}\\config.json", "r", encoding="ansi") as file:
                color = json.load(file)["color"]
        except Exception as e:
            raise e
        return color
    
    def get_nickname_session(self):
        try:
            with open(f"{self.config_folder}\\nicknames.json", "r", encoding="ansi") as file:
                nickname = json.load(file)["last_nickname"]
        except Exception as e:
            raise e
        return nickname
    
    def get_config(self):
        try:
            with open(f"{self.config_folder}\\config.json", "r", encoding="ansi") as file:
                data = json.load(file)
        except Exception as e:
            raise e
        return data

    def get_installed_versions(self):
        try:
            with open(f"{self.config_folder}\\versions.json", "r", encoding="ansi") as file:
                versions = json.load(file)
        except Exception as e:
            raise e
        return versions
    
    def fixed_system_config(self):
        try:
            os.makedirs(self.config_folder, exist_ok=True)
        except Exception as e:
            raise e
        
        # Fixed config.json
        try:
            with open(f"{self.config_folder}\\config.json", "r", encoding="ansi") as file:
                data = json.load(file)
                check = [data["color"], data["folder_game"], data["maxm"], data["window_size"], data["after_download"], data["after_start"]]
        except Exception as e:
            try:
                data = {
                    "color": "light",
                    "folder_game": mn.utils.get_minecraft_directory().replace('minecraft', 'hivelauncher'),
                    "maxm": self.helper.default_rem(),
                    "window_size": self.helper.access_screens()[0],
                    "after_download": "nothing",
                    "after_start": "hide",
                }

                with open(f"{self.config_folder}\\config.json", "w", encoding="ansi") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
            except Exception as e:
                raise e
        
        # Fixed versions.json
        try:
            with open(f"{self.config_folder}\\versions.json", "r", encoding="ansi") as file:
                data = json.load(file)
                check = [data["versions"], data["last_version"]]
        except:
            try:
                data = {
                    "versions": [],
                    "last_version": None,
                }

                with open(f"{self.config_folder}\\versions.json", "w", encoding="ansi") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
            except Exception as e:
                raise e
            
        # Fixed nicknames.json
        try:
            with open(f"{self.config_folder}\\nicknames.json", "r", encoding="ansi") as file:
                data = json.load(file)
                check = [data["nicknames"], data["last_nickname"], data["verify_code"]]
        except:
            try:
                data = {
                    "nicknames": [],
                    "last_nickname": None,
                    "verify_code": {}
                }

                with open(f"{self.config_folder}\\nicknames.json", "w", encoding="ansi") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
            except Exception as e:
                raise e
            
    def state_time_players(self, nickname, timeplus):
        try:
            if os.path.isfile(f"{self.config_folder}\\time_fixed.json"):
                with open(f"{self.config_folder}\\time_fixed.json", "r", encoding="ansi") as file:
                    data = json.load(file)
                with open(f"{self.config_folder}\\time_fixed.json", "w", encoding="ansi") as file:
                    try:
                        a = data[nickname]
                        data[nickname][0] += timeplus
                        data[nickname][1] = self.helper.hash_time_add(data[nickname][0])
                    except:
                        data[nickname] = [timeplus, self.helper.hash_time_add(timeplus)]
                    json.dump(data, file,indent=4, ensure_ascii=False)

            else:
                with open(f"{self.config_folder}\\time_fixed.json", "w", encoding="ansi") as file:
                    data = {
                        nickname: [timeplus, self.helper.hash_time_add(timeplus)]
                    }
                    json.dump(data, file,indent=4, ensure_ascii=False)
        except Exception as e:
            raise e
        
    def copy_old_to_new_config(self):
        try:
            os.makedirs(self.config_folder, exist_ok=True)
        except Exception as e:
            raise e
        try:
            config = None
            nicknames = None
            versions = None
            alls = []

            if os.path.exists(os.path.join(self.folder_launcher,"configuration","config.json")):
                config = os.path.join(self.folder_launcher,"configuration","config.json")
                alls.append([config, "config.json"])

            if os.path.exists(os.path.join(self.folder_launcher,"configuration","nicknames.json")):
                nicknames = os.path.join(self.folder_launcher,"configuration","nicknames.json")
                alls.append([nicknames, "nicknames.json"])
                
            if os.path.exists(os.path.join(self.folder_launcher,"configuration","versions_installed.json")):
                versions = os.path.join(self.folder_launcher,"configuration","versions_installed.json")
                alls.append([versions, "versions.json"])

            for x in alls:
                target_path = os.path.join(self.config_folder, x[1])
                shutil.copy2(x[0], target_path)
                os.remove(x[0])
            if os.path.exists(os.path.join(self.folder_launcher,"configuration")):
                os.removedirs(os.path.join(self.folder_launcher,"configuration"))
        except Exception as e:
            raise e