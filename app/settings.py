import os


PRODUCTION = {
    'REGION_NAME': os.environ['REGION_NAME'],
    'SENDER_EMAIL': os.environ['SENDER_EMAIL'],
    'AWS_ACCESS_KEY_ID': os.environ['AWS_ACCESS_KEY_ID'],
    'AWS_SECRET_ACCESS_KEY': os.environ['AWS_SECRET_ACCESS_KEY'],
    'CRONTAB_USER': os.environ['CRONTAB_USER'],
}
