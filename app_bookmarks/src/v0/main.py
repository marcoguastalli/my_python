from app_bookmarks.src.v0.parser.bookmarks_parser import ParseBookmarksHtmlFile
from app_bookmarks.src.v0.store.store_json import StoreJson


def main():
    bookmarks_html_file = "/Users/marcoguastalli/temp/bookmarks.html"
    print("Parsing bookmarks file '%s'" % bookmarks_html_file)

    parser = ParseBookmarksHtmlFile(bookmarks_html_file)
    bookmarks_list = parser.parse_bookmarks_html_file()

    stored_json_list = []
    for bookmarks in bookmarks_list:
        sj = StoreJson('http://localhost:8080/marco27-web/v1/bookmarks/create', bookmarks.__str__())
        stored_json = sj.store()
        stored_json_list.append(stored_json)

    print("Stored %s json from bookmarks file '%s'" % (stored_json_list.__len__(), bookmarks_html_file))
    exit(0)


if __name__ == "__main__":
    main()
