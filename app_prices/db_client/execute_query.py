from sqlite3 import Error


def execute_query(connection, query):
    """ create a table from the create_table_sql statement
    :param connection: Connection object
    :param query: a CREATE TABLE statement
    :return:
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Error as e:
        print(e)
