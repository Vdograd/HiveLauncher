from PyQt6 import QtCore, QtGui, QtWidgets
from ...utils.font_manager import FontManager
from ..page_functions.setup import scroll_page_setup, replace_auth_register_setup, access_step_continue_auth, auth_setup
from ..page_functions.page_manager import create_shadow

class WindowSetup:
    def __init__(self, main_window, ClickableQLabel):
        self.font = FontManager()
        self.main = main_window
        self.page_setup = 0 # 0 - Приветствие, 1 - Регистрация, 2 - Выбор темы, 3 - Лаунчер
        self.window_auth = 0 # 0 - Регистрация, 1 - Авторизация
        self.ClickableQLabel = ClickableQLabel
        self.conf = self.main.configuration

    def update_window_auth(self, new_parametr):
        self.window_auth = new_parametr
    def update_page(self, new_parametr):
        self.page_setup = new_parametr

    def setup_show(self):
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

        # Page 1
        self.text_hello = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.text_hello.setGeometry(QtCore.QRect(80, 154, 300, 64))
        self.text_hello.setFont(self.font.get_font(20, "1"))
        self.text_hello.setText("<font color='#005FFF'>HiveLauncher</font><br><font color='#000000'>Приветствует вас!</font>")
        self.text_hello.setObjectName("text_hello")

        self.text_description = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.text_description.setGeometry(QtCore.QRect(80, 237, 700, 83))
        self.text_description.setFont(self.font.get_font(12, "5"))
        self.text_description.setText("HiveLauncher — это оптимизированный лаунчер для Minecraft, созданный для запуска игры даже на маломощных компьютерах. Он сочетает в себе высокую производительность, интуитивно понятный современный интерфейс и бесплатную доступность")
        self.text_description.setObjectName("text_description")
        self.text_description.setWordWrap(True)

        self.person1 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.person1.setGeometry(QtCore.QRect(859, 350, 241, 350))
        self.person1.setPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\page1\\person_1.png"))
        self.person1.setObjectName("person1")

        self.down_text_1 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.down_text_1.setGeometry(QtCore.QRect(80, 618, 470, 20))
        self.down_text_1.setFont(self.font.get_font(14, "1"))
        self.down_text_1.setText("Для продолжения нажмите кнопку «Далее»")
        self.down_text_1.setObjectName("down_text_1")

        self.down_text_2 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.down_text_2.setGeometry(QtCore.QRect(80, 640, 470, 20))
        self.down_text_2.setFont(self.font.get_font(10, "5"))
        self.down_text_2.setText("Расположена в правом верхнем углу окна")
        self.down_text_2.setObjectName("down_text_2")

        self.button_continue_setup = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.button_continue_setup.setGeometry(QtCore.QRect(931, 51, 109, 35))
        self.button_continue_setup.setFont(self.font.get_font(9, "1"))
        self.button_continue_setup.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_continue_setup.setObjectName("button_continue_setup")
        self.button_continue_setup.setText("Далее")
        self.button_continue_setup.clicked.connect(lambda: self.update_page(scroll_page_setup(self, self.page_setup)))
        self.button_continue_setup.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        # Page 2
        self.error_auth_setup = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.error_auth_setup.setGeometry(QtCore.QRect(80, 403, 300, 15))
        self.error_auth_setup.setFont(self.font.get_font(10, "1"))
        self.error_auth_setup.setObjectName("error_auth_setup")
        self.error_auth_setup.hide()
        
        self.text_register_login = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.text_register_login.setGeometry(QtCore.QRect(80, 154, 320, 32))
        self.text_register_login.setFont(self.font.get_font(20, "1"))
        self.text_register_login.setText("Зарегистрироваться")
        self.text_register_login.setObjectName("text_register_login")

        self.button_or_setup = self.ClickableQLabel(parent=self.main.centralwidget)
        self.button_or_setup.setGeometry(QtCore.QRect(80, 186, 240, 19))
        self.button_or_setup.setText("или авторизоваться")
        self.button_or_setup.setFont(self.font.get_font(12, "1"))
        self.button_or_setup.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.button_or_setup.clicked.connect(lambda: self.update_window_auth(replace_auth_register_setup(self, self.window_auth)))
        self.button_or_setup.setObjectName("button_or_setup")

        self.nickname_setup = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.nickname_setup.setGeometry(QtCore.QRect(80, 230, 300, 46))
        self.nickname_setup.setFont(self.font.get_font(11, "1"))
        self.nickname_setup.setGraphicsEffect(create_shadow('light'))
        self.nickname_setup.setPlaceholderText("Никнейм (В Minecraft)")
        self.nickname_setup.textChanged.connect(lambda: access_step_continue_auth(self))
        self.nickname_setup.setObjectName("nickname_setup")

        self.password_setup = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.password_setup.setGeometry(QtCore.QRect(80, 291, 300, 46))
        self.password_setup.setFont(self.font.get_font(11, "1"))
        self.password_setup.setGraphicsEffect(create_shadow('light'))
        self.password_setup.setPlaceholderText("Пароль")
        self.password_setup.setObjectName("nickname_setup")
        self.password_setup.textChanged.connect(lambda: access_step_continue_auth(self))

        self.password_retry_setup = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.password_retry_setup.setGeometry(QtCore.QRect(80, 352, 300, 46))
        self.password_retry_setup.setFont(self.font.get_font(11, "1"))
        self.password_retry_setup.setGraphicsEffect(create_shadow('light'))
        self.password_retry_setup.setPlaceholderText("Повторить пароль")
        self.password_retry_setup.setObjectName("nickname_setup")
        self.password_retry_setup.textChanged.connect(lambda: access_step_continue_auth(self))

        self.button_auth_setup = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.button_auth_setup.setGeometry(QtCore.QRect(80, 423, 300, 35))
        self.button_auth_setup.setFont(self.font.get_font(9, "1"))
        self.button_auth_setup.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_auth_setup.setText("Создать аккаунт и продолжить")
        self.button_auth_setup.clicked.connect(lambda: auth_setup(self, self.nickname_setup.text(), self.password_setup.text()))
        self.button_auth_setup.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.button_auth_setup.setObjectName("button_auth_setup")

        access_step_continue_auth(self) # Иницилизируем блокировку кнопки

        self.text_rules_nickname_setup = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.text_rules_nickname_setup.setGeometry(QtCore.QRect(80, 483, 500, 60))
        self.text_rules_nickname_setup.setFont(self.font.get_font(12, "1"))
        self.text_rules_nickname_setup.setText("Никнейм может содержать:")
        self.text_rules_nickname_setup.setObjectName("text_rules_nickname_setup")

        self.rules_setup = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.rules_setup.setGeometry(QtCore.QRect(82, 500, 220, 100))
        self.rules_setup.setFont(self.font.get_font(10, "5"))
        self.rules_setup.setText("<font>1. Символы EN</font><br><font>2. Цифры</font><br><font>3. Спец-символы</font>")
        self.rules_setup.setObjectName("rules_setup")

        self.person2 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.person2.setGeometry(QtCore.QRect(536, 115, 504, 504))
        self.person2.setPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\page2\\person_1.png"))
        self.person2.setObjectName("person2")   

        # Page 3
        self.color_text = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.color_text.setGeometry(QtCore.QRect(80, 154, 500, 32))
        self.color_text.setFont(self.font.get_font(20, "1"))
        self.color_text.setText("<font color='#000000'>Цветовая тема оформления</font>")
        self.color_text.setObjectName("color_text")

        self.color_set_text = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.color_set_text.setGeometry(QtCore.QRect(80, 206, 500, 27))
        self.color_set_text.setFont(self.font.get_font(16, "1"))
        self.color_set_text.setText("<font color='#000000'>Выберите тему</font>")
        self.color_set_text.setObjectName("color_set_text")

        self.after_edit_text_setup = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.after_edit_text_setup.setGeometry(QtCore.QRect(80, 235, 500, 15))
        self.after_edit_text_setup.setFont(self.font.get_font(10, "5"))
        self.after_edit_text_setup.setText("Позже можно будет изменить")
        self.after_edit_text_setup.setObjectName("after_edit_text_setup")

        self.color_stamp_setup = QtWidgets.QComboBox(parent=self.main.centralwidget)
        self.color_stamp_setup.setGeometry(QtCore.QRect(80, 276, 260, 44))
        self.color_stamp_setup.setFont(self.font.get_font(12, "1"))
        self.color_stamp_setup.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.color_stamp_setup.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)
        self.color_stamp_setup.setObjectName("color_stamp_setup")
        self.color_stamp_setup.setGraphicsEffect(create_shadow('light'))

        self.color_stamp_view = QtWidgets.QListView(self.color_stamp_setup)
        self.color_stamp_view.setFont(self.font.get_font(12, "1"))
        self.color_stamp_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.color_stamp_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.color_stamp_setup.setView(self.color_stamp_view)
        self.color_stamp_view.setObjectName("color_stamp_view")
        self.color_stamp_setup.addItem("Светлая")
        self.color_stamp_setup.addItem("Темная")

        self.person3 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.person3.setGeometry(QtCore.QRect(628, 163, 472, 537))
        self.person3.setPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\page3\\person_1.png"))
        self.person3.setObjectName("person3")

        if self.page_setup == 0:
            self.text_register_login.hide()
            self.button_or_setup.hide()
            self.nickname_setup.hide()
            self.password_setup.hide()
            self.password_retry_setup.hide()
            self.button_auth_setup.hide()
            self.text_rules_nickname_setup.hide()
            self.rules_setup.hide()
            self.person2.hide()
            self.color_text.hide()
            self.color_set_text.hide()
            self.after_edit_text_setup.hide()
            self.color_stamp_setup.hide()
            self.person3.hide()