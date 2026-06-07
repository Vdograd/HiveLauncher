from PyQt6.QtWidgets import QScrollArea, QFrame, QWidget, QVBoxLayout
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal
from os.path import join as pathjoin
from PyQt6.QtGui import QCursor
from ..utils.build import build
from .style import set_style
from pathlib import Path
from typing import Union

class ClickableQLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

def currect_show_page() -> int:
    try:
        nicknames = build.get_all_nicknames()
        if nicknames == None: return 0
        else: return 1
    except Exception as e:
        raise e
    
def change_color_theme(self):
    currect_color = build.get_color_theme()
    if currect_color == 'light':
        set_color = 'dark'
    else:
        set_color = 'light'
    build.set_color_theme(set_color)
    set_style(self.main, set_color)

    self.box_users_card.update_styles(set_color)
    self.logo_auth.setPixmap(QtGui.QPixmap(pathjoin(build.static_folder, 'logotypes', 'HiveLauncher', f'logotype_{set_color}_70.svg')))