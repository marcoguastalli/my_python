from sqlite3 import Error


def execute_query(connection, query):
    """ Execute the input query
    :param connection: Connection object
    :param query: a SQL statement
    :return the result:
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Error as e:
        print(e)
