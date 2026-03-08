from PyQt6.QtGui import QFontDatabase, QFont
import os
from .configurator import Configurator

class FontManager:
    def __init__(self):
        self.fonts_loaded = False
        self.font_families = {}
        self.configurator = Configurator()
        
    def load_fonts(self):
        if self.fonts_loaded:
            return
            
        current_dir_font = self.configurator.static_folder
        font_files = {
            "montserrat_bold": f"{current_dir_font}\\fonts\\Montserrat-Bold.ttf",
            "montserrat_extrabold": f"{current_dir_font}\\fonts\\Montserrat-ExtraBold.ttf",
            "montserrat_medium": f"{current_dir_font}\\fonts\\Montserrat-Medium.ttf",
            "montserrat_regular": f"{current_dir_font}\\fonts\\Montserrat-Regular.ttf",
            "montserrat_semibold": f"{current_dir_font}\\fonts\\Montserrat-SemiBold.ttf"
        }
        
        for name, path in font_files.items():
            if os.path.exists(path):
                font_id = QFontDatabase.addApplicationFont(path)
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    self.font_families[name] = families[0]
        
        self.fonts_loaded = True
    
    def get_font(self, size, font_type):
        if not self.fonts_loaded:
            self.load_fonts()
        type_mapping = {
            "1": "montserrat_bold",
            "2": "montserrat_extrabold",
            "3": "montserrat_medium",
            "4": "montserrat_regular",
            "5": "montserrat_semibold"
        }
        font_name = type_mapping.get(str(font_type), "montserrat_regular")
        font_family = self.font_families.get(font_name, "")
        
        font = QFont()
        if font_family:
            font.setFamily(font_family)
        font.setPointSize(size)
        if font_type == "1":
            font.setWeight(QFont.Weight.Bold)
        elif font_type == "2":
            font.setWeight(QFont.Weight.ExtraBold)
        elif font_type == "3":
            font.setWeight(QFont.Weight.Medium)
        elif font_type == "4":
            font.setWeight(QFont.Weight.Normal)
        elif font_type == "5":
            font.setWeight(QFont.Weight.DemiBold)
        
        return font