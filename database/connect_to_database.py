import psycopg2
from psycopg2.extras import DictCursor

connection_string = "dbname = 'stylometry_v2' user = 'stylometry' host = 'localhost' password = 'stylometry'"


# connection_string = "dbname = 'stylometry_v2' user = 'dickson' host = 'localhost' password = 'dickson'"


def execute_insert_query(query):
    """
        This function only deals with insertion queries.
        NO VALUES WOULD BE RETURNED.
    """
    try:
        conn = psycopg2.connect(connection_string)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)
        conn.close()
    except psycopg2.DatabaseError as e:
        print "Cannot connect to database"
        print e.pgerror


def execute_select_query(query):
    """
        This function takes care of all selection queries.
        -------------------------------------------------------------
        NOTE that a LIST OF LISTS will be returned
        NOTE that a LIST OF LISTS will be returned
        NOTE that a LIST OF LISTS will be returned
        NOTE that a LIST OF LISTS will be returned
        =============================================================
        I repeat, a LIST OF LISTS will be returned
        -------------------------------------------------------------
        Consider a SQL select statement, desired rows would be returned.
        The inner list represents a row and thus the LIST OF LISTS refers
        to all the returned rows.

        Note also that 'cursor_factory=DictCursor' is also used.
        It provides the functionality that you can reference a value in
        an inner list (or, in other word, a value in a row) by using the
        column-name, which is a good practice in programming.
    """
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except psycopg2.DatabaseError as e:
        print e.pgerror


def test_if_author_exists(author):
    """
        The author.get_if_author_existing_query provides a
        SQL query in the following format:
        -------------------------------------------------------------
        SELECT author_id FROM author WHERE author_name LIKE '%name%'
        -------------------------------------------------------------
        If a row is returned, the author_id will be extracted and
        returned to the caller function for the insertion of feature
        queries.

        Otherwise, -1 will be returned to indicate the caller function
        to generate a new insertion query for a new author whose name
        does not exist in the database.
    """
    if author == -1:
        return author

    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute(author.get_if_author_existing_query())
        row = cursor.fetchone()

        if row is not None:
            return row['author_id']
        else:
            return -1

    except psycopg2.DatabaseError as e:
        print e.pgerror
