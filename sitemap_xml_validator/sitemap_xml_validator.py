import re

import requests
from bs4 import BeautifulSoup


# Given a sitemap.xml url and a reg-exp pattern
# - request to the sitemap.xml
# - parse all the url-nodes
# - for each node get the 'loc' property
# - apply the input pattern to the 'loc' property value
# - print true or false
def sitemap_xml_validator(url, pattern):
    response = requests.get(url)
    if 200 != response.status_code:
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    urls = soup.findAll('url')
    if not urls:
        return False

    p = re.compile(pattern)
    result = {}
    for u in urls:
        loc = u.find('loc').string
        print("loc: '%s'" % loc)
        match = re.match(pattern, loc)
        if match is not None:
            result[loc] = match.group()

    return result


if __name__ == '__main__':
    input_url = "https://www.postfinance.ch/sitemap.xml"
    input_pattern = "^(http://localhost:(7000|7001)\/.*|https://[-a-zA-Z0-9&#/%_!,.()]*[-a-zA-Z0-9+&@#/%=~_|])"
    output = sitemap_xml_validator(input_url, input_pattern)
    for key, value in output.items():
        if key != value:
            print(key, ': ', value)
