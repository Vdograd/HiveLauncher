import minecraft_launcher_lib as mn
from .helper import *
import json

class Build:
    def __init__(self, type_start: int):
        self.type_start = type_start
        self.path_project = helper.get_path_project(type_start)

        self.folder_launcher = self.path_project
        self.static_folder = os.path.join(self.path_project, 'launcher', 'data', 'static')
        self.config_folder = os.path.join(self.path_project, 'launcher', 'data')
        self.theme_folder = os.path.join(self.path_project, 'launcher', 'data', 'themes')
        self.logs_folder = os.path.join(self.path_project, 'launcher', 'data', 'logs')
        self.version_launcher = "4.0-beta"

    def get_color_theme(self) -> str:
        try:
            with open(os.path.join(self.config_folder, 'config.json'), "r", encoding="ansi") as file:
                color = json.load(file)["color"]
                if type(color) != str: raise ValueError('Invalid data type in config[color]')
            return color
        except Exception as e: raise e

    def get_last_nickname(self) -> str:
        try:
            with open(os.path.join(self.config_folder, 'nicknames.json'), "r", encoding="ansi") as file:
                nickname = json.load(file)["last_nickname"]
                if type(nickname) != str: raise ValueError('Invalid data type in nicknames[last_nickname]')
            return nickname
        except Exception as e:
            raise e
        
    def get_config(self) -> dict:
        try:
            with open(os.path.join(self.config_folder, 'config.json'), "r", encoding="ansi") as file:
                data = json.load(file)
            return data
        except Exception as e:
            raise e
    
    def get_installed_versions(self) -> list:
        try:
            with open(os.path.join(self.config_folder, 'versions.json'), "r", encoding="ansi") as file:
                versions = json.load(file)['versions']
                if type(versions) != list: raise ValueError('Invalid data type in versions[versions]')
            return versions
        except Exception as e:
            raise e
        
    def get_last_start_version(self) -> str:
        try:
            with open(os.path.join(self.config_folder, 'versions.json'), "r", encoding="ansi") as file:
                last_version = json.load(file)['last_version']
                if type(last_version) != str: raise ValueError('Invalid data type in versions[last_version]')
            return last_version
        except Exception as e:
            raise e
        
    def state_time_players(self, nickname: str, timeplus: float) -> None:
        file_time_fix = os.path.join(self.config_folder, 'time_fixed.json')

        try:
            if os.path.isfile(file_time_fix):
                with open(file_time_fix, "r", encoding="ansi") as file:
                    data = json.load(file)
                with open(file_time_fix, "w", encoding="ansi") as file:
                    try:
                        _ = data[nickname]
                        data[nickname][0] += timeplus
                        data[nickname][1] = helper.hash_time_add(data[nickname][0])
                    except:
                        data[nickname] = [timeplus, helper.hash_time_add(timeplus)]
                    json.dump(data, file,indent=4, ensure_ascii=False)

            else:
                with open(file_time_fix, "w", encoding="ansi") as file:
                    data = {
                        nickname: [timeplus, helper.hash_time_add(timeplus)]
                    }
                    json.dump(data, file,indent=4, ensure_ascii=False)
        except Exception as e:
            raise e

build = Build(1)

class RestartConfig:
    def __init__(self):
        self.config_folder = build.config_folder
        self.create_config_folder()
        self.config_file()
        self.versions_file()
        self.nicknames_file()

    def create_config_folder(self) -> None:
        try:
            os.makedirs(self.config_folder, exist_ok=True)
        except Exception as e:
            raise e
        
    def config_file(self) -> None:
        file_edit = os.path.join(self.config_folder, 'config.json')

        try:
            with open(file_edit, "r", encoding="ansi") as file:
                data = json.load(file)
                _ = [data["color"], data["folder_game"], data["maxm"], data["window_size"], data["after_download"], data["after_start"]]
                if not self.check_type_correct(data, [str, str, str, str, str, str]): raise
        except:
            try:
                data = {
                    "color": "light",
                    "folder_game": mn.utils.get_minecraft_directory().replace('minecraft', 'hivelauncher'),
                    "maxm": helper.default_rem(),
                    "window_size": helper.access_screens()[0],
                    "after_download": "nothing",
                    "after_start": "hide",
                }

                with open(file_edit, "w", encoding="ansi") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
            except Exception as e:
                raise e
            
    def versions_file(self) -> None:
        file_edit = os.path.join(self.config_folder, 'versions.json')

        try:
            with open(file_edit, "r", encoding="ansi") as file:
                data = json.load(file)
                _ = [data["versions"], data["last_version"]]
                if not self.check_type_correct(data, [list, None | str]): raise
        except:
            try:
                data = {
                    "versions": [],
                    "last_version": None,
                }

                with open(file_edit, "w", encoding="ansi") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
            except Exception as e:
                raise e
            
    def nicknames_file(self) -> None:
        file_edit = os.path.join(self.config_folder, 'nicknames.json')

        try:
            with open(file_edit, "r", encoding="ansi") as file:
                data = json.load(file)
                _ = [data["nicknames"], data["last_nickname"], data["verify_code"]]
                if not self.check_type_correct(data, [list, str | None, dict]): raise
        except:
            try:
                data = {
                    "nicknames": [],
                    "last_nickname": None,
                    "verify_code": {}
                }

                with open(file_edit, "w", encoding="ansi") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
            except Exception as e:
                raise e
            
    def check_type_correct(self, arr_json: dict, arr_success: list) -> bool:
        values = list(arr_json.values())

        if len(values) != len(arr_success):
            return False
        
        for value, exptype in zip(values, arr_success):
            if not isinstance(value, exptype):
                return False
        return True