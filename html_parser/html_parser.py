from bs4 import BeautifulSoup


def parse_html_first_impact(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.body.find('div', attrs={'class': 'wrapper'})


def get_soup_from_html(html):
    return BeautifulSoup(html, 'html.parser')


def get_tags_from_soup(soup, tag):
    return soup.find_all(tag)
