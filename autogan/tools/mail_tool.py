import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from typing import Dict, Optional


class SendEmail:
    def __init__(self, email_config: Dict, work_dir: Optional[str] = None):
        """A class for send email

        :param email_config: JSON format of email_config
            {"server": "smtp.xxx.xxx", "port": 465, "username": "", "password": ""}
        :param work_dir: Attachment relative path, default is extensions
        """
        if work_dir is None:
            work_dir = "extensions"
        self._work_dir = os.getcwd() + "/" + work_dir
        self._server = email_config["server"]
        self._port = email_config["port"]
        self._username = email_config["username"]
        self._password = email_config["password"]

    def send(self, to, subject, text, files=None) -> bool:
        """Send email

        :param to: Inbox list.
        :param subject: Email subject
        :param text: Email content
        :param files: Attachment name list

        :return: Successful or not
        """
        try:
            if files is None:
                files = []
            msg = MIMEMultipart()
            msg['From'] = self._username
            msg['To'] = ', '.join(to)
            msg['Subject'] = subject

            msg.attach(MIMEText(text))

            for file in files:
                part = MIMEBase('application', "octet-stream")
                path = self._work_dir+"/"+file
                with open(path, "rb") as f:
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment',
                                filename=str(Header(os.path.basename(path), 'utf-8')))  # or
                # part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(file)))
                msg.attach(part)

            server = smtplib.SMTP_SSL(self._server, self._port)
            server.login(self._username, self._password)
            server.sendmail(self._username, to, msg.as_string())
            server.close()
            return True
        except Exception as e:
            print(e)
            return False
