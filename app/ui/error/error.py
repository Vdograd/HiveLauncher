from PyQt6 import QtCore, QtGui, QtWidgets
import sys
from ...ui.style import set_style
from ...utils.build import build
from ...utils.font_manager import font
from PyQt6.QtCore import Qt
import os
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from ...utils.logger import logger
from ...core.report_email import ReportEmail
from ...core.thread_classes import CopyLog

class DialogError(QtWidgets.QDialog):
    def __init__(self, name: str, message: str, type_error: str):
        super().__init__()
        try:
            self.color = build.get_color_theme()
        except:
            self.color = 'light'

        self.message = message
        self.name = name
        self.type_error = type_error

        self.drag_pos = None
        self.drag_start_pos = None

        try:
            set_style(self, self.color)
        except:
            self.setStyleSheet(
    """
    #ErrorDialog {
        background: #F5F5F5;
    }

    #cross {
        background: rgba(0,0,0,0)
    }

    #ellips_error {
        background: #ffffff;
        border-radius: 35px;
    }

    #text_error {
        color: #000000;
    }

    #text_error_message {
        color: #656976
    }

    #box_footer {
        background: #FFFFFF;
    }

    #version_update_launcher {
        color: #A2A2A2;
    }

    #text_type_error {
        color: #A33301;
    }

    #send_report_button {
        background: #005FFF;
        color: #ffffff;
        border-radius: 12px;
    }

    #send_report_button:hover {
        background: #0055E6; /*+8*/
    }

    #copy_log_button {
        background: #656976;
        color: #E3E3E3;
        border-radius: 12px;
    }

    #copy_log_button:hover {
        background: #5D606C;
    }            
    """
)

        self.show_error()

    def show_error(self):
        self.setWindowTitle("HiveLauncher Error")
        self.resize(450, 400)
        self.setMinimumSize(QtCore.QSize(450, 400))
        self.setMaximumSize(QtCore.QSize(450, 400))
        self.setObjectName('ErrorDialog')
        self.setWindowIcon(QtGui.QIcon(f"{os.path.join(build.static_folder, 'logotypes', 'HiveLauncher', 'logotype_66x66_light.svg')}"))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.cross = QtWidgets.QPushButton(self)
        self.cross.setGeometry(QtCore.QRect(410, 18, 16, 16)) 
        self.cross.setObjectName("cross")
        self.cross.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.cross.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.cross.setIcon(QtGui.QIcon(os.path.join(build.static_folder, 'icons', 'cross.svg')))
        self.cross.clicked.connect(lambda: sys.exit())

        self.ellips_error = QtWidgets.QLabel(self)
        self.ellips_error.setGeometry(QtCore.QRect(190, 26, 70, 70))
        self.ellips_error.setObjectName("ellips_error")
        self.ellips_error.setGraphicsEffect(self.create_shadow())

        self.cloud = QtWidgets.QLabel(parent=self)
        self.cloud.setGeometry(QtCore.QRect(207, 43, 35, 35))
        self.cloud.setPixmap(QtGui.QPixmap(os.path.join(build.static_folder, 'icons', 'cloud.svg')))
        self.cloud.setObjectName("cloud")

        self.text_error = QtWidgets.QLabel(self)
        self.text_error.setGeometry(QtCore.QRect(0, 126, 450, 23))
        self.text_error.setFont(font.font(12, 18))
        self.text_error.setText(self.name)
        self.text_error.setObjectName("text_error")
        self.text_error.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text_error_message = QtWidgets.QLabel(self)
        self.text_error_message.setGeometry(QtCore.QRect(40, 159, 370, 96))
        self.text_error_message.setFont(font.font(11, 14))
        self.text_error_message.setText(self.message)
        self.text_error_message.setObjectName("text_error_message")
        self.text_error_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        self.text_error_message.setWordWrap(True)

        self.box_footer = QtWidgets.QLabel(self)
        self.box_footer.setGeometry(QtCore.QRect(0, 355, 450, 45))
        self.box_footer.setObjectName("box_footer")

        self.version_update_launcher = QtWidgets.QLabel(self)
        self.version_update_launcher.setGeometry(QtCore.QRect(40, 371, 150, 13))
        self.version_update_launcher.setFont(font.font(8, 10))
        self.version_update_launcher.setText(f'HIVELAUNCHER  v{build.update_version}-U')
        self.version_update_launcher.setObjectName("version_update_launcher")

        self.type_error_layout = QtWidgets.QHBoxLayout()
        self.type_error_layout.setContentsMargins(0, 0, 0, 0)
        self.type_error_layout.setSpacing(3)

        self.error_icon = QtWidgets.QLabel(parent=self)
        self.error_icon.setFixedSize(QtCore.QSize(13, 13))
        self.error_icon.setPixmap(QtGui.QPixmap(os.path.join(build.static_folder, 'icons', 'warn.svg')))
        self.error_icon.setObjectName("error_icon")

        self.text_type_error = QtWidgets.QLabel(self)
        self.text_type_error.setFont(font.font(12, 10))
        self.text_type_error.setText(self.type_error)
        self.text_type_error.setObjectName("text_type_error")
        self.text_type_error.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.type_error_layout.addWidget(self.error_icon)
        self.type_error_layout.addWidget(self.text_type_error)

        self.type_error_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

        container = QtWidgets.QWidget(self)
        container.setLayout(self.type_error_layout)
        container.setGeometry(QtCore.QRect(self.width()-175-40, 371, 175, 13))

        self.send_report_button = QtWidgets.QPushButton(self)
        self.send_report_button.setGeometry(QtCore.QRect(40, 285, 180, 40))
        self.send_report_button.setObjectName("send_report_button")
        self.send_report_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.send_report_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.send_report_button.setFont(font.font(10, 14))
        self.send_report_button.setText('Отправить репорт')
        self.send_report_button.clicked.connect(lambda: self.send_report_func())

        self.copy_log_button = QtWidgets.QPushButton(self)
        self.copy_log_button.setGeometry(QtCore.QRect(230, 285, 180, 40))
        self.copy_log_button.setObjectName("copy_log_button")
        self.copy_log_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.copy_log_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.copy_log_button.setFont(font.font(10, 14))
        self.copy_log_button.setText('Скопировать логи')
        self.copy_log_button.clicked.connect(lambda: self.copy_log())

    def closeEvent(self, event):
        sys.exit()

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

    def send_report_func(self):
        self.worker = ReportEmail()
        self.worker.setParent(self)
        self.worker.finished.connect(lambda: sys.exit())
        self.send_report_button.setEnabled(False)
        self.send_report_button.setText("Отправляем")
        logger.info("Send report error...")
        self.worker.start()

    def create_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(165, 51, 1, 25))
        return shadow

    def copy_log(self) -> None:
        self.copy = CopyLog()
        self.copy.finished.connect(lambda: self.end_copy())
        logger.info("Copy logs...")
        self.copy_log_button.setEnabled(False)
        self.copy.start()

    def end_copy(self) -> None:
        self.copy_log_button.setText('Скопировано!')
        QtCore.QTimer.singleShot(1500, lambda: self.end())

    def end(self) -> None:
        self.copy_log_button.setText('Скопировать логи')
        self.copy_log_button.setEnabled(True)