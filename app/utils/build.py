import os
import json

class Build:
    def __init__(self):
        self.static_folder = f"{os.path.dirname(os.path.abspath(__file__))}\\app\\data\\static"
        self.folders_versions_launcher = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
        self.logs_folder = f"{os.path.dirname(os.path.abspath(__file__))}\\app\\data\\logs"
        self.theme_folder = f"{os.path.dirname(os.path.abspath(__file__))}\\app\\data\\themes"
        self.update_version = '2.0'

build = Build()