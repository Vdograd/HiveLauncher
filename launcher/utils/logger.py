import datetime
from .configurator import Configurator

class Logger:
    def __init__(self):
        self.log_file = f"{Configurator().logs_folder}\\{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.log"
    
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

logger = Logger()