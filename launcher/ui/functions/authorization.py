from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from os.path import join as pathjoin
from PyQt6.QtWidgets import QWidget
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

def add_user(
    name: str,
    play_time: float,
    icon: Union[str, Path],
    verify: bool = True
) -> AccountCard:

    card = AccountCard()
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
    
    def add_user(
        self,
        name: str,
        play_time: float,
        icon: Union[str, Path],
        verify: bool,
        on_click=None
    ) -> AccountCard:
        card = add_user(name, play_time, icon, verify)
        
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