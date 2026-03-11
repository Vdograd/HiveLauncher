from PyQt6 import QtCore
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QSize
from ...auth.auth_manager import AuthManager
from ...utils.logger import Logger
auth = AuthManager()
logger = Logger()

class AuthRegisterAccount(QThread):
    progress = pyqtSignal()
    finished = pyqtSignal(str, float, str)
    error = pyqtSignal(str, str)

    def __init__(self, nickname, password, method):
        super().__init__()
        self.nickname = nickname
        self.password = password
        self.method = method

    def run(self):
        if self.method == 'registr':
            try:
                data = auth.create_user(self.nickname, self.password)
            except Exception as e:
                logger.error(str(e))
                self.error.emit('Произошла ошибка', "registr")
            if data == "Nickname dublicate":
                self.error.emit("Пользователь уже существует", "registr")
            elif str(type(data)) == "<class 'tuple'>":
                self.finished.emit(data[0], data[1], data[2])
        elif self.method == "auth":
            self.progress.emit()
            try:
                data = auth.auth_in_account(self.nickname, self.password)
            except Exception as e:
                self.error.emit("Произошла ошибка", "auth")
                logger.error(str(e))
            if data == "Not found nickname in db":
                self.error.emit("Пользователь не существует", "auth")
            elif data == 'Account already added':
                self.error.emit('Аккаунт уже добавлен', "auth")
            elif data == "Not correct password":
                self.error.emit("Неверный пароль", "auth")
            elif str(type(data)) == "<class 'tuple'>":
                self.finished.emit(data[0], data[1], data[2])

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

def password_check_login_start(self):
    all_chars_ru = '1234567890 ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{}|;:",.<>?/~`\'\\'
    password_check = self.password_account_login.text()
    if password_check == "":
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
        password = list(password_check)
        for pass_char in password:
            if pass_char not in all_chars_ru:
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

def change_login_page(self):
    if self.button_change_page_log_reg.text() == 'или добавьте новый':
        self.select_nickname_combobox.hide()
        if self.password_account_login.isVisible():
            self.password_account_login.hide()
        self.use_in_minecraft_text.hide()
        self.login_in_launcher.hide()
        self.creeper_left.hide()
        self.creeper_right.hide()
        self.select_nickname_text.setText("Добавить никнейм")
        self.button_change_page_log_reg.setText("или выбрать созданный")
        self.select_nickname_text.setGeometry(QtCore.QRect(0, 95, 1100, 32))
        self.button_change_page_log_reg.setGeometry(QtCore.QRect(446, 127, 220, 19))

        self.text_registr_login2.show()
        self.text_auth_login2.show()
        self.write_nickname_for_registr.show()
        self.write_nickname_for_auth.show()
        self.write_password_for_registr.show()
        self.write_password_for_auth.show()
        self.write_password_retry_for_registr.show()
        self.button_register_login2.show()
        self.button_auth_login2.show()
        self.rules_nickname_login2.show()
        self.rule_login2.show()
    else:
        self.text_registr_login2.hide()
        self.text_auth_login2.hide()
        self.write_nickname_for_registr.hide()
        self.write_nickname_for_auth.hide()
        self.write_password_for_registr.hide()
        self.write_password_for_auth.hide()
        self.write_password_retry_for_registr.hide()
        self.button_register_login2.hide()
        self.button_auth_login2.hide()
        self.rules_nickname_login2.hide()
        self.rule_login2.hide()

        self.select_nickname_combobox.show()
        self.use_in_minecraft_text.show()
        self.login_in_launcher.show()
        self.creeper_left.show()
        self.creeper_right.show()
        self.select_nickname_text.setText("Выберите аккаунт")
        self.button_change_page_log_reg.setText("или добавьте новый")
        self.select_nickname_text.setGeometry(QtCore.QRect(0, 186, 1100, 32))
        self.button_change_page_log_reg.setGeometry(QtCore.QRect(465, 223, 180, 19))
        if self.hide_pass == False:
            self.password_account_login.show()
            self.use_in_minecraft_text.setGeometry(QtCore.QRect(0, 377, 1100, 32))
            self.login_in_launcher.setGeometry(QtCore.QRect(450, 424, 200, 35))
        else:
            self.select_nickname_text.setGeometry(QtCore.QRect(0, 186, 1100, 32))
            self.button_change_page_log_reg.setGeometry(QtCore.QRect(465, 223, 180, 19))


def login_page_auth(self, nickname, password, method):
    if method == 'registr':
        self.worker = AuthRegisterAccount(nickname, password, "registr")
        self.worker.progress.connect(lambda: auth_login_progress(self))
        self.worker.error.connect(lambda x,y: auth_login_error(self, x,y))
        self.worker.finished.connect(lambda x,y,z: auth_login_finished(self,x,y,z))
        logger.info("Try create account")
        self.worker.start()
    elif method == 'auth':
        self.worker = AuthRegisterAccount(nickname, password, "auth")
        self.worker.progress.connect(lambda: auth_login_progress(self))
        self.worker.error.connect(lambda x,y: auth_login_error(self, x,y))
        self.worker.finished.connect(lambda x,y,z: auth_login_finished(self,x,y,z))
        logger.info("Try log in to account")
        self.worker.start()

def auth_login_progress(self):
    block_button = """
            QPushButton {
                border-radius: 8px;
                background: rgba(0, 95, 255, 0.5);
                color: white;
            }
        """
    
    self.button_change_page_log_reg.setEnabled(False)
    self.write_nickname_for_registr.setEnabled(False)
    self.write_nickname_for_auth.setEnabled(False)
    self.write_password_for_registr.setEnabled(False)
    self.write_password_for_auth.setEnabled(False)
    self.write_password_retry_for_registr.setEnabled(False)
    self.button_register_login2.setEnabled(False)
    self.button_register_login2.setStyleSheet(block_button)
    self.button_auth_login2.setEnabled(False)
    self.button_auth_login2.setStyleSheet(block_button)

def auth_login_error(self, reason, type_error):
    if type_error == 'registr':
        self.error_auth_login_1.setText(reason)
        self.error_auth_login_1.show()

        self.button_change_page_log_reg.setEnabled(True)
        self.write_nickname_for_registr.setEnabled(True)
        self.write_nickname_for_auth.setEnabled(True)
        self.write_password_for_registr.setEnabled(True)
        self.write_password_for_auth.setEnabled(True)
        self.write_password_retry_for_registr.setEnabled(True)
        self.write_nickname_for_registr.clear()
        self.write_nickname_for_auth.clear()
        self.write_password_retry_for_registr.clear()

    elif type_error == 'auth':
        self.error_auth_login_2.setText(reason)
        self.error_auth_login_2.show()

        self.button_change_page_log_reg.setEnabled(True)
        self.write_nickname_for_registr.setEnabled(True)
        self.write_nickname_for_auth.setEnabled(True)
        self.write_password_for_registr.setEnabled(True)
        self.write_password_for_auth.setEnabled(True)
        self.write_password_retry_for_registr.setEnabled(True)
        self.write_password_for_auth.clear()
        if reason == 'Пользователь не существует' or reason == 'Аккаунт уже добавлен':
            self.write_nickname_for_auth.clear()
    return

def auth_login_finished(self, nickname, play_time, datetime):
    self.error_auth_login_1.hide()
    self.error_auth_login_2.hide()
    self.main.nickname = nickname
    self.main.datetime = datetime
    self.main.play_time = play_time
    logger.info('Try show window launcher')
    # Переключение на лаунчер <- ->