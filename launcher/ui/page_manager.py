from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
from ..utils.logger import logger
from ..utils.configurator import Configurator
from .page_functions.page_manager import how_start_page, versions_add
from .pages.setup import WindowSetup
from .pages.login import WindowLogin
from .pages.launch import WindowLauncher
from ..utils.font_manager import FontManager
from .style import set_style
from ..core.skin_cape_manager import get_type_skin_nickname

class ClickableQLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class HiveLauncher(QMainWindow):
    def __init__(self):
        super().__init__()

        self.configuration = Configurator()
        self.logger = logger
        self.font: FontManager = FontManager()
        self.login_page = WindowLogin(self, ClickableQLabel)
        self.setup_page = WindowSetup(self, ClickableQLabel)
        self.nickname = None
        self.datetime = None
        self.play_time = None
        self.type_skin = None
        self.setup_ui()

    def show_launcher_main(self, picture):
        for child in self.centralwidget.findChildren(QtWidgets.QWidget):
            if child.__class__.__name__ == 'QFrame' or child.__class__.__name__ == 'QListView' or child.__class__.__name__ == 'QScrollBar' or child.__class__.__name__ == 'QWidget':
                continue
            child.hide()
        set_style(self, self.configuration.get_color_theme())

        self.type_skin = get_type_skin_nickname(self.nickname)
        self.launcher_page = WindowLauncher(self, ClickableQLabel, picture)
        self.launcher_page.launcher_show()

    def setup_ui(self):
        self.setObjectName("MainWindow")
        self.resize(1100, 700)
        self.setMinimumSize(QtCore.QSize(1100, 700))
        self.setMaximumSize(QtCore.QSize(1100, 700))
        self.setWindowTitle("HiveLauncher")
        self.setWindowIcon(QtGui.QIcon(f"{self.configuration.static_folder}\\global\\logo_64x64.svg"))

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        
        self.logger.info("Added version minecraft")
        versions_add(self)

        if how_start_page() == 'setup':
            set_style(self, 'setup')
            self.setup_page.setup_show() 
        else:
            set_style(self, self.configuration.get_color_theme())
            self.login_page.login_show()