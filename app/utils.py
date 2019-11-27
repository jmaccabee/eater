from lxml.etree import HTML

import re


def get_dom_from_response_content(response_content):
    # HTML method returns an lxml.etree._ElementTree object: 
    # https://lxml.de/api/lxml.etree._ElementTree-class.html
    dom = HTML(response_content)

    return dom


def clean_xpath_parsed_text(xpath_result_list, join_separator=' '):
    # the .xpath() method always returns a list of objects.
    # in our case, we're including `/text()` in our xpath expressions,
    # so .xpath() will return a list of strings.
    # 
    # ' '.join(list_of_strings) is a safe way to convert
    # a list of strings into a single string. In most cases,
    # we're iterating over a list of objects to extract
    # single attribute value strings from each one, so 
    # converting this list into a single string is what we want
    # and less prone to raising exceptions than indexing the list
    # (i.e., the for empty lists where our xpath doesn't match anything)
    
    # convert the list of strings to a single string,
    # as discussed in the above comment
    clean_text = join_separator.join(xpath_result_list)

    # sometimes, HTML text includes lots of extra whitespace. 
    # using regex we can normalize this whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text)

    # and just in case there's leading or trailing whitespace,
    # we call .strip() on the string before returning it.
    clean_text = clean_text.strip()

    return clean_text


def format_restaurants_for_email(restaurants):
    restaurant_text = (
        "A new Eater NYC Essential Restaurants "
        "list has been published!\n\n"
    )
    for restaurant in restaurants:
        restaurant_text += '{}\n'.format(restaurant['name'])
        restaurant_text += '{}\n'.format(
            restaurant['restaurant_description']
        )
        restaurant_text += 'Also featured in: {}\n\n'.format(
            restaurant['other_featured_lists']
        )
        restaurant_text += 'Address: {}\n'.format(
            restaurant['address']
        )
        restaurant_text += 'Phone Number: {}\n'.format(
            restaurant['phone_number']
        )
        restaurant_text += 'Website URL: {}\n'.format(
            restaurant['website_url']
        )
        restaurant_text += 'Google Maps URL: {}\n'.format(
            restaurant['google_maps_url']
        )
        restaurant_text += '\n\n\n'

    return restaurant_text
