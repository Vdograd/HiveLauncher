from PyQt6.QtGui import QFontDatabase, QFont
from .build import build
import os

class FontManager:
    def __init__(self):
        self.fonts_loaded = False
        self.font_families = {}
        self.font_weights = {}

    def load_fonts(self) -> None:
        if self.fonts_loaded:
            return
        
        current_dir_font = os.path.join(build.static_folder, 'fonts')
        font_files = {
            'golostext-black': (os.path.join(current_dir_font, 'Golos-Text', 'GolosText-Black.ttf'), QFont.Weight.Black),
            'golostext-bold': (os.path.join(current_dir_font, 'Golos-Text', 'GolosText-Bold.ttf'), QFont.Weight.Bold),
            'golostext-regular': (os.path.join(current_dir_font, 'Golos-Text', 'GolosText-Regular.ttf'), QFont.Weight.Normal),
            'golostext-extrabold': (os.path.join(current_dir_font, 'Golos-Text', 'GolosText-Extrabold.ttf'), QFont.Weight.ExtraBold),
            'golostext-medium': (os.path.join(current_dir_font, 'Golos-Text', 'GolosText-Medium.ttf'), QFont.Weight.Medium),
            'golostext-semibold': (os.path.join(current_dir_font, 'Golos-Text', 'GolosText-Semibold.ttf'), QFont.Weight.DemiBold),

            'onest-black': (os.path.join(current_dir_font, 'Onest', 'Onest-Black.ttf'), QFont.Weight.Black),
            'onest-bold': (os.path.join(current_dir_font, 'Onest', 'Onest-Bold.ttf'), QFont.Weight.Bold),
            'onest-regular': (os.path.join(current_dir_font, 'Onest', 'Onest-Regular.ttf'), QFont.Weight.Normal),
            'onest-extrabold': (os.path.join(current_dir_font, 'Onest', 'Onest-Extrabold.ttf'), QFont.Weight.ExtraBold),
            'onest-medium': (os.path.join(current_dir_font, 'Onest', 'Onest-Medium.ttf'), QFont.Weight.Medium),
            'onest-semibold': (os.path.join(current_dir_font, 'Onest', 'Onest-Semibold.ttf'), QFont.Weight.DemiBold),
        }

        for name, (path, weight) in font_files.items():
            if os.path.exists(path):
                font_id = QFontDatabase.addApplicationFont(path)
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    self.font_families[name] = families[0]
                    self.font_weights[name] = weight

        self.fonts_loaded = True

    def font(self, number: int, size: int) -> QFont:
        """
            1: golostext-black,
            2: golostext-bold,
            3: golostext-regular,
            4: golostext-extrabold,
            5: golostext-medium,
            6: golostext-semibold,

            7: onest-black,
            8: onest-bold,
            9: onest-regular,
            10: onest-extrabold,
            11: onest-medium,
            12: onest-semibold,
        """
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
        font_weight = self.font_weights.get(font_name, QFont.Weight.Normal)

        font = QFont()
        if font_family:
            font.setFamily(font_family)
        font.setPixelSize(size)
        font.setWeight(font_weight)
        font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.NoFontMerging)

        return font
    
font = FontManager()