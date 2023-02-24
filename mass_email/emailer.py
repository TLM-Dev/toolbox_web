import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
import glob
from typing import List
import pandas as pd
from dataclasses import dataclass

# Automation Idea - if there is no attachment, there is no email?
# Automation Idea - Pull Email Addresses from SOLID

# ATTACHMENTS_FOLDER = 'rewards-files'
# EMAIL_LIST = 'rewards-email.xlsx'
# EMAIL_SUBJECT = "Sales Rewards 2023-02"
# EMAIL_BODY = """
# Dear Valued Partner,

# Please see this month's Sales Rewards report attached.

# Best regards,
# Team Catalytic
# """
import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText

@dataclass
class MassEmailer:
    key: str
    send_from: str
    send_to: List[str]
    subject: str
    body: str
    server: smtplib.SMTP
    msg = MIMEMultipart()
    file: str
    cc: List[str]

    def populate(self):
        self.msg = MIMEMultipart()
        self.msg['From'] = self.send_from
        self.msg['To'] = COMMASPACE.join(self.send_to)
        self.msg['Date'] = formatdate(localtime=True)
        self.msg['Subject'] = self.subject
        self.msg['Cc'] = COMMASPACE.join(self.cc)
        self.msg.attach(MIMEText(self.body))

    def attach_personal_files(self):
        part = MIMEApplication(
            self.file.read(),
            Name=basename(self.file.name)
        )
        part['Content-Disposition'] = f'attachment; filename={basename(self.file.name)}' 
        self.msg.attach(part)

    def send(self):
        if self.send_to:
            print(f"Sending mail: {self.key} {self.send_to} - CC: {self.cc}")
            self.server.sendmail(
                self.send_from, 
                self.send_to + self.cc, 
                self.msg.as_string())

    def run(self):
        self.populate()
        self.attach_personal_files()
        self.send()
