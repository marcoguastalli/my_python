from pathlib import Path

from bs4 import BeautifulSoup
from app_bookmarks.src.v0.model.bookmarks_model import Bookmarks

class ParseBookmarksHtmlFile:
    def __init__(self, bookmarks_html_file):
        self.bookmarks_html_file = bookmarks_html_file

    def parse_bookmarks_html_file(self):
        with open(self.bookmarks_html_file) as file_to_parse:
            soup = BeautifulSoup(file_to_parse, 'html.parser')
            result = soup.find_all('a')

        bookmarks = Bookmarks("DuckDuck", "http:", "dir")
        result.append(bookmarks)
        return result
