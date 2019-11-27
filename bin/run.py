import datetime
import argparse

from app import mailer, web
from app.logger import eater_logger


def email_eater_nyc_list_if_new():
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
    force = args.force
    if force:
        eater_logger.info('Forcing run.')

    today_date = datetime.datetime.today().date()

    # run the scraper and check when the Eater list content was last updated
    eater_nyc_restaurants_meta = web.get_eater_nyc_restaurants()
    last_update_date = eater_nyc_restaurants_meta['last_update_date'].date()

    # if the article wasn't published today, don't do anything
    if (last_update_date != today_date) and (not force):
        # log run information
        eater_logger.info('Success: No new NYC restaurants')
        return 

    # log that we found a new list in case email sending fails
    eater_logger.info('Success: New NYC restaurants found!')
    restaurants = eater_nyc_restaurants_meta['parsed_restaurants']
    
    to = args.recipient_emails

    # format eater restaurants to plaintext to 
    # include in our email
    restaurant_text = utils.format_restaurants_for_email(
        restaurants
    )
    mailer.send_email(
        to=to,
        subject_line='New Eater NYC restaurant list!',
        body=restaurant_text,
    )

    # log run information to a file for debugging
    eater_logger.info('Success: Email sent!')


if __name__ == '__main__':
    try:
        email_eater_nyc_list_if_new()
    # catch all exceptions and log
    except Exception as e:
        eater_logger.error('Error: run failed.', exc_info=True)
