import requests
import json
from .logger import logger
import socket

class ErrorExc():
    def __init__(self, error: Exception):
        self.error = error
        self.code = self.get_code()
        self.message = self.get_message()
        try:
            logger.report(self.code, self.error)
        except:
            pass

    def get_code(self):
        errors = {
            requests.exceptions.ConnectionError: 100,
            requests.exceptions.Timeout: 101,
            requests.exceptions.TooManyRedirects: 102,
            requests.exceptions.ConnectTimeout: 103,
            requests.exceptions.ReadTimeout: 104,
            requests.exceptions.HTTPError: 105,
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
            Exception: 999
        }
        for error in errors.items():
            if self.error == error[0]:
                return error[1]
        else:
            return errors.get(Exception)
        
    def get_message(self):
        messages = {
            100: 'Не удалось подключиться к серверу.',
            101: 'Сервер не отвечает.',
            102: 'Не получен ответ от сервера.',
            103: 'Сервер не отвечает.',
            104: 'Сервер не отвечает.',
            105: 'Код статуса сервера 4xx / 5xx.',
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
            501: 'Нет соединения с сервером',
            502: 'Непредвиденная ошибка.',
            999: 'Неизвестная ошибка.'
        }
        return messages.get(self.code)