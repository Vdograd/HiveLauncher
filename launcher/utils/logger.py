import datetime
from .configurator import Configurator
import os
from .helper import Helper

class Logger:
    def __init__(self):
        try:
            conf = Configurator()
            self.log_file = f"{conf.logs_folder}\\{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.log"
            os.makedirs(conf.logs_folder, exist_ok=True)
        except Exception as e:
            raise e
    
    def get_time(self):
        return datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
    
    def session_start(self):
        time = self.get_time()
        print(f"[{time}] [INFO]: Session start")
        with open(self.log_file, "w", encoding="ansi") as file_log:
            file_log.write(f"[{time}] [INFO]: Session start\n")

    def info(self, message):
        time = self.get_time()
        print(f"[{time}] [INFO]: {message}")
        with open(self.log_file, "a", encoding="ansi") as file_log:
            file_log.write(f"[{time}] [INFO]: {message}\n")

    def warn(self, message):
        time = self.get_time()
        print(f"[{time}] [WARN]: {message}")
        with open(self.log_file, "a", encoding="ansi") as file_log:
            file_log.write(f"[{time}] [WARN]: {message}\n")

    def error(self, message):
        message = str(message)
        time = self.get_time()
        print(f"[{time}] [ERROR]: {message}")
        with open(self.log_file, "a", encoding="ansi") as file_log:
            file_log.write(f"[{time}] [ERROR]: {message}\n")

    def report(self, code: int, error: Exception):
        helper = Helper()
        time = self.get_time()
        report_message = f"""{'='*40}
| REPORT ERROR [{time}]
| {'-'*20}
| base:
|   Code error: {code}
|   Launcher version: {Configurator().version_launcher}
|   Java version: {helper.get_java()}
| {'-'*20}
| details:"""
        for x in helper.get_traceback(error)[:-1]:
            report_message += f"\n{x}"
        report_message += f"\n| {'-'*20}\n{'='*40}"
        print(report_message)
        with open(self.log_file, "a", encoding="ansi") as file_log:
            file_log.write(f"{report_message}\n")

logger = Logger()