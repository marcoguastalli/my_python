from bs4 import BeautifulSoup


def parse_html(html):
    parsed_html = BeautifulSoup(html, "html.parser")
    return parsed_html.body.find('div', attrs={'class': 'wrapper'})
