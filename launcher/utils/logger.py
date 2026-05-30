from .helper import helper
from .build import build
import datetime
import os

class Logger:
    def __init__(self):
        self.log_file = os.path.join(build.logs_folder, f"{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.log")
        self.session_start()

    def get_time(self) -> str:
        return datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
    
    def session_start(self) -> None:
        self.create_folder_for_log_files()

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
        time = self.get_time()
        print(f"[{time}] [ERROR]: {message}")
        with open(self.log_file, "a", encoding="ansi") as file_log:
            file_log.write(f"[{time}] [ERROR]: {message}\n")

    def critical_error(self, code: int, error: Exception) -> None:
        time = self.get_time()
        report_message = f"""{'='*40}\n| REPORT ERROR [{time}]\n| {'-'*20}\n| base:\n|   Code error: {code}\n|   Launcher version: {build.version_launcher}\n|   Java version: {helper.get_java()}\n| {'-'*20}\n| details:"""

        for x in helper.get_traceback(error)[:-1]:
            report_message += f"\n{x}"
        report_message += f"\n| {'-'*20}\n{'='*40}"

        print(report_message)
        with open(self.log_file, "a", encoding="ansi") as file_log:
            file_log.write(f"{report_message}\n")
    

    def create_folder_for_log_files(self) -> None:
        try:
            os.makedirs(build.logs_folder, exist_ok=True)
        except Exception as e:
            ...

logger = Logger()