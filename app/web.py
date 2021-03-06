import requests

from app import utils, parse


def get_eater_nyc_restaurants():
    # browser request converted from cURL to Python code
    # using https://curl.trillworks.com/
    headers = {
        'authority': 'ny.eater.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'sec-fetch-user': '?1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'referer': 'https://www.google.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
    }

    # execute the request
    target_url = 'https://ny.eater.com/maps/best-new-york-restaurants-38-map'
    response = requests.get(
        target_url, 
        headers=headers,
    )

    # extract the dom from the response
    dom = utils.get_dom_from_response_content(
        response.content
    )

    return parse.parse_eater_restaurants(dom)
