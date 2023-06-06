class WriteBookmarksHtmlFile:
    def __init__(self, bookmarks_html_file_name, file_content):
        self.bookmarks_html_file_name = bookmarks_html_file_name
        self.file_content = file_content

    def write_bookmarks_html_file(self):
        with open(self.bookmarks_html_file_name, 'w') as bookmarks_file:
            bookmarks_file.write(self.file_content)

        pass
