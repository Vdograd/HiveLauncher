from PyQt6 import QtCore, QtGui, QtWidgets
from ..style import set_style
from ...utils.font_manager import FontManager
from ..page_functions.setup import auth_setup
from ..page_functions.page_manager import create_shadow

class WindowLogin:
    def __init__(self, main_window, ClickableQLabel):
        self.font = FontManager()
        self.main = main_window
        self.window_auth = 0
        self.ClickableQLabel = ClickableQLabel
        set_style(self.main, self.main.configuration.get_color_theme())

    def update_window_auth(self, new_parametr):
        self.window_auth = new_parametr

    def login_show(self):
        ...