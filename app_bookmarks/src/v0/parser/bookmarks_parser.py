from app_bookmarks.src.v0.model.bookmarks_model import Bookmarks
from html_parser.html_parser import get_soup_from_html
from html_parser.html_parser import get_tags_from_soup
from utils.py_utils_date import convert_timestamp_to_str_with_format


class ParseBookmarksHtmlFile:
    def __init__(self, bookmarks_html_file):
        self.bookmarks_html_file = bookmarks_html_file

    def parse_bookmarks_html_file(self):
        result = []
        tags = self.get_a()
        for a in tags:
            href = a['href']
            title = a.contents[0]
            add_date = a['add_date']
            created_modified_date = convert_timestamp_to_str_with_format(add_date)

            bookmarks = Bookmarks(title, href, "TODO")
            bookmarks.set_created(created_modified_date)
            bookmarks.set_modified(created_modified_date)
            result.append(bookmarks)
        return result

    def get_a(self):
        with open(self.bookmarks_html_file) as file_to_parse:
            soup = get_soup_from_html(file_to_parse)
            result = get_tags_from_soup(soup, 'a')
        return result
