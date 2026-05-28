import requests
import json
from .logger import logger
import socket
from ..ui.dialogs.error_dialog import DialogError
from PyQt6.QtWidgets import QApplication
import sys
import urllib3

class ErrorExc():
    def __init__(self, error: Exception):
        logger.warn(f'Class type error: {type(error)}')
        self.error = error
        self.code = self.get_code()
        self.message = self.get_message()
        try:
            logger.report(self.code, self.error)
        except:
            pass
        self.show_dialog()

    def show_dialog(self):
        app = QApplication.instance()

        if app is None:
            app = QApplication(sys.argv)
        dialog = DialogError(self.code, self.message)
        try:
            dialog.exec()
        except Exception:
            dialog.show()

    def get_code(self) -> int:
        errors = {
            requests.exceptions.ConnectionError: 100,
            requests.exceptions.Timeout: 101,
            requests.exceptions.TooManyRedirects: 102,
            requests.exceptions.ConnectTimeout: 103,
            requests.exceptions.ReadTimeout: 104,
            requests.exceptions.HTTPError: 105,
            ConnectionAbortedError: 106,
            ConnectionResetError: 107,
            ConnectionRefusedError: 108,
            requests.exceptions.ProxyError: 110,
            ConnectionError: 109,

            PermissionError: 201,

            json.JSONDecodeError: 301,
            KeyError: 302,
            ValueError: 303,
            WindowsError: 304,
            TypeError: 305,
            SystemError: 306,
            UnicodeDecodeError: 307,
            ChildProcessError: 308,
            AttributeError: 309,
            MemoryError: 310,
            IndexError: 311,
            NameError: 312,
            ImportError: 313,
            SyntaxError: 314,

            OSError: 401,
            FileNotFoundError: 402,
            FileExistsError: 403,

            socket.gaierror: 501,
            UnboundLocalError: 502,

            urllib3.exceptions.PoolError: 601,
            urllib3.exceptions.ProxyError: 602,
            urllib3.exceptions.DecodeError: 603,
            urllib3.exceptions.RequestError: 604,
            urllib3.exceptions.TimeoutError: 605,
            urllib3.exceptions.FullPoolError: 606,
            urllib3.exceptions.MaxRetryError: 607,
            urllib3.exceptions.ProtocolError: 608,
            urllib3.exceptions.ResponseError: 609,
            urllib3.exceptions.EmptyPoolError: 610,
            urllib3.exceptions.ClosedPoolError: 611,
            urllib3.exceptions.HostChangedError: 612,
            urllib3.exceptions.ReadTimeoutError: 613,
            urllib3.exceptions.TimeoutStateError: 614,
            urllib3.exceptions.HeaderParsingError: 615,
            urllib3.exceptions.LocationParseError: 616,
            urllib3.exceptions.LocationValueError: 617,
            urllib3.exceptions.NewConnectionError: 618,
            urllib3.exceptions.ConnectTimeoutError: 619,
            urllib3.exceptions.NameResolutionError: 620,
            urllib3.exceptions.UnrewindableBodyError: 621,

            Exception: 999
        }
        for error in errors.items():
            if type(self.error) == error[0]:
                return error[1]
        else:
            return 999
        
    def get_message(self):
        names = {
            100: 'Не удалось подключиться к серверу.',
            101: 'Сервер не отвечает.',
            102: 'Не удалось подключиться к серверу.',
            103: 'Сервер не отвечает.',
            104: 'Сервер не отвечает.',
            105: 'Код статуса сервера 4xx / 5xx.',
            106: 'Соединение с сервером прервано.',
            107: 'Соединение сброшено.',
            108: 'Сервер не отвечает.',
            109: 'Проблема с соединением.',
            110: 'Не удалось подключиться к прокси.',

            201: 'Недостаточно прав к Windows.',

            301: 'Ошибка кодирования.',
            302: 'Непредвиденная ошибка.',
            303: 'Непредвиденная ошибка.',
            304: 'Ошибка с Windows.',
            305: 'Непредвиденная ошибка.',
            306: 'Системная ошибка.',
            307: 'Ошибка кодирования.',
            308: 'Ошибка взаимодействия процесса.',
            309: 'Непредвиденная ошибка.',
            310: 'Недостаточно памяти.',
            311: 'Непредвиденная ошибка.',
            312: 'Непредвиденная ошибка.',
            313: 'Непредвиденная ошибка.',
            314: 'Непредвиденная ошибка.',

            401: 'Системная ошибка.',
            402: 'Файл не найден.',
            403: 'Файл/путь не найден.',

            501: 'Нет соединения с сервером.',

            601: 'Пул соединений не доступен.',
            602: 'Не удалось подключиться к прокси.',
            603: 'Ошибка декодирования.',
            604: 'Ошибка соединения с сервером.',
            605: 'Превышено время ожидания.',
            606: 'Пул соединений занят.',
            607: 'Превышен лимит запросов к серверу.',
            608: 'Данные ответа сервера некорректны.',
            609: 'Ошибка обработки ответа от сервера.',
            610: 'Пул соединений не может выдать соединение.',
            611: 'Пул соединений закрыт для использования.',
            612: 'Хост запроса изменился.',
            613: 'Таймаут ответа на запрос.',
            614: 'Непредвиденная ошибка запроса.',
            615: 'Данные ответа сервера некорректны.',
            616: 'Непредвиденная ошибка запроса.',
            617: 'Непредвиденная ошибка запроса.',
            618: 'Не удалось подключиться к серверу.',
            619: 'Соединение оборвалось.',
            620: 'Непредвиденная ошибка запроса.',
            621: 'Ошибка отправки запроса.',

            999: 'Неизвестная ошибка.'
        }
        return names.get(self.code, 'Неизвестная ошибка.')