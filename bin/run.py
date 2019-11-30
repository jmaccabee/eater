import argparse
import datetime

from dateutil.tz import UTC

from app import mailer, utils, web
from app.logger import eater_logger


def email_eater_nyc_list_if_new(recipient_emails, force):
    if force:
        eater_logger.info('Forcing run.')

    now = datetime.datetime.now()
    # now needs to be timezone aware
    now = now.replace(tzinfo=UTC)

    # run the scraper and check when the Eater list content was last updated
    eater_nyc_restaurants_meta = web.get_eater_nyc_restaurants()
    last_update_time = eater_nyc_restaurants_meta['last_update_date']

    updated_within_last_day = (
        (now - last_update_time) < datetime.timedelta(hours=24)
    )
    # if the article wasn't published today, don't do anything
    if (not updated_within_last_day) and (not force):
        # log run information
        eater_logger.info('Success: No new NYC restaurants')
        return 

    # log that we found a new list in case email sending fails
    eater_logger.info('Success: New NYC restaurants found!')
    restaurants = eater_nyc_restaurants_meta['parsed_restaurants']
    
    # format eater restaurants to plaintext to 
    # include in our email
    restaurant_text = utils.format_restaurants_for_email(
        restaurants
    )
    mailer.send_email(
        to=recipient_emails,
        subject_line='New Eater NYC restaurant list!',
        body=restaurant_text,
    )

    # log run information to a file for debugging
    eater_logger.info('Success: Email sent!')


if __name__ == '__main__':
    # configure expected command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--recipient_emails", 
        help=(
            "Who should be emailed when a new restaurant list is published? "
            "To include multiple emails, separate with a comma and no space"
        ),
        required=True
    )
    parser.add_argument(
        "--force", 
        help="Send an email even if the Eater restaurant list isn't new.",
        action='store_true',
        default=False,
    )
    args = parser.parse_args()
    recipient_emails = args.recipient_emails
    if ',' in recipient_emails:
        recipient_emails = recipient_emails.split(',')
    force = args.force
    try:
        email_eater_nyc_list_if_new(recipient_emails, force)
    # catch all exceptions and log
    except Exception as e:
        eater_logger.error('Error: run failed.', exc_info=True)
