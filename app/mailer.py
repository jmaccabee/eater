from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3

from app import settings


def send_email(
        to, 
        subject_line, 
        body, 
        email_subtype='plain',
    ):
    ses_client = boto3.client(
        'ses', 
        region_name=settings.PRODUCTION['REGION_NAME'],
        aws_access_key_id=settings.PRODUCTION['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=settings.PRODUCTION['AWS_SECRET_ACCESS_KEY'],
    )
    multiple_emails = isinstance(to, (list, tuple))

    from_email = settings.PRODUCTION['SENDER_EMAIL']
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject_line
    msg["From"] = "Eater NYC Restaurant Alerts <{}>".format(from_email)
    msg["To"] = ", ".join(to) if multiple_emails else to
    charset = "utf-8"

    msg_body = MIMEMultipart("alternative")
    textpart = MIMEText(body.encode(charset), email_subtype, charset)
    msg_body.attach(textpart)
    msg.attach(msg_body)

    import pdb; pdb.set_trace()
    ses_client.send_raw_email(
        Source=from_email,
        Destinations=to if multiple_emails else [to],
        RawMessage={"Data": msg.as_string()},
    )
