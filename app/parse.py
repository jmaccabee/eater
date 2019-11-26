def parse_eater_restaurants(dom, requested_url_path):
    sections = dom.xpath(
        "//main[@id='content']/section"
    )
    
