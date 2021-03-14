import bs4

from app_bookmarks.src.v0.model.bookmarks_model import Bookmarks
from html_parser.html_parser import get_soup_from_html
from html_parser.html_parser import get_tags_from_soup
from utils.py_utils_date import convert_timestamp_to_str_with_format


class ParseBookmarksHtmlFile:
    def __init__(self, bookmarks_html_file):
        self.bookmarks_html_file = bookmarks_html_file

    def parse_bookmarks_html_file(self):
        result = []
        dt_tag_list = self.get_list_of_tag('dt')
        folder = ' '
        for dt_tag in dt_tag_list:
            if dt_tag.findChild():
                h3_or_a_item = dt_tag.findChild()
                tag_name = h3_or_a_item.name
                if tag_name == 'h3':
                    folder = h3_or_a_item.contents[0]
                    continue
                elif tag_name == 'a':
                    bookmarks = self.create_bookmarks_from_tag(h3_or_a_item, folder)
                    result.append(bookmarks)
                    continue
        return result

    def get_list_of_tag(self, tag: str):
        with open(self.bookmarks_html_file) as file_to_parse:
            soup = get_soup_from_html(file_to_parse)
            result = get_tags_from_soup(soup, tag)
        return result

    @staticmethod
    def create_bookmarks_from_tag(a_tag: bs4.element.Tag, folder: str):
        href = a_tag['href']
        title = a_tag.contents[0]
        add_date = a_tag['add_date']
        created_modified_date = convert_timestamp_to_str_with_format(add_date)
        bookmarks = Bookmarks(title, href, folder)
        bookmarks.set_created(created_modified_date)
        bookmarks.set_modified(created_modified_date)
        if a_tag.get('icon') is not None:
            bookmarks.set_icon(a_tag['icon'])
        return bookmarks
