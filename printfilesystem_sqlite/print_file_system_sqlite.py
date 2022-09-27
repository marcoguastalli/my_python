from printfilesystem_sqlite.read.read_folder import ReadFolder
from create_connection import create_connection
from execute_query import execute_query
from printfilesystem_sqlite.create.create_json import CreateJson


def main(extract_metadata: False):
    source_path = "/media/marco27/M27BACKUP/m27/doodie"
    database = "/home/marco27/opt/sqlite/pfs.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            # drop table
            sql_drop_table = "DROP TABLE IF EXISTS pfs"
            execute_query(conn, sql_drop_table)
            conn.commit()
            # create table
            sql_create_table = '''CREATE TABLE IF NOT EXISTS pfs
                                         (_id text PRIMARY KEY,
                                         path text NOT NULL,
                                         name text NOT NULL,
                                         namespace text NOT NULL,
                                         mime text NOT NULL,
                                         width text NOT NULL,
                                         height text NOT NULL,
                                         duration text NOT NULL,
                                         created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                         modified TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                         size REAL NOT NULL DEFAULT 0)'''
            execute_query(conn, sql_create_table)
            conn.commit()

            rf = ReadFolder(source_path)
            files_in_folder = rf.read_files_in_folder_using_os()
            print("The folder with path '%s' contains %s files" % (source_path, files_in_folder.__len__()))

            cj = CreateJson(files_in_folder, extract_metadata)
            sql_list = cj.create_sql()
            print(f"\nSuccessfully created {sql_list.__len__()} sql inserts")
            for sql in sql_list:
                execute_query(conn, sql)
                conn.commit()

        else:
            print("Error Connection to DDBB:" + database)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    try:
        extract__metadata = True
        main(extract__metadata)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os.error()
