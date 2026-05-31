from email.mime.multipart import MIMEMultipart
from PyQt6.QtCore import QThread, pyqtSignal
from email.mime.text import MIMEText
from ..utils.logger import logger
from ..utils.env import env
import pyperclip
import smtplib

class ReportEmail(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        try:
            self.file_report = logger.log_file
            self.email = env.get('EMAIL_REPORT')
            self.password = env.get('PASS_EMAIL_REPORT')
        except Exception as e:
            try: logger.error(e)
            except: pass
    
    def run(self):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.email
            msg['Subject'] = "Report HiveLauncher Update"

            with open(self.file_report, 'r', encoding='ansi') as file:
                message_report = file.read()
                
            msg.attach(MIMEText(message_report, 'plain'))
            server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, self.email, text)
            server.quit()
        except Exception as e:
            try: logger.error(e)
            except: pass
        finally:
            self.finished.emit()

class CopyLog(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            file = logger.log_file
            with open(file, 'r', encoding="ansi") as f:
                content = f.read()

            pyperclip.copy(content)
        except Exception as e:
            logger.error(e)
        self.finished.emit()