import datetime
from .build import build
import os
from .helper import Helper

class Logger:
    def __init__(self):
        try:
            self.log_file = f"{build.logs_folder}\\{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.log"
            os.makedirs(build.logs_folder, exist_ok=True)
        except Exception as e:
            raise e
    
    def get_time(self) -> str:
        return datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
    
    def session_start(self) -> None:
        time = self.get_time()
        print(f"[{time}] [INFO]: Session start")
        with open(self.log_file, "w", encoding="ansi") as file_log:
            file_log.write(f"[{time}] [INFO]: Session start\n")

    def info(self, message: str) -> None:
        time = self.get_time()
        print(f"[{time}] [INFO]: {message}")
        with open(self.log_file, "a", encoding="ansi") as file_log:
            file_log.write(f"[{time}] [INFO]: {message}\n")

    def warn(self, message: str) -> None:
        time = self.get_time()
        print(f"[{time}] [WARN]: {message}")
        with open(self.log_file, "a", encoding="ansi") as file_log:
            file_log.write(f"[{time}] [WARN]: {message}\n")

    def error(self, message: str | Exception) -> None:
        message = str(message)
        time = self.get_time()
        print(f"[{time}] [ERROR]: {message}")
        with open(self.log_file, "a", encoding="ansi") as file_log:
            file_log.write(f"[{time}] [ERROR]: {message}\n")

    def report(self, code: int, error: Exception) -> None:
        helper = Helper()
        time = self.get_time()
        report_message = f"""{'='*40}
| UPDATE REPORT ERROR [{time}]
| {'-'*20}| base:
|   Code error: {code}
|   Update version: {build.update_version}
| {'-'*20}
| details:"""
        for x in helper.get_traceback(error)[:-1]:
            report_message += f"\n{x}"
        report_message += f"\n| {'-'*20}\n{'='*40}"
        print(report_message)
        with open(self.log_file, "a", encoding="ansi") as file_log:
            file_log.write(f"{report_message}\n")

logger = Logger()