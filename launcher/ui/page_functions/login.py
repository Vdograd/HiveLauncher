from PyQt6 import QtCore
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QSize
from ...auth.auth_manager import AuthManager
from ...utils.logger import Logger
auth = AuthManager()
logger = Logger()

def connect_change_nickname_select(self, data):
    for user in data:
        nickname_select = self.select_nickname_combobox.currentText()
        if user[0] == nickname_select and user[1] == "failed":
            self.update_hide_pass(False)
            self.password_account_login.show()
            self.use_in_minecraft_text.setGeometry(QtCore.QRect(0, 377, 1100, 32))
            self.login_in_launcher.setGeometry(QtCore.QRect(450, 424, 200, 35))
            self.password_account_login.clear()
            self.login_in_launcher.setEnabled(False)
            self.login_in_launcher.setStyleSheet(
                """
                    QPushButton {
                        border-radius: 8px;
                        background: rgba(0, 95, 255, 0.5);
                        color: white;
                    }
                """
            )
            return
        else:
            self.update_hide_pass(True)
            self.password_account_login.hide()
            self.use_in_minecraft_text.setGeometry(QtCore.QRect(0, 315, 1100, 32))
            self.login_in_launcher.setGeometry(QtCore.QRect(450, 360, 200, 35)) 
            self.password_account_login.clear()
            self.login_in_launcher.setEnabled(True)
            self.login_in_launcher.setStyleSheet("""
                #login_in_launcher {
                    border-radius: 8px;
                    background: #005FFF;
                    color: white;
                }
                #login_in_launcher:hover {
                    background: rgb(0, 80, 218);
                }
            """)