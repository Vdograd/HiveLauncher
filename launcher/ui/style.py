from ..utils.build import build
import os

def set_style(self, name: str) -> None:
    try:
        with open(os.path.join(build.theme_folder, f"{name}.css"), "r", encoding="ansi") as file:
            style = file.read()
            self.setStyleSheet(style)
    except Exception as e:
        raise e