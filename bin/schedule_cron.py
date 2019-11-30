from crontab import CronTab

import os

from app import settings


def schedule_cron():
    # configure the cron to run as a specific user
    user_cron = CronTab(user=settings.PRODUCTION['CRONTAB_USER'])

    # create a new cron command to run bin.py
    command_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'run.py --recipient_emails {}'.format(
            settings.PRODUCTION['RECIPIENT_EMAILS']
        )
    )
    job = user_cron.new(
        # if you're running the app from a virtual environment,
        # you'll want to use the virtualenv's python here instead
        command='python {}'.format(command_path),
    )

    # set the job to run at noon each day
    job.hour.on(12)
    job.minute.on(0)

    user_cron.write()


if __name__ == '__main__':
    schedule_cron()
