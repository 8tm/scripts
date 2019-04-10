#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------

""" Email module """

__author__ = 'Tadeusz Miszczyk'
__version__ = "1.0.0"

# ----------------------------------------------------------------------------------------------------------------------

import os
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../library/')
import mylib.variables
import mylib.variables_sensitive

# ----------------------------------------------------------------------------------------------------------------------


def send(receiver, subject, message, template, attachments=[], debug=False):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mylib.variables_sensitive.EMAIL_LOGIN
    msg['To'] = ', '.join(receiver)
    msg['Date'] = formatdate(localtime=True)

    for attachment in attachments:
        part = MIMEBase('application', "octet-stream")
        with open(attachment, 'rb') as attachment_content:
            part.set_payload(attachment_content.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(attachment)))
        msg.attach(part)

    msg.preamble = message
    text_content = MIMEText(message, 'plain')
    html_content = MIMEText(template, 'html')
    msg.attach(text_content)
    msg.attach(html_content)

    try:
        serv = smtplib.SMTP(mylib.variables.EMAIL_SERVER,
                            mylib.variables.EMAIL_PORT)

        serv.set_debuglevel(debug)
        serv.connect(mylib.variables.EMAIL_SERVER,
                     mylib.variables.EMAIL_PORT)

        serv.ehlo()
        serv.starttls()
        serv.ehlo()
        serv.login(mylib.variables_sensitive.EMAIL_LOGIN,
                   mylib.variables_sensitive.EMAIL_PASSWORD)

        serv.sendmail(mylib.variables_sensitive.EMAIL_LOGIN, receiver, msg.as_string())
        serv.quit()

    # Update in time - some error handler + log
    except smtplib.SMTPException as Error:
        print(str(Error))

# ----------------------------------------------------------------------------------------------------------------------
