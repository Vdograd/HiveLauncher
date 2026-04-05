from ..utils.logger import logger
from PyQt6.QtCore import QThread, pyqtSignal
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..utils.getenv import GetEnv
GetEnv = GetEnv()

class ReportEmail(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        try:
            self.file_report = logger.log_file
            self.email = GetEnv.get_env('EMAIL_REPORT')
            self.password = GetEnv.get_env('PASS_EMAIL_REPORT')
        except:
            pass
    
    def run(self):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.email
            msg['Subject'] = "Report HiveLauncher"
            with open(self.file_report, 'r', encoding='ansi') as file:
                message_report = file.read()
            msg.attach(MIMEText(message_report, 'plain'))
            server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, self.email, text)
            server.quit()
        except Exception as e:
            try:
                logger.error(e)
            except:
                pass
        finally:
            self.finished.emit()
