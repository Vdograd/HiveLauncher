import json
from ...utils.configurator import Configurator
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

configurator = Configurator()

def how_start_page():
    try:
        with open(f"{configurator.config_folder}\\nicknames.json", "r", encoding="ansi") as file:
            data = json.load(file)
            return 'setup' if data["nicknames"] == [] else 'login'
    except Exception as e:
        return e

def create_shadow(type_shadow):
    if type_shadow == 'light':
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 50))
    elif type_shadow == 'dark':
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(91, 91, 91, 50))
    return shadow