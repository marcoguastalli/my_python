from bs4 import BeautifulSoup


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.body.find('div', attrs={'class': 'wrapper'})
