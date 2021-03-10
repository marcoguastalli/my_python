from app_bookmarks.src.v0.parser.bookmarks_parser import ParseBookmarksHtmlFile


def main():
    bookmarks_html_file = "~/Downloads/bookmarks.html"
    print("Parsing bookmarks file '%s'" % bookmarks_html_file)

    parser = ParseBookmarksHtmlFile(bookmarks_html_file)
    bookmarks_list = parser.parse_bookmarks_html_file()
    for bookmarks in bookmarks_list:
        print(bookmarks.__str__())
    exit(0)


if __name__ == "__main__":
    main()
