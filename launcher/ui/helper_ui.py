from PyQt6 import QtCore, QtGui, QtWidgets
from ..utils.build import build

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