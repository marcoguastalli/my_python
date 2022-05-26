from app_bookmarks.parser.bookmarks_parser import ParseBookmarksHtmlFile
from sqlite3_tables.create_connection import create_connection
from sqlite3_tables.execute_query import execute_query
from sqlite3_tables.select_query import select_query
from datetime import datetime

DATABASE = "/Users/marcoguastalli/opt/sqlite/bookmarks.py.sqlite"
BOOKMARKS_HTML_FILE = "/Users/marcoguastalli/dev/repository/gitpy/my_python/app_bookmarks/bookmarks_light.html"


def main():
    init_database(DATABASE)
    conn = create_connection(DATABASE)
    try:
        if conn is not None:
            print("Parsing bookmarks file '%s'" % BOOKMARKS_HTML_FILE)
            parser = ParseBookmarksHtmlFile(BOOKMARKS_HTML_FILE)
            bookmarks_list = parser.parse_bookmarks_html_file()
            count_insert = 0
            count_update = 0
            for bookmark_in_html in bookmarks_list:
                # read SQLite table 'bookmarks' and get existing bookmarks
                bookmarks_in_ddbb = select_query(conn, f"SELECT uri FROM bookmarks WHERE uri = '{bookmark_in_html.get_uri()}'")
                if bookmarks_in_ddbb is not None and len(bookmarks_in_ddbb) > 0:
                    updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    query_update = f"UPDATE bookmarks SET title='{bookmark_in_html.get_title()}'," \
                                   f" folder='{bookmark_in_html.get_folder()}'," \
                                   f" icon='{bookmark_in_html.get_icon()}'," \
                                   f" status={bookmark_in_html.get_status()}," \
                                   f" updated='{updated}'" \
                                   f" WHERE uri='{bookmark_in_html.get_uri()}'"
                    execute_query(conn, query_update)
                    count_update += 1
                else:
                    # insert new bookmark
                    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    query_insert = f"INSERT INTO bookmarks (title, uri, folder, icon, status, created) " \
                                   f"VALUES ('{bookmark_in_html.get_title()}', '{bookmark_in_html.get_uri()}', '{bookmark_in_html.get_folder()}'," \
                                   f"'{bookmark_in_html.get_icon()}', {bookmark_in_html.get_status()}, '{created}') "
                    execute_query(conn, query_insert)
                    count_insert += 1
            # commit
            conn.commit()
            print("Inserted %s bookmarks and updated %s bookmarks from file '%s'" % (count_insert, count_update, BOOKMARKS_HTML_FILE))
        else:
            print(f"Error Connection to DDBB: {DATABASE}")
    finally:
        if conn is not None:
            conn.close()


def init_database(database: str):
    conn = create_connection(database)
    try:
        if conn is not None:
            # check for previously created table
            table_already_exists = select_query(conn, f"SELECT title FROM bookmarks")
            if table_already_exists is None:
                print(f"Create table 'bookmarks'")
                # drop table
                # execute_query(conn, "DROP TABLE IF EXISTS bookmarks")
                # conn.commit()
                # create table
                sql_create_table = '''CREATE TABLE IF NOT EXISTS bookmarks (
                                             title TEXT NOT NULL,
                                             uri TEXT PRIMARY KEY NOT NULL,
                                             folder TEXT NOT NULL,
                                             icon TEXT NOT NULL,
                                             status TEXT NOT NULL,
                                             created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                             updated TEXT NOT NULL DEFAULT "")'''
                execute_query(conn, sql_create_table)
                conn.commit()
        else:
            print("Error Connection to DDBB:" + database)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()
