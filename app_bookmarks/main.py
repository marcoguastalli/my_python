from app_bookmarks.parser.bookmarks_parser import ParseBookmarksHtmlFile
from app_bookmarks.store.store_json import StoreJson

BOOKMARKS_HTML_FILE = "/Users/marcoguastalli/temp/bookmarks.html"
BOOKMARKS_POST_ENDPOINT_URL = "http://localhost:8080/marco27-web/v1/bookmarks/create"


def main():

    print("Parsing bookmarks file '%s'" % BOOKMARKS_HTML_FILE)

    parser = ParseBookmarksHtmlFile(BOOKMARKS_HTML_FILE)
    bookmarks_list = parser.parse_bookmarks_html_file()

    stored_json_list = []
    for bookmarks in bookmarks_list:
        sj = StoreJson(BOOKMARKS_POST_ENDPOINT_URL, bookmarks.__str__())
        stored_json = sj.store()
        stored_json_list.append(stored_json)

    print("Stored %s json from bookmarks file '%s'" % (stored_json_list.__len__(), BOOKMARKS_HTML_FILE))
    exit(0)


if __name__ == "__main__":
    main()
