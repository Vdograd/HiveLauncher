from PyQt6.QtGui import QFontDatabase, QFont
import os
from .build import build

class FontManager:
    def __init__(self):
        self.fonts_loaded = False
        self.font_families = {}

    def load_fonts(self) -> None:
        if self.fonts_loaded:
            return
        
        current_dir_font = f"{build.static_folder}\\fonts"
        font_files = {
            'golostext-black': f"{current_dir_font}\\Golos-Text\\GolosText-Black.ttf",
            'golostext-bold': f"{current_dir_font}\\Golos-Text\\GolosText-Bold.ttf",
            'golostext-regular': f"{current_dir_font}\\Golos-Text\\GolosText-Regular.ttf",
            'golostext-extrabold': f"{current_dir_font}\\Golos-Text\\GolosText-Extrabold.ttf",
            'golostext-medium': f"{current_dir_font}\\Golos-Text\\GolosText-Medium.ttf",
            'golostext-semibold': f"{current_dir_font}\\Golos-Text\\GolosText-Semibold.ttf",

            'onest-black': f"{current_dir_font}\\Onest\\Onest-Black.ttf",
            'onest-bold': f"{current_dir_font}\\Onest\\Onest-Bold.ttf",
            'onest-regular': f"{current_dir_font}\\Onest\\Onest-Regular.ttf",
            'onest-extrabold': f"{current_dir_font}\\Onest\\Onest-Extrabold.ttf",
            'onest-medium': f"{current_dir_font}\\Onest\\Onest-Medium.ttf",
            'onest-semibold': f"{current_dir_font}\\Onest\\Onest-Semibold.ttf",
        }

        for name, path in font_files.items():
            if os.path.exists(path):
                font_id = QFontDatabase.addApplicationFont(path)
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    self.font_families[name] = families[0]

        self.fonts_loaded = True

    def font(self, number: int, size: int) -> QFont:
        if not self.fonts_loaded:
            self.load_fonts()

        type_mapping = {
            "1": "golostext-black",
            "2": "golostext-bold",
            "3": "golostext-regular",
            "4": "golostext-extrabold",
            "5": "golostext-medium",
            "6": "golostext-semibold",

            "7": "onest-black",
            "8": "onest-bold",
            "9": "onest-regular",
            "10": "onest-extrabold",
            "11": "onest-medium",
            "12": "onest-semibold",
        }
        font_name = type_mapping.get(str(number))
        font_family = self.font_families.get(font_name, "")

        font = QFont()
        if font_family:
            font.setFamily(font_family)
        font.setPointSize(size)

        return font
    
font = FontManager()