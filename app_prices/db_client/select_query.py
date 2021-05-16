from sqlite3 import Error


def select_query(connection, query):
    try:
        cur = connection.cursor()
        cur.execute(query)
        return cur.fetchall()
    except Error as e:
        print(e)
