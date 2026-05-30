#from ..ui.error.error import DialogError
from PyQt6.QtWidgets import QApplication
from .logger import logger
from .build import build
import requests
import urllib3
import socket
import json
import sys

class ErrorExc:
    def __init__(self, error: Exception):
        self.all_code_error = [
            100, 101, 102, 103, 104, 105, 106, 107, 
            108, 109, 110, 201, 301, 302 ,303, 304, 
            305, 306, 307, 308, 309, 310, 311, 312, 
            313, 314, 401, 402 ,403, 501 ,502, 601, 
            602, 603, 604, 605, 606, 607, 608, 609,
            610, 611, 612, 613, 614, 615, 616, 617, 
            618, 619, 620, 621, 
            999
        ]
        
        self.error = error
        self.code = self.get_code()
        self.name = self.get_name()
        self.message = self.get_message()
        self.type_error = self.get_type_error()
        try: logger.critical_error(self.code, self.error)
        except: pass
        self.show_dialog()

    def show_dialog(self) -> None:
        print(self.name, self.message, self.type_error)
        # app = QApplication.instance()
        # if app is None:
        #     app = QApplication(sys.argv)

        # dialog = DialogError(self.name, self.message, self.type_error)
        # try: dialog.exec()
        # except Exception: dialog.show()

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
            if type(self.error) == error[0]: return error[1]
        else:
            return 999
        
    def get_name(self) -> str:
        names = {}

        for code in self.all_code_error:
            names[str(code)] = build.get_lang_text(f'errors-header-{code}')
        return names.get(str(self.code), 'Error')
    
    def get_type_error(self) -> str:
        error_types = {
            100: 'CONNECTION_ERROR',
            101: 'CONNECTION_ERROR',
            102: 'CONNECTION_ERROR',
            103: 'CONNECTION_ERROR',
            104: 'CONNECTION_ERROR',
            105: 'CONNECTION_ERROR',
            106: 'CONNECTION_ERROR',
            107: 'CONNECTION_ERROR',
            108: 'CONNECTION_ERROR',
            109: 'CONNECTION_ERROR',
            110: 'PROXY_ERROR',
            201: 'PERMISSION_ERROR',
            301: 'LAUNCHER_ERROR',
            302: 'LAUNCHER_ERROR',
            303: 'LAUNCHER_ERROR',
            304: 'LAUNCHER_ERROR',
            305: 'LAUNCHER_ERROR',
            306: 'LAUNCHER_ERROR',
            307: 'LAUNCHER_ERROR',
            308: 'LAUNCHER_ERROR',
            309: 'LAUNCHER_ERROR',
            310: 'SYSTEM_ERROR',
            311: 'LAUNCHER_ERROR',
            312: 'LAUNCHER_ERROR',
            313: 'LAUNCHER_ERROR',
            314: 'LAUNCHER_ERROR',
            401: 'FILE_ERROR',
            402: 'FILE_ERROR',
            403: 'FILE_ERROR',
            501: 'NETWORK_ERROR',
            601: 'POOL_ERROR',
            602: 'PROXY_ERROR',
            603: 'DECODE_ERROR',
            604: 'CONNECTION_ERROR',
            605: 'CONNECTION_ERROR',
            606: 'POOL_ERROR',
            607: 'CONNECTION_ERROR',
            608: 'CONNECTION_ERROR',
            609: 'CONNECTION_ERROR',
            610: 'POOL_ERROR',
            611: 'POOL_ERROR',
            612: 'CONNECTION_ERROR',
            613: 'CONNECTION_ERROR',
            614: 'CONNECTION_ERROR',
            615: 'CONNECTION_ERROR',
            616: 'CONNECTION_ERROR',
            617: 'CONNECTION_ERROR',
            618: 'CONNECTION_ERROR',
            619: 'CONNECTION_ERROR',
            620: 'CONNECTION_ERROR',
            621: 'CONNECTION_ERROR',
            999: 'UNKNOWN_ERROR'
        }
        return error_types.get(self.code, 'UNKNOWN_ERROR')
    
    def get_message(self) -> str:
        messages = {}

        for code in self.all_code_error:
            messages[str(code)] = build.get_lang_text(f'errors-center-{code}')
    
        return messages.get(str(self.code), 'Error')