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
        self.lang = None

        self.lang_cache = [] # index 0: en, index 1: ru
        self.load_lang_cache()

    def load_lang_cache(self) -> None:
        all_langs = [
            os.path.join(self.static_folder, 'lang', 'en.json'),
            os.path.join(self.static_folder, 'lang', 'ru.json'),
        ]
        for lang_file in all_langs:
            with open(lang_file, 'r', encoding="utf-8") as file:
                self.lang_cache.append(json.load(file))

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
        
    def get_lang(self) -> str:
        try:
            with open(os.path.join(self.config_folder, 'config.json'), "r", encoding="ansi") as file:
                lang = json.load(file)["lang"]
                if type(lang) != str: raise ValueError('Invalid data type in config[lang]')
            return lang
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
        
    def get_lang_text(self, key: str) -> str | None:
        if len(key) == 0: raise ValueError('Invalid value')
        lang = self.lang
        if lang == None:
            lang = self.get_lang()
            self.lang = lang

        if lang == 'ru':
            index = 1
        elif lang == 'en':
            index = 0
        else: raise ValueError('Invalid value config[lang]')

        path_json = self.lang_cache[index]
        path_json_list = key.split('-')

        try:
            for j in path_json_list:
                path_json = path_json[j]
            if type(path_json) != str: raise
            return path_json
        except:
            return None

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
                _ = [data["color"], data["lang"], data["folder_game"], data["maxm"], data["window_size"], data["after_download"], data["after_start"]]
                if not self.check_type_correct(data, [str, str, str, str, str, str, str]): raise
        except:
            try:
                data = {
                    "color": "light",
                    "lang": helper.get_lang_system(),
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