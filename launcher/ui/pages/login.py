from PyQt6 import QtCore, QtGui, QtWidgets
from ...utils.font_manager import FontManager
from ..page_functions.setup import auth_setup
from ..page_functions.page_manager import create_shadow

class WindowLogin:
    def __init__(self, main_window, ClickableQLabel):
        self.font = FontManager()
        self.main = main_window
        self.window_auth = 0
        self.ClickableQLabel = ClickableQLabel

    def update_window_auth(self, new_parametr):
        self.window_auth = new_parametr

    def login_show(self):
        self.logo = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.logo.setGeometry(QtCore.QRect(76, 40, 68, 46))
        self.logo.setMinimumSize(QtCore.QSize(68, 46))
        self.logo.setPixmap(QtGui.QPixmap(f"{self.main.configuration.static_folder}\\global\\HLlogo.svg"))
        self.logo.setObjectName("logo")

        self.version_launcher = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.version_launcher.setGeometry(QtCore.QRect(80, 85, 64, 46))
        self.version_launcher.setFont(self.font.get_font(8, "1"))
        self.version_launcher.setText(self.main.configuration.version_launcher)
        self.version_launcher.setObjectName("version_launcher")
        self.version_launcher.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)