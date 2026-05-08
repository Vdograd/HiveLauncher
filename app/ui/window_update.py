from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
from ..utils.logger import logger
from ..utils.build import build
from .functions import *
from ..utils.font_manager import font
from .style import set_style
#from ..utils.error import ErrorExc

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.color = build.get_color_theme()
        self.drag_pos = NotImplementedError
        self.setup_stage()

    def setup_stage(self) -> None:
        self.setObjectName("AppWindow")
        self.resize(500, 410)
        self.setMinimumSize(QtCore.QSize(500, 410))
        self.setMaximumSize(QtCore.QSize(500, 410))
        self.setWindowTitle("HiveLauncher")
        self.setWindowIcon(QtGui.QIcon(f"{build.static_folder}\\logotypes\\HiveLauncher\\logotype_66x66_light.svg"))
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.add_ui()

    def add_ui(self) -> None:
        self.logo_hl = QtWidgets.QLabel(parent=self.centralwidget)
        self.logo_hl.setGeometry(QtCore.QRect(217, 22, 66, 66))
        self.logo_hl.setMinimumSize(QtCore.QSize(66, 66))
        self.logo_hl.setPixmap(QtGui.QPixmap(f"{build.static_folder}\\logotypes\\HiveLauncher\\logotype_66x66_{self.color}.svg"))
        self.logo_hl.setObjectName("logo_hl")

        self.text_launcher = QtWidgets.QLabel(parent=self.centralwidget)
        self.text_launcher.setGeometry(QtCore.QRect(0, 88, 500, 31))
        self.text_launcher.setFont(font.font(12, 20))
        self.text_launcher.setText("HiveLauncher")
        self.text_launcher.setObjectName("text_launcher")
        self.text_launcher.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if event.pos().y() <= 20:
                self.drag_pos = event.globalPosition().toPoint()
                self.drag_start_pos = self.pos()
                event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton and self.drag_pos is not None:
            if self.drag_pos is not None:
                delta = event.globalPosition().toPoint() - self.drag_pos
                self.move(self.drag_start_pos + delta)
                event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_pos = None
            event.accept()