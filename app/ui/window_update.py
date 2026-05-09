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
        logger.info('Set styles')
        try:
            set_style(self, self.color)
        except Exception as e:
            ...


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
        self.text_launcher.setFont(font.font(12, 24))
        self.text_launcher.setText("HiveLauncher")
        self.text_launcher.setObjectName("text_launcher")
        self.text_launcher.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text_global_status = QtWidgets.QLabel(parent=self.centralwidget)
        self.text_global_status.setGeometry(QtCore.QRect(45, 148, 250, 15))
        self.text_global_status.setFont(font.font(12, 12))
        self.text_global_status.setText("Проверка обновлений")
        self.text_global_status.setObjectName("text_global_status")

        self.text_status = QtWidgets.QLabel(parent=self.centralwidget)
        self.text_status.setGeometry(QtCore.QRect(45, 169, 250, 18))
        self.text_status.setFont(font.font(12, 14))
        self.text_status.setText("Сканирование...")
        self.text_status.setObjectName("text_status")

        self.progress_bar = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progress_bar.setGeometry(QtCore.QRect(45, 198, 410, 10))
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setTextVisible(False)

        self.github = QtWidgets.QPushButton(parent=self.centralwidget)
        self.github.setGeometry(QtCore.QRect(388, 360, 67, 20))
        self.github.setObjectName("github")
        self.github.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.github.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.github.setIconSize(QtCore.QSize(67, 20))
        self.github.setIcon(QtGui.QIcon(f"{build.static_folder}\\logotypes\\GitHub\\logotype_{self.color}.svg"))
        self.github.clicked.connect(lambda: open_github())

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