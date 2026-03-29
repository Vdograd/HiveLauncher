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

    def change_page(self, page):
        if page != None:
            self.page = page
    
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
        self.home.clicked.connect(lambda: self.change_page(open_window(self, 'Home')))

        self.account = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.account.setGeometry(QtCore.QRect(561, 15, 55, 50))
        self.account.setObjectName("but_nav")
        self.account.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.account.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.account.setIconSize(QSize(55, 50))
        self.account.clicked.connect(lambda: self.change_page(open_window(self, 'Account')))

        self.settings = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.settings.setGeometry(QtCore.QRect(998, 15, 72, 50))
        self.settings.setObjectName("but_nav")
        self.settings.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.settings.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.settings.setIconSize(QSize(72, 50))
        self.settings.clicked.connect(lambda: self.change_page(open_window(self, 'Settings')))

        self.fon_image = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.fon_image.setGeometry(QtCore.QRect(0,80, 1100, 500))
        self.fon_image.setObjectName("nickname_text")
        self.fon_image.setPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\home\\fon.png"))

        self.select_version = self.main.select_version
        self.select_version.currentIndexChanged.connect(lambda: change_version(self))
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

        # Account Page

        self.panel_base_account = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.panel_base_account.setGeometry(QtCore.QRect(260, 160, 580, 380))
        self.panel_base_account.setObjectName('panel_base_account')
        self.panel_base_account.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))

        self.head_nickname_150 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.head_nickname_150.setGeometry(QtCore.QRect(290, 190, 150, 150))
        self.head_nickname_150.setStyleSheet("background: rgba(1, 1, 0, 0);")
        self.head_nickname_150.setObjectName('head_nickname_150')

        self.nickname_text_account = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.nickname_text_account.setGeometry(QtCore.QRect(470, 217, 340, 24))
        self.nickname_text_account.setObjectName("nickname_text_account")
        self.nickname_text_account.setFont(self.font.get_font(14,"1"))

        self.register_account = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.register_account.setGeometry(QtCore.QRect(470, 258, 340, 18))
        self.register_account.setObjectName("register_account")
        self.register_account.setFont(self.font.get_font(12,"1"))

        self.play_time = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.play_time.setGeometry(QtCore.QRect(470, 278, 340, 18))
        self.play_time.setObjectName("play_time")
        self.play_time.setFont(self.font.get_font(12,"1"))

        self.text_change_skin = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.text_change_skin.setGeometry(QtCore.QRect(290, 384, 180, 24))
        self.text_change_skin.setFont(self.font.get_font(14,"1"))
        self.text_change_skin.setText("Сменить скин")
        self.text_change_skin.setObjectName('text_change_skin')

        self.text_change_cape = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.text_change_cape.setGeometry(QtCore.QRect(470, 384, 200, 24))
        self.text_change_cape.setFont(self.font.get_font(14,"1"))
        self.text_change_cape.setText("Сменить плащ")
        self.text_change_cape.setObjectName('text_change_cape')

        self.button_load_skin = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.button_load_skin.setGeometry(QtCore.QRect(290, 416, 153, 33))
        self.button_load_skin.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_load_skin.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.button_load_skin.setText("Загрузить файл")
        self.button_load_skin.setObjectName('load_but_ac')
        self.button_load_skin.setFont(self.font.get_font(10, "1"))
        #self.button_load_skin.clicked.connect(lambda: self.load_skin(current_nickname()))

        self.button_load_cape = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.button_load_cape.setGeometry(QtCore.QRect(470, 416, 153, 33))
        self.button_load_cape.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_load_cape.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.button_load_cape.setText("Загрузить файл")
        self.button_load_cape.setObjectName('load_but_ac')
        self.button_load_cape.setFont(self.font.get_font(10, "1"))
        #self.button_load_cape.clicked.connect(lambda: self.load_cape(current_nickname()))

        self.current_size_skin = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.current_size_skin.setGeometry(QtCore.QRect(290, 454, 200, 20))
        self.current_size_skin.setFont(self.font.get_font(8,"1"))
        self.current_size_skin.setText("64x64 / 1024x1024 .png")
        self.current_size_skin.setObjectName('cur_size')

        self.current_size_cape = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.current_size_cape.setGeometry(QtCore.QRect(470, 454, 200, 20))
        self.current_size_cape.setFont(self.font.get_font(8,"1"))
        self.current_size_cape.setText("64x32 / 1024x512 .png/gif")
        self.current_size_cape.setObjectName('cur_size')

        self.button_delete_skin = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.button_delete_skin.setGeometry(QtCore.QRect(290, 478, 153, 33))
        self.button_delete_skin.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_delete_skin.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.button_delete_skin.setText("Удалить скин")
        self.button_delete_skin.setFont(self.font.get_font(10, "1"))
        self.button_delete_skin.setObjectName('delete_but_ac')
        #self.button_delete_skin.clicked.connect(lambda: self.clear_skin(current_nickname()))

        self.button_delete_cape = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.button_delete_cape.setGeometry(QtCore.QRect(470, 478, 153, 33))
        self.button_delete_cape.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_delete_cape.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.button_delete_cape.setText("Удалить плащ")
        self.button_delete_cape.setFont(self.font.get_font(10, "1"))
        self.button_delete_cape.setObjectName('delete_but_ac')
        #self.button_delete_cape.clicked.connect(lambda: self.clear_cape(current_nickname()))

        self.button_logout_account = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.button_logout_account.setGeometry(QtCore.QRect(907, 642, 153, 33))
        self.button_logout_account.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_logout_account.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.button_logout_account.setText("Выйти с аккаунта")
        self.button_logout_account.setFont(self.font.get_font(10, "1"))
        self.button_logout_account.setObjectName('delete_but_ac')
        #self.button_logout_account.clicked.connect(lambda: self.logout(current_nickname()))

        # Settings Page

        self.folder_game_text = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.folder_game_text.setGeometry(QtCore.QRect(112, 135, 200, 30))
        self.folder_game_text.setObjectName("folder_game_text")
        self.folder_game_text.setFont(self.font.get_font(14,"1"))
        self.folder_game_text.setText("Директория игры")
        self.folder_game_text.setObjectName('nickname_text')

        self.tab_show_folder_game = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.tab_show_folder_game.setFont(self.font.get_font(10, "1"))
        self.tab_show_folder_game.setGeometry(112, 170, 372, 50)
        self.tab_show_folder_game.setCursorPosition(0)
        self.tab_show_folder_game.setReadOnly(True)
        self.tab_show_folder_game.setObjectName("tab_show_folder_game")
        self.tab_show_folder_game.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.tab_show_folder_game.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))

        self.edit_folder_game = self.ClickableQLabel(parent=self.main.centralwidget)
        self.edit_folder_game.setGeometry(QtCore.QRect(398, 140, 96, 22))
        self.edit_folder_game.setText("Изменить")
        self.edit_folder_game.setFont(self.font.get_font(12, "1"))
        self.edit_folder_game.setObjectName("button_change_page_log_reg")
        self.edit_folder_game.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.edit_folder_game.clicked.connect(lambda: browse_folder(self))

        self.size_window_text = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.size_window_text.setGeometry(QtCore.QRect(112, 250, 320, 30))
        self.size_window_text.setObjectName("size_window_text")
        self.size_window_text.setFont(self.font.get_font(14,"1"))
        self.size_window_text.setText("Разрешение экрана")
        self.size_window_text.setObjectName('nickname_text')

        self.sel_window_size = QtWidgets.QComboBox(parent=self.main.centralwidget)
        self.sel_window_size.setGeometry(QtCore.QRect(112, 285, 372, 50))
        self.sel_window_size.setFont(self.font.get_font(10, "1"))
        self.sel_window_size.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.sel_window_size.setObjectName('select_version')
        self.sel_window_size.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))
        self.sel_window_size.currentIndexChanged.connect(lambda: changed_window_size(self))

        self.sel_window_size_view = QtWidgets.QListView(self.sel_window_size)
        self.sel_window_size_view.setObjectName('select_version_view')
        self.sel_window_size_view.setFont(self.font.get_font(10, "1"))
        self.sel_window_size_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.sel_window_size_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.sel_window_size.setView(self.sel_window_size_view)
        #self.sel_window_size.currentIndexChanged.connect(self.change_version)

        self.after_start_text = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.after_start_text.setGeometry(QtCore.QRect(112, 365, 320, 30))
        self.after_start_text.setObjectName("after_start_text")
        self.after_start_text.setFont(self.font.get_font(14,"1"))
        self.after_start_text.setText("После запуска игры")
        self.after_start_text.setObjectName('nickname_text')

        self.sel_after_start = QtWidgets.QComboBox(parent=self.main.centralwidget)
        self.sel_after_start.setGeometry(QtCore.QRect(112, 400, 372, 50))
        self.sel_after_start.setFont(self.font.get_font(10, "1"))
        self.sel_after_start.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.sel_after_start.setObjectName('select_version')
        self.sel_after_start.currentIndexChanged.connect(lambda: changed_after_start(self))
        self.sel_after_start.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))

        self.sel_after_start_view = QtWidgets.QListView(self.sel_window_size)
        self.sel_after_start_view.setObjectName('select_version_view')
        self.sel_after_start_view.setFont(self.font.get_font(10, "1"))
        self.sel_after_start_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.sel_after_start_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.sel_after_start.setView(self.sel_after_start_view)

        self.rem_text = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.rem_text.setGeometry(QtCore.QRect(616, 135, 320, 30))
        self.rem_text.setObjectName("rem_text")
        self.rem_text.setFont(self.font.get_font(14,"1"))
        self.rem_text.setText("Выделенная память")
        self.rem_text.setObjectName('nickname_text')

        self.sel_rem = QtWidgets.QComboBox(parent=self.main.centralwidget)
        self.sel_rem.setGeometry(QtCore.QRect(616, 170, 372, 50))
        self.sel_rem.setFont(self.font.get_font(10, "1"))
        self.sel_rem.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)   
        self.sel_rem.setObjectName('select_version')
        self.sel_rem.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))
        self.sel_rem.currentIndexChanged.connect(lambda: changed_rem(self))

        self.sel_rem_view = QtWidgets.QListView(self.sel_window_size)
        self.sel_rem_view.setObjectName('select_version_view')
        self.sel_rem_view.setFont(self.font.get_font(10, "1"))
        self.sel_rem_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.sel_rem_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.sel_rem.setView(self.sel_rem_view)

        self.after_download_text = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.after_download_text.setGeometry(QtCore.QRect(616, 250, 320, 30))
        self.after_download_text.setObjectName("after_download_text")
        self.after_download_text.setFont(self.font.get_font(14,"1"))
        self.after_download_text.setText("После установки")
        self.after_download_text.setObjectName('nickname_text')

        self.sel_after_download = QtWidgets.QComboBox(parent=self.main.centralwidget)
        self.sel_after_download.setGeometry(QtCore.QRect(616, 285, 372, 50))
        self.sel_after_download.setFont(self.font.get_font(10, "1"))
        self.sel_after_download.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.sel_after_download.setObjectName('select_version')
        self.sel_after_download.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))
        self.sel_after_download.currentIndexChanged.connect(lambda: changed_after_download(self))

        self.sel_after_download_view = QtWidgets.QListView(self.sel_after_download)
        self.sel_after_download_view.setFont(self.font.get_font(10, "1"))
        self.sel_after_download_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.sel_after_download_view.setObjectName('select_version_view')

        self.sel_after_download_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.sel_after_download.setView(self.sel_after_download_view)


        self.color_theme_text = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.color_theme_text.setGeometry(QtCore.QRect(616, 365, 320, 30))
        self.color_theme_text.setObjectName("color_theme_text")
        self.color_theme_text.setFont(self.font.get_font(14,"1"))
        self.color_theme_text.setText("Тема оформления")
        self.color_theme_text.setObjectName('nickname_text')

        self.sel_color_theme = QtWidgets.QComboBox(parent=self.main.centralwidget)
        self.sel_color_theme.setGeometry(QtCore.QRect(616, 400, 372, 50))
        self.sel_color_theme.setFont(self.font.get_font(10, "1"))
        self.sel_color_theme.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.sel_color_theme.setObjectName('select_version')
        self.sel_color_theme.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))
        self.sel_color_theme.currentIndexChanged.connect(lambda: changed_color_theme(self))

        self.sel_color_theme_view = QtWidgets.QListView(self.sel_color_theme)
        self.sel_color_theme_view.setObjectName('select_version_view')
        self.sel_color_theme_view.setFont(self.font.get_font(10, "1"))
        self.sel_color_theme_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.sel_color_theme_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.sel_color_theme.setView(self.sel_color_theme_view)

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

        self.panel_base_account.hide()
        self.head_nickname_150.hide()
        self.nickname_text_account.hide()
        self.register_account.hide()
        self.play_time.hide()
        self.text_change_skin.hide()
        self.text_change_cape.hide()
        self.button_load_skin.hide()
        self.button_load_cape.hide()
        self.current_size_skin.hide()
        self.current_size_cape.hide()
        self.button_delete_skin.hide()
        self.button_delete_cape.hide()
        self.button_logout_account.hide()

        self.folder_game_text.hide()
        self.tab_show_folder_game.hide()
        self.edit_folder_game.hide()
        self.size_window_text.hide()
        self.sel_window_size.hide()
        self.after_start_text.hide()
        self.sel_after_start.hide()
        self.rem_text.hide()
        self.sel_rem.hide()
        self.after_download_text.hide()
        self.sel_after_download.hide()
        self.color_theme_text.hide()
        self.sel_color_theme.hide()

        auth_fill_data_settings(self)
        changed_color_theme(self)

        # Show home page
        self.change_page(open_window(self, 'Home'))