from ..utils.configurator import Configurator
from ..utils.helper import Helper
import minecraft_launcher_lib as mn
import os
from pathlib import Path
import json
import re

class VersionManager:
    def __init__(self):
        self.configurator = Configurator()
        self.helper = Helper()
        self.change_minecraft_directory_isbool = False
        self.minecraft_directory = None

    def init_minecraft_directory(self):
        try:
            with open(f"{self.configurator.config_folder}\\config.json", "r", encoding="ansi") as file:
                data = json.load(file)
                self.minecraft_directory = data["folder_game"]
            if not os.path.exists(self.minecraft_directory):
                try:
                    os.makedirs(self.minecraft_directory)
                except:
                    self.minecraft_directory = mn.utils.get_minecraft_directory().replace('minecraft', 'hivelauncher')
                    self.change_minecraft_directory_isbool = True
                    if not os.path.exists(self.minecraft_directory):
                        try:
                            os.makedirs(self.minecraft_directory)
                        except Exception as e:
                            return e
            if self.change_minecraft_directory_isbool:
                with open(f"{self.configurator.config_folder}\\config.json", "w", encoding="ansi") as file_wtire:
                    data["folder_game"] = self.minecraft_directory
                    json.dump(data, file_wtire, indent=4, ensure_ascii=False)
        except Exception as e:
            return e
        
    def change_minecraft_directory(self, path_directory):
        try:
            with open(f"{self.configurator.config_folder}\\config.json", "r", encoding="ansi") as file:
                data = json.load(file)
            with open(f"{self.configurator.config_folder}\\config.json", "w", encoding="ansi") as file_wtire:
                data["folder_game"] = path_directory
                json.dump(data, file_wtire, indent=4, ensure_ascii=False)
            self.minecraft_directory = path_directory
        except Exception as e:
            return e

    def get_versions_folder_path(self, version):
        path_minecraft_version = f"{self.minecraft_directory}\\{version.replace(" ", "_")}"
        path_minecraft_versions = f"{path_minecraft_version}\\versions"
        try:
            if not os.path.exists(path_minecraft_versions):
                os.makedirs(path_minecraft_versions)
        except Exception as e:
            return e
        return path_minecraft_versions
    
    def get_version_path(self, version):
        path_minecraft_version = f"{self.minecraft_directory}\\{version.replace('Minecraft ', '').replace(" ", "_")}"
        try:
            if not os.path.exists(path_minecraft_version):
                os.makedirs(path_minecraft_version)
        except Exception as e:
            return e
        return path_minecraft_version
    
    def version_to_folder_json(self, version: str):
        minecraft_directory_vers = self.get_version_path(version.replace("Minecraft ", ""))
        versions = self.helper.find_versions_folders(minecraft_directory_vers)
        c = ""
        original_version = version
        clean_version = re.sub(r'[^0-9.]', '', version)
        for x in versions:
            if "forge" in original_version.lower() and "fabric" not in original_version.lower() or "-" in original_version and "fabric" not in original_version.lower():
                if "forge" in x.lower() or "-" in x:
                    if original_version in x or clean_version in x:
                        if self.helper.find_pattern(x, clean_version):
                            folder = Path(f"{minecraft_directory_vers}\\{x}")
                            for file in os.listdir(folder):
                                if file.endswith(".json"):
                                    c += x
                                    return c
                
            elif "Fabric" in original_version:
                if "-" in x and "fabric" in x.lower() or "fabric" in x.lower():
                    if original_version in x or clean_version in x:
                        folder = Path(f"{minecraft_directory_vers}\\{x}")
                        for file in os.listdir(folder):
                            if file.endswith(".json"):
                                c += x
                                return c
            else:
                if (original_version in x or clean_version in x) and ("forge" not in x.lower() or "-" not in x) and ("fabric" not in x.lower() or "-" not in x):
                    if original_version == x:
                        folder = Path(f"{minecraft_directory_vers}\\{x}")
                        for file in os.listdir(folder):
                            if file.endswith(".json"):
                                c += x
                                return c
                            
obj_Version_Manager = VersionManager()