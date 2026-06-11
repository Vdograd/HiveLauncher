from ..functions.authorization import *
from PyQt6 import QtCore, QtGui, QtWidgets
from os.path import join as pathjoin
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from ...utils.build import build
from ...utils.fonts import font
from ..helper_ui import *


class WindowAuthorization(QWidget):
    def __init__(self, main, ClickableQLabel):
        self.ClickableQLabel = ClickableQLabel
        self.main = main
    
    def show_page(self):

        self.logo_auth = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.logo_auth.setGeometry(QtCore.QRect(70, 40, 70, 70))
        self.logo_auth.setMinimumSize(QtCore.QSize(70, 70))
        self.logo_auth.setPixmap(QtGui.QPixmap(pathjoin(build.static_folder, 'logotypes', 'HiveLauncher', f'logotype_{build.get_color_theme()}_70.svg')))
        self.logo_auth.setObjectName("logo_auth")

        self.auth_text_1 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_text_1.setFont(font.font(12,42))
        self.auth_text_1.setObjectName("auth_text_1")
        self.auth_text_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.auth_text_2 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_text_2.setFont(font.font(11,14))
        self.auth_text_2.setObjectName("auth_text_2")
        self.auth_text_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.auth_panel_user = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_panel_user.setObjectName("auth_panel_user")

        self.auth_text_select_account = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_text_select_account.setFont(font.font(10,10))
        self.auth_text_select_account.setObjectName("auth_text_select_account")

        self.auth_text_count_saved = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_text_count_saved.setFont(font.font(10,10))
        self.auth_text_count_saved.setObjectName("auth_text_count_saved")
        self.auth_text_count_saved.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        # Box with card users
        self.box_users_card = ScrollableCardContainer(parent=self.main.centralwidget)
        self.box_users_card.move(397, 250)
        add_all_card(self)

        self.auth_text_add_account = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_text_add_account.setFont(font.font(10,10))
        self.auth_text_add_account.setObjectName("auth_text_select_account")
        
        self.auth_button_auth_new_account = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.auth_button_auth_new_account.setFont(font.font(11,14))
        self.auth_button_auth_new_account.setIconSize(QtCore.QSize(20, 20))
        self.auth_button_auth_new_account.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.auth_button_auth_new_account.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.auth_button_auth_new_account.setObjectName("auth_button_auth_new_account")
        self.auth_button_auth_new_account.clicked.connect(lambda: show_login_account(self))

        self.auth_button_reg_new_account = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.auth_button_reg_new_account.setFont(font.font(11,14))
        self.auth_button_reg_new_account.setIconSize(QtCore.QSize(20, 20))
        self.auth_button_reg_new_account.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.auth_button_reg_new_account.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.auth_button_reg_new_account.setObjectName("auth_button_auth_new_account")
        self.auth_button_reg_new_account.clicked.connect(lambda: show_register_account(self))

        self.auth_text_change_theme_container = QtWidgets.QWidget(parent=self.main.centralwidget)
        self.auth_text_change_theme_container.setObjectName("auth_text_change_theme_container")

        self.auth_layout_text_change_theme = QHBoxLayout(self.auth_text_change_theme_container)
        self.auth_layout_text_change_theme.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.auth_layout_text_change_theme.setContentsMargins(0, 0, 0, 0)

        self.auth_text_change_theme = ClickableQLabel(parent=self.auth_text_change_theme_container)
        self.auth_text_change_theme.setFont(font.font(11,12))
        self.auth_text_change_theme.setObjectName("auth_text_change_theme")
        self.auth_text_change_theme.clicked.connect(lambda: change_color_theme(self))
        self.auth_layout_text_change_theme.addWidget(self.auth_text_change_theme)

        self.btn_back = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.btn_back.setFont(font.font(10,10))
        self.btn_back.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_back.setObjectName('auth_btn_back')
        self.btn_back.clicked.connect(lambda: show_home(self))
        self.btn_back.setIconSize(QtCore.QSize(10, 10))

        # Auth page
        self.auth_qlineedit_1 = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.auth_qlineedit_1.setGeometry(QtCore.QRect(397, 250, 306, 40))
        self.auth_qlineedit_1.setFont(font.font(11, 14))
        self.auth_qlineedit_1.setObjectName("auth_qlineedit_1")

        self.auth_qlineedit_1_icon = QtWidgets.QLabel(self.auth_qlineedit_1)
        self.auth_qlineedit_1_icon.setFixedSize(16, 16)
        self.auth_qlineedit_1_icon.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.auth_qlineedit_1_icon.move(20, (40 - 16) // 2)
        self.auth_qlineedit_1.setTextMargins(20 + 16 + 8, 0, 8, 0)

        self.auth_qlineedit_2 = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.auth_qlineedit_2.setObjectName("auth_qlineedit_1")
        self.auth_qlineedit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        _placeholder_font = font.font(11, 14)

        _pwd_font = QtGui.QFont("Segoe UI", 11)
        _pwd_font.setStyleStrategy(
            QtGui.QFont.StyleStrategy.PreferAntialias
            | QtGui.QFont.StyleStrategy.NoFontMerging
        )

        self.auth_qlineedit_2.setFont(_placeholder_font)

        def _toggle_pwd_font(text):
            self.auth_qlineedit_2.setFont(_pwd_font if text else _placeholder_font)

        self.auth_qlineedit_2.textChanged.connect(_toggle_pwd_font)

        self.auth_qlineedit_2_icon = QtWidgets.QLabel(self.auth_qlineedit_2)
        self.auth_qlineedit_2_icon.setFixedSize(16, 16)
        self.auth_qlineedit_2_icon.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.auth_qlineedit_2_icon.move(20, (40 - 16) // 2)
        self.auth_qlineedit_2.setTextMargins(20 + 16 + 8, 0, 8, 0)

        self.auth_button_login_to_account = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.auth_button_login_to_account.setGeometry(QtCore.QRect(397, 403, 306, 40))
        self.auth_button_login_to_account.setFont(font.font(8,16))
        self.auth_button_login_to_account.setIconSize(QtCore.QSize(20, 20))
        self.auth_button_login_to_account.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.auth_button_login_to_account.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.auth_button_login_to_account.setObjectName("auth_button_login_to_account")
        #self.auth_button_login_to_account.clicked.connect(self.auth_new_account)

        self.auth_qlineedit_3 = QtWidgets.QLineEdit(parent=self.main.centralwidget)
        self.auth_qlineedit_3.setGeometry(QtCore.QRect(397, 339, 306, 40))
        self.auth_qlineedit_3.setFont(font.font(11, 14))
        self.auth_qlineedit_3.setObjectName("auth_qlineedit_1")

        self.auth_qlineedit_3_icon = QtWidgets.QLabel(self.auth_qlineedit_3)
        self.auth_qlineedit_3_icon.setFixedSize(16, 16)
        self.auth_qlineedit_3_icon.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.auth_qlineedit_3_icon.move(20, (40 - 16) // 2)
        self.auth_qlineedit_3.setTextMargins(20 + 16 + 8, 0, 8, 0)

        self.auth_text_password_line = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_text_password_line.setFont(font.font(10,10))
        self.auth_text_password_line.setObjectName("auth_text_select_account")
        self.auth_text_password_line.setGeometry(QtCore.QRect(400, 403, 140, 13))

        self.auth_button_create_to_account = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.auth_button_create_to_account.setGeometry(QtCore.QRect(397, 492, 306, 40))
        self.auth_button_create_to_account.setFont(font.font(8,16))
        self.auth_button_create_to_account.setIconSize(QtCore.QSize(20, 20))
        self.auth_button_create_to_account.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.auth_button_create_to_account.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.auth_button_create_to_account.setObjectName("auth_button_login_to_account")
        #self.auth_button_create_to_account.clicked.connect(self.auth_new_account)

        show_home(self)