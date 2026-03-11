from PyQt6 import QtCore, QtGui, QtWidgets
from ...utils.font_manager import FontManager
from ..page_functions.login import connect_change_nickname_select,password_check_login_start, change_login_page, login_page_auth
from ..page_functions.page_manager import create_shadow
from ...auth.auth_manager import AuthManager

class WindowLogin:
    def __init__(self, main_window, ClickableQLabel):
        self.font = FontManager()
        self.main = main_window
        self.auth = AuthManager()
        self.window_auth = 0
        self.hide_pass = True
        self.ClickableQLabel = ClickableQLabel
        self.conf = self.main.configuration

    def update_window_auth(self, new_parametr):
        self.window_auth = new_parametr

    def update_hide_pass(self, new_parametr):
        self.hide_pass = new_parametr

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

        # Page Auth
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
        self.button_change_page_log_reg.clicked.connect(lambda: change_login_page(self))

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
        self.select_nickname_combobox.setCurrentText(self.conf.get_nickname_session())

        self.select_nickname_combobox_view = QtWidgets.QListView(self.select_nickname_combobox)
        self.select_nickname_combobox_view.setIconSize(QtCore.QSize(22, 22))
        self.select_nickname_combobox_view.setObjectName('select_nickname_combobox_view')
        self.select_nickname_combobox_view.setFont(self.font.get_font(12, "1"))
        self.select_nickname_combobox_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.select_nickname_combobox_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.select_nickname_combobox.setView(self.select_nickname_combobox_view)
        self.select_nickname_combobox.currentIndexChanged.connect(lambda: connect_change_nickname_select(self, data_users))

        self.password_account_login = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.password_account_login.setGeometry(QtCore.QRect(400, 322, 300, 55))
        self.password_account_login.setFont(self.font.get_font(12, "1"))
        self.password_account_login.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))
        self.password_account_login.setPlaceholderText("Пароль")
        self.password_account_login.setObjectName('password_account_login')
        self.password_account_login.textChanged.connect(lambda: password_check_login_start(self))
        self.password_account_login.hide()

        self.use_in_minecraft_text = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.use_in_minecraft_text.setGeometry(QtCore.QRect(0, 315, 1100, 32))
        self.use_in_minecraft_text.setFont(self.font.get_font(10, "1"))
        self.use_in_minecraft_text.setText("Он будет использоваться в Minecraft")
        self.use_in_minecraft_text.setObjectName("use_in_minecraft_text")
        self.use_in_minecraft_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.login_in_launcher = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.login_in_launcher.setGeometry(QtCore.QRect(450, 360, 200, 35)) 
        self.login_in_launcher.setFont(self.font.get_font(10, "1"))
        self.login_in_launcher.setText("Войти в аккаунт")
        self.login_in_launcher.setObjectName("login_in_launcher")
        self.login_in_launcher.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.login_in_launcher.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        #self.login_in_launcher.clicked.connect(self.auth_in_launcher_login)
        connect_change_nickname_select(self, data_users)

        #Page add account
        self.error_auth_login_1 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.error_auth_login_1.setGeometry(QtCore.QRect(172, 231, 300, 15))
        self.error_auth_login_1.setFont(self.font.get_font(10, "1"))
        self.error_auth_login_1.setObjectName("error_auth_setup")
        self.error_auth_login_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.error_auth_login_1.hide()

        self.error_auth_login_2 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.error_auth_login_2.setGeometry(QtCore.QRect(628, 231, 300, 15))
        self.error_auth_login_2.setFont(self.font.get_font(10, "1"))
        self.error_auth_login_2.setObjectName("error_auth_setup")
        self.error_auth_login_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.error_auth_login_2.hide()

        self.text_registr_login2 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.text_registr_login2.setGeometry(QtCore.QRect(232, 198, 200, 32))
        self.text_registr_login2.setFont(self.font.get_font(20, "1"))
        self.text_registr_login2.setText("Регистрация")
        self.text_registr_login2.setObjectName('text_registr_login2')

        self.text_auth_login2 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.text_auth_login2.setGeometry(QtCore.QRect(685, 198, 200, 32))
        self.text_auth_login2.setFont(self.font.get_font(20, "1"))
        self.text_auth_login2.setText("Авторизация")
        self.text_auth_login2.setObjectName('text_registr_login2')

        self.write_nickname_for_registr = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.write_nickname_for_registr.setGeometry(QtCore.QRect(172, 252, 300, 55))
        self.write_nickname_for_registr.setFont(self.font.get_font(12, "1"))
        self.write_nickname_for_registr.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))
        self.write_nickname_for_registr.setPlaceholderText("Никнейм")
        self.write_nickname_for_registr.setObjectName('password_account_login')
        #self.write_nickname_for_registr.textChanged.connect(self.access_create_add_auth_acc_in_launch_register)
        
        self.write_nickname_for_auth = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.write_nickname_for_auth.setGeometry(QtCore.QRect(628, 252, 300, 55))
        self.write_nickname_for_auth.setFont(self.font.get_font(12, "1"))
        self.write_nickname_for_auth.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))
        self.write_nickname_for_auth.setPlaceholderText("Никнейм")
        self.write_nickname_for_auth.setObjectName('password_account_login')
        #self.write_nickname_for_auth.textChanged.connect(self.access_create_add_auth_acc_in_launch_auth)

        self.write_password_for_registr = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.write_password_for_registr.setGeometry(QtCore.QRect(172, 322, 300, 55))
        self.write_password_for_registr.setFont(self.font.get_font(12, "1"))
        self.write_password_for_registr.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))
        self.write_password_for_registr.setPlaceholderText("Пароль")
        self.write_password_for_registr.setObjectName('password_account_login')
        #self.write_password_for_registr.textChanged.connect(self.access_create_add_auth_acc_in_launch_register)
        
        self.write_password_for_auth = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.write_password_for_auth.setGeometry(QtCore.QRect(628, 322, 300, 55))
        self.write_password_for_auth.setFont(self.font.get_font(12, "1"))
        self.write_password_for_auth.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))
        self.write_password_for_auth.setPlaceholderText("Пароль")
        self.write_password_for_auth.setObjectName('password_account_login')
        #self.write_password_for_auth.textChanged.connect(self.access_create_add_auth_acc_in_launch_auth)

        self.write_password_retry_for_registr = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.write_password_retry_for_registr.setGeometry(QtCore.QRect(172, 392, 300, 55))
        self.write_password_retry_for_registr.setFont(self.font.get_font(12, "1"))
        self.write_password_retry_for_registr.setGraphicsEffect(create_shadow(self.conf.get_color_theme()))
        self.write_password_retry_for_registr.setPlaceholderText("Повторить пароль")
        self.write_password_retry_for_registr.setObjectName('password_account_login')
        #self.write_password_retry_for_registr.textChanged.connect(self.access_create_add_auth_acc_in_launch_register)

        self.button_register_login2 = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.button_register_login2.setGeometry(QtCore.QRect(172, 467, 300, 35)) 
        self.button_register_login2.setFont(self.font.get_font(10, "1"))
        self.button_register_login2.setText("Зарегистрироваться")
        self.button_register_login2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_register_login2.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.button_register_login2.setObjectName('login_in_launcher')
        self.button_register_login2.clicked.connect(lambda: login_page_auth(self, self.write_nickname_for_registr.text(), self.write_password_for_registr.text(), 'registr'))

        self.button_auth_login2 = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.button_auth_login2.setGeometry(QtCore.QRect(628, 397, 300, 35)) 
        self.button_auth_login2.setFont(self.font.get_font(10, "1"))
        self.button_auth_login2.setText("Авторизоваться")
        self.button_auth_login2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_auth_login2.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.button_auth_login2.setObjectName('login_in_launcher')
        self.button_auth_login2.clicked.connect(lambda: login_page_auth(self, self.write_nickname_for_auth.text(), self.write_password_for_auth.text(), 'auth'))

        self.rules_nickname_login2 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.rules_nickname_login2.setGeometry(QtCore.QRect(172, 507, 500, 60))
        self.rules_nickname_login2.setFont(self.font.get_font(12, "1"))
        self.rules_nickname_login2.setText("Никнейм может содержать:")
        self.rules_nickname_login2.setObjectName("rules_nickname_page2")

        self.rule_login2 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.rule_login2.setGeometry(QtCore.QRect(174, 524, 220, 100))
        self.rule_login2.setFont(self.font.get_font(10, "5"))
        self.rule_login2.setText("<font>1. Символы EN</font><br><font>2. Цифры</font><br><font>3. Спец-символы</font>")
        self.rule_login2.setObjectName("rule_login2")

        if self.window_auth == 0:
            self.text_auth_login2.hide()
            self.text_registr_login2.hide()
            self.write_nickname_for_registr.hide()
            self.write_nickname_for_auth.hide()
            self.write_password_for_registr.hide()
            self.write_password_for_auth.hide()
            self.write_password_retry_for_registr.hide()
            self.button_register_login2.hide()
            self.button_auth_login2.hide()
            self.rules_nickname_login2.hide()
            self.rule_login2.hide()