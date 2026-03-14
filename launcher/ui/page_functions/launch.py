from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSize

def open_window(self, page):
    conf = self.conf
    if page == self.page:
        return
    elif page == 'Home':
        self.home.setIcon(QtGui.QIcon(f"{conf.static_folder}\\action\\home.svg"))
        self.home.show()
        self.account.setIcon(QtGui.QIcon(f"{conf.static_folder}\\home\\{conf.get_color_theme()}\\account.svg"))
        self.account.show()
        self.settings.setIcon(QtGui.QIcon(f"{conf.static_folder}\\home\\{conf.get_color_theme()}\\settings.svg"))
        self.settings.show()
        self.fon_image.show()
        self.head_nickname.setPixmap(QtGui.QPixmap(self.picture[0]))
        self.head_nickname.show()
        self.nickname_text.setText(self.main.nickname)
        self.nickname_text.show()
        self.button_start.show()
        self.button_open_folder_version.show()
        self.select_version.show()
        self.page = 'Home'