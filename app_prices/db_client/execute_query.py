from sqlite3 import Error


def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Error as e:
        print(e)
