from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
from ..utils.logger import logger
from ..utils.build import build
from .functions import *
from ..utils.font_manager import font
from .style import set_style
from ..core.folder_manager import get_currect_version
#from ..utils.error import ErrorExc

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.color = build.get_color_theme()
        self.drag_pos = None
        self.drag_start_pos = None
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

        # Layout для текущей версии - иконка - новая версия | текущая версия

        self.version_layout = QtWidgets.QHBoxLayout()
        self.version_layout.setContentsMargins(0, 0, 0, 0)
        self.version_layout.setSpacing(2)

        self.cloud_layout = QtWidgets.QWidget(self.centralwidget)
        self.cloud_layout.setLayout(self.version_layout)
        self.cloud_layout.setGeometry(QtCore.QRect(45, 361, 300, 18))

        self.cloud_layout_ver = QtWidgets.QWidget()
        self.cloud_layout_ver.setObjectName('first_version_step_1')

        self.version_current_layout = QtWidgets.QHBoxLayout(self.cloud_layout_ver)
        self.version_current_layout.setContentsMargins(5, 0, 5, 0)
        self.version_current_layout.setSpacing(5)

        self.ellips_cur_ver = QtWidgets.QLabel()
        self.ellips_cur_ver.setFixedSize(8, 8)
        self.ellips_cur_ver.setStyleSheet('background-color: #005FFF; border-radius: 4px;')
        self.ellips_cur_ver.setObjectName('ellips_first_version_step_1')

        self.text_version = QtWidgets.QLabel()
        self.text_version.setFont(font.font(12, 12))
        self.text_version.setText(f"v{get_currect_version()}" if get_currect_version() != None else 'None')
        self.text_version.setObjectName('text_first_version_step_1')

        self.version_current_layout.addWidget(self.ellips_cur_ver)
        self.version_current_layout.addWidget(self.text_version)

        self.version_layout.addWidget(self.cloud_layout_ver)

        self.arrow_version = QtWidgets.QLabel()
        self.arrow_version.setFixedSize(12, 12)
        self.arrow_version.setObjectName("arrow_version")
        self.arrow_version.setPixmap(QtGui.QPixmap(f"{build.static_folder}\\icons\\arrow_right_12x12_{self.color}.svg"))

        self.version_layout.addWidget(self.arrow_version) #

        self.cloud_layout_new_ver = QtWidgets.QWidget()
        self.cloud_layout_new_ver.setObjectName('two_version')

        self.version_new_layout = QtWidgets.QHBoxLayout(self.cloud_layout_new_ver)
        self.version_new_layout.setContentsMargins(5, 0, 5, 0)
        self.version_new_layout.setSpacing(5)

        self.ellips_new_ver = QtWidgets.QLabel()
        self.ellips_new_ver.setFixedSize(8, 8)
        self.ellips_new_ver.setObjectName('ellips_two_version')

        self.text_new_version = QtWidgets.QLabel()
        self.text_new_version.setFont(font.font(12, 12))
        self.text_new_version.setText("v4.0")
        self.text_new_version.setObjectName('text_two_version')

        self.version_new_layout.addWidget(self.ellips_new_ver)
        self.version_new_layout.addWidget(self.text_new_version)

        self.version_layout.addWidget(self.cloud_layout_new_ver) #

        self.version_layout.addStretch()

        self.text_speed = QtWidgets.QLabel(parent=self.centralwidget)
        self.text_speed.setGeometry(QtCore.QRect(500 - 45 - 110, 148, 110, 15))
        self.text_speed.setFont(font.font(12, 12))
        self.text_speed.setText("СКОРОСТЬ")
        self.text_speed.setObjectName("text_speed")
        self.text_speed.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.text_speed_realtime = QtWidgets.QLabel(parent=self.centralwidget)
        self.text_speed_realtime.setGeometry(QtCore.QRect(500 - 45 - 210, 169, 210, 18))
        self.text_speed_realtime.setFont(font.font(12, 14))
        self.text_speed_realtime.setText("12.4MB/s")
        self.text_speed_realtime.setObjectName("text_speed_realtime")
        self.text_speed_realtime.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.text_approximate_time = QtWidgets.QLabel(parent=self.centralwidget)
        self.text_approximate_time.setGeometry(QtCore.QRect(500 - 45 - 210, 216, 210, 15))
        self.text_approximate_time.setFont(font.font(11, 12))
        self.text_approximate_time.setText("~ 4 минуты")
        self.text_approximate_time.setObjectName("text_approximate_time")
        self.text_approximate_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        # Set scanning
        self.text_approximate_time.hide()
        self.text_speed_realtime.hide()
        self.text_speed.hide()

        self.cloud_layout_new_ver.hide()
        self.arrow_version.hide()

        #Start scanning
        scanning(self)

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