"""
Module for decorators
"""

from __future__ import unicode_literals

import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps

from shmir import settings


def catch_errors(*errors):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except errors as e:
                return {
                    'status': 'error',
                    'data': {
                        'result': e.message,
                    }
                }
        return wrapped
    return wrapper


def send_email(file_handler=None):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            email_to = kwargs.pop('email', None)
            result = f(*args)

            if settings.EMAIL_ENABLED and email_to is not None:
                # msg = MIMEText(json.dumps(result))
                msg = MIMEMultipart('related')
                msg['Subject'] = 'Task ended'
                msg['From'] = settings.EMAIL_FROM
                msg['To'] = email_to

                msg_alternative = MIMEMultipart('alternative')

                msg_text = MIMEText(json.dumps(result), 'plain')
                msg_alternative.attach(msg_text)

                # TODO change this proof-of-contept
                msg_html = MIMEText(
                    "<html><body>{}</body></html>".format(json.dumps(result)),
                    'html'
                )
                msg_alternative.attach(msg_html)

                msg.attach(msg_alternative)

                for msg_file in file_handler(result):
                    msg.attach(msg_file)

                smtp_server = smtplib.SMTP(settings.SMTP_SERVER,
                                        settings.SMTP_PORT)
                smtp_server.starttls()
                smtp_server.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
                smtp_server.sendmail(settings.EMAIL_FROM, email_to,
                                    msg.as_string())
                smtp_server.quit()

            return result
        return wrapped
    return wrapper
