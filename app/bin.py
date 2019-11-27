import datetime
import argparse

from app import mailer, web


def email_eater_nyc_list_if_new():
    import pdb; pdb.set_trace()
    today_date = datetime.datetime.today().date()

    # run the scraper and check when the Eater list content was last updated
    eater_nyc_restaurants_meta = web.get_eater_nyc_restaurants()
    last_update_date = eater_nyc_restaurants_meta['last_update_date'].date()

    # if the article wasn't published today, don't do anything
    # if last_update_date != today_date:
    #    return 

    restaurants = eater_nyc_restaurants_meta['parsed_restaurants']
    
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
    args = parser.parse_args()
    args.recipient_emails

    recipients = []
    mailer.send_mail(eater_nyc_essential_restaurants)


if __name__ == '__main__':
    email_eater_nyc_list_if_new()
