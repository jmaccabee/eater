from lxml.etree import HTML


def get_dom_from_response_content(response_content):
    # HTML method returns an lxml.etree._ElementTree object: 
    # https://lxml.de/api/lxml.etree._ElementTree-class.html
    dom = HTML(response_content)

    return dom
