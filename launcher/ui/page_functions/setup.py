from PyQt6 import QtCore
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QSize
from ...auth.auth_manager import AuthManager
from ...utils.logger import Logger
auth = AuthManager()
logger = Logger()

def scroll_page_setup(main_window, page):
    if page == 0:
        page += 1
        main_window.text_hello.hide()
        main_window.text_description.hide()
        main_window.person1.hide()
        main_window.down_text_1.hide()
        main_window.down_text_2.hide()
        main_window.button_continue_setup.hide()

        main_window.text_register_login.show()
        main_window.button_or_setup.show()
        main_window.nickname_setup.show()
        main_window.password_setup.show()
        main_window.password_retry_setup.show()
        main_window.button_auth_setup.show()
        main_window.text_rules_nickname_setup.show()
        main_window.rules_setup.show()
        main_window.person2.show()

    elif page == 1:
        page += 1
        main_window.text_register_login.hide()
        main_window.button_or_setup.hide()
        main_window.nickname_setup.hide()
        main_window.password_setup.hide()
        main_window.password_retry_setup.hide()
        main_window.button_auth_setup.hide()
        main_window.text_rules_nickname_setup.hide()
        main_window.rules_setup.hide()
        main_window.person2.hide()

        main_window.color_text.show()
        main_window.color_set_text.show()
        main_window.after_edit_text_setup.show()
        main_window.color_stamp_setup.show()
        main_window.person3.show()
        main_window.button_continue_setup.show()
        main_window.down_text_1.show()
        main_window.down_text_2.show()
        main_window.button_continue_setup.setText("Завершить")
        main_window.down_text_1.setGeometry(QtCore.QRect(80, 618, 620, 20))
        main_window.down_text_1.setText("Для завершения нажмите кнопку «Завершить»")
    return page

def replace_auth_register_setup(main_window, window_auth):
    if window_auth == 0:
        window_auth = 1
        main_window.text_register_login.setText("Авторизоваться")
        main_window.button_or_setup.setText("или зарегистрироваться")
        main_window.button_auth_setup.setText("Войти и продолжить")
        main_window.nickname_setup.setPlaceholderText("Никнейм")
        main_window.password_retry_setup.hide()
        main_window.text_rules_nickname_setup.hide()
        main_window.rules_setup.hide()
        main_window.button_auth_setup.setGeometry(QtCore.QRect(80, 362, 300, 35))
        main_window.password_setup.clear()
        main_window.password_retry_setup.clear()
        main_window.nickname_setup.clear()
        main_window.error_auth_setup.hide()

    elif window_auth == 1:
        window_auth = 0
        main_window.text_register_login.setText("Зарегистрироваться")
        main_window.button_or_setup.setText("или авторизоваться")
        main_window.button_auth_setup.setText("Создать аккаунт и продолжить")
        main_window.nickname_setup.setPlaceholderText("Никнейм (В Minecraft)")
        main_window.password_retry_setup.show()
        main_window.text_rules_nickname_setup.show()
        main_window.rules_setup.show()
        main_window.button_auth_setup.setGeometry(QtCore.QRect(80, 423, 300, 35))
        main_window.password_setup.clear()
        main_window.password_retry_setup.clear()
        main_window.nickname_setup.clear()
        main_window.error_auth_setup.hide()
    return window_auth


def access_step_continue_auth(self):
    all_chars_en = '1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{}|;:",.<>?/~`\'\\'
    all_chars_ru = '1234567890 ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{}|;:",.<>?/~`\'\\'
    if self.text_register_login.text() == "Зарегистрироваться":
        nickname = self.nickname_setup.text()
        password = self.password_setup.text()
        password_retry = self.password_retry_setup.text()
        if nickname.strip() == "" or password == "" or password_retry == "" or password != password_retry:
            self.button_auth_setup.setEnabled(False)
            self.button_auth_setup.setStyleSheet(
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
            nickname_ls = list(nickname.strip())
            password_ls = list(password)

            for nickname_char in nickname_ls:
                if nickname_char not in all_chars_en:
                    self.button_auth_setup.setEnabled(False)
                    self.button_auth_setup.setStyleSheet(
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
                for password_char in password_ls:
                    if password_char not in all_chars_ru:
                        self.button_auth_setup.setEnabled(False)
                        self.button_auth_setup.setStyleSheet(
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
                    self.button_auth_setup.setStyleSheet(
                        """
                            #button_auth_setup {
                                border-radius: 8px;
                                background: rgba(0, 95, 255, 1);
                                color: white;
                            }
                            #button_auth_setup:hover {
                                background: rgb(0, 83, 228);
                            }
                        """
                    )
                    self.button_auth_setup.setEnabled(True)
                    return
    elif self.text_register_login.text() == "Авторизоваться":
        nickname = self.nickname_setup.text()
        password = self.password_setup.text()
        if nickname.strip() == "" or password == "":
            self.button_auth_setup.setEnabled(False)
            self.button_auth_setup.setStyleSheet(
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
            nickname_ls = list(nickname.strip())
            password_ls = list(password)

            for nickname_char in nickname_ls:
                if nickname_char not in all_chars_en:
                    self.button_auth_setup.setEnabled(False)
                    self.button_auth_setup.setStyleSheet(
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
                for password_char in password_ls:
                    if password_char not in all_chars_ru:
                        self.button_auth_setup.setEnabled(False)
                        self.button_auth_setup.setStyleSheet(
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
                    self.button_auth_setup.setStyleSheet(
                        """
                            #button_auth_setup {
                                border-radius: 8px;
                                background: rgba(0, 95, 255, 1);
                                color: white;
                            }
                            #button_auth_setup:hover {
                                background: rgb(0, 83, 228);
                            }
                        """
                    )
                    self.button_auth_setup.setEnabled(True)
                    return
                
def auth_setup(self, nickname, password):
    if self.text_register_login.text() == "Зарегистрироваться":
        self.worker = AuthRegisterAccount(nickname, password, "registr")
        self.worker.progress.connect(lambda: auth_setup_progress(self))
        self.worker.error.connect(lambda x: auth_setup_error(self, x))
        self.worker.finished.connect(lambda x,y,z: auth_setup_finished(self,x,y,z))
        logger.info("Try create account")
        self.worker.start()

    elif self.text_register_login.text() == "Авторизоваться":
        self.worker = AuthRegisterAccount(nickname, password, "auth")
        self.worker.progress.connect(lambda: auth_setup_progress(self))
        self.worker.error.connect(lambda x: auth_setup_error(self, x))
        self.worker.finished.connect(lambda x,y,z: auth_setup_finished(self,x,y,z))
        logger.info("Try log in to account")
        self.worker.start()

def auth_setup_progress(self):
    self.button_auth_setup.setEnabled(False)
    self.nickname_setup.setEnabled(False)
    self.password_setup.setEnabled(False)
    self.button_or_setup.setEnabled(False)
    self.password_retry_setup.setEnabled(False)

def auth_setup_error(self, reason):
    self.error_auth_setup.setText(reason)
    self.button_auth_setup.setEnabled(True)
    self.nickname_setup.setEnabled(True)
    self.password_setup.setEnabled(True)
    self.button_or_setup.setEnabled(True)
    self.password_retry_setup.setEnabled(True)
    if self.text_register_login.text() != 'Авторизоваться' or self.text_register_login.text() == 'Авторизоваться' and reason == 'Пользователь не существует':
        self.nickname_setup.clear()
    self.password_setup.clear()
    self.password_retry_setup.clear()
    self.error_auth_setup.show()
    return

def auth_setup_finished(self, nickname, play_time, datetime):
    self.button_auth_setup.setEnabled(True)
    self.nickname_setup.setEnabled(True)
    self.password_setup.setEnabled(True)
    self.button_or_setup.setEnabled(True)
    self.password_retry_setup.setEnabled(True)
    self.error_auth_setup.hide()
    self.main.nickname = nickname
    self.main.datetime = datetime
    self.main.play_time = play_time
    self.update_page(scroll_page_setup(self, self.page_setup))


class AuthRegisterAccount(QThread):
    progress = pyqtSignal()
    finished = pyqtSignal(str, float, str)
    error = pyqtSignal(str)

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
                self.error.emit('Произошла ошибка')
            if data == "Nickname dublicate":
                self.error.emit("Пользователь уже существует")
            elif str(type(data)) == "<class 'tuple'>":
                self.finished.emit(data[0], data[1], data[2])
        elif self.method == "auth":
            self.progress.emit()
            try:
                data = auth.auth_in_account(self.nickname, self.password)
            except Exception as e:
                self.error.emit("Произошла ошибка")
                logger.error(str(e))
            if data == "Not found nickname in db":
                self.error.emit("Пользователь не существует")
            elif data == 'Account already added':
                self.error.emit('Аккаунт уже добавлен')
            elif data == "Not correct password":
                self.error.emit("Неверный пароль")
            elif str(type(data)) == "<class 'tuple'>":
                self.finished.emit(data[0], data[1], data[2])