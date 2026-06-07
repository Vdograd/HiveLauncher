from ..functions.authorization import add_all_card, pos_size_with_count_accounts
from ..functions.authorization import ScrollableCardContainer
from PyQt6 import QtCore, QtGui, QtWidgets
from os.path import join as pathjoin
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from ...utils.build import build
from ...utils.fonts import font
from ..helper_ui import *


class WindowAuthorization(QWidget):
    def __init__(self, main, ClickableQLabel):
        self.ClickableQLabel = ClickableQLabel
        self.drag_start_pos = None
        self.drag_pos = None
        self.main = main
    
    def show_page(self):
        self.logo_auth = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.logo_auth.setGeometry(QtCore.QRect(70, 40, 70, 70))
        self.logo_auth.setMinimumSize(QtCore.QSize(70, 70))
        self.logo_auth.setPixmap(QtGui.QPixmap(pathjoin(build.static_folder, 'logotypes', 'HiveLauncher', f'logotype_{build.get_color_theme()}_70.svg')))
        self.logo_auth.setObjectName("logo_auth")

        self.auth_text_1 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_text_1.setGeometry(QtCore.QRect(0, 90, 1100, 54))
        self.auth_text_1.setFont(font.font(12,42))
        self.auth_text_1.setText(build.get_lang_text('auth_page-hello'))
        self.auth_text_1.setObjectName("auth_text_1")
        self.auth_text_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.auth_text_2 = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_text_2.setGeometry(QtCore.QRect(0, 152, 1100, 18))
        self.auth_text_2.setFont(font.font(11,14))
        self.auth_text_2.setText(build.get_lang_text('auth_page-direction'))
        self.auth_text_2.setObjectName("auth_text_2")
        self.auth_text_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.auth_panel_user = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_panel_user.setGeometry(QtCore.QRect(375, 205, 350, 377))
        self.auth_panel_user.setObjectName("auth_panel_user")

        self.auth_text_select_account = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_text_select_account.setFont(font.font(10,10))
        self.auth_text_select_account.setText(build.get_lang_text('auth_page-select_account'))
        self.auth_text_select_account.setObjectName("auth_text_select_account")
        self.auth_text_select_account.setGeometry(QtCore.QRect(400, 225, 150, 13))

        self.auth_text_count_saved = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_text_count_saved.setFont(font.font(10,10))
        self.auth_text_count_saved.setObjectName("auth_text_count_saved")
        self.auth_text_count_saved.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.auth_text_count_saved.setGeometry(QtCore.QRect(375+175, 205+20, 150, 13))

        # Box with card users
        self.box_users_card = ScrollableCardContainer(parent=self.main.centralwidget)
        self.box_users_card.move(397, 250)
        add_all_card(self)

        self.auth_text_add_account = QtWidgets.QLabel(parent=self.main.centralwidget)
        self.auth_text_add_account.setFont(font.font(10,10))
        self.auth_text_add_account.setText(build.get_lang_text('auth_page-add_account'))
        self.auth_text_add_account.setObjectName("auth_text_select_account")
        self.auth_text_add_account.setGeometry(QtCore.QRect(400, 419, 300, 13))
        
        self.auth_button_auth_new_account = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.auth_button_auth_new_account.setGeometry(QtCore.QRect(397, 444, 306, 40))
        self.auth_button_auth_new_account.setFont(font.font(11,14))
        self.auth_button_auth_new_account.setIcon(QtGui.QIcon(pathjoin(build.static_folder, 'icons', 'login.svg')))
        self.auth_button_auth_new_account.setIconSize(QtCore.QSize(20, 20))
        self.auth_button_auth_new_account.setText(f" {build.get_lang_text('auth_page-login')}")
        self.auth_button_auth_new_account.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.auth_button_auth_new_account.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.auth_button_auth_new_account.setObjectName("auth_button_auth_new_account")
        #self.auth_button_auth_new_account.clicked.connect(self.auth_new_account)

        self.auth_button_reg_new_account = QtWidgets.QPushButton(parent=self.main.centralwidget)
        self.auth_button_reg_new_account.setGeometry(QtCore.QRect(397, 492, 306, 40))
        self.auth_button_reg_new_account.setFont(font.font(11,14))
        self.auth_button_reg_new_account.setIcon(QtGui.QIcon(pathjoin(build.static_folder, 'icons', 'user_add.svg')))
        self.auth_button_reg_new_account.setIconSize(QtCore.QSize(20, 20))
        self.auth_button_reg_new_account.setText(f" {build.get_lang_text('auth_page-register')}")
        self.auth_button_reg_new_account.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.auth_button_reg_new_account.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.auth_button_reg_new_account.setObjectName("auth_button_auth_new_account")
        #self.auth_button_reg_new_account.clicked.connect(self.auth_new_account)

        self.auth_text_change_theme_container = QtWidgets.QWidget(parent=self.main.centralwidget)
        self.auth_text_change_theme_container.setGeometry(QtCore.QRect(375, 597, 350, 15))
        self.auth_text_change_theme_container.setObjectName("auth_text_change_theme_container")

        self.auth_layout_text_change_theme = QHBoxLayout(self.auth_text_change_theme_container)
        self.auth_layout_text_change_theme.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.auth_layout_text_change_theme.setContentsMargins(0, 0, 0, 0)

        self.auth_text_change_theme = ClickableQLabel(parent=self.auth_text_change_theme_container)
        self.auth_text_change_theme.setFont(font.font(11,12))
        self.auth_text_change_theme.setText(build.get_lang_text('auth_page-change_theme'))
        self.auth_text_change_theme.setObjectName("auth_text_change_theme")
        self.auth_text_change_theme.clicked.connect(lambda: change_color_theme(self))
        self.auth_layout_text_change_theme.addWidget(self.auth_text_change_theme)

        pos_size_with_count_accounts(self)
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if event.pos().y() <= 20:
                self.drag_pos = event.globalPosition().toPoint()
                self.drag_start_pos = self.pos()
                event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton and self.drag_pos is not None:
            delta = event.globalPosition().toPoint() - self.drag_pos
            self.move(self.drag_start_pos + delta)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_pos = None
            self.drag_start_pos = None
            event.accept()