from PyQt6 import QtCore, QtGui, QtWidgets
import sys
from ...ui.style import set_style
from ...utils.configurator import Configurator
from ...utils.font_manager import FontManager
from PyQt6.QtCore import Qt

class DialogError(QtWidgets.QDialog):
    def __init__(self, code, message):
        super().__init__()
        self.conf = Configurator()
        self.font = FontManager()
        try:
            self.color = self.conf.get_color_theme()
        except:
            self.color = 'light'

        self.code: int = code
        self.message: str = message
        self.show_error()

    def show_error(self):
        self.setWindowTitle("HiveLauncher Error")
        self.resize(500, 220)
        self.setMinimumSize(QtCore.QSize(500, 220))
        self.setMaximumSize(QtCore.QSize(500, 220))
        self.setObjectName('ErrorDialog')
        self.setWindowIcon(QtGui.QIcon(f"{self.conf.static_folder}\\global\\logo_64x64.svg"))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.logo_error = QtWidgets.QLabel(self)
        self.logo_error.setGeometry(QtCore.QRect(38, 25, 60, 40))
        self.logo_error.setMinimumSize(QtCore.QSize(60, 40))
        self.logo_error.setPixmap(QtGui.QPixmap(f"{self.conf.static_folder}\\error\\icon_{self.color}.svg"))
        self.logo_error.setObjectName("logo_error")

        self.reason_text = QtWidgets.QLabel(parent=self)
        self.reason_text.setGeometry(QtCore.QRect(40, 75, 370, 18))
        self.reason_text.setFont(self.font.get_font(12,"1"))
        self.reason_text.setText(self.message)
        self.reason_text.setObjectName('reason_text')

        self.code_text = QtWidgets.QLabel(parent=self)
        self.code_text.setGeometry(QtCore.QRect(40, 103, 370, 15))
        self.code_text.setFont(self.font.get_font(10,"1"))
        self.code_text.setText(f'Код ошибки: {self.code}')
        self.code_text.setObjectName('code_text')

        self.send_report = QtWidgets.QPushButton(self)
        self.send_report.setGeometry(QtCore.QRect(40, 156, 189, 32)) 
        self.send_report.setFont(self.font.get_font(10, "1"))
        self.send_report.setText("Отправить репорт")
        self.send_report.setObjectName("send_report")
        self.send_report.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.send_report.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.send_report.clicked.connect(lambda: self.send_report_func())

        self.panel1_t = QtWidgets.QLabel(parent=self)
        self.panel1_t.setGeometry(QtCore.QRect(455, 0, 45, 220))
        self.panel1_t.setObjectName('panel_error')

        self.panel2_t = QtWidgets.QLabel(parent=self)
        self.panel2_t.setGeometry(QtCore.QRect(432, 0, 45, 220))
        self.panel2_t.setObjectName('panel_error')

        self.panel3_t = QtWidgets.QLabel(parent=self)
        self.panel3_t.setGeometry(QtCore.QRect(410, 0, 45, 220))
        self.panel3_t.setObjectName('panel_error')

        self.cross = QtWidgets.QPushButton(self)
        self.cross.setGeometry(QtCore.QRect(385, 9, 16, 16)) 
        self.cross.setObjectName("cross")
        self.cross.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.cross.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.cross.setIcon(QtGui.QIcon(f"{self.conf.static_folder}\\error\\cross.svg"))
        self.cross.clicked.connect(lambda: sys.exit())

        try:
            set_style(self, self.color)
        except:
            self.setStyleSheet("""
#ErrorDialog {
    background-color: #ffffff;
}

#reason_text {
    color: #000000
}
#logo_error {
    background: rgba(0,0,0,0);
}

#code_text {
    color: rgba(0, 0, 0, 0.8)
}
                               
#send_report {
    border-radius: 4px;
    background: #005FFF;
    color: white;
}
#send_report:hover {
    background: #0054E4
}
                               
#panel_error {
    background: rgba(0,95,255,0.8);
}

#cross {
    border: none;
}
""")
                
    def send_report_func(self):
        ...