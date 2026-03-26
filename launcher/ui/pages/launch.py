from PyQt6 import QtCore, QtGui, QtWidgets
from ...utils.font_manager import FontManager
from ..page_functions.launch import *
from ..page_functions.page_manager import create_shadow
from ...auth.auth_manager import AuthManager
from PyQt6.QtCore import Qt, QSize

class WindowLauncher:
    def __init__(self, main_window, ClickableQLabel, picture):
        self.font = FontManager()
        self.main = main_window
        self.auth = AuthManager()
        self.ClickableQLabel = ClickableQLabel
        self.conf = self.main.configuration
        self.picture = picture
        self.page = None
    
    def launcher_show(self):
        # Home Page
        self.head_nickname = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.head_nickname.setGeometry(QtCore.QRect(30, 15, 50, 50))
        self.head_nickname.setStyleSheet("background: rgba(1, 1, 0, 0);")
        self.head_nickname.setObjectName("head_nickname")

        self.nickname_text = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.nickname_text.setGeometry(QtCore.QRect(95, 32, 355, 19))
        self.nickname_text.setObjectName("nickname_text")
        self.nickname_text.setFont(self.font.get_font(12,"1"))

        self.home = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.home.setGeometry(QtCore.QRect(485, 15, 61, 50))
        self.home.setObjectName("but_nav")
        self.home.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.home.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.home.setIconSize(QSize(61, 50))
        #self.home.clicked.connect(lambda: self.open_window(1))

        self.account = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.account.setGeometry(QtCore.QRect(561, 15, 55, 50))
        self.account.setObjectName("but_nav")
        self.account.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.account.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.account.setIconSize(QSize(55, 50))
        #self.account.clicked.connect(lambda: self.open_window(2))

        self.settings = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.settings.setGeometry(QtCore.QRect(998, 15, 72, 50))
        self.settings.setObjectName("but_nav")
        self.settings.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.settings.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.settings.setIconSize(QSize(72, 50))
        #self.settings.clicked.connect(lambda: self.open_window(3))

        self.fon_image = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.fon_image.setGeometry(QtCore.QRect(0,80, 1100, 500))
        self.fon_image.setObjectName("nickname_text")
        self.fon_image.setPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\home\\fon.png"))

        self.select_version = self.main.select_version
        self.select_version_view = self.main.select_version_view
        
        self.button_start = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(425, 552, 250, 55))
        self.button_start.setObjectName("button_start")
        self.button_start.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_start.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.button_start.setFont(self.font.get_font(14, "1"))
        #self.button_start.clicked.connect(self.redit_game)
        self.button_start.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))

        self.button_open_folder_version = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.button_open_folder_version.setGeometry(QtCore.QRect(718, 623, 55, 55))
        self.button_open_folder_version.setObjectName("button_open_folder_version")
        self.button_open_folder_version.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_open_folder_version.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.button_open_folder_version.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))
        self.button_open_folder_version.setIconSize(QSize(55, 55))
        self.button_open_folder_version.clicked.connect(lambda: open_folder_game(self))

        # Скрываем все элементы, перед показом главной страницы
        self.head_nickname.hide()
        self.nickname_text.hide()
        self.home.hide()
        self.account.hide()
        self.settings.hide()
        self.fon_image.hide()
        self.button_start.hide()
        self.button_open_folder_version.hide()
        self.select_version.hide()

        # Show home page
        open_window(self, 'Home')