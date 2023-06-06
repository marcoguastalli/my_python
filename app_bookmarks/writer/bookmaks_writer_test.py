import unittest

from app_bookmarks.writer.bookmarks_writer import WriteBookmarksHtmlFile

BOOKMARKS_HTML_FILE = "/Users/marcoguastalli/dev/repository/gitpy/my_python/app_bookmarks/bookmarks_created.html"
FILE_CONTENT = "<html><title>TODO</title></html>"
class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_write_bookmarks(self):
            print("Writing bookmarks file '%s'" % BOOKMARKS_HTML_FILE)
            writer = WriteBookmarksHtmlFile(BOOKMARKS_HTML_FILE, FILE_CONTENT)
            result = writer.write_bookmarks_html_file()
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(Test)
