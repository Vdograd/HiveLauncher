import os
import json

class Build:
    def __init__(self):
        self.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "static")
        self.folders_versions_launcher = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
        self.logs_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "logs")
        self.theme_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "themes")
        self.update_version = '3.0'

    def get_color_theme(self) -> str:
        try:
            with open(f"{self.theme_folder}\\color.txt", "r", encoding="ansi") as file:
                color = file.read()
            
            return color if color == 'light' or color == 'dark' else 'light'
        except Exception as e:
            raise e

build = Build()