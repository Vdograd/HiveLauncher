from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QFrame
from ...utils.error_manager.error import ErrorExc
from ...auth.auth_manager import auth_manager
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
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
    
    # Текстовый блок
    text_layout = QVBoxLayout()
    text_layout.setContentsMargins(0, 0, 0, 0)
    text_layout.setSpacing(0)
    
    text_container = QWidget()
    text_container.setStyleSheet("background: transparent;")
    text_container.setLayout(text_layout)
    
    # Имя аккаунта
    name_label = QLabel(name)
    name_label.setFont(font.font(11, 14))
    name_label.setObjectName("name_account_in_card")
    name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    
    # Игровое время
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

    def add_user(self, name: str, play_time: float, icon: Union[str, Path], verify: bool, on_click=None) -> AccountCard:
        card = add_user(self.parent_main, name, play_time, icon, verify)
        
        if on_click:
            card.clicked.connect(on_click)
        
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

            logger.info(f'Add card-user: {player[0]}')
            self.box_users_card.add_user(name, play_time, pathjoin(build.static_folder, 'textures_heads', 'icon.png'), verify)
    except Exception as e:
        ErrorExc(e)

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