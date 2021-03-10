from pathlib import Path

from bs4 import BeautifulSoup
from app_bookmarks.src.v0.model.bookmarks_model import Bookmarks

class ParseBookmarksHtmlFile:
    def __init__(self, bookmarks_html_file):
        self.bookmarks_html_file = bookmarks_html_file

    def parse_bookmarks_html_file(self):
        result = []
        posix_path = Path(self.bookmarks_html_file)
        file_name = posix_path.name

        parsed_html = BeautifulSoup("TODO", "html.parser")

        bookmarks = Bookmarks("DuckDuck", "http:", "dir")
        result.append(bookmarks)
        return result
