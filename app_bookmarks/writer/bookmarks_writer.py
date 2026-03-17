from app_bookmarks.model.bookmarks_html_template import BookmarksHtmlTemplate


class WriteBookmarksHtmlFile:
    def __init__(self, bookmarks_html_file_name):
        self.bookmarks_html_file_name = bookmarks_html_file_name

    def write_bookmarks_html_file(self):
        bookmarks_content = self.create_bookmarks()
        with open(self.bookmarks_html_file_name, 'w') as bookmarks_file:
            bookmarks_file.write(bookmarks_content)

        pass

    @staticmethod
    def create_bookmarks():
        bookmarks_html_template = BookmarksHtmlTemplate()
        return bookmarks_html_template.template