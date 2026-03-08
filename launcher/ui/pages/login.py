from PyQt6 import QtCore, QtGui, QtWidgets
from ...utils.font_manager import FontManager
from ..page_functions.setup import auth_setup
from ..page_functions.page_manager import create_shadow
from ...auth.auth_manager import AuthManager

class WindowLogin:
    def __init__(self, main_window, ClickableQLabel):
        self.font = FontManager()
        self.main = main_window
        self.auth = AuthManager()
        self.window_auth = 0
        self.ClickableQLabel = ClickableQLabel
        self.conf = self.main.configuration

    def update_window_auth(self, new_parametr):
        self.window_auth = new_parametr

    def login_show(self):
        self.logo = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.logo.setGeometry(QtCore.QRect(76, 40, 68, 46))
        self.logo.setMinimumSize(QtCore.QSize(68, 46))
        self.logo.setPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\global\\HLlogo.svg"))
        self.logo.setObjectName("logo")

        self.version_launcher = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.version_launcher.setGeometry(QtCore.QRect(80, 85, 64, 46))
        self.version_launcher.setFont(self.font.get_font(8, "1"))
        self.version_launcher.setText(self.conf.version_launcher)
        self.version_launcher.setObjectName("version_launcher")
        self.version_launcher.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.creeper_left = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.creeper_left.setGeometry(QtCore.QRect(0, 314, 257, 386))
        self.creeper_left.setPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\login\\{self.conf.get_color_theme()}\\creeper_left.png"))
        self.creeper_left.setObjectName("creeper")

        self.creeper_right = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.creeper_right.setGeometry(QtCore.QRect(843, 314, 257, 386))
        self.creeper_right.setPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\login\\{self.conf.get_color_theme()}\\creeper_right.png"))
        self.creeper_right.setObjectName("creeper")

        self.select_nickname_text = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.select_nickname_text.setGeometry(QtCore.QRect(0, 186, 1100, 32))
        self.select_nickname_text.setFont(self.font.get_font(20, "1"))
        self.select_nickname_text.setText("Выберите аккаунт")
        self.select_nickname_text.setObjectName("select_nickname_text")
        self.select_nickname_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.button_change_page_log_reg = self.ClickableQLabel(parent=self.main.centralwidget)
        self.button_change_page_log_reg.setGeometry(QtCore.QRect(465, 223, 180, 19))
        self.button_change_page_log_reg.setText("или добавьте новый")
        self.button_change_page_log_reg.setFont(self.font.get_font(12, "1"))
        self.button_change_page_log_reg.setObjectName("button_change_page_log_reg")
        self.button_change_page_log_reg.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        #self.button_change_page_log_reg.clicked.connect(self.change_page_in_login_on_select_account)

        self.select_nickname_combobox = QtWidgets.QComboBox(parent=self.main.centralwidget)
        self.select_nickname_combobox.setGeometry(QtCore.QRect(400, 259, 300, 55))
        self.select_nickname_combobox.setFont(self.font.get_font(12, "1"))
        self.select_nickname_combobox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.select_nickname_combobox.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)
        self.select_nickname_combobox.setObjectName("select_nickname_combobox")
        self.select_nickname_combobox.setIconSize(QtCore.QSize(22, 22))
        self.select_nickname_combobox.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))
        data_users = self.auth.list_nicknames()

        for user in data_users:
            if user[1] == "success":
                self.select_nickname_combobox.addItem(user[0])
            else:
                icon = QtGui.QIcon()
                color = self.conf.get_color_theme()
                icon.addPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\login\\{color}\\warn_verify.svg"), QtGui.QIcon.Mode.Normal,QtGui.QIcon.State.On)
                icon.addPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\login\\{color}\\warn_verify.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.Off)
                icon.addPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\login\\{color}\\warn_verify.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.On)
                icon.addPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\login\\{color}\\warn_verify.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.Off)
                icon.addPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\login\\{color}\\warn_verify.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.On)
                icon.addPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\login\\{color}\\warn_verify.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.Off)
                icon.addPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\login\\{color}\\warn_verify.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.On)
                self.select_nickname_combobox.addItem(icon, user[0])

