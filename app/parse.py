from dateutil.parser import parse
import json

from app import constants, utils


def parse_eater_restaurants(dom, requested_url_path):
    # start by parsing what we can from the linked data
    # included in a <script> tag on the page
    linked_data = parse_eater_restaurant_linked_json_data(
        dom,
        requested_url_path,
    )
    
    # unpack the parsed linked data so we can 
    # add parsed restaurant data not found 
    # in the <script> tag
    date_published = linked_data['date_published']
    parsed_restaurants_from_json = linked_data['parsed_restaurants']

    # then parse additional restaurant details from the HTML content
    parsed_restaurant_from_html = parse_eater_restaurant_card_html(dom)
    
    parsed_restaurants = []
    for data_slug, json_restaurant in parsed_restaurants_from_json.items():
        html_restaurant = parsed_restaurant_from_html[data_slug]
        restaurant = {**json_restaurant, **html_restaurant}
        parsed_restaurants.append(restaurant)

    return {
        'date_published': date_published,
        'parsed_restaurants': parsed_restaurants,
    }


def parse_eater_restaurant_linked_json_data(dom, requested_url_path):
    # first, extract the element containing the linked data
    restaurant_json = ''.join(
        dom.xpath(
            '//script[@type="application/ld+json"]/text()'
        )
    )
    # next, convert the linked data text into a JSON object
    restaurant_data = json.loads(restaurant_json)
    
    # we can use the "date modified" field to know when a new article
    # is published
    date_published = parse(restaurant_data['dateModified'])

    # we can also parse information on the restaurants on the list
    # from the linked data, though it won't include everything we want
    restaurant_list = restaurant_data['itemListElement']
    
    parsed_restaurants = {}
    for restaurant in restaurant_list:
        # we can use the data slug to map the restaurants
        # parsed from the linked data with the restaurants
        # parsed from the section cards
        data_slug = restaurant['item']['url'].split('/')[-1]

        # a hash will be faster than the alternative 
        # approach of creating a list of dictionaries, 
        # each representing a restaurant, and iterating
        # over each to find the one we need to match
        # i.e., O(1) vs O(n) for a list of dictionaries
        parsed_restaurants[data_slug] = {
            'list_position': restaurant['position'],
            'eater_url': restaurant['item']['url'],
            'name': restaurant['item']['name'],        
            'requested_url_path': requested_url_path,
        }

    # I prefer the pattern of returning a 
    # dictionary with explicit keys vs
    # returning a tuple or some other object
    # with an implicit value at each position,
    # even if we're going to immediately unpack the values
    return {
        'date_published': date_published,
        'parsed_restaurants': parsed_restaurants,
    }


def parse_eater_restaurant_card_html(dom):
    # each restaurant card is nested under a <section>,
    # 
    restaurant_cards = dom.xpath(
        "//main[@id='content']/section"
    )

    # parse each of the restaurant cards
    parsed_restaurants = {}
    for restaurant in restaurant_cards:
        # HTML attribute values are typically already cleaned.
        data_slug = restaurant.attrib['data-slug']

        # make sure the restaurant card is actually a restaurant
        if data_slug in constants.NON_RESTAURANT_SECTION_DATA_SLUGS:
            continue

        # parse the restaurant attributes we want from the HTML
        name = utils.clean_xpath_parsed_text(
            restaurant.xpath('.//h1//text()')
        )

        address = utils.clean_xpath_parsed_text(
            restaurant.xpath('.//div[contains(@class, "address")]//text()')
        )

        phone_number = utils.clean_xpath_parsed_text(
            restaurant.xpath('.//div[contains(@class, "phone")]/div/a/@href')
        ).replace('tel:', '')

        website_url = utils.clean_xpath_parsed_text(
            restaurant.xpath('.//a[contains(text(), "Visit Website")]/@href')
        )

        restaurant_description = utils.clean_xpath_parsed_text(
            restaurant.xpath(
                './/div[contains(@class, "entry-content")]//p//text()'
            )
        )

        google_maps_url = utils.clean_xpath_parsed_text(
            restaurant.xpath('.//ul[contains(@class, "mapstack")]' 
                             '//a[contains(text(), "Google Maps")]/@href')
        )

        other_featured_lists = utils.clean_xpath_parsed_text(
            restaurant.xpath('.//div[contains(@class, "featured")]//a/text()'),
            join_separator=', ',
        )

        # organize the data as nested object under the data_slug key,
        # so we can use that data_slug key to match each restaurant
        # with it's corresponding one in the linked data
        parsed_restaurants[data_slug] = {
            'data_slug': data_slug,
            # potentially useful to include for debugging.
            'html_name': name,
            'address': address,
            'phone_number': phone_number,
            'website_url': website_url,
            'restaurant_description': restaurant_description,
            'google_maps_url': google_maps_url,
            'other_featured_lists': other_featured_lists,
        }

    return parsed_restaurants
