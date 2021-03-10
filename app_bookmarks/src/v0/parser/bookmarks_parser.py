from pathlib import Path

from bs4 import BeautifulSoup


class ParseBookmarksHtmlFile:
    def __init__(self, bookmarks_html_file):
        self.bookmarks_html_file = bookmarks_html_file

    def parse_bookmarks_html_file(self):
        posix_path = Path(self.bookmarks_html_file)
        file_name = posix_path.name

        parsed_html = BeautifulSoup("TODO", "html.parser")

        result = file_name
        return result
