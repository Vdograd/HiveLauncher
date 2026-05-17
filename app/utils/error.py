import requests
import json
from .logger import logger
import socket
from ..ui.error.error import DialogError
from PyQt6.QtWidgets import QApplication
import sys

class ErrorExc:
    def __init__(self, error: Exception):
        self.error = error
        self.code = self.get_code()
        self.name = self.get_name()
        self.message = self.get_message()
        self.type_error = self.get_type_error()
        try:
            logger.report(self.code, self.error)
        except:
            pass
        self.show_dialog()

    def show_dialog(self) -> None:
        app = QApplication.instance()

        if app is None:
            app = QApplication(sys.argv)
        dialog = DialogError(self.name, self.message, self.type_error)
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
            if type(self.error) == error[0]:
                return error[1]
        else:
            return 999
        
    def get_name(self) -> str:
        names = {
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
        return names.get(self.code, 'Неизвестная ошибка.')
    
    def get_type_error(self) -> str:
        error_types = {
            100: 'CONNECTION_ERROR',
            101: 'TIMEOUT_ERROR',
            102: 'REDIRECT_ERROR',
            103: 'CONNECTION_TIMEOUT_ERROR',
            104: 'READ_TIMEOUT_ERROR',
            105: 'HTTP_ERROR',
            201: 'PERMISSION_ERROR',
            301: 'JSON_ERROR',
            302: 'KEY_ERROR',
            303: 'VALUE_ERROR',
            304: 'WINDOWS_ERROR',
            305: 'TYPE_ERROR',
            306: 'SYSTEM_ERROR',
            307: 'UNICODE_ERROR',
            308: 'PROCESS_ERROR',
            309: 'ATTRIBUTE_ERROR',
            310: 'MEMORY_ERROR',
            311: 'INDEX_ERROR',
            312: 'NAME_ERROR',
            313: 'IMPORT_ERROR',
            314: 'SYNTAX_ERROR',
            401: 'OS_ERROR',
            402: 'FILE_NOT_FOUND_ERROR',
            403: 'FILE_EXISTS_ERROR',
            501: 'NETWORK_ERROR',
            502: 'UNBOUND_LOCAL_ERROR',
            999: 'UNKNOWN_ERROR'
        }
        return error_types.get(self.code, 'UNKNOWN_ERROR')
    
    def get_message(self) -> str:
        messages = {
            100: 'Не удалось подключиться к удаленным серверам. Пожалуйста, проверьте ваше интернет-соединение и перезапустите лаунчер.',
            101: 'Сервер слишком долго не отвечает. Попробуйте повторить попытку позже или проверьте соединение.',
            102: 'Слишком много перенаправлений при подключении к серверу. Возможно, проблема на стороне сервера.',
            103: 'Не удалось подключиться к серверу из-за превышения времени ожидания соединения.',
            104: 'Сервер не отправляет данные. Проверьте стабильность интернет-соединения.',
            105: 'Сервер вернул ошибку HTTP. Возможно, сервер временно недоступен.',
            201: 'Недостаточно прав для выполнения операции. Запустите лаунчер от имени администратора.',
            301: 'Ошибка декодирования JSON. Файл конфигурации поврежден. Перезапустите лаунчер.',
            302: 'Отсутствует необходимый ключ в данных. Возможно, повреждены файлы конфигурации. Перезапустите лаунчер.',
            303: 'Неверный формат данных. Перезапустите лаунчер.',
            304: 'Системная ошибка Windows. Перезапустите лаунчер.',
            305: 'Неверный тип данных. Перезапустите лаунчер.',
            306: 'Критическая системная ошибка. Перезапустите лаунчер.',
            307: 'Ошибка кодировки символов. Перезапустите лаунчер.',
            308: 'Ошибка при взаимодействии с дочерним процессом. Попробуйте завершить все связанные процессы и перезапустить лаунчер.',
            309: 'Отсутствует необходимый атрибут. Перезапустите лаунчер.',
            310: 'Недостаточно оперативной памяти. Закройте другие приложения и попробуйте снова.',
            311: 'Обращение к несуществующему индексу. Перезапустите лаунчер.',
            312: 'Использование неопределенной переменной. Перезапустите лаунчер.',
            313: 'Не удалось импортировать модуль. Перезапустите лаунчер.',
            314: 'Синтаксическая ошибка в конфигурации. Перезапустите лаунчер.',
            401: 'Системная ошибка ввода-вывода. Проверьте доступность дискового пространства и перезапустите лаунчер.',
            402: 'Не удалось найти необходимый файл. Попробуйте перезапустить или переустановить лаунчер.',
            403: 'Файл или директория уже существует. Перезапустите лаунчер.',
            501: 'Не удалось разрешить DNS-имя сервера. Проверьте интернет-соединение или DNS-настройки.',
            502: 'Использование локальной переменной до присвоения значения. Перезапустите лаунчер.',
            999: 'Произошла неизвестная ошибка. Попробуйте перезапустить лаунчер.'
        }
        
        message = messages.get(self.code, 'Произошла неизвестная ошибка. Попробуйте перезапустить лаунчер.')
        return message