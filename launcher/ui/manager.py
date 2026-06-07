from .window_classes.authorization import WindowAuthorization
from ..utils.error_manager.error import ErrorExc
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
from os.path import join as pathjoin
from ..utils.logger import logger
from ..utils.build import build
from .style import set_style
from .helper_ui import *

class HiveLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.auth_window = WindowAuthorization(self, ClickableQLabel)
        self.nickname = None
        self.datetime = None
        self.play_time = None
        self.email = None
        self.type_skin = None
        self.setup_default_settings()

    def setup_default_settings(self):
        self.setObjectName("HiveLauncher")
        self.resize(1100, 700)
        self.setMinimumSize(QtCore.QSize(1100, 700))
        self.setMaximumSize(QtCore.QSize(1100, 700))
        self.setWindowTitle("HiveLauncher")
        self.setWindowIcon(QtGui.QIcon(pathjoin(build.static_folder, 'logotypes', 'HiveLauncher', 'logotype_64.svg')))

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.set_page_start()

    def set_page_start(self) -> None:
        try:
            page = currect_show_page()
            if page == 0:
                set_style(self, build.get_color_theme())
            else:
                set_style(self, build.get_color_theme())
                logger.info('Show authorization.')
                self.auth_window.show_page()
        except Exception as e:
            ErrorExc(e)