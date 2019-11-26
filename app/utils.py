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
