from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from ...utils.error_manager.error import ErrorExc
from ...auth.auth_manager import auth_manager
from os.path import join as pathjoin
from PyQt6.QtWidgets import QWidget
from ...utils.logger import logger
from ...utils.build import build
from PyQt6.QtGui import QPixmap
from ...utils.fonts import font
from PyQt6.QtGui import QCursor
from ..style import set_style
from pathlib import Path
from typing import Union
from PyQt6 import QtCore
from PyQt6 import QtGui


# ------------------------------------------------

# POSITION ELEMENTS AND SHOW/HIDE PAGES

# ------------------------------------------------


def pos_size_with_count_accounts(self) -> None:
    count = len(build.get_all_nicknames()) # type: ignore

    if count == 1:
        self.auth_text_add_account.move(QPoint(400, 310+24))
        self.auth_button_auth_new_account.move(QPoint(400, self.auth_text_add_account.pos().y()+13+12))
        self.auth_button_reg_new_account.move(QPoint(400, self.auth_button_auth_new_account.pos().y()+40+8))
        self.auth_panel_user.setFixedHeight(292)
        self.auth_text_change_theme_container.move(QPoint(375, 205+292+15))

    if count == 2:
        self.auth_text_add_account.move(QPoint(400, 250+(60*2)+8+24))
        self.auth_button_auth_new_account.move(QPoint(400, self.auth_text_add_account.pos().y()+13+12))
        self.auth_button_reg_new_account.move(QPoint(400, self.auth_button_auth_new_account.pos().y()+40+8))
        self.auth_panel_user.setFixedHeight(360)
        self.auth_text_change_theme_container.move(QPoint(375, 205+360+15))

def show_login_account(self) -> None:
    hide_all_elements(self)

    self.auth_qlineedit_1.clear()
    self.auth_qlineedit_2.clear()
    self.auth_qlineedit_3.clear()

    self.logo_auth.show()
    self.auth_text_1.show()
    self.auth_text_2.show()
    self.auth_panel_user.show()
    self.auth_text_select_account.show()
    self.auth_qlineedit_1.show()
    self.auth_text_add_account.show()
    self.auth_qlineedit_2.show()
    self.auth_button_login_to_account.show()
    self.auth_text_change_theme_container.show()
    self.auth_forgot_password.show()

    self.auth_qlineedit_2.setGeometry(QtCore.QRect(397, 339, 306, 40))
    self.auth_text_1.setText(build.get_lang_text('auth_page-login_page-text_1'))
    self.auth_text_2.setText(build.get_lang_text('auth_page-login_page-text_2'))
    self.auth_text_select_account.setText(build.get_lang_text('auth_page-login_page-text_3'))
    self.auth_qlineedit_1_icon.setPixmap(QtGui.QIcon(pathjoin(build.static_folder, 'icons', 'user.svg')).pixmap(16, 16))
    self.auth_qlineedit_1.setPlaceholderText(build.get_lang_text('auth_page-login_page-placeholder_1'))
    self.auth_text_add_account.move(400, 314)
    self.auth_text_add_account.setText(build.get_lang_text('auth_page-login_page-text_4'))
    self.auth_qlineedit_2.setPlaceholderText(build.get_lang_text('auth_page-login_page-placeholder_2'))
    self.auth_qlineedit_2_icon.setPixmap(QtGui.QIcon(pathjoin(build.static_folder, 'icons', 'lock.svg')).pixmap(16, 16))
    self.auth_button_login_to_account.setText(build.get_lang_text('auth_page-login_page-button'))
    self.auth_panel_user.setFixedHeight(288)
    self.auth_text_change_theme_container.move(QPoint(375, 508))
    self.btn_back.setIcon(QtGui.QIcon(pathjoin(build.static_folder, 'icons', f'arrow_left_10x10.svg')))
    self.btn_back.setText(build.get_lang_text('auth_page-login_page-back'))
    self.btn_back.show()
    self.btn_back.move(1100-400-self.btn_back.size().width(), 225)
    self.auth_forgot_password.setText(build.get_lang_text('auth_page-login_page-forgot_password'))
    self.auth_forgot_password.adjustSize()
    self.auth_forgot_password.move(1100-400-self.auth_forgot_password.size().width(), 314)

def show_register_account(self) -> None:
    hide_all_elements(self)

    self.auth_qlineedit_1.clear()
    self.auth_qlineedit_2.clear()
    self.auth_qlineedit_3.clear()

    self.logo_auth.show()
    self.auth_text_1.show()
    self.auth_text_2.show()
    self.auth_panel_user.show()
    self.auth_text_select_account.show()
    self.auth_qlineedit_1.show()
    self.auth_text_add_account.show()
    self.auth_qlineedit_2.show()
    self.auth_qlineedit_3.show()
    self.auth_text_password_line.show()
    self.auth_button_create_to_account.show()
    self.auth_text_change_theme_container.show()

    self.auth_text_1.setText(build.get_lang_text('auth_page-register_page-text_1'))
    self.auth_text_2.setText(build.get_lang_text('auth_page-register_page-text_2'))
    self.auth_text_select_account.setText(build.get_lang_text('auth_page-register_page-text_3'))
    self.auth_qlineedit_1.setPlaceholderText(build.get_lang_text('auth_page-register_page-placeholder_1'))
    self.auth_qlineedit_1_icon.setPixmap(QtGui.QIcon(pathjoin(build.static_folder, 'icons', 'mail.svg')).pixmap(16, 16))
    self.auth_text_add_account.move(400, 314)
    self.auth_text_add_account.setText(build.get_lang_text('auth_page-register_page-text_4'))
    self.auth_qlineedit_3.setPlaceholderText(build.get_lang_text('auth_page-register_page-placeholder_2'))
    self.auth_qlineedit_3_icon.setPixmap(QtGui.QIcon(pathjoin(build.static_folder, 'icons', 'user.svg')).pixmap(16, 16))
    self.auth_text_password_line.setText(build.get_lang_text('auth_page-register_page-text_5'))

    self.btn_back.setIcon(QtGui.QIcon(pathjoin(build.static_folder, 'icons', f'arrow_left_10x10.svg')))
    self.btn_back.setText(build.get_lang_text('auth_page-login_page-back'))
    self.btn_back.show()
    self.btn_back.move(1100-400-self.btn_back.size().width(), 225)

    self.auth_qlineedit_2.setPlaceholderText(build.get_lang_text('auth_page-register_page-placeholder_3'))
    self.auth_qlineedit_2_icon.setPixmap(QtGui.QIcon(pathjoin(build.static_folder, 'icons', 'lock.svg')).pixmap(16, 16))
    self.auth_qlineedit_2.setGeometry(QtCore.QRect(397, 428, 306, 40))

    self.auth_button_create_to_account.setText(build.get_lang_text('auth_page-register_page-button'))
    self.auth_text_change_theme_container.move(QPoint(375, 597))
    self.auth_panel_user.setFixedHeight(377)

def show_home(self) -> None:
    hide_all_elements(self)

    self.logo_auth.show()
    self.auth_text_1.show()
    self.auth_text_2.show()
    self.auth_panel_user.show()
    self.auth_text_select_account.show()
    self.auth_text_count_saved.show()
    self.box_users_card.show()
    self.auth_text_add_account.show()
    self.auth_button_auth_new_account.show()
    self.auth_button_reg_new_account.show()
    self.auth_text_change_theme_container.show()

    self.auth_text_1.setGeometry(QtCore.QRect(0, 90, 1100, 54))
    self.auth_text_1.setText(build.get_lang_text('auth_page-hello'))

    self.auth_text_2.setGeometry(QtCore.QRect(0, 152, 1100, 18))
    self.auth_text_2.setText(build.get_lang_text('auth_page-direction'))

    self.auth_text_select_account.setText(build.get_lang_text('auth_page-select_account'))
    self.auth_text_select_account.setGeometry(QtCore.QRect(400, 225, 150, 13))
    self.auth_text_count_saved.setGeometry(QtCore.QRect(375+175, 205+20, 150, 13))
    self.auth_text_add_account.setText(build.get_lang_text('auth_page-add_account'))
    self.auth_text_add_account.setGeometry(QtCore.QRect(400, 419, 300, 13))
    self.auth_button_auth_new_account.setGeometry(QtCore.QRect(397, 444, 306, 40))
    self.auth_button_auth_new_account.setIcon(QtGui.QIcon(pathjoin(build.static_folder, 'icons', 'login.svg')))
    self.auth_button_auth_new_account.setText(f" {build.get_lang_text('auth_page-login')}")
    self.auth_button_reg_new_account.setGeometry(QtCore.QRect(397, 492, 306, 40))
    self.auth_button_reg_new_account.setText(f" {build.get_lang_text('auth_page-register')}")
    self.auth_button_reg_new_account.setIcon(QtGui.QIcon(pathjoin(build.static_folder, 'icons', 'user_add.svg')))
    self.auth_text_change_theme.setText(build.get_lang_text('auth_page-change_theme'))
    self.auth_text_change_theme_container.setGeometry(QtCore.QRect(375, 597, 350, 15))
    self.auth_panel_user.setGeometry(QtCore.QRect(375, 205, 350, 377))

    pos_size_with_count_accounts(self)

def hide_all_elements(self) -> None: 
    self.logo_auth.hide()
    self.auth_text_1.hide()
    self.auth_text_2.hide()
    self.auth_panel_user.hide()
    self.auth_text_select_account.hide()
    self.auth_text_count_saved.hide()
    self.box_users_card.hide()
    self.auth_text_add_account.hide()
    self.auth_button_auth_new_account.hide()
    self.auth_button_reg_new_account.hide()
    self.auth_text_change_theme_container.hide()
    self.auth_qlineedit_1.hide()
    self.auth_qlineedit_2.hide()
    self.auth_button_login_to_account.hide()
    self.btn_back.hide()
    self.auth_qlineedit_3.hide()
    self.auth_text_password_line.hide()
    self.auth_button_create_to_account.hide()
    self.auth_forgot_password.hide()
    self.auth_button_confirm_email.hide()

def show_set_email_for_account(self, nickname) -> None:
    hide_all_elements(self)

    self.auth_qlineedit_1.clear()
    self.logo_auth.show()
    self.auth_text_1.show()
    self.auth_text_2.show()
    self.auth_panel_user.show()
    self.auth_text_select_account.show()
    self.auth_text_count_saved.show()
    self.auth_qlineedit_1.show()
    self.auth_button_confirm_email.show()
    self.auth_text_change_theme.show()

    self.auth_panel_user.setGeometry(QtCore.QRect(375, 243, 350, 199))
    self.auth_panel_user.setFixedHeight(199)
    self.auth_text_1.setGeometry(QtCore.QRect(265, 90, 570, 92))
    self.auth_text_1.setText(build.get_lang_text('auth_set_email-page1-text1'))
    self.auth_text_1.setWordWrap(True)
    self.auth_text_1.setFont(font.font(12,36))

    self.auth_text_2.setGeometry(QtCore.QRect(0, 190, 1100, 18))
    self.auth_text_2.setText(build.get_lang_text('auth_set_email-page1-direction'))

    self.auth_text_select_account.setText(build.get_lang_text('auth_set_email-page1-select_account'))
    self.auth_text_select_account.setGeometry(QtCore.QRect(400, 263, 150, 13))
    self.auth_text_count_saved.setGeometry(QtCore.QRect(540, 263, 160, 13))
    self.auth_text_count_saved.setText(nickname.upper())
    self.auth_qlineedit_1.setPlaceholderText(build.get_lang_text('auth_page-register_page-placeholder_1'))
    self.auth_qlineedit_1.setGeometry(QtCore.QRect(397, 288, 306, 40))
    self.auth_qlineedit_1_icon.setPixmap(QtGui.QIcon(pathjoin(build.static_folder, 'icons', 'mail.svg')).pixmap(16, 16))

    self.auth_button_confirm_email.setGeometry(QtCore.QRect(397, 352, 306, 40))
    self.auth_button_confirm_email.setText(build.get_lang_text('auth_set_email-page1-confirm'))

    self.auth_text_change_theme.setText(build.get_lang_text('auth_page-change_theme'))
    self.auth_text_change_theme_container.setGeometry(QtCore.QRect(375, 454, 350, 15))


# ------------------------------------------------

# SYSTEM-FUNCTIONS FOR AUTH, REGISTER,
# SET EMAIL, SHOW ERROR, CONTINUE IN LAUNCHER

# ------------------------------------------------


def click_on_card_user(self, nickname, email, verify, play_time, data_register) -> None:
    if not verify: print('Not verify')
    elif email == None: show_set_email_for_account(self, nickname)
    else: print("All ok, let's go in launcher")


# ------------------------------------------------

# SETTING CARDS

# ------------------------------------------------


class AccountCard(QWidget):
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

def add_user(parent, name: str, play_time: float,icon: Union[str, Path],verify: bool) -> AccountCard:
    card = AccountCard(parent)
    card.setFixedSize(306, 60)
    card.setObjectName("accountCard")
    
    main_layout = QHBoxLayout(card)
    main_layout.setContentsMargins(25, 0, 0, 0)
    main_layout.setSpacing(10)
    main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    
    icon_label = QLabel()
    icon_label.setFixedSize(30, 30)
    icon_path = str(icon) if isinstance(icon, Path) else icon
    pixmap = QPixmap(icon_path)
    if not pixmap.isNull():
        icon_label.setPixmap(pixmap.scaled(
            30, 30,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
    icon_label.setStyleSheet("background: transparent;")
    main_layout.addWidget(icon_label)
    
    text_layout = QVBoxLayout()
    text_layout.setContentsMargins(0, 0, 0, 0)
    text_layout.setSpacing(0)
    
    text_container = QWidget()
    text_container.setStyleSheet("background: transparent;")
    text_container.setLayout(text_layout)
    
    name_label = QLabel(name)
    name_label.setFont(font.font(11, 14))
    name_label.setObjectName("name_account_in_card")
    name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    
    time_text = f"{round(play_time)}{build.get_lang_text('global-times-hour')}"
    time_label = QLabel(time_text)
    time_label.setObjectName("time_account_in_card")
    time_label.setFont(font.font(12, 12))
    time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    
    text_layout.addWidget(name_label)
    text_layout.addWidget(time_label)
    main_layout.addWidget(text_container)
    
    if not verify:
        lock_icon = QLabel(card)
        lock_icon.setFixedSize(16, 16)
        lock_icon.setStyleSheet("background: transparent;")
        lock_icon.setPixmap(QPixmap(pathjoin(build.static_folder, 'icons', 'lock.svg')))
        
        lock_icon.move(265, 22)
        lock_icon.raise_()
        
        lock_icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    else:
        main_layout.addStretch()

    set_style(card, build.get_color_theme())
    return card

class ScrollableCardContainer(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_main = parent
        self.setFixedSize(306, 145)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        
        self.cards_layout = QVBoxLayout(self.container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(8)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.setWidget(self.container)
        self.setWidgetResizable(True)
    
    def update_styles(self, color):
        for i in range(self.cards_layout.count()):
            item = self.cards_layout.itemAt(i)
            if item and item.widget():
                card = item.widget()
                if isinstance(card, AccountCard):
                    set_style(card, color)

    def add_user(self,selfmain, name: str, play_time: float, icon: Union[str, Path], verify: bool, email: str | None, register_time: str) -> AccountCard:
        card = add_user(self.parent_main, name, play_time, icon, verify)
        card.clicked.connect(lambda: click_on_card_user(selfmain, name, email, verify, play_time, register_time))
        
        self.cards_layout.addWidget(card)
        return card
    
    def clear(self):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget(): # type: ignore
                item.widget().deleteLater() # type: ignore
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.value() - delta // 6) # type: ignore

def add_all_card(self) -> None:
    try:
        players = auth_manager.list_nicknames()
        last_nickname = build.get_last_nickname()

        if last_nickname in [user[0] for user in players]:
            players_edit = [user for user in players if user[0] == last_nickname]
            players_edit += [user for user in players if user[0] != last_nickname]
        else: players_edit = players

        self.auth_text_count_saved.setText(f"{len(players)} {build.get_lang_text('auth_page-saved')}")
        for player in players_edit:
            name = player[0]
            verify = player[1]
            play_time = player[2]
            email = player[3]
            register_time = player[4]

            logger.info(f'Add card-user: {player[0]}')
            self.box_users_card.add_user(self, name, play_time, pathjoin(build.static_folder, 'textures_heads', 'icon.png'), verify, email, register_time)
    except Exception as e:
        ErrorExc(e)