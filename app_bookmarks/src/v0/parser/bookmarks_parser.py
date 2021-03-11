from app_bookmarks.src.v0.model.bookmarks_model import Bookmarks
from html_parser.html_parser import get_soup_from_html
from html_parser.html_parser import get_tags_from_soup


class ParseBookmarksHtmlFile:
    def __init__(self, bookmarks_html_file):
        self.bookmarks_html_file = bookmarks_html_file

    def parse_bookmarks_html_file(self):
        tags = self.get_a()
        for a in tags:
            print(a['href'])

        result = []
        bookmarks = Bookmarks("DuckDuck", "http:", "dir")
        result.append(bookmarks)
        return result

    def get_a(self):
        with open(self.bookmarks_html_file) as file_to_parse:
            soup = get_soup_from_html(file_to_parse)
            result = get_tags_from_soup(soup, 'a')
        return result
