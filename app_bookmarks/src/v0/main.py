from app_bookmarks.src.v0.parser.bookmarks_parser import ParseBookmarksHtmlFile


def main():
    bookmarks_html_file = "~/Downloads/bookmarks.html"
    print("Parsing bookmarks file '%s'" % bookmarks_html_file)

    parser = ParseBookmarksHtmlFile(bookmarks_html_file)
    print("TODO" + parser.__str__())
    exit(0)


if __name__ == "__main__":
    main()
